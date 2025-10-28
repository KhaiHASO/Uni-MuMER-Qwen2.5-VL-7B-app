"""
Cấu hình tối ưu hóa cho ứng dụng Uni-MuMER-Qwen2.5-VL-7B
"""

import os
import torch

class Config:
    """Class chứa các cấu hình cho ứng dụng"""
    
    # Đường dẫn mô hình
    MODEL_PATH = "./Uni-MuMER-Qwen2.5-VL-7B"
    
    # Cấu hình GPU
    USE_GPU = torch.cuda.is_available()
    DEVICE = "cuda" if USE_GPU else "cpu"
    
    # Cấu hình mô hình
    MODEL_CONFIG = {
        "torch_dtype": torch.bfloat16,
        "device_map": "auto",
        "trust_remote_code": True
    }
    
    # Cấu hình generation
    GENERATION_CONFIG = {
        "max_new_tokens": 512,
        "do_sample": False,
        "temperature": 0.1,
        "top_p": 0.9,
        "repetition_penalty": 1.1,
        "pad_token_id": None
    }
    
    # Cấu hình ảnh
    IMAGE_CONFIG = {
        "max_size": (1024, 1024),
        "supported_formats": ['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        "max_file_size": 10 * 1024 * 1024  # 10MB
    }
    
    # Cấu hình Streamlit
    STREAMLIT_CONFIG = {
        "page_title": "Uni-MuMER-Qwen2.5-VL-7B Demo",
        "page_icon": "🧮",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # Prompt templates
    PROMPTS = {
        "math_to_latex": "Convert this mathematical image to LaTeX format. Only output the LaTeX code without any explanation.",
        "equation_to_latex": "Convert this mathematical equation to LaTeX format. Only output the LaTeX code.",
        "formula_to_latex": "Convert this mathematical formula to LaTeX format. Only output the LaTeX code."
    }
    
    # Cấu hình logging
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
    
    @classmethod
    def get_device_info(cls):
        """Lấy thông tin về device"""
        info = {
            "device": cls.DEVICE,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
        }
        
        if torch.cuda.is_available():
            info.update({
                "cuda_version": torch.version.cuda,
                "current_device": torch.cuda.current_device(),
                "device_name": torch.cuda.get_device_name(0)
            })
        
        return info
    
    @classmethod
    def optimize_for_device(cls):
        """Tối ưu hóa cấu hình cho device hiện tại"""
        if cls.USE_GPU:
            # Tối ưu cho GPU
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            
            # Cấu hình memory
            if hasattr(torch.cuda, 'set_memory_fraction'):
                torch.cuda.set_memory_fraction(0.9)
        else:
            # Tối ưu cho CPU
            torch.set_num_threads(os.cpu_count())
    
    @classmethod
    def get_model_config(cls):
        """Lấy cấu hình mô hình"""
        config = cls.MODEL_CONFIG.copy()
        
        if not cls.USE_GPU:
            config["device_map"] = None
            config["torch_dtype"] = torch.float32
        
        return config

# Khởi tạo cấu hình
config = Config()
config.optimize_for_device()

# Export các cấu hình quan trọng
DEVICE = config.DEVICE
USE_GPU = config.USE_GPU
MODEL_PATH = config.MODEL_PATH
GENERATION_CONFIG = config.GENERATION_CONFIG
IMAGE_CONFIG = config.IMAGE_CONFIG
PROMPTS = config.PROMPTS
