FROM python:3.8-slim

# Cài đặt các dependencies hệ thống
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    tesseract-ocr \
    tesseract-ocr-vie \
    tesseract-ocr-eng \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục app
WORKDIR /app

# Copy requirements trước
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code vào container
COPY main.py /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

