from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from PIL import Image
import pytesseract
import numpy as np
import io
import time

app = FastAPI()

# Khởi tạo sẵn model PaddleOCR cho tiếng Anh và tiếng Việt
ocr_models = {
    "eng": PaddleOCR(use_angle_cls=True, lang="en"),
    "vie": PaddleOCR(use_angle_cls=True, lang="vi")
}

# Helper: đọc ảnh
def read_image(contents: bytes):
    return np.array(Image.open(io.BytesIO(contents)).convert("RGB"))

@app.post("/ocr-full")
async def ocr_full(
    file: UploadFile = File(...),
    model: str = Form(...),  # 'paddle' hoặc 'tesseract'
    lang: str = Form(...),   # 'eng' hoặc 'vie'
):
    if model not in ("paddle", "tesseract"):
        raise HTTPException(status_code=400, detail="Model must be 'paddle' or 'tesseract'")
    if lang not in ("eng", "vie"):
        raise HTTPException(status_code=400, detail="Lang must be 'eng' or 'vie'")

    try:
        start_time = time.time()
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    result = []

    # PaddleOCR xử lý tất cả block
    if model == "paddle":
        paddle = ocr_models[lang]
        raw = paddle.ocr(image_np, cls=True)
        for block in raw:
            for line in block:
                result.append({
                    "box": line[0],
                    "text": line[1][0],
                    "confidence": line[1][1]
                })

    # Tesseract xử lý từng box sau khi phát hiện bằng PaddleOCR
    elif model == "tesseract":
        paddle = ocr_models[lang]
        raw = paddle.ocr(image_np, cls=True)
        for block in raw:
            for line in block:
                box = line[0]
                try:
                    x_coords = [int(pt[0]) for pt in box]
                    y_coords = [int(pt[1]) for pt in box]
                    x_min, x_max = max(0, min(x_coords)), max(x_coords)
                    y_min, y_max = max(0, min(y_coords)), max(y_coords)
                    cropped = image_np[y_min:y_max, x_min:x_max]
                except:
                    continue

                try:
                    text = pytesseract.image_to_string(cropped, lang=lang)
                except Exception as e:
                    text = f"[ERROR: {str(e)}]"

                result.append({
                    "box": box,
                    "text": text.strip()
                })

    return JSONResponse(content={
        "result": result,
        "time_ms": round((time.time() - start_time) * 1000, 2)
    })


@app.post("/ocr-fullV2")
async def ocr_fullV2(
    file: UploadFile = File(...),
    model: str = Form(...),  # 'paddle' hoặc 'tesseract'
    lang: str = Form(...),   # 'eng' hoặc 'vie'
):
    if model not in ("paddle", "tesseract"):
        raise HTTPException(status_code=400, detail="Model must be 'paddle' or 'tesseract'")
    if lang not in ("eng", "vie"):
        raise HTTPException(status_code=400, detail="Lang must be 'eng' or 'vie'")

    try:
        start_time = time.time()
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    result = []

    if model == "paddle":
        paddle = ocr_models[lang]
        raw = paddle.ocr(image_np, cls=True)
        # Trả về đúng format gốc
        result = raw

    elif model == "tesseract":
        paddle = ocr_models[lang]
        raw = paddle.ocr(image_np, cls=True)
        for block in raw:
            for line in block:
                box = line[0]
                try:
                    x_coords = [int(pt[0]) for pt in box]
                    y_coords = [int(pt[1]) for pt in box]
                    x_min, x_max = max(0, min(x_coords)), max(x_coords)
                    y_min, y_max = max(0, min(y_coords)), max(y_coords)
                    cropped = image_np[y_min:y_max, x_min:x_max]
                except:
                    continue

                try:
                    text = pytesseract.image_to_string(cropped, lang=lang)
                except Exception as e:
                    text = f"[ERROR: {str(e)}]"

                result.append([
                    box,
                    [text.strip(), 1.0]  # Confidence giả định là 1.0
                ])

    return JSONResponse(content={
        "result": result,
        "time_ms": round((time.time() - start_time) * 1000, 2)
    })
