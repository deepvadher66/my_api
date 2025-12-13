from flask import Flask, Response, jsonify
import mysql.connector
import json
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="13.204.140.150",
        user="ocean_crawling",
        password="OceanCrawling@13",
        database="pimerce"
    )

@app.route("/download_today_instamart", methods=["GET"])
def download_today_instamart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM tb_instamart_category_data
    WHERE DATE(created_on) = CURDATE()
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    json_data = json.dumps(rows, indent=4, default=str)

    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=instamart_today.json"}
    )

@app.route("/")
def home():
    return jsonify({
        "platform": "Instamart",
        "download": "/download_today_instamart"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
