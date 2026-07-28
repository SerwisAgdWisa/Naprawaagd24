#!/usr/bin/env python3
"""
Добавляет РЕАЛЬНО уникальный абзац контента на каждую страницу вида
naprawa-{urzadzenie}/{miasto}/{marka}.html — чтобы страницы для разных
городов не были почти идентичными шаблонами (что Google расценивает
как near-duplicate / thin content).

ВАЖНО: это НЕ synonym-spinning. Уникальность должна быть настоящей —
конкретные районы города, реальная локальная специфика. Ниже в
CITY_CONTENT — только ЗАГОТОВКИ с примерами структуры. Замените текст
на реальные факты про ваши города, иначе смысла в скрипте немного
(Google достаточно легко отличает реальный уникальный контент от
шаблона с переставленными словами).

Использование:
    1. Заполните CITY_CONTENT и BRAND_ISSUE_VARIANTS реальными данными
    2. Сухой прогон (ничего не меняет, только показывает список):
         python add_unique_content.py
    3. Реальная запись (с бэкапом .bak каждого файла):
         python add_unique_content.py --apply
"""

import argparse
import random
import re
import sys
from pathlib import Path

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}

# Маркер, по которому скрипт узнаёт "тут уже вставлен уникальный блок"
# и не будет дублировать при повторном запуске.
MARKER = "<!-- unique-local-block -->"

# ------------------------------------------------------------------
# 1. РЕАЛЬНАЯ локальная специфика по каждому городу.
#    ЗАПОЛНИТЕ реальными районами/фактами — это даёт настоящую
#    уникальность, а не просто смену названия города в шаблоне.
#    Ключ — нормализованный слаг папки города (без диакритики, lower).
# ------------------------------------------------------------------
CITY_CONTENT = {
    "goleniow": {
        "display": "Goleniowie",
        "districts": ["Centrum", "Osiedle Słoneczne", "Helenów"],
        "note": (
            "Obsługujemy zarówno starą zabudowę w centrum Goleniowa, "
            "jak i nowsze osiedla — dojazd zwykle w ciągu 60–90 minut."
        ),
    },
    "nowogard": {
        "display": "Nowogardzie",
        "districts": ["Centrum", "Osiedle Bema", "Warnkowo"],
        "note": (
            "Serwisujemy sprzęt zarówno w centrum Nowogardu, jak i w "
            "okolicznych miejscowościach gminy."
        ),
    },
    "maszewo": {
        "display": "Maszewie",
        "districts": ["Centrum Maszewa"],
        "note": "Dojazd do klientów na terenie całej gminy Maszewo.",
    },
    "szczecin": {
        "display": "Szczecinie",
        "districts": ["Pogodno", "Niebuszewo", "Prawobrzeże", "Centrum"],
        "note": (
            "Obsługujemy wszystkie dzielnice Szczecina — od Prawobrzeża "
            "po Pogodno."
        ),
    },
    "stargard": {
        "display": "Stargardzie",
        "districts": ["Centrum", "Osiedle Kluczewo", "Pyrzyckie Przedmieście"],
        "note": "Serwis dostępny na terenie całego Stargardu i okolic.",
    },
    "police": {
        "display": "Policach",
        "districts": ["Centrum", "Mścięcino", "Jasienica"],
        "note": "Obsługujemy Police oraz sąsiadujące miejscowości.",
    },
    "pyrzyce": {
        "display": "Pyrzycach",
        "districts": ["Centrum Pyrzyc"],
        "note": "Dojazd na terenie Pyrzyc i gminy.",
    },
    "gryfino": {
        "display": "Gryfinie",
        "districts": ["Centrum", "Osiedle Południe"],
        "note": "Serwisujemy Gryfino i okoliczne miejscowości.",
    },
}

# ------------------------------------------------------------------
# 2. Варианты формулировок по бренду — чтобы один и тот же бренд
#    в разных городах не был описан слово-в-слово одинаково.
#    Добавьте реальные типичные неисправности, если знаете больше.
# ------------------------------------------------------------------
BRAND_ISSUE_VARIANTS = {
    "bosch": [
        "Najczęściej zgłaszane usterki to błędy E1/E2/E3 oraz problem z chłodzeniem.",
        "Klienci najczęściej zgłaszają się z błędami serii E oraz brakiem chłodzenia.",
    ],
    "samsung": [
        "Typowe zgłoszenia to kody błędów 1E/5E/22E oraz brak chłodzenia.",
        "Najczęstsze problemy: błędy 1E, 5E, 22E i niewystarczające chłodzenie.",
    ],
    # Добавьте остальные бренды по аналогии — иначе для них
    # будет использован общий (менее специфичный) вариант ниже.
}

