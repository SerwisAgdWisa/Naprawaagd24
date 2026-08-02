#!/usr/bin/env python3
"""
Генерирует НАБОР уникальных блоков контента для каждой страницы
naprawa-{urzadzenie}/{miasto}/{marka}.html:

  1. Вводный абзац (город + техника + бренд, из пула формулировок)
  2. Абзац "почему мы" (разные аргументы на разных страницах)
  3. Блок FAQ (2 вопроса/ответа, специфичных для бренд+техника)
     + JSON-LD FAQPage разметка — реальный SEO-бонус, может дать
       расширенный сниппет в выдаче Google
  4. Локальный блок (районы города + примечание)

Выбор варианта из пула — ДЕТЕРМИНИРОВАННЫЙ (основан на хэше пути файла),
а не случайный при каждом запуске: повторный запуск даст тот же
результат, контент не будет "плавать" от прогона к прогону.

ВАЖНО: без заполнения реальными фактами (CITY_FACTS, APPLIANCE_FACTS,
BRAND_FACTS) это всё ещё комбинаторика шаблонных фраз, а не подлинная
уникальность. Чем больше реальных, проверяемых деталей вы добавите —
тем устойчивее результат к алгоритмам оценки качества контента.

Использование:
    python generate_unique_seo_content.py            # сухой прогон
    python generate_unique_seo_content.py --apply     # запись + .bak
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}
MARKER = "<!-- unique-seo-block-v2 -->"

# ------------------------------------------------------------------
# СЛОВАРИ — ЗАПОЛНИТЕ РЕАЛЬНЫМИ ДАННЫМИ. Ниже только структура
# и примеры, чтобы скрипт можно было сразу тестово запустить.
# ------------------------------------------------------------------

CITY_FACTS = {
    "goleniow": {
        "display_locative": "goleniowie",   # "w goleniowie"
        "display_nominative": "goleniow",
        "districts": ["Centrum", "Osiedle Słoneczne", "Helenów"],
        "facts": [
            "Obsługujemy zarówno starą zabudowę w centrum, jak i nowsze osiedla.",
            "Dojeżdżamy do klientów w goleniowie zwykle w ciągu 60–90 minut.",
        ],
    },
    "nowogard": {
        "display_locative": "Nowogardzie",
        "display_nominative": "Nowogard",
        "districts": ["Centrum", "Osiedle Bema", "Warnkowo"],
        "facts": [
            "Serwisujemy sprzęt w całym Nowogardzie i okolicznych miejscowościach gminy.",
        ],
    },
    "maszewo": {
        "display_locative": "Maszewie",
        "display_nominative": "Maszewo",
        "districts": ["Centrum Maszewa"],
        "facts": ["Dojazd do klientów na terenie całej gminy Maszewo."],
    },
    "szczecin": {
        "display_locative": "Szczecinie",
        "display_nominative": "Szczecin",
        "districts": ["Pogodno", "Niebuszewo", "Prawobrzeże", "Centrum"],
        "facts": ["Obsługujemy wszystkie dzielnice Szczecina."],
    },
    "stargard": {
        "display_locative": "Stargardzie",
        "display_nominative": "Stargard",
        "districts": ["Centrum", "Osiedle Kluczewo", "Pyrzyckie Przedmieście"],
        "facts": ["Serwis dostępny na terenie całego Stargardu i okolic."],
    },
    "police": {
        "display_locative": "Policach",
        "display_nominative": "Police",
        "districts": ["Centrum", "Mścięcino", "Jasienica"],
        "facts": ["Obsługujemy Police oraz sąsiadujące miejscowości."],
    },
    "pyrzyce": {
        "display_locative": "Pyrzycach",
        "display_nominative": "Pyrzyce",
        "districts": ["Centrum Pyrzyc"],
        "facts": ["Dojazd na terenie Pyrzyc i gminy."],
    },
    "gryfino": {
        "display_locative": "Gryfinie",
        "display_nominative": "Gryfino",
        "districts": ["Centrum", "Osiedle Południe"],
        "facts": ["Serwisujemy Gryfino i okoliczne miejscowości."],
    },
}

# Категория техники -> человекочитаемое имя + типовые вопросы FAQ
APPLIANCE_FACTS = {
    "naprawa-pralek": {
        "name": "pralki",
        "faq_pool": [
            ("Ile kosztuje naprawa pralki?",
             "Cena zależy od usterki — po diagnozie na miejscu podajemy dokładny koszt przed naprawą."),
            ("Czy naprawiacie pralki starszych roczników?",
             "Tak, naprawiamy pralki niezależnie od wieku, o ile dostępne są części zamienne."),
            ("Jak szybko możecie przyjechać?",
             "Zwykle w ciągu 24–48 godzin od zgłoszenia, w pilnych przypadkach staramy się szybciej."),
        ],
    },
    "naprawa-lodowek": {
        "name": "lodówki",
        "faq_pool": [
            ("Lodówka nie chłodzi — co robić?",
             "Sprawdź czy nie jest zapchany parownik lub uszczelka drzwi nie jest uszkodzona; jeśli problem nie ustąpi, zgłoś się do nas."),
            ("Czy naprawa lodówki wymaga wymiany całej sprężarki?",
             "Nie zawsze — w wielu przypadkach wystarczy naprawa układu elektroniki lub czujnika."),
        ],
    },
    "naprawa-zmywarek": {
        "name": "zmywarki",
        "faq_pool": [
            ("Zmywarka nie myje dobrze naczyń — dlaczego?",
             "Najczęstsza przyczyna to zapchane ramiona spryskujące lub filtr — sprawdzimy to podczas wizyty."),
            ("Czy warto naprawiać starszą zmywarkę?",
             "Zależy od kosztu naprawy względem wartości sprzętu — doradzimy to podczas diagnozy."),
        ],
    },
    "naprawa-piekarnikow": {
        "name": "piekarniki",
        "faq_pool": [
            ("Piekarnik nie grzeje równomiernie — co to może być?",
             "Zwykle to uszkodzona grzałka górna lub dolna, ewentualnie termoobieg."),
        ],
    },
    "naprawa-suszarek": {
        "name": "suszarki",
        "faq_pool": [
            ("Suszarka nie suszy do końca — jaka to usterka?",
             "Najczęściej zapchany filtr, skraplacz lub uszkodzony czujnik wilgotności."),
        ],
    },
    "naprawa-pralko-suszarek": {
        "name": "pralko-suszarki",
        "faq_pool": [
            ("Pralko-suszarka pierze, ale nie suszy — co robić?",
             "Zwykle to osobny obwód suszenia — sprawdzimy grzałkę i czujnik wilgotności niezależnie od funkcji prania."),
        ],
    },
}

BRAND_FACTS = {
    "bosch": ["błędy E1/E2/E3", "problem z chłodzeniem lub grzaniem"],
    "samsung": ["kody błędów 1E/5E/22E", "brak chłodzenia lub głośna praca"],
    "whirlpool": ["kod błędu AL/E1", "problem z funkcją 6th Sense"],
    "siemens": ["błędy E1/E2", "problem z modułem HyperFresh / iSensoric"],
    # Добавьте остальные бренды по аналогии
}
BRAND_FACTS_FALLBACK = ["typowe usterki elektroniki", "problemy mechaniczne"]

INTRO_TEMPLATES = [
    "Serwisujemy {brand} ({device}) w {city_loc} — {city_fact}",
    "Nasz zespół naprawia {device} marki {brand} na terenie {city_nom} i okolic. {city_fact}",
    "Potrzebujesz naprawy {device} {brand} w {city_loc}? {city_fact}",
]

WHY_US_TEMPLATES = [
    "Diagnoza na miejscu, wycena przed naprawą, dojazd do klienta tego samego lub następnego dnia.",
    "Pracujemy z gwarancją na wykonaną usługę i oryginalnymi lub równoważnymi częściami zamiennymi.",
    "Serwisujemy sprzęt od lat — znamy typowe usterki: {brand_issue}.",
]

# ------------------------------------------------------------------


def normalize_city_slug(folder_name: str) -> str:
    s = folder_name.strip().lower()
    repl = {"ó": "o", "ą": "a", "ę": "e", "ł": "l", "ż": "z", "ź": "z", "ś": "s", "ć": "c", "ń": "n"}
    for a, b in repl.items():
        s = s.replace(a, b)
    return s


def deterministic_choice(pool, *seed_parts):
    """Выбирает элемент пула детерминированно (по хэшу), не рандомно
    при каждом запуске — так контент не 'плавает' между прогонами."""
    if not pool:
        return None
    key = "|".join(seed_parts).encode("utf-8")
    h = int(hashlib.sha256(key).hexdigest(), 16)
    return pool[h % len(pool)]


def find_pages(root: Path):
    for appliance_dir in APPLIANCE_FACTS.keys():
        base = root / appliance_dir
        if not base.exists():
            continue
        for path in base.glob("*/*.html"):
            if path.stem == "index":
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            yield appliance_dir, path


def build_block(appliance_dir: str, path: Path) -> str | None:
    appliance = APPLIANCE_FACTS[appliance_dir]
    city_slug = normalize_city_slug(path.parent.name)
    brand_slug = path.stem.strip().lower()

    city = CITY_FACTS.get(city_slug)
    if city is None:
        return None

    brand_display = brand_slug.replace("-", " ").title()
    brand_issues = BRAND_FACTS.get(brand_slug, BRAND_FACTS_FALLBACK)
    brand_issue_str = " i ".join(brand_issues)

    seed_key = f"{appliance_dir}/{path.parent.name}/{path.stem}"

    intro_tpl = deterministic_choice(INTRO_TEMPLATES, seed_key, "intro")
    why_tpl = deterministic_choice(WHY_US_TEMPLATES, seed_key, "why")
    city_fact = deterministic_choice(city["facts"], seed_key, "cityfact")

    intro = intro_tpl.format(
        brand=brand_display,
        device=appliance["name"],
        city_loc=city["display_locative"],
        city_nom=city["display_nominative"],
        city_fact=city_fact,
    )
    why = why_tpl.format(brand_issue=brand_issue_str)

    districts_line = ", ".join(city["districts"])

    faq_pool = appliance["faq_pool"]
    faq_items = []
    if faq_pool:
        # берём до 2 разных вопросов детерминированно
        idx1 = int(hashlib.sha256(f"{seed_key}-faq1".encode()).hexdigest(), 16) % len(faq_pool)
        faq_items.append(faq_pool[idx1])
        if len(faq_pool) > 1:
            idx2 = idx1
            while idx2 == idx1:
                idx2 = int(hashlib.sha256(f"{seed_key}-faq2".encode()).hexdigest(), 16) % len(faq_pool)
            faq_items.append(faq_pool[idx2])

    faq_html_parts = []
    faq_jsonld_entities = []
    for q, a in faq_items:
        faq_html_parts.append(f"    <div class='faq-item'><p><strong>{q}</strong></p><p>{a}</p></div>")
        faq_jsonld_entities.append(
            "    {\n"
            '      "@type": "Question",\n'
            f'      "name": {q!r},\n'
            '      "acceptedAnswer": {\n'
            '        "@type": "Answer",\n'
            f'        "text": {a!r}\n'
            "      }\n"
            "    }"
        )

    faq_html = "\n".join(faq_html_parts)
    faq_jsonld = ",\n".join(faq_jsonld_entities)

    block = f"""{MARKER}
