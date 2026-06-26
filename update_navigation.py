import re
from pathlib import Path

# Все категории и их бренды
SERVICES = {
    "naprawa-piekarnikow": {
        "name": "Naprawa Piekarnikow",
        "brands": ["samsung", "lg", "bosch", "whirlpool", "electrolux", "beko",
                   "aeg", "siemens", "candy", "indesit", "miele", "sharp",
                   "haier", "hisense", "hotpoint-ariston", "zanussi", "amica", "gorenje"]
    },
    "naprawa-suszarek": {
        "name": "Naprawa Suszarek",
        "brands": ["samsung", "lg", "bosch", "whirlpool", "electrolux", "beko",
                   "aeg", "siemens", "candy", "indesit", "miele", "sharp",
                   "haier", "hisense", "hotpoint-ariston", "zanussi", "amica", "gorenje"]
    },
    "naprawa-zmywarek": {
        "name": "Naprawa Zmywarek",
        "brands": ["samsung", "lg", "bosch", "whirlpool", "electrolux", "beko",
                   "aeg", "siemens", "candy", "indesit", "miele", "sharp",
                   "haier", "hisense", "hotpoint-ariston", "zanussi", "amica", "gorenje"]
    },
}

BRAND_DISPLAY = {
    "samsung": "Samsung", "lg": "LG", "bosch": "Bosch",
    "whirlpool": "Whirlpool", "electrolux": "Electrolux", "beko": "Beko",
    "aeg": "AEG", "siemens": "Siemens", "candy": "Candy",
    "indesit": "Indesit", "miele": "Miele", "sharp": "Sharp",
    "haier": "Haier", "hisense": "Hisense", "hotpoint-ariston": "Hotpoint-Ariston",
    "zanussi": "Zanussi", "amica": "Amica", "gorenje": "Gorenje"
}

CITIES = {
    "szczecin": "Szczecin", "stargard": "Stargard", "goleniow": "Goleniow",
    "nowogard": "Nowogard", "maszewo": "Maszewo", "police": "Police",
    "pyrzyce": "Pyrzyce", "gryfino": "Gryfino"
}

def generate_brands_section(service_slug, city_slug, city_name, service_name):
    """Генерирует секцию с брендами"""
    brands = SERVICES[service_slug]["brands"]
    
    brand_cards = ""
    for brand in brands:
        brand_name = BRAND_DISPLAY.get(brand, brand.capitalize())
        # Проверяем существует ли файл бренда
        brand_file = Path(service_slug) / city_slug / f"{brand}.html"
        if brand_file.exists():
            brand_cards += f'''
            <a href="{brand}.html" style="
                display:block;
                background:rgba(255,255,255,0.15);
                backdrop-filter:blur(10px);
                color:white;
                padding:20px;
                border-radius:12px;
                text-decoration:none;
                text-align:center;
                border:1px solid rgba(255,255,255,0.3);
                transition:all 0.3s ease;
                font-weight:bold;
            " onmouseover="this.style.background='rgba(255,255,255,0.25)'"
               onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                {brand_name}
            </a>'''
    
    return f'''
    <!-- СЕКЦИЯ БРЕНДОВ - ДОБАВЛЕНО СКРИПТОМ -->
    <section style="background:linear-gradient(135deg,#667eea,#764ba2);padding:3rem 0;">
        <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
            <h2 style="color:white;text-align:center;margin-bottom:2rem;font-size:2rem;">
                Wybierz marke - {service_name} {city_name}
            </h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;">
                {brand_cards}
            </div>
        </div>
    </section>
    <!-- KONIEC SEKCJI BRANDOW -->'''

