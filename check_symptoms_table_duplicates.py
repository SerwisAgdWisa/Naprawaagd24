#!/usr/bin/env python3
"""
Ищет дублирующиеся строки в <table class="symptoms-table"> между РАЗНЫМИ
брендами внутри одной категории техники — то есть случаи, когда для
одного и того же "Problem" (например "Pralka nie wiruje") у двух разных
брендов дословно совпадает "Przyczyna".

Это не про AI-блок и не про похожесть файлов целиком — это про исходный,
ещё до AI, контент таблицы симптомов, который местами оказался
скопирован под копирку между брендами.

Требует: pip install beautifulsoup4 --break-system-packages

Запуск:
    python check_symptoms_table_duplicates.py
"""

import sys
from collections import defaultdict
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Установите: pip install beautifulsoup4 --break-system-packages")
    sys.exit(1)

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode", "__pycache__"}

APPLIANCE_DIRS = [
    "naprawa-pralek", "naprawa-lodowek", "naprawa-zmywarek",
    "naprawa-piekarnikow", "naprawa-suszarek", "naprawa-pralko-suszarek",
]


def extract_symptom_rows(html: str) -> dict[str, str]:
    """Возвращает {Problem: Przyczyna} из symptoms-table, если есть."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="symptoms-table")
    if table is None:
        return {}

    result = {}
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        problem = cells[0].get_text(strip=True)
        cause = cells[1].get_text(strip=True)
        if problem and cause:
            result[problem] = cause
    return result


def find_pages(root: Path):
    for appliance_dir in APPLIANCE_DIRS:
        base = root / appliance_dir
        if not base.exists():
            continue
        for path in base.glob("*/*.html"):
            if path.stem == "index":
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            yield appliance_dir, path


def main():
    pages = list(find_pages(ROOT_DIR))
    if not pages:
        print("Файлы не найдены. Запустите из корня проекта.")
        sys.exit(1)

    print(f"Сканирую {len(pages)} страниц на наличие symptoms-table...\n")

    # (appliance_dir, city) -> {problem: {cause: [brand, brand, ...]}}
    by_context = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    scanned = 0
    for appliance_dir, path in pages:
        city = path.parent.name
        brand = path.stem

        try:
            html = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        rows = extract_symptom_rows(html)
        if not rows:
            continue
        scanned += 1

        for problem, cause in rows.items():
            by_context[(appliance_dir, city)][problem][cause].append(brand)

    print(f"Страниц с symptoms-table: {scanned}\n")
    print("=" * 70)
    print("НАЙДЕННЫЕ ДУБЛИРУЮЩИЕСЯ ПРИЧИНЫ МЕЖДУ РАЗНЫМИ БРЕНДАМИ")
    print("=" * 70)

    total_duplicate_groups = 0
    affected_pages = set()

    for (appliance_dir, city), problems in sorted(by_context.items()):
        for problem, causes in problems.items():
            for cause, brands in causes.items():
                if len(brands) > 1:
                    total_duplicate_groups += 1
                    print(f"\n[{appliance_dir} / {city}] \"{problem}\"")
                    print(f"  Причина: \"{cause}\"")
                    print(f"  Одинаково у брендов: {', '.join(sorted(brands))}")
                    for b in brands:
                        affected_pages.add(f"{appliance_dir}/{city}/{b}.html")

    print("\n" + "=" * 70)
    print(f"Всего групп дублей: {total_duplicate_groups}")
    print(f"Затронуто уникальных страниц: {len(affected_pages)}")

    if total_duplicate_groups == 0:
        print("\nДублей не найдено — таблицы симптомов уникальны по брендам.")
    else:
        out_file = Path("symptoms_duplicates.txt")
        out_file.write_text("\n".join(sorted(affected_pages)), encoding="utf-8")
        print(f"\nСписок затронутых страниц сохранён в {out_file}")


if __name__ == "__main__":
    main()
