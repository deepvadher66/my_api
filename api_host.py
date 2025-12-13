from flask import Flask, Response, jsonify
import mysql.connector
import json
import os

app = Flask(__name__)

# -----------------------------
# DB Connection
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="13.204.140.150",
        user="ocean_crawling",
        password="OceanCrawling@13",
        database="pimerce"
    )

# -----------------------------
# Blinkit
# -----------------------------
@app.route("/download/blinkit", methods=["GET"])
def download_blinkit():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * 
        FROM tb_blinkit_category_data 
        WHERE DATE(created_on) = CURDATE()
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return Response(
        json.dumps(rows, indent=4, default=str),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=blinkit_today.json"}
    )

# -----------------------------
# Zepto
# -----------------------------
@app.route("/download/zepto", methods=["GET"])
def download_zepto():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * 
        FROM tb_zepto_category_data 
        WHERE DATE(created_on) = CURDATE()
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return Response(
        json.dumps(rows, indent=4, default=str),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=zepto_today.json"}
    )

# -----------------------------
# Instamart
# -----------------------------
@app.route("/download/instamart", methods=["GET"])
def download_instamart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * 
        FROM tb_instamart_category_data 
        WHERE DATE(created_on) = CURDATE()
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return Response(
        json.dumps(rows, indent=4, default=str),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=instamart_today.json"}
    )

# -----------------------------
# Health Check
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "API running",
        "endpoints": {
            "blinkit": "/download/blinkit",
            "zepto": "/download/zepto",
            "instamart": "/download/instamart"
        }
    })

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
