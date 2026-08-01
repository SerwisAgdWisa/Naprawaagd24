#!/usr/bin/env python3
"""
Проверяет ВСЕ страницы вида naprawa-{urzadzenie}/{miasto}/{marka}.html
на соответствие: указанный в пути город и бренд должны встречаться
в <title> / <h1> самой страницы.

Находит не только точные дубли (как duplicate_report.txt), но и любые
случаи, где контент "поехал" — например, город обрезан, бренд частично
заменён, или страница вообще пустая/битая.

Запуск:
    python check_content_consistency.py

Результат: подробный отчёт в консоль + файл mismatch_report.txt
"""

import re
from pathlib import Path
from html.parser import HTMLParser

ROOT_DIR = Path(".")

# Слаги города -> как они должны выглядеть в тексте (можно расширять)
CITY_NAMES = {
    "goleniów": ["Goleniów", "Goleniówie", "Goleniówa"],
    "Goleniów": ["Goleniów", "Goleniówie", "Goleniówa"],
    "nowogard": ["Nowogard", "Nowogardzie", "Nowogardu"],
    "maszewo": ["Maszewo", "Maszewie"],
    "szczecin": ["Szczecin", "Szczecinie", "Szczecina"],
    "stargard": ["Stargard", "Stargardzie", "Stargardu"],
    "police": ["Police", "Policach"],
    "pyrzyce": ["Pyrzyce", "Pyrzycach"],
    "gryfino": ["Gryfino", "Gryfinie"],
}

# Слаги бренда -> отображаемое имя (расширяйте по мере надобности)
BRAND_NAMES = {
    "aeg": "AEG",
    "amica": "Amica",
    "beko": "Beko",
    "bosch": "Bosch",
    "candy": "Candy",
    "electrolux": "Electrolux",
    "gorenje": "Gorenje",
    "haier": "Haier",
    "hisense": "Hisense",
    "hotpoint-ariston": "Hotpoint-Ariston",
    "indesit": "Indesit",
    "lg": "LG",
    "liebherr": "Liebherr",
    "miele": "Miele",
    "samsung": "Samsung",
    "sharp": "Sharp",
    "siemens": "Siemens",
    "whirlpool": "Whirlpool",
    "zanussi": "Zanussi",
}


class TitleH1Extractor(HTMLParser):
    """Извлекает содержимое <title> и первого <h1>."""

    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.title = ""
        self.h1 = ""
        self._h1_done = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "h1" and not self._h1_done:
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            self._h1_done = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h1:
            self.h1 += data


def find_pages(root: Path):
    """
    Находит страницы вида naprawa-*/{miasto}/{marka}.html
    Игнорирует index.html внутри папки города (это страница
    без конкретного бренда — категория "город").
    """
    for path in root.glob("naprawa-*/*/*.html"):
        yield path


def slugify_folder(name: str) -> str:
    return name.strip().lower()


def check_file(path: Path):
    city_slug = slugify_folder(path.parent.name)
    brand_slug = slugify_folder(path.stem)  # имя файла без .html

    expected_city_forms = CITY_NAMES.get(city_slug)
    expected_brand = BRAND_NAMES.get(brand_slug)

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"path": path, "error": "Не UTF-8 / не удалось прочитать"}

    parser = TitleH1Extractor()
    try:
        parser.feed(content)
    except Exception as e:
        return {"path": path, "error": f"Ошибка парсинга HTML: {e}"}

    combined = f"{parser.title} {parser.h1}"

    issues = []

    if path.stem != "index":
        if expected_city_forms is None:
            issues.append(f"Неизвестный слаг города '{city_slug}' — добавьте в CITY_NAMES")
        elif not any(form in combined for form in expected_city_forms):
            issues.append(
                f"Город '{city_slug}' НЕ найден в title/h1 "
                f"(ожидались формы: {expected_city_forms})"
            )

        if expected_brand is None:
            issues.append(f"Неизвестный слаг бренда '{brand_slug}' — добавьте в BRAND_NAMES")
        elif expected_brand not in combined:
            issues.append(f"Бренд '{expected_brand}' НЕ найден в title/h1")

    # Проверка на явно "чужой" город/бренд в тексте (более точная диагностика)
    for slug, forms in CITY_NAMES.items():
        if slug != city_slug and any(form in combined for form in forms):
            issues.append(f"Обнаружено упоминание ДРУГОГО города '{forms[0]}' вместо своего")

    for slug, name in BRAND_NAMES.items():
        if slug != brand_slug and name in combined and path.stem != "index":
            issues.append(f"Обнаружено упоминание ДРУГОГО бренда '{name}' вместо своего")

    if not parser.title.strip():
        issues.append("Пустой <title>")

    return {
        "path": path,
        "title": parser.title.strip(),
        "h1": parser.h1.strip(),
        "issues": issues,
    }


def main():
    pages = list(find_pages(ROOT_DIR))
    if not pages:
        print("Не найдено файлов по маске naprawa-*/*/*.html")
        print("Запустите скрипт из корня проекта.")
        return

    problems = []
    for path in pages:
        result = check_file(path)
        if result.get("error") or result.get("issues"):
            problems.append(result)

    print(f"Проверено страниц: {len(pages)}")
    print(f"Страниц с проблемами: {len(problems)}\n")

    report_lines = []
    for r in problems:
        report_lines.append(f"ФАЙЛ: {r['path']}")
        if r.get("error"):
            report_lines.append(f"  ОШИБКА: {r['error']}")
        else:
            report_lines.append(f"  title: {r['title']!r}")
            report_lines.append(f"  h1:    {r['h1']!r}")
            for issue in r["issues"]:
                report_lines.append(f"  - {issue}")
        report_lines.append("")

    report_text = "\n".join(report_lines)
    print(report_text[:3000])
    if len(report_text) > 3000:
        print("... (полный список смотрите в mismatch_report.txt)")

    Path("mismatch_report.txt").write_text(report_text, encoding="utf-8")
    print("\nПолный отчёт сохранён в mismatch_report.txt")


if __name__ == "__main__":
    main()
