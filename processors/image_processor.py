from pathlib import Path
from typing import Optional
from PIL import Image
from .base_processor import BaseProcessor
from config import SUPPORTED_IMAGE_FORMATS, IMAGE_MAX_SIZE, IMAGE_MAX_SIZE_MB


class ImageProcessor(BaseProcessor):
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in SUPPORTED_IMAGE_FORMATS
    
    def extract_text(self, file_path: Path, llm_provider=None) -> str:
        try:
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            if file_size_mb > IMAGE_MAX_SIZE_MB:
                return (
                    f"Изображение '{file_path.name}' слишком большое ({file_size_mb:.2f} МБ). "
                    f"Максимальный размер для анализа: {IMAGE_MAX_SIZE_MB} МБ."
                )
            
            if llm_provider:
                try:
                    print(f"  Анализ изображения с помощью vision-модели...")
                    analysis = llm_provider.analyze_image(file_path)
                    return analysis
                except Exception as e:
                    print(f"  Предупреждение: Не удалось проанализировать изображение через vision API: {str(e)}")
                    print(f"  Используется базовое описание метаданных.")
            
            with Image.open(file_path) as img:
                width, height = img.size
                format_name = img.format
                mode = img.mode
                
                description = (
                    f"Изображение: {file_path.name}\n"
                    f"Формат: {format_name}\n"
                    f"Размеры: {width}x{height} пикселей\n"
                    f"Цветовой режим: {mode}\n"
                    f"Размер файла: {file_size_mb:.2f} МБ\n"
                    f"Примечание: Содержимое изображения не было проанализировано. "
                    f"Для анализа используйте vision-модель."
                )
                
                return description
                
        except Exception as e:
            return f"Ошибка при обработке изображения '{file_path.name}': {str(e)}"
    
    def prepare_image_for_ocr(self, file_path: Path) -> Optional[Image.Image]:      
        try:
            img = Image.open(file_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.thumbnail(IMAGE_MAX_SIZE, Image.Resampling.LANCZOS)
            
            return img
        except Exception as e:
            print(f"Ошибка при подготовке изображения: {str(e)}")
            return None
