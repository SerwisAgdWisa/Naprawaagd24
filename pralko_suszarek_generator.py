import os
from pathlib import Path

DOMAIN = "https://naprawaagd24.pl"

CITIES = {
    "szczecin": "Szczecin",
    "stargard": "Stargard",
    "goleniow": "Goleniow",
    "nowogard": "Nowogard",
    "maszewo": "Maszewo",
    "police": "Police",
    "pyrzyce": "Pyrzyce",
    "gryfino": "Gryfino"
}

BRANDS = {
    "samsung": {
        "name": "Samsung",
        "errors": ["E3", "E4", "E8", "dC", "tE", "HE", "5E", "4E"],
        "specific": "Samsung pralko-suszarka serii WD - problemy z funkcja suszenia pompa ciepla i czujnikiem wilgotnosci"
    },
    "lg": {
        "name": "LG",
        "errors": ["FE", "tE", "dE", "LE", "OE", "IE", "CE", "PE"],
        "specific": "LG pralko-suszarka TwinWash - awarie systemu Direct Drive i czujnika wilgotnosci"
    },
    "bosch": {
        "name": "Bosch",
        "errors": ["E01", "E17", "E18", "E21", "E23", "F21", "F23", "E32"],
        "specific": "Bosch pralko-suszarka WVH - problemy z grzalka suszenia i systemem kondensacji"
    },
    "whirlpool": {
        "name": "Whirlpool",
        "errors": ["F06", "F07", "F08", "F09", "F11", "F15", "F18", "F21"],
        "specific": "Whirlpool Fresh Care+ - awarie pompy ciepla i filtra kłaczkow"
    },
    "electrolux": {
        "name": "Electrolux",
        "errors": ["E11", "E20", "E21", "E40", "E60", "E61", "E66", "E67"],
        "specific": "Electrolux SteamCare - problemy z modułem suszenia i czujnikiem Lambda"
    },
    "beko": {
        "name": "Beko",
        "errors": ["E1", "E2", "E3", "E4", "H1", "H2", "H3", "H4"],
        "specific": "Beko SteamCure - awarie grzalki suszenia i termostatu"
    },
    "siemens": {
        "name": "Siemens",
        "errors": ["E01", "E17", "E18", "E21", "E23", "E67", "F01", "F21"],
        "specific": "Siemens iQ500 - problemy z pompa ciepla i systemem autodry"
    },
    "aeg": {
        "name": "AEG",
        "errors": ["E10", "E20", "E40", "E60", "E61", "E66", "E90", "E97"],
        "specific": "AEG OKOMix - awarie czujnika wilgotnosci i grzalki"
    },
    "candy": {
        "name": "Candy",
        "errors": ["E01", "E02", "E03", "E08", "E09", "E14", "E16", "E20"],
        "specific": "Candy RapidO - problemy z modułem suszenia i filtrem skraplacza"
    },
    "indesit": {
        "name": "Indesit",
        "errors": ["F01", "F03", "F05", "F06", "F07", "F12", "F15", "F17"],
        "specific": "Indesit XWDE - awarie silnika i grzalki suszenia"
    },
    "hotpoint-ariston": {
        "name": "Hotpoint-Ariston",
        "errors": ["F01", "F03", "F05", "F06", "F07", "F12", "F15", "F17"],
        "specific": "Hotpoint AQD - problemy z pompa i czujnikiem temperatury"
    },
    "gorenje": {
        "name": "Gorenje",
        "errors": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"],
        "specific": "Gorenje WD - awarie systemu kondensacji i wentylatora"
    }
}

