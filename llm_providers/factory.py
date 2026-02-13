from typing import Optional
from .base import BaseLLMProvider
from .openrouter import OpenRouterProvider
from config import LLM_PROVIDER


class LLMProviderFactory:
    
    _providers = {
        'openrouter': OpenRouterProvider,
        # Здесь можно добавить другие провайдеры:
        # 'openai': OpenAIProvider,
        # 'anthropic': AnthropicProvider,
        # 'local': LocalLLMProvider,
    }
    
    @classmethod
    def create_provider(
        cls,
        provider_name: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        vision_model: Optional[str] = None,
        **kwargs
    ) -> BaseLLMProvider:
        provider_name = provider_name or LLM_PROVIDER
        
        if provider_name not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Неизвестный провайдер '{provider_name}'. "
                f"Доступные провайдеры: {available}"
            )
        
        provider_class = cls._providers[provider_name]
        
        return provider_class(
            api_key=api_key,
            model=model,
            vision_model=vision_model,
            **kwargs
        )
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        if not issubclass(provider_class, BaseLLMProvider):
            raise ValueError("Провайдер должен наследоваться от BaseLLMProvider")
        
        cls._providers[name] = provider_class
    
    @classmethod
    def list_providers(cls):
        return list(cls._providers.keys())
