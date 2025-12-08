from flask import Flask, jsonify
import mysql.connector
import pandas as pd
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="13.204.140.150",
        user="ocean_crawling",
        password="OceanCrawling@13",
        database="mnm"
    )

@app.route("/get_today_json", methods=["GET"])
def get_today_json():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rb_pdp_week WHERE DATE(created_on)=DATE(NOW())")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # If no data today, return empty list
    return jsonify(rows)

@app.route("/")
def home():
    return jsonify({"message": "API running. Use /get_today_json"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