# Реальные запросы людей (из поиска)
HUMAN_QUERIES = [
    "pralko suszarka nie suszy",
    "pralko suszarka nie dosusza ubran",
    "pralko suszarka pranie wychodzi mokre",
    "pralko suszarka suszy za dlugo",
    "pralko suszarka nie grzeje podczas suszenia",
    "pralko suszarka filtr klaczkow zatkany",
    "pralko suszarka halas podczas suszenia",
    "pralko suszarka program suszenia nie konczy sie",
    "pralko suszarka nie wiruje i nie suszy",
    "pralko suszarka nie odprowadza wody po suszeniu",
    "pralko suszarka zbiornik na wode pelny szybko",
    "pralko suszarka sonda lambda nie dziala",
    "pralko suszarka czujnik wilgotnosci uszkodzony",
    "pralko suszarka pompa ciepla nie dziala",
    "pralko suszarka grzalka przepalona",
    "pralko suszarka wyswietla blad kod",
    "pralko suszarka beben nie obraca sie podczas suszenia",
    "pralko suszarka wentylator nie dziala",
    "pralko suszarka ubrania gorące ale mokre",
    "pralko suszarka nie startuje program suszenia"
]

# Типичные поломки с причинами
TYPICAL_FAILURES = [
    ("Pralko-suszarka nie suszy - pranie mokre po cyklu", "Uszkodzona grzalka suszenia lub zatkany filtr klaczkow"),
    ("Pralko-suszarka nie dosusza - ubrania lekko wilgotne", "Brudna sonda Lambda lub uszkodzony czujnik wilgotnosci"),
    ("Pralko-suszarka suszy za dlugo", "Zatkany filtr skraplacza lub przepełniony zbiornik na wode"),
    ("Pralko-suszarka nie grzeje podczas suszenia", "Przepalona grzalka lub uszkodzony termostat"),
    ("Pralko-suszarka halas podczas suszenia", "Zuzyte lozyska bebna lub uszkodzony wentylator"),
    ("Pralko-suszarka nie konczy programu suszenia", "Uszkodzony czujnik temperatury lub modul sterujacy"),
    ("Pralko-suszarka wyswietla blad podczas suszenia", "Awaria czujnika wilgotnosci lub sondy Lambda"),
    ("Pralko-suszarka pompa ciepla nie dziala", "Uszkodzona sprezarka lub wymiennik ciepla"),
    ("Pralko-suszarka beben nie kreci przy suszeniu", "Zerwany pasek napedowy lub uszkodzony silnik"),
    ("Pralko-suszarka zbiornik szybko sie napelnia", "Nieprawidlowa kondensacja - problem z wymiennikiem"),
    ("Pralko-suszarka nie odprowadza wody po suszeniu", "Zatkana pompa odplywowa lub przewod"),
    ("Pralko-suszarka przerywa suszenie w polowie", "Przegrzanie - zatkany filtr lub awaria termostatu"),
]

def generate_brand_page(city_slug, city_name, brand_slug, brand_data):
    errors_list = "".join(f"<li><strong>Blad {e}</strong> - diagnostyka i naprawa</li>" for e in brand_data["errors"])
    failures_list = "".join(f"<li><strong>{f[0]}</strong><br><small style='color:rgba(255,255,255,0.7)'>{f[1]}</small></li>" for f in TYPICAL_FAILURES[:8])
    queries_list = "".join(f"<li>{q} {city_name}</li>" for q in HUMAN_QUERIES[:10])
    
    page_url = f"{DOMAIN}/naprawa-pralko-suszarek/{city_slug}/{brand_slug}.html"
    brand_name = brand_data["name"]
    
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow">
    <title>Naprawa Pralko-Suszarek {brand_name} {city_name} | Nie suszy, blad | 721 988 949</title>
    <meta name="description" content="Pralko-suszarka {brand_name} nie suszy w {city_name}? Pranie mokre po cyklu? Blad {brand_data["errors"][0]}? Naprawiamy na miejscu. Dojazd tego samego dnia. Tel: 721 988 949">
    <link rel="canonical" href="{page_url}">
    <link rel="stylesheet" href="../../css/style.css">
    <script>type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Naprawa Pralko-Suszarek {brand_name} {city_name}",
        "telephone": "+48721988949",
        "address": {{"@type": "PostalAddress", "addressLocality": "{city_name}", "addressCountry": "PL"}},
        "url": "{page_url}"
    }}
    </script>
