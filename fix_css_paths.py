import os
import re
from pathlib import Path

def fix_css_and_html_paths():
    project_root = Path('.')
    fixed_count = 0

    print("🚀 Корректное исправление путей к CSS (без бэкапов)...\n")

    for root, dirs, files in os.walk(project_root):
        # ИСКЛЮЧАЕМ бэкапы, служебные и системные папки
        dirs[:] = [
            d for d in dirs 
            if not d.startswith('.') 
            and not d.startswith('_') 
            and d not in ['node_modules', 'git', 'venv']
        ]
        
        for file in files:
            if not file.endswith('.html'):
                continue
                
            filepath = Path(root) / file
            rel_path = filepath.relative_to(project_root)
            depth = len(rel_path.parts) - 1

            # Формируем точный относительный путь к CSS
            if depth == 0:
                correct_css_path = "./css/premium-theme.css"
            else:
                correct_css_path = "../" * depth + "css/premium-theme.css"

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            new_link_tag = f'<link rel="stylesheet" href="{correct_css_path}">'

            # Заменяем ссылки на стили CSS
            css_pattern = re.compile(r'<link\s+[^>]*href=["\'][^"\']*\.css["\'][^>]*>', re.IGNORECASE)

            if css_pattern.search(content):
                content = css_pattern.sub(new_link_tag, content)
            else:
                if '</head>' in content:
                    content = content.replace('</head>', f'    {new_link_tag}\n</head>')

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ {rel_path}  -->  {correct_css_path}")
                fixed_count += 1

    print(f"\n==================================================")
    print(f"🎉 Готово! Исправлено рабочих файлов: {fixed_count}")

if __name__ == "__main__":
    fix_css_and_html_paths()