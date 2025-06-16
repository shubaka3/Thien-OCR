from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from PIL import Image
import io
import numpy as np

app = FastAPI()

ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.post("/ocr-basic")
async def ocr_basic(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_np = np.array(image)  # <--- chuyển đổi
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    result = ocr.ocr(image_np, cls=True)

    output = []
    for line in result:
        output.append({
            "box": line[0],
            "text": line[1][0],
            "confidence": line[1][1]
        })

    return JSONResponse(content={"result": output})

@app.post("/ocr-full")
async def ocr_full(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_np = np.array(image)  # <--- chuyển đổi
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    result = ocr.ocr(image_np, cls=True)

    return JSONResponse(content={"result": result})

@app.post("/ocr-fullv2")
async def ocr_full(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_np = np.array(image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    raw_result = ocr.ocr(image_np, cls=True)

    formatted_result = []
    for line in raw_result:
        formatted_result.append({
            "box": line[0],            # list 4 điểm
            "text": line[1][0],        # text string
        })

    return JSONResponse(content={"result": formatted_result})


