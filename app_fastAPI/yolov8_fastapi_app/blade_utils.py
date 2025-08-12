import psycopg2
from pymongo import MongoClient
import datetime

# Lấy thông tin từ PostgreSQL
def get_blade_info(bladeid):
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mydb",
            user="postgres",
            password="280800leuleu"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT bladeid, turbine_id, position, length, width, status FROM blade WHERE bladeid = %s;", (bladeid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return {
                "bladeid": result[0],
                "turbine_id": result[1],
                "position": result[2],
                "length": result[3],
                "width": result[4],
                "status": result[5],
            }
        else:
            return None
    except Exception as e:
        print("PostgreSQL error:", e)
        return None

# Ghi dữ liệu vào MongoDB
def insert_to_mongodb_with_blade_info(bladeid, image_path, defect_analysis, blade_info):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["image_database"]
        collection = db["detections"]

        document = {
            "bladeid": bladeid,
            "image_path": image_path,
            "defect_analysis": defect_analysis,
            "blade_info": blade_info,
            "timestamp": datetime.datetime.utcnow()
        }


        collection.insert_one(document)

    except Exception as e:
        print("MongoDB error:", e)
