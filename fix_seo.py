import os
import re
import json

DOMAIN = "https://naprawaagd24.pl"
PHONE = "+48721988949"

SERVICES = {
    "naprawa-lodowek": ("Naprawa Lodówek", "Lodówek"),
    "naprawa-piekarnikow": ("Naprawa Piekarników", "Piekarników"),
    "naprawa-pralek": ("Naprawa Pralek", "Pralek"),
    "naprawa-pralko-suszarek": ("Naprawa Pralko-Suszarek", "Pralko-Suszarek"),
    "naprawa-suszarek": ("Naprawa Suszarek", "Suszarek"),
    "naprawa-zmywarek": ("Naprawa Zmywarek", "Zmywarek"),
}

CITIES = {
    "goleniow": ("goleniow", "goleniowie", "72-100"),
    "goleniow": ("goleniow", "goleniowie", "72-100"),
    "maszewo": ("Maszewo", "Maszewie", "72-130"),
    "nowogard": ("Nowogard", "Nowogardzie", "72-200"),
    "police": ("Police", "Policach", "72-010"),
    "pyrzyce": ("Pyrzyce", "Pyrzycach", "74-200"),
    "stargard": ("Stargard", "Stargardzie", "73-110"),
    "szczecin": ("Szczecin", "Szczecinie", "70-001"),
}

BRANDS = {
    "aeg": "AEG", "amica": "Amica", "ariston": "Ariston", "beko": "Beko",
    "bosch": "Bosch", "candy": "Candy", "electrolux": "Electrolux",
    "elektrolux": "Electrolux", "gorenje": "Gorenje", "gorenie": "Gorenje",
    "haier": "Haier", "hisense": "Hisense", "hotpoint-ariston": "Hotpoint-Ariston",
    "indesit": "Indesit", "lg": "LG", "liebherr": "Liebherr", "miele": "Miele",
    "neff": "Neff", "samsung": "Samsung", "sharp": "Sharp", "siemens": "Siemens",
    "whirlpool": "Whirlpool", "zanussi": "Zanussi",
}

def build_json_ld(service_slug, city_slug, brand_file):
    service_name, service_gen = SERVICES[service_slug]
    city_nom, city_loc, zip_code = CITIES[city_slug]
    
    is_index = brand_file == "index"
    brand_name = BRANDS.get(brand_file, brand_file.capitalize())

    # Формируем корректный URL страницы
    if is_index:
        page_url = f"{DOMAIN}/{service_slug}/{city_slug}/"
        page_name = f"{service_name} {city_nom}"
    else:
        page_url = f"{DOMAIN}/{service_slug}/{city_slug}/{brand_file}.html"
        page_name = f"{service_name} {brand_name} {city_nom}"

    # 1. BreadcrumbList
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona Główna", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": service_name, "item": f"{DOMAIN}/{service_slug}/"},
            {"@type": "ListItem", "position": 3, "name": city_nom, "item": f"{DOMAIN}/{service_slug}/{city_slug}/"}
        ]
    }
    
    if not is_index:
        breadcrumbs["itemListElement"].append({
            "@type": "ListItem",
            "position": 4,
            "name": brand_name,
            "item": page_url
        })

    # 2. LocalBusiness (без заглушек вроде "Podaj ulice")
    local_business = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": page_name,
        "image": f"{DOMAIN}/logo.jpg",
        "url": page_url,
        "telephone": PHONE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city_nom,
            "addressRegion": "Zachodniopomorskie",
            "postalCode": zip_code,
            "addressCountry": "PL"
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "08:00",
                "closes": "21:00"
            }
        ]
    }

    bc_script = f'<script type="application/ld+json">\n{json.dumps(breadcrumbs, ensure_ascii=False, indent=2)}\n</script>'
    lb_script = f'<script type="application/ld+json">\n{json.dumps(local_business, ensure_ascii=False, indent=2)}\n</script>'
    
    return f"{bc_script}\n{lb_script}"

def fix_file(file_path):
    parts = file_path.replace("\\", "/").split("/")
    if len(parts) < 3:
        return

    service_slug, city_slug = parts[-3], parts[-2].lower()
    brand_file = parts[-1].replace(".html", "").lower()

    if service_slug not in SERVICES or city_slug not in CITIES:
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Удаляем старые теги <script type="application/ld+json">...</script>
    content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)

    # Генерируем новый валидный JSON-LD
    new_json_ld = build_json_ld(service_slug, city_slug, brand_file)

    # Вставляем новый JSON-LD прямо перед </head>
    content = content.replace("</head>", f"{new_json_ld}\n</head>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] JSON-LD обновлен: {file_path}")

# Запуск
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            fix_file(os.path.join(root, file))