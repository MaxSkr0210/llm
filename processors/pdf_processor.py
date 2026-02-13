from pathlib import Path
from typing import Optional
import PyPDF2
from .base_processor import BaseProcessor
from config import SUPPORTED_PDF_FORMATS


class PDFProcessor(BaseProcessor):
    
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in SUPPORTED_PDF_FORMATS
    
    def extract_text(self, file_path: Path) -> str:
        try:
            text_parts = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():
                        text_parts.append(text)
            
            extracted_text = "\n".join(text_parts)
            
            if not extracted_text.strip():
                return f"PDF файл '{file_path.name}' не содержит извлекаемого текста (возможно, это сканированное изображение)."
            
            return extracted_text
            
        except Exception as e:
            return f"Ошибка при обработке PDF файла '{file_path.name}': {str(e)}"
