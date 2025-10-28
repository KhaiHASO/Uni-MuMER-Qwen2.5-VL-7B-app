import streamlit as st
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from PIL import Image
import io
import base64
import re
from config import DEVICE, USE_GPU, GENERATION_CONFIG, PROMPTS

# Cấu hình trang
st.set_page_config(
    page_title="Uni-MuMER-Qwen2.5-VL-7B Demo",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .result-box {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .latex-preview {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    .upload-section {
        border: 2px dashed #007bff;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        background-color: #f8f9ff;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load mô hình và tokenizer"""
    try:
        # Load mô hình từ thư mục local
        from config import MODEL_PATH, MODEL_CONFIG
        
        # Load processor và tokenizer
        processor = AutoProcessor.from_pretrained(MODEL_PATH, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        
        # Load mô hình với cấu hình tối ưu
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            MODEL_PATH,
            **MODEL_CONFIG
        )
        
        return model, processor, tokenizer
    except Exception as e:
        st.error(f"Lỗi khi load mô hình: {str(e)}")
        return None, None, None

def process_image_to_latex(image, model, processor, tokenizer):
    """Chuyển đổi ảnh thành LaTeX"""
    try:
        # Chuẩn bị prompt cho toán học
        prompt = PROMPTS["math_to_latex"]
        
        # Xử lý ảnh và text
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Tokenize
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = processor.process_vision_info(messages)
        inputs = processor(text=[text], images=image_inputs, videos=video_inputs, return_tensors="pt")
        
        # Generate với cấu hình tối ưu
        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                **GENERATION_CONFIG
            )
        
        # Decode
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Làm sạch output để chỉ lấy LaTeX
        latex_code = clean_latex_output(response)
        
        return latex_code
        
    except Exception as e:
        st.error(f"Lỗi khi xử lý ảnh: {str(e)}")
        return None

def clean_latex_output(text):
    """Làm sạch output để chỉ lấy LaTeX code"""
    # Loại bỏ các từ khóa không cần thiết
    text = re.sub(r'^(LaTeX|latex|Latex):?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(Here is|The|This is).*?:\s*', '', text, flags=re.IGNORECASE)
    
    # Tìm và trích xuất LaTeX code trong dấu $$
    latex_match = re.search(r'\$\$(.*?)\$\$', text, re.DOTALL)
    if latex_match:
        return latex_match.group(1).strip()
    
    # Tìm LaTeX code trong dấu $
    latex_match = re.search(r'\$(.*?)\$', text, re.DOTALL)
    if latex_match:
        return latex_match.group(1).strip()
    
    # Nếu không tìm thấy dấu $, trả về text đã làm sạch
    return text.strip()

def render_latex(latex_code):
    """Render LaTeX code thành công thức toán học"""
    try:
        # Sử dụng st.latex để render
        st.latex(latex_code)
        return True
    except Exception as e:
        st.warning(f"Không thể render LaTeX: {str(e)}")
        return False

def main():
    # Header
    st.markdown('<h1 class="main-header">🧮 Uni-MuMER-Qwen2.5-VL-7B Demo</h1>', unsafe_allow_html=True)
    st.markdown("### Chuyển đổi ảnh toán học thành LaTeX")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Cài đặt")
        
        # Model settings
        st.subheader("Thông số mô hình")
        max_tokens = st.slider("Max tokens", 100, 1000, 512)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.1)
        
        # Instructions
        st.subheader("📖 Hướng dẫn")
        st.markdown("""
        1. **Upload ảnh**: Chọn file ảnh chứa công thức toán học
        2. **Xử lý**: Nhấn nút "Chuyển đổi" để chạy mô hình
        3. **Kết quả**: Xem LaTeX code và công thức được render
        4. **Copy**: Sao chép LaTeX code để sử dụng
        """)
        
        # Supported formats
        st.subheader("📁 Định dạng hỗ trợ")
        st.markdown("""
        - **PNG** (.png)
        - **JPEG** (.jpg, .jpeg)
        - **BMP** (.bmp)
        - **TIFF** (.tiff)
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload ảnh")
        
        # Upload file
        uploaded_file = st.file_uploader(
            "Chọn file ảnh chứa công thức toán học",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload ảnh chứa công thức toán học để chuyển đổi thành LaTeX"
        )
        
        if uploaded_file is not None:
            # Hiển thị ảnh
            image = Image.open(uploaded_file)
            st.image(image, caption="Ảnh đã upload", use_column_width=True)
            
            # Thông tin file
            st.info(f"📁 **File**: {uploaded_file.name}  \n📏 **Kích thước**: {image.size}")
    
    with col2:
        st.subheader("⚡ Xử lý")
        
        if uploaded_file is not None:
            # Load model
            with st.spinner("🔄 Đang load mô hình..."):
                model, processor, tokenizer = load_model()
            
            if model is not None:
                # Process button
                if st.button("🚀 Chuyển đổi sang LaTeX", type="primary", use_container_width=True):
                    with st.spinner("🔄 Đang xử lý ảnh..."):
                        latex_result = process_image_to_latex(image, model, processor, tokenizer)
                    
                    if latex_result:
                        st.success("✅ Chuyển đổi thành công!")
                        
                        # Display results
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.subheader("📝 LaTeX Code:")
                        
                        # LaTeX code
                        st.code(latex_result, language="latex")
                        
                        # Copy button
                        if st.button("📋 Copy LaTeX Code", use_container_width=True):
                            st.code(latex_result)
                            st.success("✅ Đã copy vào clipboard!")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Preview
                        st.subheader("👁️ Preview:")
                        st.markdown('<div class="latex-preview">', unsafe_allow_html=True)
                        if render_latex(latex_result):
                            st.success("✅ Render thành công!")
                        else:
                            st.warning("⚠️ Không thể render LaTeX")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("❌ Không thể chuyển đổi ảnh")
            else:
                st.error("❌ Không thể load mô hình. Vui lòng kiểm tra đường dẫn mô hình.")
        else:
            st.info("👆 Vui lòng upload ảnh để bắt đầu")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚀 <strong>Uni-MuMER-Qwen2.5-VL-7B</strong> - Chuyển đổi ảnh toán học thành LaTeX</p>
        <p>💡 Dựa trên mô hình Qwen2.5-VL-7B-Instruct</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
