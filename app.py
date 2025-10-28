import streamlit as st
from PIL import Image

from config import APP_TITLE, IMAGE_MAX_SIZE
from model_loader import load_tamer_model


st.set_page_config(page_title=APP_TITLE, page_icon="📝", layout="wide", initial_sidebar_state="expanded")


@st.cache_resource
def get_model():
    return load_tamer_model()


def main():
    st.title(APP_TITLE)
    st.markdown("Chuyển đổi ảnh công thức toán học viết tay sang LaTeX bằng TAMER.")

    model = get_model()
    if model is None:
        st.warning("Chưa tìm thấy checkpoint TAMER. Hãy đặt file checkpoint vào thư mục `weights/` hoặc cấu hình `TAMER_MODEL_DIR`/`TAMER_CHECKPOINT`.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Upload ảnh")
        uploaded_file = st.file_uploader("Chọn ảnh HME", type=["png", "jpg", "jpeg", "bmp", "tiff"]) 
        image = None
        if uploaded_file:
            image = Image.open(uploaded_file)
            image.thumbnail(IMAGE_MAX_SIZE)
            st.image(image, caption="Ảnh đã upload", width='stretch')

    with col2:
        st.subheader("Kết quả")
        if st.button("Nhận dạng LaTeX", type="primary", disabled=(model is None), width='stretch'):
            if image is None:
                st.error("Vui lòng upload ảnh trước.")
            else:
                with st.spinner("Đang nhận dạng..."):
                    latex = model.infer(image) if model else None
                if latex:
                    st.success("Nhận dạng thành công!")
                    st.code(latex, language="latex")
                else:
                    st.error("Không nhận dạng được. Kiểm tra model/checkpoint.")

    st.markdown("---")
    st.caption("TAMER: Tree-Aware Transformer for Handwritten Mathematical Expression Recognition")


if __name__ == "__main__":
    main()


