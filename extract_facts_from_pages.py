#!/usr/bin/env python3
"""
Вместо того чтобы вручную переписывать факты (коды ошибок, причины) в
tech_facts_db.py — этот скрипт САМ вытаскивает их из уже существующих
на страницах таблиц (class="symptoms-table") и строит базу автоматически.

Как работает:
  1. Проходит по всем naprawa-*/{miasto}/{marka}.html
  2. Ищет <table class="symptoms-table"> с колонками Problem/Przyczyna
  3. Группирует найденные факты по (категория техники, бренд) —
     если один и тот же бренд встречается в нескольких городах с
     одинаковой таблицей, берёт её один раз (не дублирует)
  4. Сохраняет результат в auto_tech_facts_db.py — файл с таким же
     форматом TECH_FACTS_DB, как вы заполняли вручную

Дальше generate_content_api.py можно поправить, чтобы он сначала
смотрел в ручной tech_facts_db.py, а если там пусто — брал данные
из auto_tech_facts_db.py (см. инструкцию в конце вывода).

Требует: pip install beautifulsoup4 --break-system-packages

Запуск:
    python extract_facts_from_pages.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Установите: pip install beautifulsoup4 --break-system-packages")
    sys.exit(1)

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}
OUTPUT_FILE = Path("auto_tech_facts_db.py")

APPLIANCE_DIRS = [
    "naprawa-pralek",
    "naprawa-lodowek",
    "naprawa-zmywarek",
    "naprawa-piekarnikow",
    "naprawa-suszarek",
    "naprawa-pralko-suszarek",
]


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


def extract_symptoms_table(html: str) -> list[dict]:
    """
    Ищет <table class="symptoms-table"> с колонками Problem | Przyczyna
    и возвращает список {"code": ..., "cause": ..., "part": "", "price_range_pln": ""}
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="symptoms-table")
    if table is None:
        return []

    rows = table.find_all("tr")
    results = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue  # это заголовок (th) или пустая строка
        problem = cells[0].get_text(strip=True)
        cause = cells[1].get_text(strip=True)
        if problem and cause:
            results.append({
                "code": problem,       # используем "Проблема" вместо кода ошибки
                "cause": cause,
                "part": "",           # на странице этого может не быть — оставляем пусто
                "price_range_pln": "",
            })
    return results


def main():
    pages = list(find_pages(ROOT_DIR))
    if not pages:
        print("Файлы не найдены. Запустите из корня проекта.")
        sys.exit(1)

    print(f"Сканирую {len(pages)} страниц на наличие symptoms-table...\n")

    # (appliance_dir, brand_slug) -> list of facts (берём первую найденную непустую)
    facts_db = defaultdict(dict)
    found_count = 0
    empty_count = 0

    for appliance_dir, path in pages:
        brand_slug = path.stem.strip().lower()

        try:
            html = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        facts = extract_symptoms_table(html)
        if not facts:
            empty_count += 1
            continue

        # Если для этого бренда+техники уже есть факты (из другого города) —
        # не перезаписываем, считаем что достаточно одного набора
        if brand_slug not in facts_db[appliance_dir]:
            facts_db[appliance_dir][brand_slug] = facts
            found_count += 1
            print(f"[НАЙДЕНО] {appliance_dir}/{brand_slug}: {len(facts)} симптомов (из {path})")

    print(f"\nВсего уникальных пар (техника+бренд) с фактами: {found_count}")
    print(f"Страниц без таблицы symptoms-table: {empty_count}")

    # Пишем результат в формате, совместимом с tech_facts_db.py
    lines = [
        '"""',
        "Автоматически извлечённая база фактов из уже существующих на страницах",
        "таблиц symptoms-table. Сгенерировано extract_facts_from_pages.py —",
        "не редактируйте руками, перезапустите скрипт при изменении HTML.",
        '"""',
        "",
        "AUTO_TECH_FACTS_DB = {",
    ]
    for appliance_dir, brands in facts_db.items():
        pass  # структура собирается ниже по бренду, а не по технике — перегруппируем

    # Перегруппировка: бренд -> техника -> common_errors (как в ручном tech_facts_db.py)
    by_brand = defaultdict(dict)
    for appliance_dir, brands in facts_db.items():
        for brand_slug, facts in brands.items():
            by_brand[brand_slug][appliance_dir] = {"common_errors": facts}

    import json
    lines = [
        '"""',
        "Автоматически извлечённая база фактов из уже существующих на страницах",
        "таблиц symptoms-table. Сгенерировано extract_facts_from_pages.py.",
        "Формат идентичен ручному TECH_FACTS_DB из tech_facts_db.py.",
        '"""',
        "",
        f"AUTO_TECH_FACTS_DB = {json.dumps(by_brand, ensure_ascii=False, indent=4)}",
        "",
    ]
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nСохранено в {OUTPUT_FILE}")
    print(
        "\nДальше в generate_content_api.py поправьте импорт и логику поиска фактов:\n"
        "  from tech_facts_db import TECH_FACTS_DB\n"
        "  from auto_tech_facts_db import AUTO_TECH_FACTS_DB\n"
        "  ...\n"
        "  brand_tech = (TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)\n"
        "                or AUTO_TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir))\n"
        "\n"
        "Так ручные факты (если есть) будут в приоритете, а для остальных "
        "брендов подтянутся автоматически извлечённые с сайта."
    )


if __name__ == "__main__":
    main()
