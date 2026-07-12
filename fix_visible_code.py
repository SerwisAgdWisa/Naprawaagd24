import os
import re
from pathlib import Path

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # ПРОБЛЕМА: Карта вставилась МЕЖДУ </script> и </body>
    # Нужно переместить карту ПЕРЕД последним <script>
    
    # Ищем паттерн: </script> ... <!-- MAPA GOOGLE --> ... </body>
    # И меняем порядок: <!-- MAPA GOOGLE --> ... <script> ... </script> ... </body>
    
    map_pattern = re.compile(
        r'(</script>\s*\n?)(<!-- MAPA GOOGLE.*?<!-- KONIEC MAPY -->)',
        re.DOTALL
    )
    
    if map_pattern.search(content):
        def swap_map_and_script(match):
            script_close = match.group(1)
            map_section = match.group(2)
            return map_section + '\n' + script_close
        
        content = map_pattern.sub(swap_map_and_script, content)
    
    # PROBELM 2: Mapa wstawiła się po </body>
    after_body = re.compile(
        r'(</body>)\s*(<!-- MAPA GOOGLE.*?<!-- KONIEC MAPY -->)',
        re.DOTALL
    )
    
    if after_body.search(content):
        def move_map_before_body(match):
            map_section = match.group(2)
            return map_section + '\n</body>'
        
        content = after_body.sub(move_map_before_body, content)
    
    # PROBLEM 3: Nawigacja wstawiła się po </body>
    after_body_nav = re.compile(
        r'(</body>)\s*(<!-- NAWIGACJA.*?<!-- KONIEC NAWIGACJI -->)',
        re.DOTALL
    )
    
    if after_body_nav.search(content):
        def move_nav_before_body(match):
            nav_section = match.group(2)
            return nav_section + '\n</body>'
        
        content = after_body_nav.sub(move_nav_before_body, content)
    
    # PROBLEM 4: Breadcrumb schema wstawiła się po </body>
    after_body_bc = re.compile(
        r'(</body>)\s*(<script type="application/ld\+json">.*?</script>)',
        re.DOTALL
    )
    
    if after_body_bc.search(content):
        def move_schema_to_head(match):
            schema = match.group(2)
            return '</body>'
        
        # Pobieramy schemę i przenosimy do head
        bc_match = after_body_bc.search(content)
        if bc_match:
            schema_to_move = bc_match.group(2)
            content = after_body_bc.sub(r'</body>', content)
            if '</head>' in content:
                content = content.replace('</head>', schema_to_move + '\n</head>', 1)
    
    # PROBLEM 5: Widoczny JS po </script> ale przed </body>
    # Szukamy tekstu który wygląda jak JS ale nie jest w tagu script
    visible_js = re.compile(
        r'(?<=</script>)\s*\n\s*(function\s+\w+|document\.|window\.|const\s+|let\s+|var\s+)',
        re.MULTILINE
    )
    
    if visible_js.search(content):
        # Znajdujemy gdzie zaczyna się widoczny JS
        match = visible_js.search(content)
        if match:
            start_pos = match.start()
            # Szukamy końca - zwykle to </body> lub </html>
            end_patterns = ['</body>', '</html>', '\n\n\n']
            end_pos = len(content)
            for pat in end_patterns:
                idx = content.find(pat, match.end())
                if idx != -1 and idx < end_pos:
                    end_pos = idx
            
            # Pobieramy widoczny JS
            visible_code = content[start_pos:end_pos].strip()
            
            # Owijamy w script tag i wstawiamy przed </body>
            if visible_code and not visible_code.startswith('<'):
                wrapped = f'\n<script>\n{visible_code}\n</script>'
                # Usuwamy widoczny kod
                content = content[:start_pos] + content[end_pos:]
                # Wstawiamy przed </body>
                content = content.replace('</body>', wrapped + '\n</body>', 1)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all():
    print("🔨 Исправляю все HTML файлы...\n")
    fixed = 0
    ok = 0
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.html'):
                continue
            
            filepath = Path(root) / file
            
            # Быстрая проверка есть ли проблема
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Признаки проблемы
            has_problem = (
                'function sendToWhatsApp' in content and 
                '</script>' in content and
                content.rfind('function sendToWhatsApp') > content.rfind('<script')
            ) or (
                '<!-- MAPA GOOGLE' in content and
                content.find('<!-- MAPA GOOGLE') > content.find('</body>')
            ) or (
                content.count('</body>') > 1
            )
            
            if has_problem:
                result = fix_file(filepath)
                if result:
                    print(f"✅ Исправлено: {filepath}")
                    fixed += 1
                else:
                    print(f"⚠️  Не удалось: {filepath}")
            else:
                ok += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Исправлено: {fixed} файлов")
    print(f"👍 Без изменений: {ok} файлов")
    print(f"\n🎉 Готово! Загрузи все файлы на GitHub.")

if __name__ == "__main__":
    fix_all()