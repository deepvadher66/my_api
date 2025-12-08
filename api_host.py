from flask import Flask, Response, jsonify
import mysql.connector
import pandas as pd
import os
import json

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="13.204.140.150",
        user="ocean_crawling",
        password="OceanCrawling@13",
        database="mnm"
    )

# -----------------------------
# JSON Auto-download Endpoint
# -----------------------------
@app.route("/download_today_json", methods=["GET"])
def download_today_json():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rb_pdp_week WHERE DATE(created_on)=DATE(NOW())")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert rows (list of dicts) to JSON
    json_data = json.dumps(rows, indent=4)

    # Return as downloadable file
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=today_data.json"}
    )

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "API running",
        "download": "/download_today_json"
    })

# -----------------------------
# Render Entry
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
