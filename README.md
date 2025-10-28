# 🧮 Uni-MuMER-Qwen2.5-VL-7B Streamlit Demo

Ứng dụng Streamlit để demo mô hình **Uni-MuMER-Qwen2.5-VL-7B** - chuyển đổi ảnh toán học thành LaTeX code.

## 📋 Mô tả

Uni-MuMER-Qwen2.5-VL-7B là một mô hình Vision-Language được fine-tune từ Qwen2.5-VL-7B-Instruct, chuyên dụng để chuyển đổi ảnh chứa công thức toán học thành mã LaTeX. Ứng dụng này cung cấp giao diện web thân thiện để demo khả năng của mô hình.

## ✨ Tính năng

- 🖼️ **Upload ảnh**: Hỗ trợ nhiều định dạng ảnh (PNG, JPEG, BMP, TIFF)
- 🔄 **Chuyển đổi tự động**: Chuyển đổi ảnh toán học thành LaTeX code
- 👁️ **Preview**: Xem trước công thức được render
- 📋 **Copy code**: Sao chép LaTeX code để sử dụng
- ⚙️ **Tùy chỉnh**: Điều chỉnh các tham số mô hình
- 📱 **Responsive**: Giao diện thân thiện trên mọi thiết bị

## 🚀 Cài đặt

### Yêu cầu hệ thống

- **Python**: 3.10+
- **CUDA**: 11.8+ (khuyến nghị cho GPU)
- **RAM**: Tối thiểu 16GB (khuyến nghị 32GB+)
- **VRAM**: Tối thiểu 8GB (nếu sử dụng GPU)

### Cài đặt bằng Conda (Khuyến nghị)

1. **Clone repository**:
```bash
git clone <repository-url>
cd uni-mumer-qwen2.5-vl-streamlit
```

2. **Tạo môi trường conda**:
```bash
conda env create -f environment.yml
```

3. **Kích hoạt môi trường**:
```bash
conda activate uni-mumer-qwen2.5-vl
```

4. **Kiểm tra cài đặt**:
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Cài đặt bằng pip

1. **Tạo môi trường Python**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

2. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

## 📁 Cấu trúc thư mục

```
uni-mumer-qwen2.5-vl-streamlit/
├── app.py                 # Ứng dụng Streamlit chính
├── model_loader.py        # Module load mô hình
├── requirements.txt       # Dependencies cho pip
├── environment.yml        # Environment cho conda
├── README.md             # Hướng dẫn này
└── Uni-MuMER-Qwen2.5-VL-7B/  # Thư mục chứa mô hình
    ├── config.json
    ├── model.safetensors.index.json
    ├── tokenizer.json
    └── ... (các file mô hình khác)
```

## 🎯 Sử dụng

### Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

### Hướng dẫn sử dụng

1. **Upload ảnh**: 
   - Nhấn "Browse files" để chọn ảnh chứa công thức toán học
   - Hỗ trợ định dạng: PNG, JPEG, BMP, TIFF

2. **Chuyển đổi**:
   - Nhấn nút "🚀 Chuyển đổi sang LaTeX"
   - Chờ mô hình xử lý (có thể mất vài giây)

3. **Xem kết quả**:
   - LaTeX code sẽ hiển thị trong ô kết quả
   - Preview công thức được render bên dưới
   - Sử dụng nút "📋 Copy LaTeX Code" để sao chép

4. **Tùy chỉnh**:
   - Điều chỉnh các tham số trong sidebar
   - Max tokens, Temperature, Top-p, etc.

### Sử dụng module trực tiếp

```python
from model_loader import UniMuMERModel

# Khởi tạo mô hình
model = UniMuMERModel("./Uni-MuMER-Qwen2.5-VL-7B")

# Load mô hình
if model.load_model():
    # Chuyển đổi ảnh
    latex_code = model.convert_image_to_latex("path/to/image.png")
    print(f"LaTeX: {latex_code}")
```

## ⚙️ Cấu hình

### Tham số mô hình

- **Max tokens**: Số token tối đa để generate (mặc định: 512)
- **Temperature**: Nhiệt độ sampling (mặc định: 0.1)
- **Top-p**: Top-p sampling (mặc định: 0.9)
- **Repetition penalty**: Penalty cho repetition (mặc định: 1.1)

### Cấu hình GPU

Mô hình sẽ tự động sử dụng GPU nếu có sẵn. Để kiểm tra:

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
```

## 🔧 Troubleshooting

### Lỗi thường gặp

1. **"Không thể load mô hình"**:
   - Kiểm tra đường dẫn thư mục mô hình
   - Đảm bảo có đủ RAM/VRAM
   - Kiểm tra các file mô hình có đầy đủ không

2. **"CUDA out of memory"**:
   - Giảm batch size
   - Sử dụng CPU thay vì GPU
   - Giảm độ phân giải ảnh

3. **"Module not found"**:
   - Cài đặt lại dependencies: `pip install -r requirements.txt`
   - Kiểm tra môi trường conda đã được kích hoạt

### Performance Tips

- **GPU**: Sử dụng GPU để tăng tốc độ xử lý
- **RAM**: Đảm bảo có đủ RAM (16GB+)
- **Ảnh**: Sử dụng ảnh có độ phân giải vừa phải
- **Batch**: Xử lý từng ảnh một để tránh out of memory

## 📊 Thông tin mô hình

- **Base model**: Qwen2.5-VL-7B-Instruct
- **Architecture**: Qwen2_5_VLForConditionalGeneration
- **Parameters**: ~7B
- **Input**: Ảnh + Text prompt
- **Output**: LaTeX code
- **License**: Apache 2.0

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới giấy phép Apache 2.0. Xem file `LICENSE` để biết thêm chi tiết.

## 🙏 Acknowledgments

- **Qwen Team**: Cho mô hình Qwen2.5-VL-7B-Instruct
- **Hugging Face**: Cho thư viện Transformers
- **Streamlit**: Cho framework web app

## 📞 Liên hệ

Nếu có câu hỏi hoặc gặp vấn đề, vui lòng tạo issue trên GitHub repository.

---

**Lưu ý**: Mô hình này được fine-tune cho mục đích chuyển đổi ảnh toán học thành LaTeX. Kết quả có thể khác nhau tùy thuộc vào chất lượng và độ phức tạp của ảnh đầu vào.