from flask import Flask, Response
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

@app.route("/download_today", methods=["GET"])
def download_today():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rb_pdp_week WHERE DATE(created_on)=DATE(NOW())")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    df = pd.DataFrame(rows)

    # Convert to CSV
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=today_data.csv"}
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
