from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Dict
from prompts import build_summary_prompt, build_combined_summary_prompt


class BaseLLMProvider(ABC):
    
    @abstractmethod
    def generate_summary(self, text: str, context: Optional[str] = None) -> str:
        pass
    
    @abstractmethod
    def generate_combined_summary(self, summaries: List[Dict[str, str]]) -> str:
        pass
    
    @abstractmethod
    def analyze_image(self, image_path: Path) -> str:
        pass
    
    def _build_prompt(self, text: str, context: Optional[str] = None) -> str:
        return build_summary_prompt(text, context)
    
    def _build_combined_prompt(self, combined_text: str) -> str:
        return build_combined_summary_prompt(combined_text)
    
    def _format_summaries_for_combining(self, summaries: List[Dict[str, str]]) -> str:
        formatted = []
        for i, item in enumerate(summaries, 1):
            formatted.append(f"Документ {i} ({item['filename']}):\n{item['summary']}\n")
        return "\n".join(formatted)
