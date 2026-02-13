import requests
import base64
from typing import Optional, List, Dict
from pathlib import Path
from PIL import Image
import io

from .base import BaseLLMProvider
from config import (
    OPENROUTER_API_KEY, OPENROUTER_API_URL, DEFAULT_MODEL, DEFAULT_VISION_MODEL,
    MAX_TOKENS, TEMPERATURE
)
from prompts import IMAGE_ANALYSIS_PROMPT



class OpenRouterProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, vision_model: Optional[str] = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or DEFAULT_MODEL
        self.vision_model = vision_model or DEFAULT_VISION_MODEL
        
        if not self.api_key:
            raise ValueError(
                "API ключ OpenRouter не найден. "
                "Установите OPENROUTER_API_KEY в переменных окружения или .env файле"
            )
    
    def generate_summary(self, text: str, context: Optional[str] = None) -> str:
        prompt = self._build_prompt(text, context)
        
        try:
            response = self._make_request(prompt)
            return response
        except Exception as e:
            raise Exception(f"Ошибка при генерации саммари: {str(e)}")
    
    def generate_combined_summary(self, summaries: List[Dict[str, str]]) -> str:
        combined_text = self._format_summaries_for_combining(summaries)
        prompt = self._build_combined_prompt(combined_text)
        
        try:
            response = self._make_request(prompt)
            return response
        except Exception as e:
            raise Exception(f"Ошибка при генерации объединенного саммари: {str(e)}")
    
    def analyze_image(self, image_path: Path) -> str:
        try:
            image_base64 = self._image_to_base64(image_path)
            response = self._make_vision_request(IMAGE_ANALYSIS_PROMPT, image_base64)
            return response
        except Exception as e:
            raise Exception(f"Ошибка при анализе изображения: {str(e)}")
    
    def _image_to_base64(self, image_path: Path) -> str:
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                from config import IMAGE_MAX_SIZE
                img.thumbnail(IMAGE_MAX_SIZE, Image.Resampling.LANCZOS)
                
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                buffer.seek(0)
                image_bytes = buffer.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                return image_base64
        except Exception as e:
            raise Exception(f"Ошибка при конвертации изображения: {str(e)}")
    
    def _make_vision_request(self, prompt: str, image_base64: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com",
            "X-Title": "Document Summarizer"
        }
        
        payload = {
            "model": self.vision_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
        
        return self._execute_request(headers, payload, is_vision=True)
    
    def _make_request(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com",
            "X-Title": "Document Summarizer"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
        
        return self._execute_request(headers, payload)
    
    def _execute_request(self, headers: dict, payload: dict, is_vision: bool = False) -> str:
        try:
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=90 if is_vision else 60)
            
            if response.status_code == 404:
                model_name = payload.get("model", "unknown")
                error_type = "Vision-модель" if is_vision else "Модель"
                error_msg = (
                    f"Ошибка 404: {error_type} '{model_name}' не найдена."
                )
                try:
                    error_detail = response.json()
                    if "error" in error_detail:
                        error_msg += f"\nДетали: {error_detail['error']}"
                except:
                    error_msg += f"\nОтвет сервера: {response.text[:200]}"
                raise Exception(error_msg)
            
            if response.status_code == 401:
                raise Exception(
                    "Ошибка 401: Неверный API ключ. "
                    "Проверьте правильность OPENROUTER_API_KEY в .env файле или переменных окружения."
                )
            
            if response.status_code == 429:
                raise Exception(
                    "Ошибка 429: Превышен лимит запросов. "
                    "Подождите немного и попробуйте снова."
                )
            
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                error_info = result["error"]
                error_msg = f"Ошибка API: {error_info.get('message', 'Неизвестная ошибка')}"
                if "type" in error_info:
                    error_msg += f" (тип: {error_info['type']})"
                raise Exception(error_msg)
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"Неожиданный формат ответа от API: {result}")
                
        except requests.exceptions.Timeout:
            raise Exception("Таймаут при запросе к API. Попробуйте позже.")
        except requests.exceptions.ConnectionError:
            raise Exception("Ошибка подключения к API. Проверьте интернет-соединение.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к API: {str(e)}")
