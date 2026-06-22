import os
from pathlib import Path

DOMAIN = "https://naprawaagd24.pl"

cities = {
    "szczecin": {
        "name": "Szczecin",
        "icon": "🏙️",
        "districts": "Pogodno, Niebuszewo, Centrum, Prawobrzeze, Dabie, Gumience, Bukowe, Warszewo",
        "desc": "Profesjonalny serwis AGD w Szczecinie. Naprawiamy pralki, zmywarki, lodowki, piekarniki i suszarki we wszystkich dzielnicach Szczecina."
    },
    "stargard": {
        "name": "Stargard",
        "icon": "🏛️",
        "districts": "Centrum, Kluczewo, Osiedle Zachod, Osiedle Pyrzyckie, Stare Miasto, Lipnik",
        "desc": "Serwis AGD w Stargardzie. Szybka naprawa sprzetu AGD wszystkich marek. Dojazd do klienta."
    },
    "goleniow": {
        "name": "Goleniow",
        "icon": "✈️",
        "districts": "Centrum, Osiedle Helenow, Krzewno, Kliniska Wielkie, Mosty, Marszewo",
        "desc": "Naprawa AGD w Goleniowie i okolicach. Obslugujemy centrum i okoliczne miejscowosci."
    },
    "nowogard": {
        "name": "Nowogard",
        "icon": "🌳",
        "districts": "Centrum, Karsk, Warnkowo, Osiedle Mlodych, Dabrowa Nowogardzka",
        "desc": "Serwis AGD w Nowogardzie. Naprawiamy pralki, zmywarki i lodowki w Nowogardzie i okolicach."
    },
    "maszewo": {
        "name": "Maszewo",
        "icon": "🌾",
        "districts": "Centrum, Badelnik, Maciejewo, Debice, Stare Maszewo",
        "desc": "Naprawa AGD w Maszewie i okolicznych wsiach. Dojazd do klienta."
    },
    "police": {
        "name": "Police",
        "icon": "🏭",
        "districts": "Centrum, Tanowo, Trzebież, Pilchowo, Jasienica, Msciecino",
        "desc": "Serwis AGD w Policach. Szybki dojazd ze Szczecina. Naprawa wszystkich marek AGD."
    },
    "pyrzyce": {
        "name": "Pyrzyce",
        "icon": "🏘️",
        "districts": "Stare Miasto, Osiedle Mlodych, Mielecin, Okunica, Kozielice",
        "desc": "Naprawa AGD w Pyrzycach i okolicach. Obslugujemy Pyrzyce i gminy okoliczne."
    },
    "gryfino": {
        "name": "Gryfino",
        "icon": "🌊",
        "districts": "Stare Miasto, Osiedle Nadodrzanskie, Zabnica, Nowe Czarnowo, Lubczyno",
        "desc": "Serwis AGD w Gryfinie. Naprawa pralek, zmywarek i lodowek w Gryfinie i okolicach."
    }
}

services = [
    {"slug": "naprawa-pralek", "name": "Naprawa Pralek", "icon": "🔧", "desc": "Wszystkie marki pralek automatycznych"},
    {"slug": "naprawa-zmywarek", "name": "Naprawa Zmywarek", "icon": "🍽️", "desc": "Serwis zmywarek wszystkich typow"},
    {"slug": "naprawa-lodowek", "name": "Naprawa Lodowek", "icon": "❄️", "desc": "Uklady chlodnicze, termostaty, uszczelki"},
    {"slug": "naprawa-piekarnikow", "name": "Naprawa Piekarnikow", "icon": "🔥", "desc": "Piekarniki elektryczne i gazowe"},
    {"slug": "naprawa-suszarek", "name": "Naprawa Suszarek", "icon": "🌪️", "desc": "Suszarki bebnowe wszystkich marek"},
]

