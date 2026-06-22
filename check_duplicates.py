import os
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup

# Папка с сайтом (запускай из корневой папки)
SITE_FOLDER = "."

def get_page_text(html_path):
    """Извлекает текст из HTML файла"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            # Убираем скрипты и стили
            for tag in soup(['script', 'style', 'meta', 'link']):
                tag.decompose()
            return soup.get_text(separator=' ', strip=True)
    except:
        return ""

def get_hash(text):
    """Создает хэш текста для сравнения"""
    # Нормализуем текст (убираем пробелы, приводим к нижнему регистру)
    normalized = ' '.join(text.lower().split())
    return hashlib.md5(normalized.encode()).hexdigest()

def check_duplicates():
    """Сканирует все HTML файлы и находит дубликаты"""
    
    print("🔍 Сканирую все HTML файлы...")
    
    pages = {}  # {путь: {hash, текст, длина}}
    hashes = {}  # {hash: [список файлов с таким же хешем]}
    
    # Сканируем все HTML файлы
    for root, dirs, files in os.walk(SITE_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.html'):
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, SITE_FOLDER)
            
            text = get_page_text(full_path)
            if not text:
                continue
            
            page_hash = get_hash(text)
            text_length = len(text)
            
            pages[rel_path] = {
                'hash': page_hash,
                'length': text_length,
                'text_preview': text[:200]
            }
            
            if page_hash not in hashes:
                hashes[page_hash] = []
            hashes[page_hash].append(rel_path)
    
    # Находим дубликаты
    duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
    unique_pages = {h: files for h, files in hashes.items() if len(files) == 1}
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Всего страниц: {len(pages)}")
    print(f"   Уникальных: {len(unique_pages)}")
    print(f"   Групп дубликатов: {len(duplicates)}")
    print(f"   Страниц с дублированным контентом: {sum(len(f) for f in duplicates.values())}")
    
    if duplicates:
        print(f"\n⚠️  НАЙДЕНЫ ДУБЛИКАТЫ:")
        for i, (hash_val, files) in enumerate(duplicates.items(), 1):
            print(f"\n   Группа {i} ({len(files)} одинаковых страниц):")
            for f in files[:5]:  # Показываем первые 5
                length = pages[f]['length']
                print(f"      📄 {f} ({length} символов)")
            if len(files) > 5:
                print(f"      ... и ещё {len(files) - 5} файлов")
            # Показываем превью текста
            preview = pages[files[0]]['text_preview'][:100]
            print(f"      📝 Текст: {preview}...")
    
    # Сохраняем отчет
    report_path = "duplicate_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ О ДУБЛИРОВАННОМ КОНТЕНТЕ\n")
        f.write("="*50 + "\n\n")
        f.write(f"Всего страниц: {len(pages)}\n")
        f.write(f"Уникальных: {len(unique_pages)}\n")
        f.write(f"Групп дубликатов: {len(duplicates)}\n\n")
        
        for i, (hash_val, files) in enumerate(duplicates.items(), 1):
            f.write(f"ГРУППА {i} ({len(files)} одинаковых страниц):\n")
            for file in files:
                f.write(f"  - {file}\n")
            f.write(f"  Превью: {pages[files[0]]['text_preview'][:150]}...\n\n")
    
    print(f"\n📋 Полный отчет сохранен: {report_path}")
    
    return duplicates, pages

if __name__ == "__main__":
    # Проверяем что установлена библиотека beautifulsoup4
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Нужно установить библиотеку:")
        print("   pip install beautifulsoup4")
        exit()
    
    duplicates, pages = check_duplicates()
    
    if not duplicates:
        print("\n✅ Дубликатов не найдено! Весь контент уникальный.")
    else:
        print(f"\n⚠️  Найдено {len(duplicates)} групп дубликатов.")
        print("📋 Смотри файл duplicate_report.txt для деталей")