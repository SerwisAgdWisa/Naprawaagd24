import re
from pathlib import Path

CITY_STREETS = {
    "szczecin": {
        "name": "Szczecin",
        "streets": [
            "al. Bohaterów Warszawy", "ul. Niepodległości", "ul. Monte Cassino",
            "ul. Wojska Polskiego", "ul. Jagiellońska", "ul. Piastów",
            "ul. Rayskiego", "ul. Wyzwolenia", "ul. Słowackiego",
            "ul. Mickiewicza", "ul. Krasickiego", "ul. Broniewskiego",
            "ul. Energetyków", "ul. Ku Słońcu", "ul. Struga",
            "ul. Bandurskiego", "al. Papieża Jana Pawła II", "ul. Kolumba",
            "ul. Spichrzowa", "ul. Roosevelta", "ul. Mazurska",
            "ul. Kopernika", "ul. Łomżyńska", "ul. Strzałowska",
            "ul. Północna", "ul. Leśna", "ul. Dąbrowskiego",
            "ul. Spacerowa", "ul. Sosnowa", "ul. Lipowa"
        ]
    },
    "stargard": {
        "name": "Stargard",
        "streets": [
            "ul. Jagiellońska", "ul. Mickiewicza", "ul. Wojska Polskiego",
            "ul. Słowackiego", "ul. Pierwszej Brygady", "ul. Skłodowskiej",
            "ul. Piłsudskiego", "ul. Bohaterów Warszawy", "ul. Wyszyńskiego",
            "ul. Szczecińska", "ul. Pyrzycka", "ul. Ogrodowa",
            "ul. Kościuszki", "ul. 11 Listopada", "ul. Limanowskiego",
            "ul. Sikorskiego", "ul. Konopnickiej", "ul. Orzeszkowej",
            "ul. Chopina", "ul. Reymonta", "ul. Sienkiewicza",
            "ul. Norwida", "ul. Wolności", "ul. Rynek Staromiejski"
        ]
    },
    "goleniow": {
        "name": "Goleniów",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodległości", "ul. Konstytucji 3 Maja",
            "ul. Moniuszki", "ul. Chopina", "ul. Słowackiego",
            "ul. Mickiewicza", "ul. Kościuszki", "ul. Sikorskiego",
            "ul. Szczecińska", "ul. Nowogardzka", "ul. Lotników",
            "ul. Kwiatowa", "ul. Polna", "ul. Ogrodowa",
            "ul. Leśna", "ul. Sosnowa", "ul. Brzozowa",
            "ul. Parkowa", "ul. Lipowa"
        ]
    },
    "nowogard": {
        "name": "Nowogard",
        "streets": [
            "ul. Wojska Polskiego", "ul. Rynek", "ul. Kościuszki",
            "ul. Niepodległości", "ul. Mickiewicza", "ul. Słowackiego",
            "ul. Piłsudskiego", "ul. Szczecińska", "ul. Stargardzka",
            "ul. Ogrodowa", "ul. Polna", "ul. Leśna",
            "ul. Parkowa", "ul. Szkolna", "ul. Spokojna",
            "ul. Kwiatowa", "ul. Sosnowa", "ul. Lipowa"
        ]
    },
    "maszewo": {
        "name": "Maszewo",
        "streets": [
            "ul. Wojska Polskiego", "ul. Kościuszki", "ul. Niepodległości",
            "ul. Rynek", "ul. Mickiewicza", "ul. Słowackiego",
            "ul. Ogrodowa", "ul. Polna", "ul. Leśna",
            "ul. Szkolna", "ul. Spokojna", "ul. Kwiatowa",
            "ul. Parkowa", "ul. Lipowa", "ul. Sosnowa"
        ]
    },
    "police": {
        "name": "Police",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodległości", "ul. Bankowa",
            "ul. Siedlecka", "ul. Tanowska", "ul. Szczecińska",
            "ul. Kościuszki", "ul. Chopina", "ul. Słowackiego",
            "ul. Mickiewicza", "ul. Piłsudskiego", "ul. Ogrodowa",
            "ul. Polna", "ul. Leśna", "ul. Parkowa",
            "ul. Kwiatowa", "ul. Sosnowa", "ul. Lipowa",
            "ul. Szkolna", "ul. Spokojna"
        ]
    },
    "pyrzyce": {
        "name": "Pyrzyce",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodległości", "ul. Rynek",
            "ul. Kościuszki", "ul. Mickiewicza", "ul. Słowackiego",
            "ul. Lipiańska", "ul. Stargardzka", "ul. Szczecińska",
            "ul. Ogrodowa", "ul. Polna", "ul. Leśna",
            "ul. Parkowa", "ul. Kwiatowa", "ul. Sosnowa"
        ]
    },
    "gryfino": {
        "name": "Gryfino",
        "streets": [
            "ul. Wojska Polskiego", "ul. Niepodległości", "ul. Rynek",
            "ul. Kościuszki", "ul. Mickiewicza", "ul. Słowackiego",
            "ul. Szczecińska", "ul. Nad Odrą", "ul. Ogrodowa",
            "ul. Polna", "ul. Leśna", "ul. Parkowa",
            "ul. Kwiatowa", "ul. Sosnowa", "ul. Lipowa",
            "ul. Szkolna", "ul. Spokojna", "ul. Nadbrzeżna"
        ]
    }
}

# Исправлен пропуск запятой!
SERVICES = [
    "naprawa-pralek",
    "naprawa-zmywarek", 
    "naprawa-lodowek",
    "naprawa-piekarnikow",
    "naprawa-suszarek",
    "naprawa-pralko-suszarek"
]

SERVICE_NAMES = {
    "naprawa-pralek": "pralek",
    "naprawa-zmywarek": "zmywarek",
    "naprawa-lodowek": "lodówek",
    "naprawa-piekarnikow": "piekarników",
    "naprawa-suszarek": "suszarek",
    "naprawa-pralko-suszarek": "pralko-suszarek"
}

def generate_streets_section(city_slug, service_slug):
    city_data = CITY_STREETS[city_slug]
    city_name = city_data["name"]
    streets = city_data["streets"]
    service_name = SERVICE_NAMES.get(service_slug, "AGD")
    
    streets_list_html = "".join(f"<li style='padding: 3px 0;'>{s}</li>" for s in streets)
    
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
        <ul style="list-style:none;padding:0;margin:0;columns:3 200px;column-gap:30px;">
            {streets_list_html}
        </ul>
        <p style="text-align:center;margin-top:1.5rem;color:rgba(255,255,255,0.7);">
            Nie widzisz swojej ulicy? Zadzwoń - obsługujemy cały {city_name}!
            <a href="tel:+48721988949" style="color:#f39c12;font-weight:bold;text-decoration:none;"> 721 988 949</a>
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
        
        for city_slug in CITY_STREETS:
            city_folder = service_folder / city_slug
            
            if not city_folder.exists():
                continue
            
            index_file = city_folder / "index.html"
            
            if not index_file.exists():
                print(f"   ⚠️  {city_slug}/index.html не найден")
                continue
            
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'KONIEC ULIC' in content:
                print(f"   ⏭️  {city_slug} - улицы уже есть")
                skipped += 1
                continue
            
            streets_section = generate_streets_section(city_slug, service_slug)
            
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

if __name__ == "__main__":
    print("🔨 Добавляю улицы для локального SEO...\n")
    add_streets_to_files()