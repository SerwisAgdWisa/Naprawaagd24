import os
from pathlib import Path

# Уникальные title для каждого бренда холодильников
BRAND_TITLES = {
    'samsung': 'nie chlodzi, blad 1E 5E 22E, No Frost',
    'lg': 'kompresor liniowy, blad Er dH, No Frost',
    'bosch': 'nie chlodzi, VitaFresh, blad E1 E2 E3',
    'whirlpool': 'blad AL E1, 6th Sense, No Frost',
    'electrolux': 'blad E10 E20, TwinTech, No Frost',
    'beko': 'blad E1 E2, NeoFrost, nie chlodzi',
    'aeg': 'blad E1 E4, CustomFlex, nie chlodzi',
    'siemens': 'blad E1 E2, HyperFresh, No Frost',
    'liebherr': 'blad F1 F2, BioFresh, kompresor',
    'gorenje': 'blad E1 E2, MultiFlow, nie chlodzi',
    'candy': 'blad E1 E2, nie chlodzi, alarm temp',
    'indesit': 'blad F01 F02, nie chlodzi, No Frost',
    'miele': 'blad F1 F2, PerfectFresh, kompresor',
    'sharp': 'blad E1 E2, nie chlodzi, halas',
    'haier': 'blad E1 E2, MyZone, nie chlodzi',
    'hisense': 'blad E1 E3, nie chlodzi, No Frost',
    'hotpoint-ariston': 'blad F01 F02, nie chlodzi, No Frost',
    'gorenje': 'blad E1 E2, AdaptTech, nie chlodzi',
    'zanussi': 'blad E10 E20, nie chlodzi, No Frost',
    'amica': 'blad E1 E2, nie chlodzi, No Frost',
}

# Правильные названия городов
CITY_NAMES = {
    'szczecin': 'Szczecin',
    'stargard': 'Stargard',
    'goleniow': 'Goleniow',
    'goleniów': 'Goleniow',
    'nowogard': 'Nowogard',
    'maszewo': 'Maszewo',
    'police': 'Police',
    'pyrzyce': 'Pyrzyce',
    'gryfino': 'Gryfino',
}

# Правильные названия брендов
BRAND_NAMES = {
    'samsung': 'Samsung',
    'lg': 'LG',
    'bosch': 'Bosch',
    'whirlpool': 'Whirlpool',
    'electrolux': 'Electrolux',
    'beko': 'Beko',
    'aeg': 'AEG',
    'siemens': 'Siemens',
    'liebherr': 'Liebherr',
    'gorenje': 'Gorenje',
    'candy': 'Candy',
    'indesit': 'Indesit',
    'miele': 'Miele',
    'sharp': 'Sharp',
    'haier': 'Haier',
    'hisense': 'Hisense',
    'hotpoint-ariston': 'Hotpoint-Ariston',
    'zanussi': 'Zanussi',
    'amica': 'Amica',
}

def fix_titles():
    folder = Path("naprawa-lodowek")
    
    if not folder.exists():
        print("❌ Папка naprawa-lodowek не найдена!")
        print("   Запускай из корня сайта!")
        return
    
    fixed = 0
    skipped = 0
    
    # Проходим по всем городам
    for city_folder in folder.iterdir():
        if not city_folder.is_dir():
            continue
        
        city_slug = city_folder.name.lower()
        city_name = CITY_NAMES.get(city_slug, city_slug.capitalize())
        
        # Проходим по всем HTML файлам бренда
        for html_file in city_folder.glob("*.html"):
            brand_slug = html_file.stem.lower()
            
            # Пропускаем index.html
            if brand_slug == 'index':
                continue
            
            brand_name = BRAND_NAMES.get(brand_slug, brand_slug.capitalize())
            brand_keywords = BRAND_TITLES.get(brand_slug, 'nie chlodzi, No Frost, kompresor')
            
            # Новый уникальный title
            new_title = f"Naprawa Lodowek {brand_name} {city_name} | {brand_keywords} | 721 988 949"
            
            # Новый description
            new_desc = f"Serwis lodowek {brand_name} w {city_name}. Naprawiamy: {brand_keywords}. Dojazd do klienta tego samego dnia. Tel: 721 988 949"
            
            # Читаем файл
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Заменяем title
            import re
            content = re.sub(
                r'<title>[^<]*</title>',
                f'<title>{new_title}</title>',
                content
            )
            
            # Заменяем description
            content = re.sub(
                r'<meta name="description" content="[^"]*">',
                f'<meta name="description" content="{new_desc}">',
                content
            )
            
            # Заменяем og:title
            content = re.sub(
                r'<meta property="og:title" content="[^"]*">',
                f'<meta property="og:title" content="Naprawa Lodowek {brand_name} {city_name} | 721 988 949">',
                content
            )
            
            # Заменяем og:description
            content = re.sub(
                r'<meta property="og:description" content="[^"]*">',
                f'<meta property="og:description" content="{new_desc[:150]}">',
                content
            )
            
            # Сохраняем если были изменения
            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {city_folder.name}/{html_file.name}")
                print(f"   Title: {new_title[:70]}...")
                fixed += 1
            else:
                skipped += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Исправлено: {fixed} файлов")
    print(f"⏭️  Пропущено: {skipped} файлов")
    print(f"\n🎉 Готово! Загрузи папку naprawa-lodowek на GitHub.")

if __name__ == "__main__":
    print("🔨 Исправляю title в naprawa-lodowek...\n")
    fix_titles()