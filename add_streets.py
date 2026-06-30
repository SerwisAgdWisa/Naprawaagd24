import re
from pathlib import Path

# Реальные улицы для каждого города
CITY_STREETS = {
    "szczecin": {
        "name": "Szczecin",
        "streets": [
            "al. Bohaterow Warszawy", "ul. Niepodleglosci", "ul. Monte Cassino",
            "ul. Wojska Polskiego", "ul. Jagiellonska", "ul. Piastow",
            "ul. Rayskiego", "ul. Wyzwolenia", "ul. Slowackiego",
            "ul. Mickiewicza", "ul. Krasickiego", "ul. Broniewskiego",
            "ul. Energetykow", "ul. Ku Sloncu", "ul. Struga",
            "ul. Bandurskiego", "al. Papiezа Jana Pawla II", "ul. Kolumba",
            "ul. Spichrzowa", "ul. Roosevelta", "ul. Mazurska",
            "ul. Kopernika", "ul. Lomzynska", "ul. Strzalowska",
            "ul. Polnocna", "ul. Lesna", "ul. Dabrowskiego",
            "ul. Spacerowa", "ul. Sosnowa", "ul. Lipowa"
        ]
    },
    "stargard": {
        "name": "Stargard",
        "streets": [
            "ul. Jagiellonska", "ul. Mickiewicza", "ul. Wojska Polskiego",
            "ul. Slowackiego", "ul. Pierwszej Brygady", "ul. Sklodowskiej",
            "ul. Pilsudskiego", "ul. Bohaterow Warszawy", "ul. Wyszynskiego",
            "ul. Szczecinska", "ul. Pyrzycka", "ul. Ogrodowa",
            "ul. Kosciuszki", "ul. 11 Listopada", "ul. Limanowskiego",
            "ul. Sikorskiego", "ul. Konopnickiej", "ul. Orzeszkowej",
            "ul. Chopina", "ul. Reymonta", "ul. Sienkiewicza",
            "ul. Norwida", "ul. Wolnosci", "ul. Rynek Staromiejski"
        ]
    },
    "goleniow": {
        "name": "Goleniow",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodleglosci", "ul. Konstytucji 3 Maja",
            "ul. Moniuszki", "ul. Chopina", "ul. Slowackiego",
            "ul. Mickiewicza", "ul. Kosciuszki", "ul. Sikorskiego",
            "ul. Szczecinska", "ul. Nowogardzka", "ul. Lotnikow",
            "ul. Kwiatowa", "ul. Polna", "ul. Ogrodowa",
            "ul. Lesna", "ul. Sosnowa", "ul. Brzozowa",
            "ul. Parkowa", "ul. Lipowa"
        ]
    },
    "nowogard": {
        "name": "Nowogard",
        "streets": [
            "ul. Wojska Polskiego", "ul. Rynek", "ul. Kosciuszki",
            "ul. Niepodleglosci", "ul. Mickiewicza", "ul. Slowackiego",
            "ul. Pilsudskiego", "ul. Szczecinska", "ul. Stargardzka",
            "ul. Ogrodowa", "ul. Polna", "ul. Lesna",
            "ul. Parkowa", "ul. Szkolna", "ul. Spokojna",
            "ul. Kwiatowa", "ul. Sosnowa", "ul. Lipowa"
        ]
    },
    "maszewo": {
        "name": "Maszewo",
        "streets": [
            "ul. Wojska Polskiego", "ul. Kosciuszki", "ul. Niepodleglosci",
            "ul. Rynek", "ul. Mickiewicza", "ul. Slowackiego",
            "ul. Ogrodowa", "ul. Polna", "ul. Lesna",
            "ul. Szkolna", "ul. Spokojna", "ul. Kwiatowa",
            "ul. Parkowa", "ul. Lipowa", "ul. Sosnowa"
        ]
    },
    "police": {
        "name": "Police",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodleglosci", "ul. Bankowa",
            "ul. Siedlecka", "ul. Tanowska", "ul. Szczecinska",
            "ul. Kosciuszki", "ul. Chopina", "ul. Slowackiego",
            "ul. Mickiewicza", "ul. Pilsudskiego", "ul. Ogrodowa",
            "ul. Polna", "ul. Lesna", "ul. Parkowa",
            "ul. Kwiatowa", "ul. Sosnowa", "ul. Lipowa",
            "ul. Szkolna", "ul. Spokojna"
        ]
    },
    "pyrzyce": {
        "name": "Pyrzyce",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodleglosci", "ul. Rynek",
            "ul. Kosciuszki", "ul. Mickiewicza", "ul. Slowackiego",
            "ul. Lipianska", "ul. Stargardzka", "ul. Szczecinska",
            "ul. Ogrodowa", "ul. Polna", "ul. Lesna",
            "ul. Parkowa", "ul. Kwiatowa", "ul. Sosnowa"
        ]
    },
    "gryfino": {
        "name": "Gryfino",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodleglosci", "ul. Rynek",
            "ul. Kosciuszki", "ul. Mickiewicza", "ul. Slowackiego",
            "ul. Szczecinska", "ul. Nad Odra", "ul. Ogrodowa",
            "ul. Polna", "ul. Lesna", "ul. Parkowa",
            "ul. Kwiatowa", "ul. Sosnowa", "ul. Lipowa",
            "ul. Szkolna", "ul. Spokojna", "ul. Nadbrzezna"
        ]
    }
}