def generate_navigation(service_slug, city_slug, city_name, service_name):
    """Генерирует навигационные ссылки"""
    
    # Ссылки на другие города
    other_cities = ""
    for slug, name in CITIES.items():
        if slug != city_slug:
            city_path = Path(service_slug) / slug
            if city_path.exists():
                other_cities += f'<a href="../{slug}/" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">{name}</a>'
    
    return f'''
    <!-- НАВИГАЦИЯ - ДОБАВЛЕНО СКРИПТОМ -->
    <div style="background:#2c3e50;padding:20px;text-align:center;">
        <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;text-align:left;">
            <div>
                <h4 style="color:#667eea;margin:0 0 10px 0;">Nawigacja</h4>
                <a href="../../" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">← Strona Glowna</a>
                <a href="../" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">← {service_name}</a>
            </div>
            <div>
                <h4 style="color:#667eea;margin:0 0 10px 0;">Inne miasta</h4>
                {other_cities}
            </div>
            <div>
                <h4 style="color:#667eea;margin:0 0 10px 0;">Inne uslugi</h4>
                <a href="../../naprawa-pralek/{city_slug}/" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">Naprawa Pralek</a>
                <a href="../../naprawa-zmywarek/{city_slug}/" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">Naprawa Zmywarek</a>
                <a href="../../naprawa-lodowek/{city_slug}/" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">Naprawa Lodowek</a>
                <a href="../../naprawa-piekarnikow/{city_slug}/" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">Naprawa Piekarnikow</a>
                <a href="../../naprawa-suszarek/{city_slug}/" style="color:#667eea;text-decoration:none;display:block;margin:5px 0;">Naprawa Suszarek</a>
            </div>
        </div>
    </div>
    <!-- KONIEC NAWIGACJI -->'''

def fix_index_files():
    fixed = 0
    skipped = 0
    
    for service_slug, service_info in SERVICES.items():
        service_folder = Path(service_slug)
        
        if not service_folder.exists():
            print(f"⚠️  Папка {service_slug} не найдена - пропускаю")
            continue
        
        print(f"\n📁 Обрабатываю: {service_slug}")
        
        for city_folder in service_folder.iterdir():
            if not city_folder.is_dir():
                continue
            
            city_slug = city_folder.name.lower()
            city_name = CITIES.get(city_slug, city_slug.capitalize())
            service_name = service_info["name"]

            index_file = city_folder / "index.html"
            
            if not index_file.exists():
                print(f"   ⚠️  {city_slug}/index.html не найден")
                continue
            
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content
            changed = False
           
            # Проверяем есть ли уже бренды
            if 'SEKCJI BRANDOW' not in content and 'brand_cards' not in content:
                brands_section = generate_brands_section(service_slug, city_slug, city_name, service_name)
                # Добавляем перед footer
                if '</footer>' in content:
                    content = content.replace('</footer>', brands_section + '\n</footer>', 1)
                elif '</body>' in content:
                    content = content.replace('</body>', brands_section + '\n</body>', 1)
                changed = True
                print(f"   ✅ {city_slug} - добавлены бренды")
            else:
                print(f"   ⏭️  {city_slug} - бренды уже есть")
            
            # Проверяем есть ли навигация
            if 'KONIEC NAWIGACJI' not in content:
                nav_section = generate_navigation(service_slug, city_slug, city_name, service_name)
                # Добавляем перед закрывающим тегом body
                if '</body>' in content:
                    content = content.replace('</body>', nav_section + '\n</body>', 1)
                changed = True
                print(f"   ✅ {city_slug} - добавлена навигация")
            else:
                print(f"   ⏭️  {city_slug} - навигация уже есть")
            
            if changed and content != original:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed += 1
            else:
                skipped += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Исправлено: {fixed} файлов")
    print(f"⏭️  Пропущено: {skipped} файлов")
    print(f"\n🎉 Готово! Загрузи на GitHub:")
    print(f"   - папку naprawa-piekarnikow/")
    print(f"   - папку naprawa-suszarek/")
    print(f"   - папку naprawa-zmywarek/")

if __name__ == "__main__":
    print("🔨 Добавляю бренды и навигацию...\n")
    fix_index_files()