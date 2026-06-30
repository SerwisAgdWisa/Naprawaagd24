import os
from pathlib import Path

# Что меняем
REPLACEMENTS = [
    ("Serwis AGD WISA", "Naprawaagd24"),
    ("WISA Serwis AGD", "Naprawaagd24"),
    (">WISA<", ">Naprawaagd24<"),  # логотип в header
    ("Oleksandr Chumnyi WISA", "Oleksandr Chumnyi - Naprawaagd24"),
]

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    
    original = content
    
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all_files():
    fixed = 0
    skipped = 0
    
    # Сканируем все HTML файлы
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if not file.endswith('.html'):
                continue
            
            filepath = Path(root) / file
            
            if fix_file(filepath):
                print(f"✅ {filepath}")
                fixed += 1
            else:
                skipped += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Исправлено: {fixed} файлов")
    print(f"⏭️  Без изменений: {skipped} файлов")
    print(f"\n🎉 Готово! Все 'WISA' заменены на 'Naprawaagd24'")
    print(f"Загрузи все измененные файлы на GitHub.")

if __name__ == "__main__":
    print("🔨 Заменяю WISA на Naprawaagd24 во всех файлах...\n")
    fix_all_files()