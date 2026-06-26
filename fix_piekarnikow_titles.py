import re
from pathlib import Path

BRAND_TITLES = {
    'samsung':          'blad SE FE tE, nie grzeje, programator',
    'lg':               'blad F1 F2, grzalka, termostat',
    'bosch':            'blad E0 E1 E2, nie grzeje, grzalka',
    'whirlpool':        'blad F01 F05, termostat, nie grzeje',
    'electrolux':       'blad E1 E2, grzalka, wentylator',
    'beko':             'blad E1 E2, nie nagrzewa, termostat',
    'aeg':              'blad E1 E2, grzalka, programator',
    'siemens':          'blad E1 E2, termostat, nie grzeje',
    'candy':            'blad E01 E02, grzalka, nie nagrzewa',
    'indesit':          'blad F01 F05, termostat, grzalka',
    'miele':            'blad F1 F2, programator, nie grzeje',
    'sharp':            'blad E1 E2, grzalka, termostat',
    'haier':            'blad E1 E2, nie grzeje, wentylator',
    'hisense':          'blad E1 E3, grzalka, nie nagrzewa',
    'hotpoint-ariston': 'blad F01 F05, grzalka, termostat',
    'zanussi':          'blad E10 E20, nie grzeje, grzalka',
    'amica':            'blad E1 E2, termostat, nie nagrzewa',
    'gorenje':          'blad E1 E2, grzalka, nie grzeje',
    'liebherr':         'blad F1 F2, termostat, programator',
}

CITY_NAMES = {
    'szczecin': 'Szczecin',
    'stargard': 'Stargard',
    'goleniow': 'Goleniow',
    'goleniów': 'Goleniow',
    'nowogard': 'Nowogard',
    'maszewo':  'Maszewo',
    'police':   'Police',
    'pyrzyce':  'Pyrzyce',
    'gryfino':  'Gryfino',
}

BRAND_NAMES = {
    'samsung': 'Samsung', 'lg': 'LG', 'bosch': 'Bosch',
    'whirlpool': 'Whirlpool', 'electrolux': 'Electrolux',
    'beko': 'Beko', 'aeg': 'AEG', 'siemens': 'Siemens',
    'candy': 'Candy', 'indesit': 'Indesit', 'miele': 'Miele',
    'sharp': 'Sharp', 'haier': 'Haier', 'hisense': 'Hisense',
    'hotpoint-ariston': 'Hotpoint-Ariston', 'zanussi': 'Zanussi',
    'amica': 'Amica', 'gorenje': 'Gorenje', 'liebherr': 'Liebherr',
}

def fix_titles():
    folder = Path("naprawa-piekarnikow")

    if not folder.exists():
        print("❌ Папка naprawa-piekarnikow не найдена!")
        print("   Запускай из корня сайта!")
        return

    fixed = 0
    skipped = 0

    for city_folder in folder.iterdir():
        if not city_folder.is_dir():
            continue

        city_slug = city_folder.name.lower()
        city_name = CITY_NAMES.get(city_slug, city_slug.capitalize())

        for html_file in city_folder.glob("*.html"):
            brand_slug = html_file.stem.lower()

            if brand_slug == 'index':
                continue

            brand_name = BRAND_NAMES.get(brand_slug, brand_slug.capitalize())
            brand_keywords = BRAND_TITLES.get(brand_slug, 'nie grzeje, grzalka, termostat')

            new_title = f"Naprawa Piekarnikow {brand_name} {city_name} | {brand_keywords} | 721 988 949"
            new_desc = f"Serwis piekarnikow {brand_name} w {city_name}. Naprawiamy: {brand_keywords}. Dojazd do klienta tego samego dnia. Tel: 721 988 949"

            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content

            content = re.sub(r'<title>[^<]*</title>', f'<title>{new_title}</title>', content)
            content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{new_desc}">', content)
            content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="Naprawa Piekarnikow {brand_name} {city_name} | 721 988 949">', content)
            content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{new_desc[:150]}">', content)

            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {city_folder.name}/{html_file.name}")
                print(f"   → {new_title[:70]}...")
                fixed += 1
            else:
                skipped += 1

    print(f"\n{'='*50}")
    print(f"✅ Исправлено: {fixed} файлов")
    print(f"⏭️  Пропущено: {skipped} файлов")
    print(f"\n🎉 Готово! Загрузи папку naprawa-piekarnikow на GitHub.")

if __name__ == "__main__":
    print("🔨 Исправляю title в naprawa-piekarnikow...\n")
    fix_titles()