import os
from datetime import date

# Твой домен
DOMAIN = "https://naprawaagd24.pl"

# Дата последнего обновления
TODAY = date.today().strftime("%Y-%m-%d")

def generate_sitemap(site_folder="."):
    """
    Сканирует все папки и создает sitemap.xml
    Запускай из корневой папки сайта!
    """
    
    urls = []
    
    # Главная страница - высший приоритет
    urls.append({
        "loc": f"{DOMAIN}/",
        "priority": "1.0",
        "changefreq": "weekly"
    })
    
    # Сканируем все HTML файлы в папках
    for root, dirs, files in os.walk(site_folder):
        # Пропускаем скрытые папки и служebные
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if not file.endswith('.html'):
                continue
            
            # Полный путь к файлу
            full_path = os.path.join(root, file)
            
            # Относительный путь от корня сайта
            rel_path = os.path.relpath(full_path, site_folder)
            
            # Конвертируем в URL формат (слеши)
            url_path = rel_path.replace("\\", "/")
            
            # Пропускаем корневой index.html (уже добавили выше)
            if url_path == "index.html":
                continue
            
            # Убираем index.html - заменяем на /
            if url_path.endswith("/index.html"):
                url_path = url_path[:-10]  # убираем index.html
            
            # Определяем приоритет по глубине вложенности
            depth = url_path.count("/")
            
            if depth == 0:
                # Страницы первого уровня (naprawa-pralek/index.html)
                priority = "0.9"
                changefreq = "weekly"
            elif depth == 1:
                # Страницы городов (naprawa-pralek/szczecin/)
                priority = "0.8"
                changefreq = "weekly"
            elif depth == 2:
                # Страницы брендов (naprawa-pralek/szczecin/samsung.html)
                priority = "0.7"
                changefreq = "monthly"
            else:
                priority = "0.6"
                changefreq = "monthly"
            
            urls.append({
                "loc": f"{DOMAIN}/{url_path}",
                "priority": priority,
                "changefreq": changefreq
            })
    
    # Генерируем XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    
    # Сортируем по URL для читаемости
    urls.sort(key=lambda x: x["loc"])
    
    # Главная всегда первая
    main_url = next((u for u in urls if u["loc"] == f"{DOMAIN}/"), None)
    other_urls = [u for u in urls if u["loc"] != f"{DOMAIN}/"]
    
    all_urls = ([main_url] if main_url else []) + other_urls
    
    for url in all_urls:
        xml += "  <url>\n"
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{TODAY}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += "  </url>\n\n"
    
    xml += "</urlset>"
    
    # Сохраняем файл
    output_path = os.path.join(site_folder, "sitemap.xml")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml)
    
    print(f"✅ sitemap.xml создан!")
    print(f"📊 Всего URL: {len(all_urls)}")
    print(f"📁 Файл: {os.path.abspath(output_path)}")
    print(f"\n📋 Первые 10 URL:")
    for url in all_urls[:10]:
        print(f"   {url['loc']}")
    print(f"   ... и ещё {len(all_urls) - 10} URL")

if __name__ == "__main__":
    # Запускай из корневой папки сайта!
    # Например: cd C:\Users\...\Naprawaagd24 && python generate_sitemap.py
    generate_sitemap(".")