<section class="unique-seo-content">
  <p>{intro}</p>
  <p>{why}</p>
  <p>Obsługujemy dzielnice: {districts_line}.</p>
  <div class="faq-block">
{faq_html}
  </div>
</section>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_jsonld}
  ]
}}
</script>
"""
    return block


def insert_before_footer(content: str, block: str) -> str | None:
    if MARKER in content:
        return None
    idx = content.rfind("</footer>")
    if idx == -1:
        idx = content.rfind("</body>")
        if idx == -1:
            return None
    footer_start = content.rfind("<footer", 0, idx)
    insert_at = footer_start if footer_start != -1 else idx
    return content[:insert_at] + block + "\n" + content[insert_at:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root)
    pages = list(find_pages(root))

    if not pages:
        print("Файлы не найдены. Запустите из корня проекта (там, где папки naprawa-*).")
        sys.exit(1)

    changed = skipped_no_city = skipped_done = 0

    for appliance_dir, path in pages:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"[ПРОПУЩЕН, не UTF-8] {path}")
            continue

        if MARKER in content:
            skipped_done += 1
            continue

        block = build_block(appliance_dir, path)
        if block is None:
            skipped_no_city += 1
            print(f"[НЕТ ДАННЫХ О ГОРОДЕ] {path}")
            continue

        new_content = insert_before_footer(content, block)
        if new_content is None:
            continue

        changed += 1
        print(f"[{'ЗАПИСАН' if args.apply else 'БУДЕТ ИЗМЕНЁН'}] {path}")

        if args.apply:
            path.with_suffix(path.suffix + ".bak").write_text(content, encoding="utf-8")
            path.write_text(new_content, encoding="utf-8")

    print("\n--- Итог ---")
    print(f"Всего страниц:                {len(pages)}")
    print(f"Изменено/будет изменено:      {changed}")
    print(f"Пропущено (уже сделано):      {skipped_done}")
    print(f"Пропущено (нет данных город): {skipped_no_city}")

    if not args.apply and changed > 0:
        print("\nСухой прогон. Проверьте и запустите с --apply.")


if __name__ == "__main__":
    main()
