#!/usr/bin/env python3
"""
Показывает, каких пар (техника, бренд) не хватает в tech_facts_db.py —
именно из-за них generate_content_api.py пропускает страницы.

Запуск:
    python find_missing_tech_facts.py
"""

from pathlib import Path
from collections import defaultdict

from tech_facts_db import TECH_FACTS_DB
try:
    from auto_tech_facts_db import AUTO_TECH_FACTS_DB
except ImportError:
    AUTO_TECH_FACTS_DB = {}
try:
    from tech_facts_db_extra import TECH_FACTS_DB_EXTRA
except ImportError:
    TECH_FACTS_DB_EXTRA = {}

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}

APPLIANCE_NAMES = {
    "naprawa-pralek": "pralki",
    "naprawa-lodowek": "lodówki",
    "naprawa-zmywarek": "zmywarki",
    "naprawa-piekarnikow": "piekarniki",
    "naprawa-suszarek": "suszarki",
    "naprawa-pralko-suszarek": "pralko-suszarki",
}


def find_pages(root: Path):
    for appliance_dir in APPLIANCE_NAMES.keys():
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

    # Собираем реально существующие на сайте пары (техника, бренд)
    existing_combos = defaultdict(set)
    for appliance_dir, path in pages:
        brand_slug = path.stem.strip().lower()
        existing_combos[appliance_dir].add(brand_slug)

    print(f"Всего страниц найдено: {len(pages)}\n")

    total_covered = 0
    total_missing = 0
    missing_by_appliance = defaultdict(list)

    for appliance_dir, brands in existing_combos.items():
        for brand_slug in sorted(brands):
            def has_errors(db: dict) -> bool:
                return bool(db.get(brand_slug, {}).get(appliance_dir, {}).get("common_errors"))

            has_data = (
                has_errors(TECH_FACTS_DB)
                or has_errors(AUTO_TECH_FACTS_DB)
                or has_errors(TECH_FACTS_DB_EXTRA)
            )
            if has_data:
                total_covered += 1
            else:
                total_missing += 1
                missing_by_appliance[appliance_dir].append(brand_slug)

    print(f"Пар (бренд+техника), для которых ЕСТЬ данные: {total_covered}")
    print(f"Пар (бренд+техника), для которых НЕТ данных:  {total_missing}\n")

    print("=" * 60)
    print("НЕ ХВАТАЕТ ДАННЫХ ПО СЛЕДУЮЩИМ КОМБИНАЦИЯМ:")
    print("=" * 60)
    for appliance_dir, brands in missing_by_appliance.items():
        print(f"\n{appliance_dir} ({APPLIANCE_NAMES[appliance_dir]}):")
        for brand in brands:
            print(f"  - {brand}")

    print(
        "\nЧтобы покрыть эти страницы — добавьте соответствующие записи "
        "в TECH_FACTS_DB в tech_facts_db.py (хотя бы 1-2 common_errors "
        "на каждую пару), затем запустите generate_content_api.py заново — "
        "новые пары подхватятся автоматически, старые (уже в кэше) трогать не будет."
    )


if __name__ == "__main__":
    main()