def generate_city_page(city_slug, city):
    html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow">
    <title>Serwis AGD {city['name']} | Naprawa pralek, zmywarek, lodowek | 721 988 949</title>
    <meta name="description" content="{city['desc']} Tel: 721 988 949">
    <link rel="canonical" href="{DOMAIN}/{city_slug}/">
    <link rel="stylesheet" href="../css/style.css">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Serwis AGD WISA {city['name']}",
      "telephone": "+48721988949",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "{city['name']}",
        "addressCountry": "PL"
      }},
      "url": "{DOMAIN}/{city_slug}/"
    }}
    </script>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="../" class="logo">WISA</a>
                <a href="tel:+48721988949" class="phone">📞 721 988 949</a>
            </div>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>{city['icon']} Serwis AGD {city['name']}</h1>
            <p>{city['desc']}</p>
            <a href="#order" class="cta-button">Zamow Naprawe</a>
        </div>
    </section>

    <section class="services">
        <div class="container">
            <h2>Nasze uslugi w {city['name']}</h2>
            <div class="services-grid">'''

    for service in services:
        html += f'''
                <a href="../{service['slug']}/{city_slug}/" class="service-link-card">
                    <div class="service-icon">{service['icon']}</div>
                    <h3>{service['name']}</h3>
                    <p>{service['desc']}</p>
                </a>'''

    html += f'''
            </div>
        </div>
    </section>

    <section class="cities-navigation">
        <div class="container">
            <h2>Obsługiwane obszary - {city['name']}</h2>
            <p>{city['districts']}</p>
            <p><strong>Dojazd tego samego dnia | Gwarancja | Oryginalne czesci</strong></p>
        </div>
    </section>

    <section class="order-section" id="order">
        <div class="container">
            <div class="order-form">
                <h2>Zamow naprawe AGD w {city['name']}</h2>
                <form id="orderForm">
                    <div class="form-group">
                        <label>Rodzaj uslugi:</label>
                        <select name="service" required>
                            <option value="">Wybierz usluge</option>
                            <option value="pralka">Naprawa pralki</option>
                            <option value="zmywarka">Naprawa zmywarki</option>
                            <option value="lodowka">Naprawa lodowki</option>
                            <option value="piekarnik">Naprawa piekarnika</option>
                            <option value="suszarka">Naprawa suszarki</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Imie:</label>
                        <input type="text" name="name" required>
                    </div>
                    <div class="form-group">
                        <label>Telefon:</label>
                        <input type="tel" name="phone" required>
                    </div>
                    <div class="form-group">
                        <label>Adres w {city['name']}:</label>
                        <input type="text" name="address" required>
                    </div>
                    <div class="form-group">
                        <label>Opis problemu:</label>
                        <textarea name="problem" required></textarea>
                    </div>
                    <button type="submit" class="submit-btn">Wyslij przez WhatsApp</button>
                </form>
            </div>
        </div>
    </section>

    <div class="breadcrumb">
        <div class="container">
            <a href="../">Strona Glowna</a> →
            <span class="current">{city['name']}</span>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Kontakt</h3>
                    <p>Oleksandr Chumnyi WISA</p>
                    <p>📞 <a href="tel:+48721988949">721 988 949</a></p>
                    <p>💬 <a href="https://wa.me/48721988949">WhatsApp</a></p>
                </div>
                <div class="footer-section">
                    <h3>Uslugi w {city['name']}</h3>
                    <p><a href="../naprawa-pralek/{city_slug}/">Naprawa Pralek</a></p>
                    <p><a href="../naprawa-zmywarek/{city_slug}/">Naprawa Zmywarek</a></p>
                    <p><a href="../naprawa-lodowek/{city_slug}/">Naprawa Lodowek</a></p>
                    <p><a href="../naprawa-piekarnikow/{city_slug}/">Naprawa Piekarnikow</a></p>
                    <p><a href="../naprawa-suszarek/{city_slug}/">Naprawa Suszarek</a></p>
                </div>
                <div class="footer-section">
                    <h3>Inne miasta</h3>'''

    for other_slug, other_city in list(cities.items())[:4]:
        if other_slug != city_slug:
            html += f'\n                    <p><a href="../{other_slug}/">{other_city["name"]}</a></p>'

    html += f'''
                </div>
            </div>
            <p>© 2025 Serwis AGD WISA {city['name']} | 721 988 949</p>
        </div>
    </footer>

    <a href="https://wa.me/48721988949?text=Serwis%20AGD%20{city['name']}" class="whatsapp-float">💬</a>

    <script>
        document.getElementById('orderForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const name = this.name.value;
            const phone = this.phone.value;
            const address = this.address.value;
            const service = this.service.value;
            const problem = this.problem.value;

            const message = `Serwis AGD {city['name']}\\n\\n${{name}}\\n${{phone}}\\n${{address}}\\n${{service}}\\n\\n${{problem}}`;
            window.open(`https://wa.me/48721988949?text=${{encodeURIComponent(message)}}`, '_blank');
            alert('Przekierowanie do WhatsApp...');
        }});
    </script>
</body>
</html>'''

    return html

def create_city_pages():
    total = 0
    for city_slug, city in cities.items():
        folder = Path(city_slug)
        folder.mkdir(exist_ok=True)

        html = generate_city_page(city_slug, city)
        filepath = folder / "index.html"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        total += 1
        print(f"✅ {city_slug}/index.html - {city['name']}")

    print(f"\n🎉 Utworzono {total} stron miast!")
    print(f"\n📋 Teraz zaktualizuj linki na glownej stronie:")
    for city_slug, city in cities.items():
        print(f"   {city['name']}: ../{city_slug}/")

if __name__ == "__main__":
    create_city_pages()