</head>
<body>
<header>
    <div class="container">
        <div class="header-content">
            <a href="/" class="logo">Naprawaagd24</a>
            <a href="tel:+48721988949" class="phone">📞 721 988 949</a>
        </div>
    </div>
</header>

<!-- BREADCRUMB -->
<nav style="background:rgba(0,0,0,0.3);padding:12px 20px;font-size:0.9rem;">
    <div style="max-width:1200px;margin:0 auto;">
        <a href="/" style="color:#a0b4f8;text-decoration:none;">Strona Glowna</a>
        <span style="color:rgba(255,255,255,0.6);margin:0 6px;">›</span>
        <a href="/naprawa-pralko-suszarek/" style="color:#a0b4f8;text-decoration:none;">Naprawa Pralko-Suszarek</a>
        <span style="color:rgba(255,255,255,0.6);margin:0 6px;">›</span>
        <a href="/naprawa-pralko-suszarek/{city_slug}/" style="color:#a0b4f8;text-decoration:none;">{city_name}</a>
        <span style="color:rgba(255,255,255,0.6);margin:0 6px;">›</span>
        <span style="color:white;font-weight:bold;">{brand_name}</span>
    </div>
</nav>

<section class="hero">
    <div class="container">
        <h1>Pralko-Suszarka {brand_name} nie suszy w {city_name}?</h1>
        <p>Pranie wychodzi mokre? Program suszenia nie konczy sie? Naprawiamy na miejscu tego samego dnia!</p>
        <a href="#order" class="cta-button">Zamow Naprawe - 721 988 949</a>
    </div>
</section>

<section class="services">
    <div class="container">
        <div class="services-grid">

            <div class="service-link-card">
                <div class="service-icon">🔍</div>
                <h3>Co ludzie wpisuja w Google</h3>
                <ul style="text-align:left;color:white;font-size:0.9rem;">
                    {queries_list}
                </ul>
            </div>

            <div class="service-link-card">
                <div class="service-icon">⚠️</div>
                <h3>Typowe usterki pralko-suszarek {brand_name}</h3>
                <ul style="text-align:left;color:white;font-size:0.9rem;">
                    {failures_list}
                </ul>
            </div>

            <div class="service-link-card">
                <div class="service-icon">🔢</div>
                <h3>Kody bledow {brand_name}</h3>
                <ul style="text-align:left;color:white;font-size:0.9rem;">
                    {errors_list}
                </ul>
            </div>

        </div>

        <div class="service-link-card" style="margin-top:2rem;">
            <div class="service-icon">ℹ️</div>
            <h3>Specyfika {brand_name} w {city_name}</h3>
            <p style="color:rgba(255,255,255,0.9);">{brand_data["specific"]}. Naprawiamy wszystkie modele pralko-suszarek {brand_name} w {city_name} i okolicach. Dojazd do klienta, gwarancja na usluge.</p>
        </div>
    </div>
</section>

<section class="order-section" id="order">
    <div class="container">
        <div class="order-form">
            <h2>Zamow naprawe pralko-suszarki {brand_name} w {city_name}</h2>
            <form id="orderForm">
                <div class="form-group">
                    <label>Imie:</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Telefon:</label>
                    <input type="tel" name="phone" required>
                </div>
                <div class="form-group">
                    <label>Adres w {city_name}:</label>
                    <input type="text" name="address" required>
                </div>
                <div class="form-group">
                    <label>Model pralko-suszarki:</label>
                    <input type="text" name="model" placeholder="np. {brand_name} WD...">
                </div>
                <div class="form-group">
                    <label>Opis problemu:</label>
                    <textarea name="problem" placeholder="np. pralko-suszarka nie suszy, pranie mokre, blad na wyswietlaczu..." required></textarea>
                </div>
                <button type="submit" class="submit-btn">Wyslij przez WhatsApp</button>
            </form>
        </div>
    </div>
