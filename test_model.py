"""
Script demo để test mô hình Uni-MuMER-Qwen2.5-VL-7B
"""

import os
import sys
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def create_sample_math_image():
    """Tạo ảnh mẫu chứa công thức toán học"""
    
    # Tạo figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Công thức toán học mẫu
    formulas = [
        r"$E = mc^2$",
        r"$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$",
        r"$\frac{d}{dx}[x^n] = nx^{n-1}$",
        r"$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$",
        r"$\lim_{x \to 0} \frac{\sin x}{x} = 1$"
    ]
    
    # Vẽ các công thức
    y_positions = [6.5, 5.5, 4.5, 3.5, 2.5]
    
    for i, (formula, y) in enumerate(zip(formulas, y_positions)):
        ax.text(5, y, formula, fontsize=16, ha='center', va='center')
    
    # Thêm tiêu đề
    ax.text(5, 7.5, "Mathematical Formulas", fontsize=20, ha='center', va='center', weight='bold')
    
    # Lưu ảnh
    plt.tight_layout()
    plt.savefig('sample_math_image.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Đã tạo ảnh mẫu: sample_math_image.png")

def test_model():
    """Test mô hình với ảnh mẫu"""
    
    # Kiểm tra file mẫu
    if not os.path.exists('sample_math_image.png'):
        print("🔄 Tạo ảnh mẫu...")
        create_sample_math_image()
    
    # Import model loader
    try:
        from model_loader import UniMuMERModel
    except ImportError:
        print("❌ Không thể import model_loader.py")
        return
    
    # Khởi tạo mô hình
    print("🔄 Khởi tạo mô hình...")
    model = UniMuMERModel()
    
    # Load mô hình
    if not model.load_model():
        print("❌ Không thể load mô hình")
        return
    
    print("✅ Load mô hình thành công!")
    
    # Test với ảnh mẫu
    print("🔄 Test với ảnh mẫu...")
    latex_result = model.convert_image_to_latex('sample_math_image.png')
    
    if latex_result:
        print("✅ Chuyển đổi thành công!")
        print(f"📝 LaTeX code: {latex_result}")
    else:
        print("❌ Không thể chuyển đổi ảnh")
    
    # Hiển thị thông tin mô hình
    info = model.get_model_info()
    print("\n📊 Thông tin mô hình:")
    for key, value in info.items():
        print(f"   {key}: {value}")

def create_test_images():
    """Tạo các ảnh test khác nhau"""
    
    # Tạo thư mục test
    os.makedirs('test_images', exist_ok=True)
    
    # Test 1: Công thức đơn giản
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')
    ax.text(0.5, 0.5, r"$x^2 + y^2 = r^2$", fontsize=24, ha='center', va='center', transform=ax.transAxes)
    plt.savefig('test_images/simple_formula.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Test 2: Phương trình phức tạp
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    ax.text(0.5, 0.5, r"$\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u$", fontsize=20, ha='center', va='center', transform=ax.transAxes)
    plt.savefig('test_images/complex_equation.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Test 3: Ma trận
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')
    ax.text(0.5, 0.5, r"$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$", fontsize=20, ha='center', va='center', transform=ax.transAxes)
    plt.savefig('test_images/matrix.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Đã tạo các ảnh test trong thư mục 'test_images/'")

if __name__ == "__main__":
    print("🧮 Uni-MuMER-Qwen2.5-VL-7B Test Script")
    print("=======================================")
    
    if len(sys.argv) > 1 and sys.argv[1] == "create_images":
        create_test_images()
    else:
        test_model()
