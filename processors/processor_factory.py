from pathlib import Path
from typing import Optional, List
from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor


class ProcessorFactory:
    def __init__(self):
        self.processors: List[BaseProcessor] = [
            PDFProcessor(),
            ImageProcessor(),
        ]
    
    def get_processor(self, file_path: Path) -> Optional[BaseProcessor]:
        for processor in self.processors:
            if processor.can_process(file_path):
                return processor
        
        return None
    
    def register_processor(self, processor: BaseProcessor):
        self.processors.append(processor)
    
    def can_process_file(self, file_path: Path) -> bool:
        return self.get_processor(file_path) is not None
