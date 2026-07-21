import os
import re
from pathlib import Path

# Уникальные title для каждого бренда холодильников (с исправленным gorenje)
BRAND_TITLES = {
    'samsung':          'nie chłodzii, błąd 1E 5E 22E, No Frost',
    'lg':               'kompresor liniowy, błąd Er dH, No Frost',
    'bosch':            'nie chłodzi, VitaFresh, błąd E1 E2 E3',
    'whirlpool':        'błąd AL E1, 6th Sense, No Frost',
    'electrolux':       'błąd E10 E20, TwinTech, No Frost',
    'beko':             'błąd E1 E2, NeoFrost, nie chłodzi',
    'aeg':              'błąd E1 E4, CustomFlex, nie chłodzi',
    'siemens':          'błąd E1 E2, HyperFresh, No Frost',
    'liebherr':         'błąd F1 F2, BioFresh, kompresor',
    'gorenje':          'błąd E1 E2, AdaptTech, MultiFlow',
    'candy':            'błąd E1 E2, nie chłodzi, alarm temp',
    'indesit':          'błąd F01 F02, nie chłodzi, No Frost',
    'miele':            'błąd F1 F2, PerfectFresh, kompresor',
    'sharp':            'błąd E1 E2, nie chłodzi, hałas',
    'haier':            'błąd E1 E2, MyZone, nie chłodzi',
    'hisense':          'błąd E1 E3, nie chłodzi, No Frost',
    'hotpoint-ariston': 'błąd F01 F02, nie chłodzi, No Frost',
    'zanussi':          'błąd E10 E20, nie chłodzi, No Frost',
    'amica':            'błąd E1 E2, nie chłodzi, No Frost',
}

# Правильные названия городов
CITY_NAMES = {
    'szczecin': 'Szczecin',
    'stargard': 'Stargard',
    'goleniow': 'Goleniów',
    'goleniów': 'Goleniów',
    'nowogard': 'Nowogard',
    'maszewo':  'Maszewo',
    'police':   'Police',
    'pyrzyce':  'Pyrzyce',
    'gryfino':  'Gryfino',
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
            brand_keywords = BRAND_TITLES.get(brand_slug, 'nie chłodzi, No Frost, kompresor')
            
            # Новый уникальный title с правильной символикой (Lodówek)
            new_title = f"Naprawa Lodówek {brand_name} {city_name} | {brand_keywords} | 721 988 949"
            
            # Новый description
            new_desc = f"Serwis lodówek {brand_name} w {city_name}. Naprawiamy: {brand_keywords}. Dojazd do klienta tego samego dnia. Tel: 721 988 949"
            
            # Читаем файл
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Заменяем title
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
                f'<meta property="og:title" content="Naprawa Lodówek {brand_name} {city_name} | 721 988 949">',
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