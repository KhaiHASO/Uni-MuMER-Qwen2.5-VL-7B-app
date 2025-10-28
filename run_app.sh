#!/bin/bash

# Script để chạy ứng dụng Uni-MuMER-Qwen2.5-VL-7B Streamlit Demo

echo "🧮 Uni-MuMER-Qwen2.5-VL-7B Streamlit Demo"
echo "=========================================="

# Kiểm tra Python
if ! command -v python &> /dev/null; then
    echo "❌ Python không được tìm thấy. Vui lòng cài đặt Python 3.10+"
    exit 1
fi

# Kiểm tra conda
if command -v conda &> /dev/null; then
    echo "✅ Conda được tìm thấy"
    
    # Kiểm tra environment
    if conda env list | grep -q "uni-mumer-qwen2.5-vl"; then
        echo "✅ Environment 'uni-mumer-qwen2.5-vl' đã tồn tại"
        echo "🔄 Kích hoạt environment..."
        conda activate uni-mumer-qwen2.5-vl
    else
        echo "⚠️ Environment 'uni-mumer-qwen2.5-vl' chưa tồn tại"
        echo "🔄 Tạo environment từ environment.yml..."
        conda env create -f environment.yml
        conda activate uni-mumer-qwen2.5-vl
    fi
else
    echo "⚠️ Conda không được tìm thấy, sử dụng pip"
    
    # Kiểm tra virtual environment
    if [ ! -d "venv" ]; then
        echo "🔄 Tạo virtual environment..."
        python -m venv venv
    fi
    
    # Kích hoạt virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Cài đặt dependencies
    echo "🔄 Cài đặt dependencies..."
    pip install -r requirements.txt
fi

# Kiểm tra Streamlit
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit chưa được cài đặt"
    exit 1
fi

# Kiểm tra thư mục mô hình
if [ ! -d "Uni-MuMER-Qwen2.5-VL-7B" ]; then
    echo "⚠️ Thư mục mô hình 'Uni-MuMER-Qwen2.5-VL-7B' không tồn tại"
    echo "📁 Vui lòng đảm bảo thư mục mô hình có trong thư mục hiện tại"
    echo "📁 Cấu trúc mong đợi:"
    echo "   Uni-MuMER-Qwen2.5-VL-7B/"
    echo "   ├── config.json"
    echo "   ├── model.safetensors.index.json"
    echo "   ├── tokenizer.json"
    echo "   └── ..."
    exit 1
fi

echo "✅ Tất cả kiểm tra đã hoàn thành!"
echo "🚀 Khởi động ứng dụng Streamlit..."
echo ""
echo "📱 Ứng dụng sẽ mở tại: http://localhost:8501"
echo "🛑 Nhấn Ctrl+C để dừng ứng dụng"
echo ""

# Chạy ứng dụng
streamlit run app.py
