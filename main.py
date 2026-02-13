import argparse
from pathlib import Path
from summarizer import DocumentSummarizer
from llm_providers.factory import LLMProviderFactory
from config import LLM_PROVIDER, OPENROUTER_API_KEY


def print_results(results: dict):
    print("\n" + "="*80)
    print("РЕЗУЛЬТАТЫ ОБРАБОТКИ ДОКУМЕНТОВ")
    print("="*80)
    
    print(f"\nВсего файлов найдено: {results['total_files']}")
    print(f"Успешно обработано: {results['processed_files']}")
    
    print("\n" + "-"*80)
    print("ОБЩЕЕ САММАРИ:")
    print("-"*80)
    print(f"\n{results['combined_summary']}")
    print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(
        description='Создает общее саммари по содержимому папки с документами',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py docs/
  python main.py docs/ --model "meta-llama/llama-3.2-3b-instruct:free"
        """
    )
    
    parser.add_argument(
        'folder',
        type=str,
        help='Путь к папке с документами'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Модель для использования (если не указана, используется модель по умолчанию)'
    )
    
    parser.add_argument(
        '--vision-model',
        type=str,
        default=None,
        help='Vision-модель для анализа изображений (если не указана, используется модель по умолчанию)'
    )
    
    parser.add_argument(
        '--provider',
        type=str,
        default=None,
        help=f'LLM провайдер (openrouter, openai, anthropic и т.д.). По умолчанию: {LLM_PROVIDER}'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='API ключ (если не указан, берется из переменных окружения)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Путь к файлу для сохранения результатов (опционально)'
    )
    
    args = parser.parse_args()
    
    provider = args.provider or LLM_PROVIDER
    
    if args.api_key:
        api_key = args.api_key
    elif provider == 'openrouter':
        api_key = OPENROUTER_API_KEY
    
    if not api_key:
        print(f"ОШИБКА: API ключ для провайдера '{provider}' не найден!")
        print(f"Установите соответствующий API ключ в переменных окружения или используйте --api-key")
        return 1
    
    folder_path = Path(args.folder)
    if not folder_path.exists():
        print(f"ОШИБКА: Папка не существует: {folder_path}")
        return 1
    
    try:
        print(f"Инициализация саммаризатора (провайдер: {provider})...")
        summarizer = DocumentSummarizer(
            provider=provider,
            api_key=api_key,
            model=args.model,
            vision_model=args.vision_model
        )
        
        print(f"Обработка папки: {folder_path.absolute()}")
        results = summarizer.process_folder(folder_path)
        
        print_results(results)
        
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("РЕЗУЛЬТАТЫ ОБРАБОТКИ ДОКУМЕНТОВ\n")
                f.write("="*80 + "\n\n")
                f.write(f"Всего файлов найдено: {results['total_files']}\n")
                f.write(f"Успешно обработано: {results['processed_files']}\n\n")
                
                f.write("ОБЩЕЕ САММАРИ:\n")
                f.write("-"*80 + "\n")
                f.write(f"\n{results['combined_summary']}\n")
            
            print(f"\nРезультаты сохранены в файл: {output_path.absolute()}")
        
        return 0
        
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