SERVICES = [
    "naprawa-pralek",
    "naprawa-zmywarek", 
    "naprawa-lodowek",
    "naprawa-piekarnikow",
    "naprawa-suszarek"
]

SERVICE_NAMES = {
    "naprawa-pralek": "pralek",
    "naprawa-zmywarek": "zmywarek",
    "naprawa-lodowek": "lodowek",
    "naprawa-piekarnikow": "piekarnikow",
    "naprawa-suszarek": "suszarek"
}

def generate_streets_section(city_slug, service_slug):
    city_data = CITY_STREETS[city_slug]
    city_name = city_data["name"]
    streets = city_data["streets"]
    service_name = SERVICE_NAMES.get(service_slug, "AGD")
    
    # Разбиваем улицы на 3 колонки
    col_size = len(streets) // 3 + 1
    col1 = streets[:col_size]
    col2 = streets[col_size:col_size*2]
    col3 = streets[col_size*2:]
    
    def make_col(street_list):
        return "".join(f"<li>{s}</li>" for s in street_list)
    
    return f"""
<!-- ULICE - SEO LOKALNE -->
<section style="background:linear-gradient(135deg,#2c3e50,#34495e);padding:3rem 0;color:white;">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
        <h2 style="text-align:center;margin-bottom:0.5rem;font-size:1.8rem;">
            Naprawa {service_name} - ulice w {city_name}
        </h2>
        <p style="text-align:center;color:rgba(255,255,255,0.7);margin-bottom:2rem;">
            Dojeżdżamy do wszystkich ulic w {city_name} i okolicach
        </p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;">
            <ul style="list-style:none;padding:0;margin:0;">
                {make_col(col1)}
            </ul>
            <ul style="list-style:none;padding:0;margin:0;">
                {make_col(col2)}
            </ul>
            <ul style="list-style:none;padding:0;margin:0;">
                {make_col(col3)}
            </ul>
        </div>
        <p style="text-align:center;margin-top:1.5rem;color:rgba(255,255,255,0.7);">
            Nie widzisz swojej ulicy? Zadzwon - obslugujemy caly {city_name}!
            <a href="tel:+48721988949" style="color:#f39c12;font-weight:bold;"> 721 988 949</a>
        </p>
    </div>
</section>
<!-- KONIEC ULIC -->
"""

def add_streets_to_files():
    fixed = 0
    skipped = 0
    
    for service_slug in SERVICES:
        service_folder = Path(service_slug)
        
        if not service_folder.exists():
            print(f"⚠️  {service_slug} - папка не найдена")
            continue
        
        print(f"\n📁 {service_slug}")
        
        for city_slug, city_data in CITY_STREETS.items():
            city_folder = service_folder / city_slug
            
            if not city_folder.exists():
                # Пробуем с польскими буквами
                continue
            
            index_file = city_folder / "index.html"
            
            if not index_file.exists():
                print(f"   ⚠️  {city_slug}/index.html не найден")
                continue
            
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Пропускаем если улицы уже добавлены
            if 'KONIEC ULIC' in content:
                print(f"   ⏭️  {city_slug} - улицы уже есть")
                skipped += 1
                continue
            
            streets_section = generate_streets_section(city_slug, service_slug)
            
            # Добавляем перед footer
            if '<footer' in content:
                content = content.replace('<footer', streets_section + '\n<footer', 1)
            elif '</body>' in content:
                content = content.replace('</body>', streets_section + '\n</body>', 1)
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ {city_slug}/index.html - улицы добавлены")
            fixed += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Обновлено: {fixed} файлов")
    print(f"⏭️  Пропущено: {skipped} файлов")
    print(f"\n🎉 Готово! Загрузи все папки на GitHub.")

if __name__ == "__main__":
    print("🔨 Добавляю улицы для локального SEO...\n")
    add_streets_to_files()