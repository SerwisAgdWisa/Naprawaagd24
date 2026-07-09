from pathlib import Path

DOMAIN = "https://naprawaagd24.pl"

def get_html(slug, title, desc, h1, content):
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{DOMAIN}/{slug}">
    <link rel="stylesheet" href="css/style.css">
    type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{h1}",
      "author": {{"@type": "Person", "name": "Oleksandr Chumnyi WISA"}},
      "publisher": {{"@type": "Organization", "name": "WISA Serwis AGD"}},
      "url": "{DOMAIN}/{slug}"
    }}
    </script>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">WISA</a>
                <a href="tel:+48721988949" class="phone">📞 721 988 949</a>
            </div>
        </div>
    </header>

    {content}

    <section class="order-section" id="order">
        <div class="container">
            <div class="order-form">
                <h2>Zamow naprawe AGD</h2>
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
                        <label>Miasto:</label>
                        <select name="city" required>
                            <option value="">Wybierz miasto</option>
                            <option>Szczecin</option>
                            <option>Stargard</option>
                            <option>Goleniow</option>
                            <option>Nowogard</option>
                            <option>Maszewo</option>
                            <option>Police</option>
                            <option>Pyrzyce</option>
                            <option>Gryfino</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Opis problemu:</label>
                        <textarea name="problem" placeholder="Opisz co sie dzieje z urzadzeniem..." required></textarea>
                    </div>
                    <button type="submit" class="submit-btn">Wyslij przez WhatsApp</button>
                </form>
            </div>
        </div>
    </section>

    <div class="breadcrumb">
        <div class="container">
            <a href="/">Strona Glowna</a> → <span>{h1}</span>
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
                    <h3>Uslugi</h3>
                    <p><a href="/naprawa-pralek/">Naprawa Pralek</a></p>
                    <p><a href="/naprawa-zmywarek/">Naprawa Zmywarek</a></p>
                    <p><a href="/naprawa-lodowek/">Naprawa Lodowek</a></p>
                    <p><a href="/naprawa-piekarnikow/">Naprawa Piekarnikow</a></p>
                    <p><a href="/naprawa-suszarek/">Naprawa Suszarek</a></p>
                </div>
                <div class="footer-section">
                    <h3>Artykuly</h3>
                    <p><a href="/czy-oplaca-sie-naprawiac-pralke.html">Czy naprawiac pralke?</a></p>
                    <p><a href="/czy-oplaca-sie-naprawiac-zmywarke.html">Czy naprawiac zmywarke?</a></p>
                    <p><a href="/czy-oplaca-sie-naprawiac-lodowke.html">Czy naprawiac lodowke?</a></p>
                    <p><a href="/naprawa-agd-a-srodowisko.html">AGD a srodowisko</a></p>
                    <p><a href="/jak-przedluzyc-zycie-pralki.html">Jak dbac o pralke?</a></p>
                </div>
            </div>
            <p>© 2025 Serwis AGD WISA | 721 988 949</p>
        </div>
    </footer>

    <a href="https://wa.me/48721988949" class="whatsapp-float">💬</a>

   >
    document.getElementById('orderForm').addEventListener('submit', function(e) {{
        e.preventDefault();
        const name = this.name.value;
        const phone = this.phone.value;
        const city = this.city.value;
        const service = this.service.value;
        const problem = this.problem.value;
        const message = `Zgloszenie\\n\\n${{name}}\\n${{phone}}\\n${{city}}\\n${{service}}\\n\\n${{problem}}`;
        window.open(`https://wa.me/48721988949?text=${{encodeURIComponent(message)}}`, '_blank');
    }});
    </script>
