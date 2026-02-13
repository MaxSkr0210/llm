"""
Основной модуль для создания саммари документов
"""
from pathlib import Path
from typing import List, Dict, Optional
from llm_providers.factory import LLMProviderFactory
from processors.processor_factory import ProcessorFactory
from processors.image_processor import ImageProcessor
from config import SUPPORTED_FORMATS, MAX_FILE_SIZE_MB, SUPPORTED_IMAGE_FORMATS


class DocumentSummarizer:
    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        vision_model: Optional[str] = None
    ):
        """
        Инициализация саммаризатора
        
        Args:
            provider: Имя провайдера LLM ('openrouter', 'openai', и т.д.)
            api_key: API ключ (опционально)
            model: Модель для использования (опционально)
            vision_model: Vision-модель для анализа изображений (опционально)
        """
        self.llm_provider = LLMProviderFactory.create_provider(
            provider_name=provider,
            api_key=api_key,
            model=model,
            vision_model=vision_model
        )
        self.processor_factory = ProcessorFactory()
    
    def process_folder(self, folder_path: Path) -> Dict[str, any]:
        if not folder_path.exists():
            raise ValueError(f"Папка не существует: {folder_path}")
        
        if not folder_path.is_dir():
            raise ValueError(f"Указанный путь не является папкой: {folder_path}")
        
        files = self._find_supported_files(folder_path)
        
        if not files:
            return {
                'total_files': 0,
                'processed_files': 0,
                'individual_summaries': [],
                'combined_summary': 'Не найдено поддерживаемых файлов для обработки.'
            }
        
        individual_summaries = []
        processed_count = 0
        
        for file_path in files:
            try:
                result = self._process_file(file_path)
                if result:
                    individual_summaries.append(result)
                    processed_count += 1
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path.name}: {str(e)}")
                continue
        
        combined_summary = ""
        if individual_summaries:
            try:
                combined_summary = self.llm_provider.generate_combined_summary(individual_summaries)
            except Exception as e:
                combined_summary = f"Ошибка при создании общего саммари: {str(e)}"
        
        return {
            'total_files': len(files),
            'processed_files': processed_count,
            'individual_summaries': individual_summaries,
            'combined_summary': combined_summary
        }
    
    def _find_supported_files(self, folder_path: Path) -> List[Path]:
        files = []
        
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                if file_path.suffix.lower() in SUPPORTED_FORMATS:
                    file_size_mb = file_path.stat().st_size / (1024 * 1024)
                    if file_size_mb <= MAX_FILE_SIZE_MB:
                        files.append(file_path)
                    else:
                        print(f"Файл {file_path.name} слишком большой ({file_size_mb:.2f} МБ), пропускаем")
        
        return sorted(files)
    
    def _process_file(self, file_path: Path) -> Optional[Dict[str, str]]:
        processor = self.processor_factory.get_processor(file_path)
        
        if not processor:
            print(f"Не найден процессор для файла: {file_path.name}")
            return None
        
        print(f"Обработка файла: {file_path.name}")
        
        is_image = file_path.suffix.lower() in SUPPORTED_IMAGE_FORMATS
        if is_image and isinstance(processor, ImageProcessor):
            extracted_content = processor.extract_text(file_path, llm_provider=self.llm_provider)
        else:
            extracted_content = processor.extract_text(file_path)
        
        if not extracted_content or not extracted_content.strip():
            print(f"Не удалось извлечь содержимое из файла: {file_path.name}")
            return None
        
        try:
            if is_image:
                summary = self.llm_provider.generate_summary(extracted_content)
            else:
                summary = self.llm_provider.generate_summary(extracted_content)
            
            return {
                'filename': file_path.name,
                'summary': summary
            }
        except Exception as e:
            print(f"Ошибка при создании саммари для {file_path.name}: {str(e)}")
            return None
    
    def add_processor(self, processor):
        self.processor_factory.register_processor(processor)
