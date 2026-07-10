import re
from pathlib import Path
import os

def fix_html_structure(filepath):
    """Исправляет структуру HTML файла"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixed = False
    
    # ПРОБЛЕМА 1: Schema.org код виден на странице
    # Это происходит когда </script> отсутствует или неправильно закрыт
    # Ищем незакрытые теги script с ld+json
    
    # ПРОБЛЕМА 2: JS код виден внизу страницы
    # Это происходит когда <script> тег вставлен после </body>
    
    # Исправляем - убираем всё что после </html>
    if '</html>' in content:
        parts = content.split('</html>')
        if len(parts) > 1 and parts[1].strip():
            content = parts[0] + '</html>'
            fixed = True
    
    # Исправляем - убираем всё что после </body> но до </html>
    body_html_pattern = re.compile(r'</body>(.*?)</html>', re.DOTALL)
    match = body_html_pattern.search(content)
    if match and match.group(1).strip():
        # Есть лишний контент между </body> и </html>
        garbage = match.group(1).strip()
        # Если это не пробелы и не комментарии
        if garbage and not garbage.startswith('<!--'):
            content = content.replace(match.group(0), '</body>\n</html>')
            fixed = True
    
    # Исправляем - Script с JSON должен быть в <head>
    # Если он оказался в <body> - перемещаем
    ld_json_pattern = re.compile(
        r'(<script type="application/ld\+json">.*?</script>)', 
        re.DOTALL
    )
    
    # Находим все ld+json скрипты в body
    body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        ld_scripts_in_body = ld_json_pattern.findall(body_content)
        
        # Если есть ld+json в body - перемещаем в head
        for script in ld_scripts_in_body:
            if script in body_content:
                # Удаляем из body
                content = content.replace(script + '\n', '', 1)
                content = content.replace(script, '', 1)
                # Добавляем в head перед </head>
                if '</head>' in content and script not in content.split('<body>')[0]:
                    content = content.replace('</head>', script + '\n</head>', 1)
                fixed = True
    
    # Исправляем breadcrumb Schema который попал в видимую часть
    # Иногда скрипт вставляет Schema без тегов script
    json_ld_bare = re.compile(
        r'(?<!<script type="application/ld\+json">)\s*\{\s*"@context":\s*"https://schema\.org".*?\}\s*(?!</script>)',
        re.DOTALL
    )
    
    # Проверяем что body не содержит голый JSON (без тегов script)
    if '<body>' in content:
        body_part = content.split('<body>', 1)[1]
        if '"@context": "https://schema.org"' in body_part:
            # Проверяем обернут ли в script тег
            lines = body_part.split('\n')
            for i, line in enumerate(lines):
                if '"@context": "https://schema.org"' in line:
                    # Ищем контекст строки
                    context_start = max(0, i-3)
                    context = '\n'.join(lines[context_start:i+3])
                    if '<script' not in context:
                        # Голый JSON в body - это проблема
                        # Но исправлять сложно без полного парсинга
                        pass
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def check_and_fix_visible_code():
    """Проверяет все файлы на видимый код"""
    
    print("🔍 Проверяю все HTML файлы...\n")
    
    problems = []
    fixed_count = 0
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules']]
        
        for file in files:
            if not file.endswith('.html'):
                continue
            
            filepath = Path(root) / file
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_problem = False
            problem_types = []
            
            # Проблема 1: Контент после </html>
            if '</html>' in content:
                after_html = content.split('</html>')[-1].strip()
                if after_html:
                    problem_types.append("контент после </html>")
                    has_problem = True
            
            # Проблема 2: Нет закрывающего </body>
            if '<body>' in content and '</body>' not in content:
                problem_types.append("нет </body>")
                has_problem = True
            
            # Проблема 3: Нет закрывающего </html>
            if '<html' in content and '</html>' not in content:
                problem_types.append("нет </html>")
                has_problem = True
            
            # Проблема 4: JSON виден в body (без script тега)
            if '<body>' in content:
                body = content.split('<body>', 1)[1].split('</body>')[0] if '</body>' in content else content.split('<body>', 1)[1]
                # Ищем JSON объекты без обертки script
                if '{"@context"' in body or '{ "@context"' in body:
                    # Проверяем не обернуто ли в script
                    json_idx = body.find('"@context"')
                    before_json = body[max(0, json_idx-100):json_idx]
                    if '<script' not in before_json:
                        problem_types.append("JSON виден в body")
                        has_problem = True
            
            if has_problem:
                problems.append((str(filepath), problem_types))
                print(f"⚠️  {filepath}: {', '.join(problem_types)}")
                
                # Пробуем исправить
                if fix_html_structure(filepath):
                    print(f"   ✅ Исправлено!")
                    fixed_count += 1
                else:
                    print(f"   ❌ Требует ручного исправления")
    
    print(f"\n{'='*50}")
    print(f"🔍 Найдено проблем: {len(problems)}")
    print(f"✅ Исправлено автоматически: {fixed_count}")
    print(f"❌ Требует ручного исправления: {len(problems) - fixed_count}")
    
    if len(problems) - fixed_count > 0:
        print(f"\n📋 Файлы требующие ручного исправления:")
        for filepath, types in problems:
            print(f"   {filepath}: {', '.join(types)}")
    
    return problems

if __name__ == "__main__":
    print("🔨 Исправляю структуру HTML файлов...\n")
    problems = check_and_fix_visible_code()
    
    if not problems:
        print("✅ Все файлы в порядке!")
    else:
        print(f"\n💡 Совет: Загрузи исправленные файлы на GitHub")