</body>
</html>'''


# ============================================================
# СТАТЬЯ 1: Czy oplaca sie naprawiac pralke
# ============================================================
pralka_content = '''
    <section class="hero">
        <div class="container">
            <h1>Czy oplaca sie naprawiac pralke?</h1>
            <p>Pralka nie wiruje? Nie odprowadza wody? Sprawdz zanim wyrzucisz!</p>
            <a href="#order" class="cta-button">Zadzwon 721 988 949</a>
        </div>
    </section>

    <section class="services">
        <div class="container">

            <h2>To co ludzie najczesciej wpisuja w Google:</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">🔍</div>
                    <h3>Najczestsze zapytania</h3>
                    <ul style="text-align:left; color:white;">
                        <li>pralka nie wiruje co robic</li>
                        <li>pralka nie odprowadza wody</li>
                        <li>pralka klika ale nie kreci</li>
                        <li>woda zostaje w pralce po praniu</li>
                        <li>pralka hałasuje i stuka</li>
                        <li>pralka wycieka z dolu</li>
                        <li>pralka nie grzeje wody</li>
                        <li>po praniu ubrania mokre</li>
                        <li>pralka wywala bezpieczniki</li>
                        <li>blad E18 E24 F06 co oznacza</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">✅</div>
                    <h3>90% tych usterek naprawiamy na miejscu</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Nie wiruje - pasek lub szczotki silnika</li>
                        <li>Woda zostaje - zatkana pompa lub filtr</li>
                        <li>Klika nie kreci - uszkodzony silnik</li>
                        <li>Hałasuje - zuzyte lozyska bebna</li>
                        <li>Wycieka - uszkodzona uszczelka drzwi</li>
                        <li>Nie grzeje - przepalona grzalka</li>
                        <li>Mokre ubrania - problem z wirowaniem</li>
                        <li>Wywala korki - zwarcie w silniku</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">💰</div>
                    <h3>Naprawa vs nowa pralka</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Naprawa: srednio 200-400 zl</li>
                        <li>Nowa pralka: 800-3000 zl</li>
                        <li>Oszczednosc: nawet 2600 zl!</li>
                        <li>Wymiana paska: 150-200 zl</li>
                        <li>Wymiana pompy: 200-300 zl</li>
                        <li>Wymiana grzalki: 200-350 zl</li>
                        <li>Wymiana lozysk: 300-500 zl</li>
                        <li>Diagnoza: GRATIS przy naprawie</li>
                    </ul>
                </div>
            </div>

            <h2>Kiedy NIE warto naprawiac?</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">❌</div>
                    <h3>Rozważ nową pralke gdy:</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Pralka ma ponad 15 lat</li>
                        <li>Kilka awarii w krotkim czasie</li>
                        <li>Koszt naprawy powyzej 70% nowej</li>
                        <li>Rdza na bebnie lub obudowie</li>
                        <li>Brak czesci zamiennych</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">📞</div>
                    <h3>Zadzwon - powiemy uczciwie</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Bezplatna wycena przez telefon</li>
                        <li>Jesli nieoplacalne - powiemy wprost</li>
                        <li>Dojazd tego samego dnia</li>
                        <li>Naprawa w domu klienta</li>
                        <li>Gwarancja na usluge</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
'''

# ============================================================
# СТАТЬЯ 2: Czy oplaca sie naprawiac zmywarke
# ============================================================
zmywarka_content = '''
    <section class="hero">
        <div class="container">
            <h1>Czy oplaca sie naprawiac zmywarke?</h1>
            <p>Zmywarka nie myje? Smigla sie nie kreca? Sprawdz zanim wyrzucisz!</p>
            <a href="#order" class="cta-button">Zadzwon 721 988 949</a>
        </div>
    </section>

    <section class="services">
        <div class="container">

            <h2>To co ludzie wpisuja w Google o zmywarkach:</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">🔍</div>
                    <h3>Realne zapytania ludzi</h3>
                    <ul style="text-align:left; color:white;">
                        <li>zmywarka nie domywa naczyn</li>
                        <li>smigla w zmywarce sie nie kreca</li>
                        <li>zatkany spryskiwacz zmywarka</li>
                        <li>zmywarka nie domywa gornego kosza</li>
                        <li>zmywarka pobiera wode ale nie myje</li>
                        <li>naczynia niedomyte po zmywarce</li>
                        <li>zmywarka nie odprowadza wody</li>
                        <li>zmywarka wycieka z dolu</li>
                        <li>zmywarka nie podgrzewa wody</li>
                        <li>blad E1 E2 i10 w zmywarce</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">✅</div>
                    <h3>Co naprawiamy na miejscu</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Smigla sie nie kreca - pompa myjaca</li>
                        <li>Zatkany spryskiwacz - czyszczenie dysz</li>
                        <li>Nie domywa gornego kosza - spryskiwacz gorny</li>
                        <li>Nie odprowadza wody - pompa odplywowa</li>
                        <li>Pobiera wode ale nie myje - elektrozawor</li>
                        <li>Nie podgrzewa - grzalka</li>
                        <li>Wycieka - uszczelka lub waz</li>
                        <li>Bledy E - elektronika lub czujniki</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">💰</div>
                    <h3>Koszt naprawy vs nowa zmywarka</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Naprawa: srednio 200-450 zl</li>
                        <li>Nowa zmywarka: 800-3000 zl</li>
                        <li>Oszczednosc: nawet 2500 zl!</li>
                        <li>Naprawa pompy: 250-350 zl</li>
                        <li>Naprawa grzalki: 200-300 zl</li>
                        <li>Czyszczenie spryskiwaczy: 100-150 zl</li>
                        <li>Diagnoza: GRATIS przy naprawie</li>
                        <li>Dojazd tego samego dnia</li>
                    </ul>
                </div>
            </div>

            <h2>Dlaczego smigla sie nie kreca?</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">💧</div>
                    <h3>Najczestsze przyczyny</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Zatkane dysze w spryskiwaczu</li>
                        <li>Uszkodzona pompa myjaca</li>
                        <li>Zbyt wysokie naczynie blokuje smiglo</li>
                        <li>Zapchany elektrozawor kamieniem</li>
                        <li>Zatkany plasz wodny</li>
                        <li>Za niskie cisnienie wody</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">📞</div>
                    <h3>Nasz serwis zmywarek</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Dojazd do domu klienta</li>
                        <li>Szczecin i okolice 50km</li>
                        <li>Naprawiamy wszystkie marki</li>
                        <li>Bosch Siemens Samsung LG Whirlpool</li>
                        <li>Gwarancja na naprawe</li>
                        <li>Tel: 721 988 949</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