GENERIC_ISSUE_FALLBACK = [
    "Naprawiamy zarówno drobne usterki, jak i poważniejsze awarie — z dojazdem do klienta.",
    "Diagnozujemy usterkę na miejscu i w większości przypadków naprawiamy tego samego dnia.",
]


def normalize_city_slug(folder_name: str) -> str:
    s = folder_name.strip().lower()
    replacements = {"ó": "o", "ą": "a", "ę": "e", "ł": "l", "ż": "z", "ź": "z", "ś": "s", "ć": "c", "ń": "n"}
    for a, b in replacements.items():
        s = s.replace(a, b)
    return s


def find_pages(root: Path):
    for path in root.glob("naprawa-*/*/*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.stem == "index":
            continue  # категорийные страницы города пропускаем — там своя логика
        yield path


def build_unique_block(city_slug: str, brand_slug: str) -> str | None:
    city = CITY_CONTENT.get(city_slug)
    if city is None:
        return None  # нет данных по городу — пропускаем, ничего не портим

    issue_variants = BRAND_ISSUE_VARIANTS.get(brand_slug, GENERIC_ISSUE_FALLBACK)
    issue_line = random.choice(issue_variants)

    districts_line = ", ".join(city["districts"])

    block = (
        f'{MARKER}\n'
        f'<section class="local-info">\n'
        f'  <p>Obsługujemy klientów w {city["display"]} w dzielnicach: '
        f'{districts_line}. {city["note"]}</p>\n'
        f'  <p>{issue_line}</p>\n'
        f'</section>\n'
    )
    return block


def insert_before_footer(content: str, block: str) -> str | None:
    if MARKER in content:
        return None  # уже вставлено ранее

    idx = content.rfind("</footer>")
    if idx == -1:
        # нет футера — пробуем вставить перед </body>
        idx = content.rfind("</body>")
        if idx == -1:
            return None

    # ищем начало тега <footer ...> перед этим индексом, чтобы вставить блок ПЕРЕД футером
    footer_start = content.rfind("<footer", 0, idx)
    insert_at = footer_start if footer_start != -1 else idx

    line_start = content.rfind("\n", 0, insert_at) + 1
    indent = re.match(r"[ \t]*", content[line_start:insert_at]).group(0)

    indented_block = "\n".join(indent + line if line else line for line in block.splitlines())
    new_content = content[:insert_at] + indented_block + "\n\n" + content[insert_at:]
    return new_content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Реально записать изменения")
    parser.add_argument("--root", default=".", help="Корневая папка проекта")
    args = parser.parse_args()

    root = Path(args.root)
    pages = list(find_pages(root))

    if not pages:
        print("Не найдено файлов naprawa-*/*/*.html. Запустите из корня проекта.")
        sys.exit(1)

    changed = 0
    skipped_no_city_data = 0
    skipped_already_done = 0

    for path in pages:
        city_slug = normalize_city_slug(path.parent.name)
        brand_slug = path.stem.strip().lower()

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"[ПРОПУЩЕН, не UTF-8] {path}")
            continue

        if MARKER in content:
            skipped_already_done += 1
            continue

        block = build_unique_block(city_slug, brand_slug)
        if block is None:
            skipped_no_city_data += 1
            print(f"[НЕТ ДАННЫХ ПО ГОРОДУ '{city_slug}'] {path} — добавьте в CITY_CONTENT")
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
    print(f"Всего страниц найдено:              {len(pages)}")
    print(f"Изменено/будет изменено:            {changed}")
    print(f"Пропущено (уже есть блок):          {skipped_already_done}")
    print(f"Пропущено (нет данных о городе):    {skipped_no_city_data}")

    if not args.apply and changed > 0:
        print(
            "\nЭто сухой прогон. Проверьте список, затем запустите:\n"
            "    python add_unique_content.py --apply"
        )


if __name__ == "__main__":
    main()
