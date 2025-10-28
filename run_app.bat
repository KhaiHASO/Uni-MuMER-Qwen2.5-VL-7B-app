@echo off
REM Script để chạy ứng dụng Uni-MuMER-Qwen2.5-VL-7B Streamlit Demo trên Windows

echo 🧮 Uni-MuMER-Qwen2.5-VL-7B Streamlit Demo
echo ==========================================

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy. Vui lòng cài đặt Python 3.10+
    pause
    exit /b 1
)

REM Kiểm tra conda
conda --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Conda được tìm thấy
    
    REM Kiểm tra environment
    conda env list | findstr "uni-mumer-qwen2.5-vl" >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Environment 'uni-mumer-qwen2.5-vl' đã tồn tại
        echo 🔄 Kích hoạt environment...
        call conda activate uni-mumer-qwen2.5-vl
    ) else (
        echo ⚠️ Environment 'uni-mumer-qwen2.5-vl' chưa tồn tại
        echo 🔄 Tạo environment từ environment.yml...
        conda env create -f environment.yml
        call conda activate uni-mumer-qwen2.5-vl
    )
) else (
    echo ⚠️ Conda không được tìm thấy, sử dụng pip
    
    REM Kiểm tra virtual environment
    if not exist "venv" (
        echo 🔄 Tạo virtual environment...
        python -m venv venv
    )
    
    REM Kích hoạt virtual environment
    call venv\Scripts\activate.bat
    
    REM Cài đặt dependencies
    echo 🔄 Cài đặt dependencies...
    pip install -r requirements.txt
)

REM Kiểm tra Streamlit
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit chưa được cài đặt
    pause
    exit /b 1
)

REM Kiểm tra thư mục mô hình
if not exist "Uni-MuMER-Qwen2.5-VL-7B" (
    echo ⚠️ Thư mục mô hình 'Uni-MuMER-Qwen2.5-VL-7B' không tồn tại
    echo 📁 Vui lòng đảm bảo thư mục mô hình có trong thư mục hiện tại
    echo 📁 Cấu trúc mong đợi:
    echo    Uni-MuMER-Qwen2.5-VL-7B/
    echo    ├── config.json
    echo    ├── model.safetensors.index.json
    echo    ├── tokenizer.json
    echo    └── ...
    pause
    exit /b 1
)

echo ✅ Tất cả kiểm tra đã hoàn thành!
echo 🚀 Khởi động ứng dụng Streamlit...
echo.
echo 📱 Ứng dụng sẽ mở tại: http://localhost:8501
echo 🛑 Nhấn Ctrl+C để dừng ứng dụng
echo.

REM Chạy ứng dụng
streamlit run app.py

pause