</section>

<footer>
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h3>Kontakt</h3>
                <p>📞 <a href="tel:+48721988949">721 988 949</a></p>
                <p>💬 <a href="https://wa.me/48721988949">WhatsApp</a></p>
            </div>
            <div class="footer-section">
                <h3>Inne marki w {city_name}</h3>
                {''.join(f'<p><a href="{b}.html">{BRANDS[b]["name"]}</a></p>' for b in list(BRANDS.keys())[:5] if b != brand_slug)}
            </div>
            <div class="footer-section">
                <h3>Inne uslugi {city_name}</h3>
                <p><a href="/naprawa-pralek/{city_slug}/">Naprawa Pralek</a></p>
                <p><a href="/naprawa-suszarek/{city_slug}/">Naprawa Suszarek</a></p>
                <p><a href="/naprawa-zmywarek/{city_slug}/">Naprawa Zmywarek</a></p>
                <p><a href="/naprawa-lodowek/{city_slug}/">Naprawa Lodowek</a></p>
                <p><a href="/naprawa-piekarnikow/{city_slug}/">Naprawa Piekarnikow</a></p>
            </div>
        </div>
        <p>© 2026 Naprawaagd24 | Naprawa Pralko-Suszarek {brand_name} {city_name} | 721 988 949</p>
    </div>
</footer>

<a href="https://wa.me/48721988949" class="whatsapp-float">💬</a>

<script>
document.getElementById('orderForm').addEventListener('submit', function(e) {{
    e.preventDefault();
    const name = this.name.value;
    const phone = this.phone.value;
    const address = this.address.value;
    const model = this.model.value;
    const problem = this.problem.value;
    const message = `Naprawa Pralko-Suszarki {brand_name} - {city_name}\\n\\n${{name}}\\n${{phone}}\\n${{address}}\\nModel: ${{model}}\\n\\n${{problem}}`;
    window.open(`https://wa.me/48721988949?text=${{encodeURIComponent(message)}}`, '_blank');
}});
</script>
</body>
</html>'''

def generate_city_index(city_slug, city_name):
    brand_cards = ""
    for brand_slug, brand_data in BRANDS.items():
        brand_cards += f'''
        <a href="{brand_slug}.html" class="service-link-card">
            <div class="service-icon">🔧</div>
            <h3>{brand_data["name"]}</h3>
            <p>Pralko-suszarka {brand_data["name"]} nie suszy w {city_name}? Naprawiamy!</p>
        </a>'''

    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Naprawa Pralko-Suszarek {city_name} | Wszystkie marki | 721 988 949</title>
    <meta name="description" content="Naprawa pralko-suszarek {city_name}. Nie suszy, pranie mokre, blad na wyswietlaczu? Naprawiamy wszystkie marki. Dojazd tego samego dnia. Tel: 721 988 949">
    <link rel="canonical" href="{DOMAIN}/naprawa-pralko-suszarek/{city_slug}/">
    <link rel="stylesheet" href="../../css/style.css">
</head>
<body>
<header>
    <div class="container">
        <div class="header-content">
            <a href="/" class="logo">Naprawaagd24</a>
            <a href="tel:+48721988949" class="phone">📞 721 988 949</a>
        </div>
    </div>
</header>

<nav style="background:rgba(0,0,0,0.3);padding:12px 20px;font-size:0.9rem;">
    <div style="max-width:1200px;margin:0 auto;">
        <a href="/" style="color:#a0b4f8;text-decoration:none;">Strona Glowna</a>
        <span style="color:rgba(255,255,255,0.6);margin:0 6px;">›</span>
        <a href="/naprawa-pralko-suszarek/" style="color:#a0b4f8;text-decoration:none;">Naprawa Pralko-Suszarek</a>
        <span style="color:rgba(255,255,255,0.6);margin:0 6px;">›</span>
        <span style="color:white;font-weight:bold;">{city_name}</span>
    </div>
</nav>

<section class="hero">
    <div class="container">
        <h1>Naprawa Pralko-Suszarek {city_name}</h1>
        <p>Pralko-suszarka nie suszy? Pranie wychodzi mokre? Wybierz marke i zamow naprawe!</p>
        <a href="#order" class="cta-button">Zadzwon 721 988 949</a>
    </div>
</section>

<section class="services">
    <div class="container">
        <h2>Wybierz marke pralko-suszarki - {city_name}</h2>
        <div class="services-grid">
            {brand_cards}
        </div>
    </div>
</section>

<footer>
    <div class="container">
        <p>© 2026 Naprawaagd24 | Naprawa Pralko-Suszarek {city_name} | 721 988 949</p>
    </div>
</footer>
<a href="https://wa.me/48721988949" class="whatsapp-float">💬</a>
</body>
</html>'''

