#!/usr/bin/env python3
"""
Исправляет дублирующиеся ячейки "Przyczyna" в symptoms-table — там, где
у нескольких брендов в одном городе для одного и того же "Problem"
дословно совпадает причина.

Логика:
  1. Проходит по всем страницам, собирает {(appliance, city, problem): {cause: [brands]}}
  2. Там, где cause совпадает у 2+ брендов — оставляет причину у ПЕРВОГО
     (по алфавиту) бренда как есть, а для остальных генерирует новую,
     отличную причину из расширенного пула вариантов (детерминированно
     по бренду — стабильно между запусками).
  3. Заменяет текст именно в этой ячейке <td> в HTML-файле, остальное
     не трогает.

ВАЖНО: делает .bak копию каждого изменяемого файла.

Требует: pip install beautifulsoup4 --break-system-packages

Запуск:
    python fix_symptoms_table_duplicates.py            # сухой прогон
    python fix_symptoms_table_duplicates.py --apply     # реальная запись
"""

import argparse
import hashlib
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

# Расширенный пул причин по каждому известному симптому пралек.
# Если встретите незнакомый Problem не из этого списка — скрипт его
# просто пропустит (не станет придумывать причину "из воздуха").
EXTRA_CAUSE_POOL = {
    "Pralka nie wiruje": [
        "Zatkany filtr pompy odpływowej - blokada wirnika",
        "Przerwany pasek napędowy bębna",
        "Uszkodzony kondensator rozruchowy silnika",
        "Zużyte szczotki silnika - brak styku",
        "Błąd czujnika prędkości obrotowej (tachometr)",
        "Uszkodzony amortyzator bębna - nadmierne wibracje blokują wirowanie",
    ],
    "Pralka nie grzeje wody": [
        "Osad kamienia na grzałce blokujący przewodzenie ciepła",
        "Uszkodzony czujnik temperatury (NTC)",
        "Wadliwy przekaźnik grzania na module sterującym",
        "Przerwany obwód grzejny grzałki",
        "Uszkodzony termostat bezpieczeństwa",
    ],
    "Pralka nie pobiera wody": [
        "Uszkodzony zawór elektromagnetyczny wlewu wody",
        "Zapchany filtr siatkowy na wężu dopływowym",
        "Awaria presostatu (czujnika poziomu wody)",
        "Uszkodzona elektronika sterująca poborem wody",
    ],
    "Pralka hałasuje i stuka": [
        "Obce ciało (np. moneta, guzik) w bębnie lub pompie",
        "Poluzowane przeciwwagi bębna",
        "Zużyty łożysko bębna wymagające wymiany",
        "Uszkodzone sprężyny zawieszenia bębna",
    ],
    "Woda zostaje w pralce": [
        "Zagięty lub zablokowany wąż odpływowy",
        "Uszkodzony elektrozawór odpływu",
        "Zablokowany presostat sygnalizujący pełny bęben",
        "Awaria modułu sterującego cyklem odpompowania",
    ],
    "Pralka wywala bezpieczniki": [
        "Uszkodzenie izolacji przewodów zasilających",
        "Zwarcie w grzałce grzewczej",
        "Uszkodzony filtr przeciwzakłóceniowy (EMI)",
        "Wilgoć w obudowie silnika powodująca upływność",
    ],
}


def normalize_city_slug(folder_name: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFD", folder_name.strip().lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


def deterministic_choice(pool: list[str], *seed_parts: str) -> str:
    key = "|".join(seed_parts).encode("utf-8")
    h = int(hashlib.sha256(key).hexdigest(), 16)
    return pool[h % len(pool)]


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


def extract_symptom_rows(soup: BeautifulSoup) -> dict[str, str]:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    pages = list(find_pages(ROOT_DIR))
    if not pages:
        print("Файлы не найдены. Запустите из корня проекта.")
        sys.exit(1)

    # Шаг 1: собрать все причины по (appliance, city, problem)
    context_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    page_rows_cache = {}

    for appliance_dir, path in pages:
        try:
            html = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        soup = BeautifulSoup(html, "html.parser")
        rows = extract_symptom_rows(soup)
        if not rows:
            continue
        city = normalize_city_slug(path.parent.name)
        brand = path.stem
        page_rows_cache[path] = (appliance_dir, city, brand, rows)
        for problem, cause in rows.items():
            context_data[(appliance_dir, city)][problem][cause].append((brand, path))

    # Шаг 2: определить, каким страницам/ячейкам нужна замена
    # (все, кроме первого по алфавиту бренда в каждой дублирующейся группе)
    replacements_needed = defaultdict(dict)  # path -> {problem: new_cause}

    for (appliance_dir, city), problems in context_data.items():
        for problem, causes in problems.items():
            for cause, brand_paths in causes.items():
                if len(brand_paths) <= 1:
                    continue
                brand_paths_sorted = sorted(brand_paths)
                # первый оставляем как есть, остальным меняем причину
                for brand, path in brand_paths_sorted[1:]:
                    pool = EXTRA_CAUSE_POOL.get(problem)
                    if not pool:
                        continue  # незнакомый симптом - не трогаем
                    new_cause = deterministic_choice(pool, appliance_dir, city, brand, problem)
                    replacements_needed[path][problem] = new_cause

    print(f"Страниц, требующих замены хотя бы одной ячейки: {len(replacements_needed)}\n")

    changed = 0
    for path, problem_map in replacements_needed.items():
        html = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="symptoms-table")
        if table is None:
            continue

        page_changed = False
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            problem_text = cells[0].get_text(strip=True)
            if problem_text in problem_map:
                old_cause = cells[1].get_text(strip=True)
                new_cause = problem_map[problem_text]
                print(f"[{path}] \"{problem_text}\": \"{old_cause}\" -> \"{new_cause}\"")
                cells[1].string = new_cause
                page_changed = True

        if page_changed:
            changed += 1
            if args.apply:
                path.with_suffix(path.suffix + ".bak").write_text(html, encoding="utf-8")
                path.write_text(str(soup), encoding="utf-8")

    print(f"\n{'Изменено' if args.apply else 'Будет изменено'} страниц: {changed}")
    if not args.apply:
        print("Это сухой прогон. Запустите с --apply, чтобы записать изменения.")


if __name__ == "__main__":
    main()
