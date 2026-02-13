"""
Пакет процессоров для обработки различных типов файлов
"""
from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .processor_factory import ProcessorFactory

__all__ = [
    'BaseProcessor',
    'PDFProcessor',
    'ImageProcessor',
    'ProcessorFactory'
]
