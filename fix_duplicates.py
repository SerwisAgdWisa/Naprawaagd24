import os
import re
from pathlib import Path

# Пары дубликатов из отчета - что нужно исправить
# Формат: (файл с ошибкой, правильный город, неправильный город)
DUPLICATES_TO_FIX = [
    # Группы 1-19: Goleniów скопировался в Nowogard
    ("naprawa-pralek/nowogard/aeg.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/amica.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/beko.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/bosch.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/candy.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/electrolux.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/gorenje.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/haier.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/hisense.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/hotpoint-ariston.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/indesit.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/lg.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/miele.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/samsung.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/sharp.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/siemens.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/whirlpool.html", "Nowogard", "Goleniów"),
    ("naprawa-pralek/nowogard/zanussi.html", "Nowogard", "Goleniów"),
    
    # Группа 12: Goleniów index скопировался в Maszewo
    ("naprawa-pralek/goleniów/index.html", "Goleniów", "Maszewo"),
    
    # Группа 20: Miele скопировался в Samsung (Nowogard suszarki)
    ("naprawa-suszarek/nowogard/samsung.html", "Samsung", "Miele"),
    
    # Группа 21: Stargard скопировался в Szczecin (suszarki whirlpool)
    ("naprawa-suszarek/stargard/whirlpool.html", "Stargard", "Szczecin"),
    
    # Группа 22: Miele скопировался в Hisense (zmywarki maszewo)
    ("naprawa-zmywarek/maszewo/hisense.html", "Hisense", "Miele"),
]

# Уникальные описания для городов
CITY_DESCRIPTIONS = {
    "Nowogard": {
        "desc": "Specjalizujemy sie w naprawie pralek w Nowogardzie i okolicznych miejscowosciach.",
        "districts": "Centrum, Karsk, Warnkowo, Osiedle Mlodych, Dabrowa Nowogardzka",
        "unique": "Serwisujemy pralki w Nowogardzie i pobliskich miejscowosciach takich jak Karsk i Warnkowo."
    },
    "Goleniow": {
        "desc": "Profesjonalny serwis pralek w Goleniowie i okolicach lotniska.",
        "districts": "Centrum, Osiedle Helenow, Krzewno, Kliniska Wielkie, Mosty",
        "unique": "Dzialamy na terenie Goleniowa w okolicach lotniska Szczecin-Goleniow."
    },
    "Maszewo": {
        "desc": "Naprawa pralek w Maszewie i okolicznych wsiach gminy Maszewo.",
        "districts": "Centrum, Badelnik, Maciejewo, Debice, Stare Maszewo",
        "unique": "Pomagamy mieszkancom Maszewa i okolicznych wsi. Znamy problemy pralek w malych miejscowosciach."
    },
    "Stargard": {
        "desc": "Specjalizujemy sie w naprawie pralek w Stargardzie.",
        "districts": "Centrum, Kluczewo, Osiedle Zachod, Osiedle Pyrzyckie, Stare Miasto",
        "unique": "Znamy specyfike starych kamienic w Srodmiesciu i nowych osiedli na Zachodzie Stargardu."
    },
    "Szczecin": {
        "desc": "Serwisujemy pralki we wszystkich dzielnicach Szczecina.",
        "districts": "Pogodno, Niebuszewo, Centrum, Prawobrzeze, Dabie, Gumience",
        "unique": "Obslugujemy Szczecin od Pogodna po Prawobrzeze. Twarda woda szczecinska czesto uszkadza grzalki."
    }
}

# Уникальные описания для брендов (suszarki)
BRAND_SUSZAREK = {
    "Samsung": {
        "problems": [
            "Suszarka Samsung nie grzeje - uszkodzona grzalka",
            "Beben nie obraca sie - pasek napedowy",
            "Blad tE - czujnik temperatury",
            "Blad dE - problem z drzwiami",
            "Halas podczas suszenia - lozyska"
        ]
    },
    "Miele": {
        "problems": [
            "Suszarka Miele nie grzeje - grzalka lub termostat",
            "Program nie konczy sie - czujnik wilgotnosci",
            "Blad F01 - problem z elektronika",
            "Kondensator nie dziala - pompa",
            "Bardzo glosna praca - lozyska bebna"
        ]
    },
    "Whirlpool": {
        "problems": [
            "Suszarka Whirlpool nie nagrzewa - element grzejny",
            "Beben zatrzymuje sie - silnik lub pasek",
            "Blad F06 - awaria silnika",
            "Nie suszy dobrze - zatkany filtr",
            "Wycieka woda - uszkodzony skraplacz"
        ]
    }
}

BRAND_ZMYWAREK = {
    "Hisense": {
        "problems": [
            "Zmywarka Hisense nie myje - zatkane ramiona",
            "Nie odprowadza wody - pompa odplywowa",
            "Blad E3 - problem z grzaniem",
            "Nie pobiera wody - zawor elektromagnetyczny",
            "Halas podczas pracy - pompa obiegowa"
        ]
    },
    "Miele": {
        "problems": [
            "Zmywarka Miele nie myje dokladnie - zatkany filtr",
            "Blad F11 - problem z odpompowaniem",
            "Nie nagrzewa wody - grzalka lub termostat",
            "Wycieka woda - uszkodzona uszczelka",
            "Program nie konczy sie - czujnik"
        ]
    }
}