'''

# ============================================================
# СТАТЬЯ 3: Czy oplaca sie naprawiac lodowke
# ============================================================
lodowka_content = '''
    <section class="hero">
        <div class="container">
            <h1>Czy oplaca sie naprawiac lodowke?</h1>
            <p>Lodowka nie chlodzi? Zamarza za mocno? Sprawdz zanim wyrzucisz produkty i urzadzenie!</p>
            <a href="#order" class="cta-button">Zadzwon 721 988 949</a>
        </div>
    </section>

    <section class="services">
        <div class="container">

            <h2>To co ludzie wpisuja w Google o lodowkach:</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">🔍</div>
                    <h3>Realne zapytania ludzi</h3>
                    <ul style="text-align:left; color:white;">
                        <li>lodowka nie chlodzi co robic</li>
                        <li>zamrazarka mrozi lodowka nie chlodzi</li>
                        <li>spod lodowki cieknie woda</li>
                        <li>lodowka bardzo glosna w nocy</li>
                        <li>lod na tylnej scianie lodowki</li>
                        <li>lodowka zamarza jedzenie</li>
                        <li>No Frost nie dziala</li>
                        <li>lodowka nie wylacza sie</li>
                        <li>czerwona lampka w lodowce</li>
                        <li>lodowka nie dziala po przeprowadzce</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">✅</div>
                    <h3>90% tych usterek naprawiamy</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Nie chlodzi - kompresor lub freon</li>
                        <li>Zamrazarka mrozi lodowka nie - obieg czynnika</li>
                        <li>Woda pod lodowka - zatkany odplyw</li>
                        <li>Glosna w nocy - wentylator lub kompresor</li>
                        <li>Lod na scianie - awaria No Frost</li>
                        <li>Zamarza jedzenie - uszkodzony termostat</li>
                        <li>Nie wylacza sie - czujnik temperatury</li>
                        <li>Po przeprowadzce nie dziala - uklad chlodniczy</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">⚡</div>
                    <h3>Pilna naprawa lodowki</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Dojazd tego samego dnia!</li>
                        <li>Ratujemy Twoje produkty</li>
                        <li>Naprawa w domu klienta</li>
                        <li>Szczecin i okolice 50km</li>
                        <li>Uzupelnienie freonu: 300-500 zl</li>
                        <li>Nowa lodowka: 1500-5000 zl</li>
                        <li>Oszczedzasz nawet 4500 zl!</li>
                        <li>Diagnoza GRATIS</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