def create_all():
    total = 0
    base = Path("naprawa-pralko-suszarek")
    base.mkdir(exist_ok=True)

    # Главная страница категории
    main_html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Naprawa Pralko-Suszarek | Szczecin, Stargard, Goleniow | 721 988 949</title>
    <meta name="description" content="Naprawa pralko-suszarek Szczecin, Stargard, Goleniow i okolice. Nie suszy? Pranie mokre? Naprawiamy wszystkie marki. Tel: 721 988 949">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header>
    <div class="container">
        <div class="header-content">
            <a href="/" class="logo">Naprawaagd24</a>
            <a href="tel:+48721988949" class="phone">📞 721 988 949</a>
        </div>
    </div>
</header>
<section class="hero">
    <div class="container">
        <h1>Naprawa Pralko-Suszarek</h1>
        <p>Wybierz swoje miasto i marke urzadzenia</p>
        <a href="#cities" class="cta-button">Wybierz miasto</a>
    </div>
</section>
<section class="services" id="cities">
    <div class="container">
        <h2>Wybierz miasto</h2>
        <div class="services-grid">
            {''.join(f'<a href="{slug}/" class="service-link-card"><div class="service-icon">📍</div><h3>{name}</h3><p>Naprawa pralko-suszarek w {name}</p></a>' for slug, name in CITIES.items())}
        </div>
    </div>
</section>
<footer>
    <div class="container">
        <p>© 2026 Naprawaagd24 | Naprawa Pralko-Suszarek | 721 988 949</p>
    </div>
</footer>
<a href="https://wa.me/48721988949" class="whatsapp-float">💬</a>
</body>
</html>'''

    with open(base / "index.html", 'w', encoding='utf-8') as f:
        f.write(main_html)
    print("✅ naprawa-pralko-suszarek/index.html")

    for city_slug, city_name in CITIES.items():
        city_folder = base / city_slug
        city_folder.mkdir(exist_ok=True)

        # Страница города
        with open(city_folder / "index.html", 'w', encoding='utf-8') as f:
            f.write(generate_city_index(city_slug, city_name))
        print(f"✅ {city_slug}/index.html")

        # Страницы брендов
        for brand_slug, brand_data in BRANDS.items():
            html = generate_brand_page(city_slug, city_name, brand_slug, brand_data)
            filepath = city_folder / f"{brand_slug}.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            total += 1
            print(f"   ✅ {city_slug}/{brand_slug}.html")

    print(f"\n🎉 Gotowe!")
    print(f"📊 Utworzono: {total} stron marek + {len(CITIES)} stron miast + 1 glowna")
    print(f"📁 Folder: naprawa-pralko-suszarek/")
    print(f"\n➡️  Dodaj link do index.html na glownej stronie!")

if __name__ == "__main__":
    print("🚀 Tworze strony naprawa-pralko-suszarek...\n")
    create_all()