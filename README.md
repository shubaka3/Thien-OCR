### CHECKED-DONE

Chạy Docker build
test với postman
http://localhost:8000/ocr-full
body: from-data
Key: file
Value: image.jpg/png

Docker
1) docker build -t my-python-app . (thay my-python-app bằng tên bạn muốn)
1.5) docker build -t thien-ocr .

2) docker run -p 8000:8000 my-python-app (hoặc mở docker desktop và chạy container
nhưng phải chạy 1 lần để build container)

3) có thể sửa theo lệnh dưới để hỗ trợ đa luồng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]



