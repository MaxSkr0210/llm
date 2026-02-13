# Система создания саммари документов

Программа для создания общего саммари по содержимому папки с документами различных форматов (PDF, изображения и др.) с поддержкой различных LLM провайдеров (OpenRouter, OpenAI, Anthropic и др.).

## Возможности

- ✅ Обработка PDF файлов (извлечение текста)
- ✅ **Обработка изображений с анализом содержимого через vision-модели** (PNG, JPG, JPEG, WebP, GIF, BMP)
- ✅ Автоматическое распознавание текста на изображениях
- ✅ Создание общего объединенного саммари всех документов
- ✅ Модульная архитектура для легкого расширения
- ✅ **Поддержка переключения между LLM провайдерами** (OpenRouter, OpenAI, Anthropic и др.)
- ✅ Поддержка бесплатных моделей через OpenRouter

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Получите бесплатный API ключ на [OpenRouter](https://openrouter.ai/)

3. Создайте файл `.env` в корне проекта:
```bash
cp .env.example .env
```

4. Добавьте ваш API ключ в `.env`:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Использование

### Базовое использование:
```bash
python main.py docs/
```

### С указанием API ключа:
```bash
python main.py docs/ --api-key YOUR_API_KEY
```

### С выбором модели:
```bash
python main.py docs/ --model "google/gemini-3-flash-preview"
```

### С выбором vision-модели для изображений:
```bash
python main.py docs/ --vision-model "google/gemini-3-flash-preview"
```

### С выбором LLM провайдера:
```bash
# Использовать OpenRouter (по умолчанию)
python main.py docs/ --provider openrouter

# Использовать OpenAI (требует OPENAI_API_KEY)
python main.py docs/ --provider openai --api-key YOUR_OPENAI_KEY

# Использовать Anthropic (требует ANTHROPIC_API_KEY)
python main.py docs/ --provider anthropic --api-key YOUR_ANTHROPIC_KEY
```

### С сохранением результатов в файл:
```bash
python main.py docs/ --output results.txt
```

## Архитектура

Проект организован модульно для легкого расширения:

```
.
├── main.py                 # Точка входа, CLI интерфейс
├── config.py              # Конфигурация приложения
├── prompts.py             # Промпты для LLM (все на русском языке)
├── summarizer.py          # Основной класс для создания саммари
├── llm_providers/         # Модули LLM провайдеров
│   ├── __init__.py
│   ├── base.py            # Базовый класс для всех провайдеров
│   ├── factory.py         # Фабрика для создания провайдеров
│   └── openrouter.py      # Реализация OpenRouter провайдера
├── processors/            # Модули обработки файлов
│   ├── __init__.py
│   ├── base_processor.py  # Базовый класс для процессоров
│   ├── pdf_processor.py   # Обработка PDF
│   ├── image_processor.py # Обработка изображений
│   └── processor_factory.py # Фабрика процессоров
└── requirements.txt       # Зависимости
```

## Переключение между LLM провайдерами

Система поддерживает легкое переключение между различными LLM провайдерами.

### Настройка провайдера

1. **Через переменную окружения:**
   ```bash
   export LLM_PROVIDER=openrouter
   # или
   export LLM_PROVIDER=openai
   ```

2. **Через .env файл:**
   ```
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your_key_here
   ```

3. **Через аргумент командной строки:**
   ```bash
   python main.py docs/ --provider openrouter
   ```

### Добавление нового провайдера

Чтобы добавить поддержку нового LLM провайдера:

1. Создайте новый файл в `llm_providers/` (например, `my_provider.py`)
2. Наследуйтесь от `BaseLLMProvider`:
   ```python
   from .base import BaseLLMProvider
   
   class MyProvider(BaseLLMProvider):
       def generate_summary(self, text: str, context: Optional[str] = None) -> str:
           # Ваша реализация
           pass
       
       def generate_combined_summary(self, summaries: List[Dict[str, str]]) -> str:
           # Ваша реализация
           pass
       
       def analyze_image(self, image_path: Path) -> str:
           # Ваша реализация
           pass
   ```

3. Зарегистрируйте провайдер в `llm_providers/factory.py`:
   ```python
   from .my_provider import MyProvider
   
   _providers = {
       'openrouter': OpenRouterProvider,
       'my_provider': MyProvider,  # Добавьте здесь
   }
   ```

4. Добавьте настройки в `config.py` (API ключ, URL и т.д.)

## Расширение функциональности

### Добавление нового типа файлов

1. Создайте новый процессор, наследуясь от `BaseProcessor`:
```python
from processors.base_processor import BaseProcessor

class MyProcessor(BaseProcessor):
    def can_process(self, file_path):
        return file_path.suffix == '.myformat'
    
    def extract_text(self, file_path):
        # Ваша логика извлечения
        return "извлеченный текст"
```

2. Зарегистрируйте его в `ProcessorFactory` или через `summarizer.add_processor()`

### Изменение промптов

Все промпты для LLM находятся в файле `prompts.py`:
- `SUMMARY_PROMPT_TEMPLATE` - шаблон для индивидуальных саммари
- `COMBINED_SUMMARY_PROMPT_TEMPLATE` - шаблон для общего саммари
- `IMAGE_ANALYSIS_PROMPT` - промпт для анализа изображений

Для изменения промптов откройте `prompts.py` и отредактируйте соответствующие шаблоны. Все промпты на русском языке.

## Поддерживаемые форматы

- **PDF**: `.pdf`
- **Изображения**: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`

## Настройки

Основные настройки находятся в `config.py`:
- Модель по умолчанию
- Максимальный размер файла
- Поддерживаемые форматы
- Параметры LLM (temperature, max_tokens)

## Требования

- Python 3.8+
- OpenRouter API ключ (бесплатный)

## Устранение проблем

### Ошибка 404: "No endpoints found for model"

Если вы получаете ошибку `No endpoints found for [model_name]`:

1. **Измените модель в config.py:**
   Откройте `config.py` и измените:
   - `DEFAULT_MODEL` - для текстовых документов
   - `DEFAULT_VISION_MODEL` - для анализа изображений

2. **Проверьте актуальный список моделей:**
   - Откройте [OpenRouter Models](https://openrouter.ai/models)
   - Найдите бесплатные модели (они помечены как "Free")
   - Для vision-моделей ищите модели с поддержкой "vision" или "multimodal"
   - Используйте точное имя модели из списка

3. **Проверьте правильность API ключа:**
   - Ключ должен начинаться с `sk-or-v1-`
   - Убедитесь, что ключ скопирован полностью без пробелов

4. **Попробуйте другую модель через CLI:**
   ```bash
   python main.py docs/ --model "google/gemini-3-flash-preview"
   python main.py docs/ --vision-model "google/gemini-3-flash-preview"
   ```

### Ошибка 401 (Unauthorized)

- Проверьте правильность API ключа в `.env` файле
- Убедитесь, что ключ активен на сайте OpenRouter

### Ошибка 429 (Rate Limit)

- Вы превысили лимит запросов
- Подождите несколько минут и попробуйте снова
- Рассмотрите использование другой модели

## Обработка изображений

Программа теперь поддерживает **полноценный анализ изображений** через vision-модели OpenRouter:

- **Автоматический анализ содержимого** - программа описывает, что изображено на картинке
- **Распознавание текста** - если на изображении есть текст, он будет извлечен и включен в описание
- **Поддержка больших изображений** - автоматическое масштабирование для оптимизации