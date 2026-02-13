from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseProcessor(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def can_process(self, file_path: Path) -> bool:
        pass
    
    @abstractmethod
    def extract_text(self, file_path: Path) -> str:
        pass
    
    def get_file_info(self, file_path: Path) -> dict:
        stat = file_path.stat()
        return {
            'filename': file_path.name,
            'size': stat.st_size,
            'extension': file_path.suffix.lower()
        }
