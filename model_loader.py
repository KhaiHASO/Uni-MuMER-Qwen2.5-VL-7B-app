"""
Module để load và sử dụng mô hình Uni-MuMER-Qwen2.5-VL-7B
"""

import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
import logging
from typing import Optional, Tuple, Union
from PIL import Image
import os

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniMuMERModel:
    """Class để quản lý mô hình Uni-MuMER-Qwen2.5-VL-7B"""
    
    def __init__(self, model_path: str = "./Uni-MuMER-Qwen2.5-VL-7B"):
        """
        Khởi tạo mô hình
        
        Args:
            model_path (str): Đường dẫn đến thư mục chứa mô hình
        """
        self.model_path = model_path
        self.model = None
        self.processor = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self) -> bool:
        """
        Load mô hình và các components
        
        Returns:
            bool: True nếu load thành công, False nếu có lỗi
        """
        try:
            logger.info(f"Đang load mô hình từ: {self.model_path}")
            
            # Kiểm tra đường dẫn mô hình
            if not os.path.exists(self.model_path):
                logger.error(f"Không tìm thấy thư mục mô hình: {self.model_path}")
                return False
            
            # Load processor và tokenizer
            logger.info("Đang load processor và tokenizer...")
            self.processor = AutoProcessor.from_pretrained(
                self.model_path, 
                trust_remote_code=True
            )
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, 
                trust_remote_code=True
            )
            
            # Load mô hình
            logger.info("Đang load mô hình...")
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("Load mô hình thành công!")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi load mô hình: {str(e)}")
            return False
    
    def is_loaded(self) -> bool:
        """Kiểm tra xem mô hình đã được load chưa"""
        return self.model is not None and self.processor is not None and self.tokenizer is not None
    
    def convert_image_to_latex(
        self, 
        image: Union[Image.Image, str], 
        prompt: str = None,
        max_new_tokens: int = 512,
        temperature: float = 0.1,
        top_p: float = 0.9,
        repetition_penalty: float = 1.1
    ) -> Optional[str]:
        """
        Chuyển đổi ảnh toán học thành LaTeX
        
        Args:
            image: Ảnh đầu vào (PIL Image hoặc đường dẫn file)
            prompt: Prompt để hướng dẫn mô hình
            max_new_tokens: Số token tối đa để generate
            temperature: Nhiệt độ sampling
            top_p: Top-p sampling
            repetition_penalty: Penalty cho repetition
            
        Returns:
            str: LaTeX code hoặc None nếu có lỗi
        """
        if not self.is_loaded():
            logger.error("Mô hình chưa được load!")
            return None
        
        try:
            # Load ảnh nếu là đường dẫn
            if isinstance(image, str):
                image = Image.open(image)
            
            # Prompt mặc định
            if prompt is None:
                prompt = "Convert this mathematical image to LaTeX format. Only output the LaTeX code without any explanation."
            
            # Chuẩn bị messages
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
            text = self.processor.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            image_inputs, video_inputs = self.processor.process_vision_info(messages)
            inputs = self.processor(
                text=[text], 
                images=image_inputs, 
                videos=video_inputs, 
                return_tensors="pt"
            )
            
            # Generate
            logger.info("Đang generate LaTeX...")
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    temperature=temperature,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty
                )
            
            # Decode
            generated_ids = [
                output_ids[len(input_ids):] 
                for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
            ]
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Làm sạch output
            latex_code = self._clean_latex_output(response)
            
            logger.info("Generate LaTeX thành công!")
            return latex_code
            
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi ảnh: {str(e)}")
            return None
    
    def _clean_latex_output(self, text: str) -> str:
        """
        Làm sạch output để chỉ lấy LaTeX code
        
        Args:
            text: Text output từ mô hình
            
        Returns:
            str: LaTeX code đã làm sạch
        """
        import re
        
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
    
    def get_model_info(self) -> dict:
        """
        Lấy thông tin về mô hình
        
        Returns:
            dict: Thông tin mô hình
        """
        info = {
            "model_path": self.model_path,
            "device": self.device,
            "is_loaded": self.is_loaded(),
            "cuda_available": torch.cuda.is_available()
        }
        
        if self.is_loaded():
            info.update({
                "model_type": type(self.model).__name__,
                "tokenizer_type": type(self.tokenizer).__name__,
                "processor_type": type(self.processor).__name__
            })
        
        return info

# Hàm tiện ích để sử dụng nhanh
def quick_convert(image_path: str, model_path: str = "./Uni-MuMER-Qwen2.5-VL-7B") -> Optional[str]:
    """
    Hàm tiện ích để chuyển đổi nhanh ảnh thành LaTeX
    
    Args:
        image_path: Đường dẫn đến file ảnh
        model_path: Đường dẫn đến thư mục mô hình
        
    Returns:
        str: LaTeX code hoặc None nếu có lỗi
    """
    model = UniMuMERModel(model_path)
    
    if not model.load_model():
        return None
    
    return model.convert_image_to_latex(image_path)

if __name__ == "__main__":
    # Test mô hình
    model = UniMuMERModel()
    
    if model.load_model():
        print("✅ Load mô hình thành công!")
        print(f"📊 Thông tin mô hình: {model.get_model_info()}")
    else:
        print("❌ Không thể load mô hình!")