def fix_city_in_file(filepath, correct_city, wrong_city):
    """Заменяет неправильное название города на правильное в файле"""
    
    path = Path(filepath)
    if not path.exists():
        # Пробуем с другим слешем
        filepath_alt = filepath.replace("/", "\\")
        path = Path(filepath_alt)
        if not path.exists():
            print(f"   ⚠️  Файл не найден: {filepath}")
            return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Заменяем все вхождения неправильного города на правильный
    replacements = [
        (wrong_city, correct_city),
        (wrong_city.lower(), correct_city.lower()),
        (wrong_city.upper(), correct_city.upper()),
    ]
    
    for wrong, correct in replacements:
        content = content.replace(wrong, correct)
    
    # Обновляем canonical URL
    wrong_slug = wrong_city.lower().replace("ó", "o").replace("ę", "e")
    correct_slug = correct_city.lower().replace("ó", "o").replace("ę", "e")
    content = content.replace(f"/{wrong_slug}/", f"/{correct_slug}/")
    
    # Добавляем уникальное описание для города если есть
    if correct_city in CITY_DESCRIPTIONS:
        city_info = CITY_DESCRIPTIONS[correct_city]
        # Заменяем описание в meta
        content = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{city_info["desc"]} Tel: 721 988 949">',
            content
        )
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def fix_brand_in_file(filepath, correct_brand, wrong_brand):
    """Заменяет неправильное название бренда на правильное"""
    
    path = Path(filepath)
    if not path.exists():
        print(f"   ⚠️  Файл не найден: {filepath}")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    content = content.replace(wrong_brand, correct_brand)
    content = content.replace(wrong_brand.lower(), correct_brand.lower())
    content = content.replace(wrong_brand.upper(), correct_brand.upper())
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def fix_all_duplicates():
    """Исправляет все дубликаты из отчета"""
    
    print("🔨 ИСПРАВЛЯЮ ДУБЛИКАТЫ...\n")
    
    fixed = 0
    failed = 0
    
    # Группы 1-19: Nowogard имеет контент Goleniów
    print("📁 Исправляю naprawa-pralek/nowogard/ (заменяю Goleniów на Nowogard):")
    city_files = [d for d in DUPLICATES_TO_FIX if "nowogard" in d[0] and "pralek" in d[0]]
    
    for filepath, correct, wrong in city_files:
        result = fix_city_in_file(filepath, correct, wrong)
        if result:
            print(f"   ✅ {Path(filepath).name}")
            fixed += 1
        else:
            print(f"   ❌ {Path(filepath).name}")
            failed += 1
    
    # Группа 12: Goleniów index = Maszewo index
    print("\n📁 Исправляю naprawa-pralek/goleniów/index.html:")
    result = fix_city_in_file(
        "naprawa-pralek/goleniów/index.html", 
        "Goleniów", 
        "Maszewo"
    )
    if result:
        print("   ✅ index.html исправлен")
        fixed += 1
    else:
        print("   ❌ Не удалось исправить")
        failed += 1
    
    # Группа 20: suszarki nowogard - samsung = miele
    print("\n📁 Исправляю naprawa-suszarek/nowogard/samsung.html:")
    result = fix_brand_in_file(
        "naprawa-suszarek/nowogard/samsung.html",
        "Samsung",
        "Miele"
    )
    if result:
        print("   ✅ samsung.html исправлен")
        fixed += 1
    else:
        print("   ❌ Не удалось исправить")
        failed += 1
    
    # Группа 21: suszarki stargard whirlpool = szczecin whirlpool
    print("\n📁 Исправляю naprawa-suszarek/stargard/whirlpool.html:")
    result = fix_city_in_file(
        "naprawa-suszarek/stargard/whirlpool.html",
        "Stargard",
        "Szczecin"
    )
    if result:
        print("   ✅ whirlpool.html исправлен")
        fixed += 1
    else:
        print("   ❌ Не удалось исправить")
        failed += 1
    
    # Группа 22: zmywarki maszewo hisense = miele
    print("\n📁 Исправляю naprawa-zmywarek/maszewo/hisense.html:")
    result = fix_brand_in_file(
        "naprawa-zmywarek/maszewo/hisense.html",
        "Hisense",
        "Miele"
    )
    if result:
        print("   ✅ hisense.html исправлен")
        fixed += 1
    else:
        print("   ❌ Не удалось исправить")
        failed += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Исправлено: {fixed} файлов")
    print(f"❌ Не удалось: {failed} файлов")
    print(f"\n🎉 ГОТОВО! Загрузи исправленные файлы на GitHub.")

if __name__ == "__main__":
    fix_all_duplicates()