'''

# ============================================================
# СТАТЬЯ 4: Naprawa AGD a srodowisko
# ============================================================
srodowisko_content = '''
    <section class="hero">
        <div class="container">
            <h1>Nie wyrzucaj - naprawiaj! Chron srodowisko</h1>
            <p>Wyrzucona pralka to 600 kg CO2. Naprawiona to tylko 10 kg. Wybor nalezy do Ciebie!</p>
            <a href="#order" class="cta-button">Zadzwon 721 988 949</a>
        </div>
    </section>

    <section class="services">
        <div class="container">

            <h2>Czy wiesz co dzieje sie z wyrzucona pralka?</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">🌍</div>
                    <h3>Fakty o elektroodpadach</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Produkcja pralki = 600 kg CO2</li>
                        <li>Naprawa pralki = tylko 10 kg CO2</li>
                        <li>Lodowka zawiera szkodliwy freon R600a</li>
                        <li>Plastik rozklada sie 500 lat w glebie</li>
                        <li>Elektronika - metale ciezkie w srodowisku</li>
                        <li>Co roku Polacy wyrzucaja miliony AGD</li>
                        <li>Tylko 20% jest prawidlowo utylizowana</li>
                        <li>Naprawa zmniejsza slad weglowy o 98%</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">♻️</div>
                    <h3>Korzysci dla Ciebie i planety</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Oszczedzasz 500-3000 zl</li>
                        <li>Chronisz srodowisko naturalne</li>
                        <li>Nie tracisz czasu na zakupy</li>
                        <li>Znasz swoje urzadzenie</li>
                        <li>Brak klopotu z utylizacja</li>
                        <li>Szybka naprawa tego samego dnia</li>
                        <li>Gwarancja na usluge</li>
                        <li>Oryginalne czesci zamienne</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">💚</div>
                    <h3>Nasza misja - mniej odpadow</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Przedluzamy zycie sprzetu AGD</li>
                        <li>Naprawiamy zamiast wyrzucac</li>
                        <li>Uczciwe ceny bez sciem</li>
                        <li>Jesli nie warto - powiemy wprost</li>
                        <li>Dojazd do klienta - zero transportu</li>
                        <li>Szczecin Stargard Goleniow i okolice</li>
                        <li>Tel: 721 988 949</li>
                        <li>WhatsApp dostepny</li>
                    </ul>
                </div>
            </div>

            <h2>Zanim wyrzucisz - zadzwon do nas!</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">📞</div>
                    <h3>Bezplatna wycena przez telefon</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Opisz problem - ocenimy przez telefon</li>
                        <li>Jesli nieoplacalne - powiemy uczciwie</li>
                        <li>Jesli oplacalne - przyjedziemy tego samego dnia</li>
                        <li>Naprawa w domu - bez transportu</li>
                        <li>Gwarancja na wykonana prace</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
'''

# ============================================================
# СТАТЬЯ 5: Jak przedluzyc zycie pralki
# ============================================================
zycie_pralki_content = '''
    <section class="hero">
        <div class="container">
            <h1>Jak przedluzyc zycie pralki? Porady serwisanta</h1>
            <p>Prosta pielegnacja moze sprawic ze pralka posluzy Ci 15-20 lat!</p>
            <a href="#order" class="cta-button">Zadzwon 721 988 949</a>
        </div>
    </section>

    <section class="services">
        <div class="container">

            <h2>5 rzeczy ktore niszcza pralke - a mozna tego uniknac</h2>
            <div class="services-grid">
                <div class="service-link-card">
                    <div class="service-icon">⚠️</div>
                    <h3>Czego NIE robic</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Nie upychac za duzo rzeczy naraz</li>
                        <li>Nie wkladac rzeczy z monetami w kieszeniach</li>
                        <li>Nie uzywac za duzo proszku</li>
                        <li>Nie zostawiac mokrego prania w bebnie</li>
                        <li>Nie ignorowac pierwszych dziwnych dzwiekow</li>
                        <li>Nie prац bez sprawdzenia filtra</li>
                        <li>Nie blokowac wentylacji z tylu</li>
                        <li>Nie przesuwac pralki na nodze</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">🧹</div>
                    <h3>Co robic regularnie</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Czyscic filtr pompy raz w miesiacu</li>
                        <li>Wycierac gume drzwi po kazdym praniu</li>
                        <li>Zostawiac drzwi uchylone po praniu</li>
                        <li>Plukac szuflada na proszek co tydzien</li>
                        <li>Odkamienianie raz na 3 miesiace</li>
                        <li>Program czyszczenia bebna raz w miesiacu</li>
                        <li>Sprawdzac weze co roku</li>
                        <li>Poziomowac pralke jesli skacze</li>
                    </ul>
                </div>
                <div class="service-link-card">
                    <div class="service-icon">🔧</div>
                    <h3>Kiedy dzwonic do serwisu</h3>
                    <ul style="text-align:left; color:white;">
                        <li>Pralka zaczela glosniej hałasowac</li>
                        <li>Widzisz male przecieki wody</li>
                        <li>Pranie trwa dluzej niz normalnie</li>
                        <li>Ubrania sa mniej czyste niz zwykle</li>
                        <li>Pojawil sie kod bledu</li>
                        <li>Pralka wibruje bardziej niz wczesniej</li>
                        <li>Czujesz dziwny zapach podczas prania</li>
                        <li>Nie czekaj - wczesna naprawa = tanszy koszt!</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
