import re
from pathlib import Path

SERVICES = {
    "naprawa-pralek": "Naprawa Pralek",
    "naprawa-zmywarek": "Naprawa Zmywarek",
    "naprawa-lodowek": "Naprawa Lodowek",
    "naprawa-piekarnikow": "Naprawa Piekarnikow",
    "naprawa-suszarek": "Naprawa Suszarek",
}

CITIES = {
    "szczecin": "Szczecin", "stargard": "Stargard",
    "goleniow": "Goleniow", "nowogard": "Nowogard",
    "maszewo": "Maszewo", "police": "Police",
    "pyrzyce": "Pyrzyce", "gryfino": "Gryfino"
}

BRANDS = {
    "samsung": "Samsung", "lg": "LG", "bosch": "Bosch",
    "whirlpool": "Whirlpool", "electrolux": "Electrolux", "beko": "Beko",
    "aeg": "AEG", "siemens": "Siemens", "candy": "Candy",
    "indesit": "Indesit", "miele": "Miele", "sharp": "Sharp",
    "haier": "Haier", "hisense": "Hisense", "hotpoint-ariston": "Hotpoint-Ariston",
    "zanussi": "Zanussi", "amica": "Amica", "gorenje": "Gorenje"
}



BREADCRUMB_CSS = """
<style>
.breadcrumb-nav {
    background: rgba(0,0,0,0.3);
    padding: 12px 20px;
    font-size: 0.9rem;
}
.breadcrumb-nav a {
    color: #a0b4f8;
    text-decoration: none;
}
.breadcrumb-nav a:hover {
    color: white;
    text-decoration: underline;
}
.breadcrumb-nav span {
    color: rgba(255,255,255,0.6);
    margin: 0 6px;
}
.breadcrumb-nav .current {
    color: white;
    font-weight: bold;
}
</style>
"""

def make_breadcrumb(items):
    """
    items = lista (nazwa, url) lub (nazwa, None) dla ostatniego
    """
    parts = []
    for i, (name, url) in enumerate(items):
        if url:
            parts.append(f'<a href="{url}">{name}</a>')
        else:
            parts.append(f'<span class="current">{name}</span>')
        if i < len(items) - 1:
            parts.append('<span>›</span>')
    
    html = f"""
<!-- BREADCRUMB -->
<nav class="breadcrumb-nav" aria-label="Breadcrumb">
    <div style="max-width:1200px;margin:0 auto;">
        {''.join(parts)}
    </div>
</nav>
<!-- KONIEC BREADCRUMB -->"""
    
    # Schema.org dla breadcrumb
    schema_items = []
    for i, (name, url) in enumerate(items, 1):
        if url:
            full_url = f"https://naprawaagd24.pl{url}" if url.startswith('/') else url
            schema_items.append(f'''{{
                "@type": "ListItem",
                "position": {i},
                "name": "{name}",
                "item": "{full_url}"
            }}''')
        else:
            schema_items.append(f'''{{
                "@type": "ListItem",
                "position": {i},
                "name": "{name}"
            }}''')
    
    schema = f"""
</script> type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {','.join(schema_items)}
    ]
}}
</script>"""
    
    return html, schema

def add_breadcrumb_to_file(filepath, breadcrumb_html, schema_html):
    """Добавляет хлебные крошки в HTML файл"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Если уже есть - пропускаем
    if 'BREADCRUMB' in content:
        return False
    
    # Добавляем CSS в head
    if BREADCRUMB_CSS not in content:
        content = content.replace('</head>', BREADCRUMB_CSS + '\n</head>', 1)
    
    # Добавляем Schema в head
    content = content.replace('</head>', schema_html + '\n</head>', 1)
    
    # Добавляем breadcrumb после header
    if '</header>' in content:
        content = content.replace('</header>', '</header>\n' + breadcrumb_html, 1)
    elif '<section class="hero">' in content:
        content = content.replace('<section class="hero">', breadcrumb_html + '\n<section class="hero">', 1)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all_breadcrumbs():
    fixed = 0
    skipped = 0
    
    for service_slug, service_name in SERVICES.items():
        service_folder = Path(service_slug)
        
        if not service_folder.exists():
            print(f"⚠️  {service_slug} - папка не найдена")
            continue
        
        print(f"\n📁 {service_slug}")
        
        for city_folder in service_folder.iterdir():
            if not city_folder.is_dir():
                continue
            
            city_slug = city_folder.name.lower()
            city_name = CITIES.get(city_slug, city_slug.capitalize())
            
            # 1. Страница города (index.html)
            # Крошки: Strona Glowna › Naprawa Pralek › Szczecin
            city_index = city_folder / "index.html"
            if city_index.exists():
                items = [
                    ("Strona Glowna", "/"),
                    (service_name, f"/{service_slug}/"),
                    (city_name, None)
                ]
                bc_html, schema = make_breadcrumb(items)
                result = add_breadcrumb_to_file(city_index, bc_html, schema)
                if result:
                    print(f"   ✅ {city_slug}/index.html")
                    fixed += 1
                else:
                    print(f"   ⏭️  {city_slug}/index.html - уже есть")
                    skipped += 1
            
            # 2. Страницы брендов
            # Крошки: Strona Glowna › Naprawa Pralek › Szczecin › Samsung
            for html_file in city_folder.glob("*.html"):
                if html_file.name == "index.html":
                    continue
                
                brand_slug = html_file.stem.lower()
                brand_name = BRANDS.get(brand_slug, brand_slug.capitalize())
                
                items = [
                    ("Strona Glowna", "/"),
                    (service_name, f"/{service_slug}/"),
                    (city_name, f"/{service_slug}/{city_slug}/"),
                    (brand_name, None)
                ]
                bc_html, schema = make_breadcrumb(items)
                result = add_breadcrumb_to_file(html_file, bc_html, schema)
                if result:
                    print(f"   ✅ {city_slug}/{html_file.name}")
                    fixed += 1
                else:
                    skipped += 1
        
        # 3. Главная страница раздела (service/index.html)
        service_index = service_folder / "index.html"
        if service_index.exists():
            items = [
                ("Strona Glowna", "/"),
                (service_name, None)
            ]
            bc_html, schema = make_breadcrumb(items)
            result = add_breadcrumb_to_file(service_index, bc_html, schema)
            if result:
                print(f"   ✅ {service_slug}/index.html")
                fixed += 1
            else:
                skipped += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Добавлено: {fixed} файлов")
    print(f"⏭️  Пропущено: {skipped} файлов")
    print(f"\n🎉 Готово! Загрузи все папки на GitHub.")

if __name__ == "__main__":
    print("🔨 Добавляю хлебные крошки на все страницы...\n")
    fix_all_breadcrumbs()