import os

# Папка с проектом (текущая)
project_dir = "."
output_file = "mapa-stron.html"

html_files = []

# Ищем все .html файлы, кроме самой карты
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".html") and file != output_file:
            # Формируем относительный путь
            rel_path = os.path.relpath(os.path.join(root, file), project_dir)
            rel_path = rel_path.replace("\\", "/")
            html_files.append(rel_path)

# Сортируем для порядка
html_files.sort()

# Генерируем HTML-код
html_content = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa Stron - Naprawa AGD</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; }}
        li a {{ color: #0066cc; text-decoration: none; font-size: 14px; }}
        li a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Mapa Stron</h1>
    <ul>
"""

for path in html_files:
    # Красивое имя ссылки из пути
    clean_name = path.replace(".html", "").replace("/", " » ").replace("-", " ").title()
    html_content += f'        <li><a href="/{path}">{clean_name}</a></li>\n'

html_content += """    </ul>
</body>
</html>"""

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Успешно сгенерирован {output_file}! Найдено страниц: {len(html_files)}")