'''

# ============================================================
# ГЕНЕРАЦИЯ ВСЕХ 5 СТАТЕЙ
# ============================================================
articles = [
    {
        "slug": "czy-oplaca-sie-naprawiac-pralke.html",
        "title": "Czy oplaca sie naprawiac pralke? Pralka nie wiruje, nie odprowadza wody | WISA 721 988 949",
        "desc": "Pralka nie wiruje, nie odprowadza wody, klika ale nie kreci? 90% usterek naprawiamy na miejscu. Uczciwa wycena przez telefon. Szczecin i okolice. Tel: 721 988 949",
        "h1": "Czy oplaca sie naprawiac pralke?",
        "content": pralka_content
    },
    {
        "slug": "czy-oplaca-sie-naprawiac-zmywarke.html",
        "title": "Czy oplaca sie naprawiac zmywarke? Smigla nie kreca, nie domywa naczyn | WISA 721 988 949",
        "desc": "Smigla w zmywarce sie nie kreca? Zatkany spryskiwacz? Zmywarka nie domywa gornego kosza? Naprawiamy na miejscu. Szczecin i okolice. Tel: 721 988 949",
        "h1": "Czy oplaca sie naprawiac zmywarke?",
        "content": zmywarka_content
    },
    {
        "slug": "czy-oplaca-sie-naprawiac-lodowke.html",
        "title": "Czy oplaca sie naprawiac lodowke? Nie chlodzi, zamarza, wycieka | WISA 721 988 949",
        "desc": "Lodowka nie chlodzi? Zamrazarka mrozi a lodowka nie? Woda pod lodowka? Naprawiamy na miejscu tego samego dnia. Szczecin i okolice. Tel: 721 988 949",
        "h1": "Czy oplaca sie naprawiac lodowke?",
        "content": lodowka_content
    },
    {
        "slug": "naprawa-agd-a-srodowisko.html",
        "title": "Nie wyrzucaj pralki - naprawiaj! Chron srodowisko | WISA Serwis AGD",
        "desc": "Wyrzucona pralka to 600 kg CO2. Naprawiona tylko 10 kg. Chron srodowisko i zaoszczedz 500-3000 zl. Serwis AGD Szczecin. Tel: 721 988 949",
        "h1": "Nie wyrzucaj - naprawiaj! Chron srodowisko",
        "content": srodowisko_content
    },
    {
        "slug": "jak-przedluzyc-zycie-pralki.html",
        "title": "Jak przedluzyc zycie pralki? Porady serwisanta AGD | WISA 721 988 949",
        "desc": "Praktyczne porady jak dbac o pralke zeby sluzyla 15-20 lat. Co niszczy pralki i jak tego unikac. Serwis AGD Szczecin. Tel: 721 988 949",
        "h1": "Jak przedluzyc zycie pralki?",
        "content": zycie_pralki_content
    },
]

def create_articles():
    print("🚀 Tworze artykuly z realnymi zapytaniami ludzi...\n")

    for article in articles:
        html = get_html(
            article["slug"],
            article["title"],
            article["desc"],
            article["h1"],
            article["content"]
        )

        filepath = Path(article["slug"])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ {article['slug']}")

    print(f"\n🎉 Gotowe! Utworzono {len(articles)} artykulow!")
    print("\n📋 Dodaj linki do index.html w sekcji footer lub nav:")
    for a in articles:
        print(f"   <a href='/{a['slug']}'>{a['h1']}</a>")

if __name__ == "__main__":
    create_articles()