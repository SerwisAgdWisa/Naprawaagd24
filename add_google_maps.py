import re
from pathlib import Path

# Координаты и embed коды для каждого города
CITY_MAPS = {
    "szczecin": {
        "name": "Szczecin",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d154426!2d14.5528!3d53.4285!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa093800d06837%3A0x42b45b23a5895509!2sSzczecin!5e0!3m2!1spl!2spl!4v1625000000000",
        "area": "Szczecin i okolice w promieniu 50km"
    },
    "stargard": {
        "name": "Stargard",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d15.0497!3d53.3353!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b3b%3A0x42b45b23a5895509!2sStargard!5e0!3m2!1spl!2spl!4v1625000000001",
        "area": "Stargard i okolice w promieniu 30km"
    },
    "goleniow": {
        "name": "Goleniow",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d14.8219!3d53.5588!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b3c%3A0x42b45b23a5895509!2sGoleni%C3%B3w!5e0!3m2!1spl!2spl!4v1625000000002",
        "area": "Goleniow i okolice w promieniu 25km"
    },
    "nowogard": {
        "name": "Nowogard",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d15.1167!3d53.6667!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b3d%3A0x42b45b23a5895509!2sNowogard!5e0!3m2!1spl!2spl!4v1625000000003",
        "area": "Nowogard i okolice w promieniu 25km"
    },
    "maszewo": {
        "name": "Maszewo",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d14.9167!3d53.4833!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b3e%3A0x42b45b23a5895509!2sMaszewo!5e0!3m2!1spl!2spl!4v1625000000004",
        "area": "Maszewo i okolice w promieniu 20km"
    },
    "police": {
        "name": "Police",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d14.5667!3d53.5500!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b3f%3A0x42b45b23a5895509!2sPolice!5e0!3m2!1spl!2spl!4v1625000000005",
        "area": "Police i okolice w promieniu 20km"
    },
    "pyrzyce": {
        "name": "Pyrzyce",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d14.8833!3d53.1500!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b40%3A0x42b45b23a5895509!2sPyrzyce!5e0!3m2!1spl!2spl!4v1625000000006",
        "area": "Pyrzyce i okolice w promieniu 20km"
    },
    "gryfino": {
        "name": "Gryfino",
        "embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39442!2d14.4833!3d53.2500!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47aa3a3b3b3b3b41%3A0x42b45b23a5895509!2sGryfino!5e0!3m2!1spl!2spl!4v1625000000007",
        "area": "Gryfino i okolice w promieniu 20km"
    }
}

# Папки в которых искать index.html городов
SERVICE_FOLDERS = [
    "naprawa-pralek",
    "naprawa-zmywarek",
    "naprawa-lodowek",
    "naprawa-piekarnikow",
    "naprawa-suszarek",
    "naprawa-pralko-suszarek",
]

# Также папки городов в корне
ROOT_CITY_FOLDERS = True

def generate_map_section(city_slug, city_name, embed_url, area):
    return f"""
<!-- MAPA GOOGLE - DODANA SKRYPTEM -->
<section style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:3rem 0;">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
        <h2 style="color:white;text-align:center;margin-bottom:0.5rem;font-size:1.8rem;">
            Obszar obslugi - {city_name}
        </h2>
        <p style="color:rgba(255,255,255,0.7);text-align:center;margin-bottom:1.5rem;">
            {area} | Dojazd tego samego dnia | Tel: 721 988 949
        </p>
        <iframe
            src="{embed_url}"
            width="100%"
            height="400"
            style="border:0;border-radius:12px;box-shadow:0 5px 20px rgba(0,0,0,0.3);"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
        <p style="color:rgba(255,255,255,0.6);text-align:center;margin-top:1rem;font-size:0.9rem;">
            Nie widzisz swojej miejscowosci? Zadzwon - obslugujemy caly region!
            <a href="tel:+48721988949" style="color:#f39c12;font-weight:bold;"> 721 988 949</a>
        </p>
    </div>
</section>
<!-- KONIEC MAPY -->
"""

def add_map_to_file(filepath, city_slug):
    city_data = CITY_MAPS.get(city_slug)
    if not city_data:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Пропускаем если карта уже есть
    if 'KONIEC MAPY' in content:
        return False

    map_section = generate_map_section(
        city_slug,
        city_data["name"],
        city_data["embed"],
        city_data["area"]
    )

    # Добавляем перед footer
    if '<footer' in content:
        content = content.replace('<footer', map_section + '\n<footer', 1)
    elif '</body>' in content:
        content = content.replace('</body>', map_section + '\n</body>', 1)
    else:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def add_maps_to_all():
    fixed = 0
    skipped = 0

    print("🗺️  Dodaje mapy Google do stron miast...\n")

    # 1. Страницы услуг/город (naprawa-pralek/szczecin/index.html)
    for service in SERVICE_FOLDERS:
        service_path = Path(service)
        if not service_path.exists():
            print(f"⚠️  {service} - папка не найдена")
            continue

        print(f"\n📁 {service}")

        for city_slug, city_data in CITY_MAPS.items():
            city_path = service_path / city_slug
            if not city_path.exists():
                continue

            index_file = city_path / "index.html"
            if not index_file.exists():
                continue

            result = add_map_to_file(index_file, city_slug)
            if result:
                print(f"   ✅ {city_slug}/index.html - mapa dodana")
                fixed += 1
            else:
                print(f"   ⏭️  {city_slug}/index.html - juz ma mape")
                skipped += 1

    # 2. Страницы городов в корне (szczecin/index.html)
    if ROOT_CITY_FOLDERS:
        print(f"\n📁 Strony miast (korzen)")
        for city_slug, city_data in CITY_MAPS.items():
            city_path = Path(city_slug)
            if not city_path.exists():
                continue

            index_file = city_path / "index.html"
            if not index_file.exists():
                continue

            result = add_map_to_file(index_file, city_slug)
            if result:
                print(f"   ✅ {city_slug}/index.html - mapa dodana")
                fixed += 1
            else:
                print(f"   ⏭️  {city_slug}/index.html - juz ma mape")
                skipped += 1

    print(f"\n{'='*50}")
    print(f"✅ Dodano mapy: {fixed} plikow")
    print(f"⏭️  Pominieto: {skipped} plikow")
    print(f"\n🎉 Gotowe! Zaladuj zmiany na GitHub.")

if __name__ == "__main__":
    add_maps_to_all()