from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
import shutil
import cv2

from blade_utils import insert_to_mongodb_with_blade_info, get_blade_info
from ultralytics import YOLO

app = FastAPI()

# Thư mục lưu ảnh upload
UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model YOLOv8
model = YOLO("best.pt")

def analyze_blade_image(image_path):
    """
    Phân tích ảnh bằng YOLOv8, trả về số lỗi, nhãn vật thể, độ tin cậy, bounding box, diện tích, class_id, và status dựa theo cấp độ LV.
    """
    results = model(image_path)[0]

    detections = []
    try:
        boxes = results.boxes
        for i in range(len(boxes)):
            class_id = int(boxes.cls[i])
            label = model.names[class_id]
            confidence = float(boxes.conf[i])
            bbox = boxes.xyxy[i].tolist()  # [x1, y1, x2, y2]
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

            detections.append({
                "label": label,
                "class_id": class_id,
                "confidence": round(confidence, 4),
                "bbox": [round(coord, 2) for coord in bbox],
                "area": round(area, 2)
            })
    except Exception as e:
        print("Error processing results:", e)

    # Ưu tiên xác định status theo mức độ nghiêm trọng nhất nếu có nhiều nhãn
    status_priority = {
        "LV_5": "stop operation, emergency repair",
        "LV_4": "repair in 3-6 months",
        "LV_3": "repair in 6-12 months",
        "LV_2": "repair with other items",
        "LV_1": "follow-up"
    }

    status = "good"  # mặc định
    for level in ["LV_5", "LV_4", "LV_3", "LV_2", "LV_1"]:
        if any(det["label"] == level for det in detections):
            status = status_priority[level]
            break

    return {
        "defects": len(detections),
        "status": status,
        "detections": detections
    }



@app.post("/uploads/")
async def upload_image(
    file: UploadFile = File(...),
    bladeid: int = Form(...)
):
    try:
        # Lưu ảnh vào thư mục
        file_id = str(uuid4())
        ext = file.filename.split(".")[-1]
        filename = f"{file_id}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Đảm bảo ảnh đọc được
        image = cv2.imread(file_path)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format or corrupted file.")

        # Phân tích ảnh bằng YOLO
        defect_analysis = analyze_blade_image(file_path)

        # Truy vấn thông tin lưỡi dao từ PostgreSQL
        blade_info = get_blade_info(bladeid)

        # Gửi toàn bộ thông tin vào MongoDB
        insert_to_mongodb_with_blade_info(
            bladeid=bladeid,
            image_path=file_path,
            defect_analysis=defect_analysis,
            blade_info=blade_info
        )

        return JSONResponse(content={
            "message": "Upload and analysis successful",
            "bladeid": bladeid,
            "blade_info": blade_info,
            "defect_analysis": defect_analysis
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
