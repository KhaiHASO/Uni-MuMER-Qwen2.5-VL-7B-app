# 🚀 Quick Start Guide

## Cài đặt nhanh (Conda)

```bash
# 1. Tạo environment
conda env create -f environment.yml

# 2. Kích hoạt environment
conda activate uni-mumer-qwen2.5-vl

# 3. Chạy ứng dụng
streamlit run app.py
```

## Cài đặt nhanh (Pip)

```bash
# 1. Tạo virtual environment
python -m venv venv

# 2. Kích hoạt environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Chạy ứng dụng
streamlit run app.py
```

## Chạy bằng script

### Windows:
```bash
run_app.bat
```

### Linux/Mac:
```bash
chmod +x run_app.sh
./run_app.sh
```

## Test mô hình

```bash
# Test với ảnh mẫu
python test_model.py

# Tạo ảnh test
python test_model.py create_images
```

## Truy cập ứng dụng

Mở trình duyệt và truy cập: `http://localhost:8501`

## Yêu cầu hệ thống

- **Python**: 3.10+
- **RAM**: 16GB+ (khuyến nghị 32GB+)
- **VRAM**: 8GB+ (nếu sử dụng GPU)
- **CUDA**: 11.8+ (khuyến nghị)

## Troubleshooting

### Lỗi "Không thể load mô hình":
- Kiểm tra thư mục `Uni-MuMER-Qwen2.5-VL-7B` có đầy đủ file không
- Đảm bảo có đủ RAM/VRAM

### Lỗi "CUDA out of memory":
- Giảm độ phân giải ảnh
- Sử dụng CPU thay vì GPU
- Xử lý từng ảnh một

### Lỗi "Module not found":
- Cài đặt lại dependencies
- Kiểm tra environment đã được kích hoạt
