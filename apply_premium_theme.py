#!/usr/bin/env python3
"""
Разворачивает premium-theme.css по всему сайту:

  1. Добавляет <link rel="stylesheet" href="/css/premium-theme.css">
     перед </head> на КАЖДОЙ html-странице (идемпотентно — повторный
     запуск не задублирует).
  2. На страницах, где есть Google Maps iframe (обычно только index.html
     в корне), оборачивает секцию нужными классами (.map-section,
     .map-title, .map-desc, .map-wrapper, .map-phone), чтобы заработали
     соответствующие правила в premium-theme.css.
  3. Добавляет мобильную "прилипающую" нижнюю панель звонка
     (.sticky-bottom-bar) перед </body>, если её ещё нет — номер телефона
     берётся из уже существующей ссылки tel: на странице.

Требует: pip install beautifulsoup4 --break-system-packages

Запуск:
    python apply_premium_theme.py            # сухой прогон — список изменений
    python apply_premium_theme.py --apply     # реальная запись + .bak
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Установите: pip install beautifulsoup4 --break-system-packages")
    sys.exit(1)

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode", "__pycache__"}
CSS_LINK_HREF = "/css/premium-theme.css"
STICKY_BAR_MARKER_CLASS = "sticky-bottom-bar"


def find_all_html(root: Path):
    for path in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def ensure_css_link(soup: BeautifulSoup) -> bool:
    """Добавляет <link> на premium-theme.css в <head>, если его там нет.
    Возвращает True, если что-то изменилось."""
    head = soup.find("head")
    if head is None:
        return False

    existing = head.find("link", href=lambda h: h and "premium-theme.css" in h)
    if existing:
        return False

    new_link = soup.new_tag("link", rel="stylesheet", href=CSS_LINK_HREF)
    head.append(new_link)
    return True


def wrap_maps_section(soup: BeautifulSoup) -> bool:
    """Находит iframe с Google Maps embed и оборачивает окружающую
    разметку нужными классами. Возвращает True, если что-то изменилось."""
    iframe = soup.find("iframe", src=lambda s: s and "google.com/maps/embed" in s)
    if iframe is None:
        return False

    changed = False

    # Уже обработано раньше?
    if iframe.find_parent(class_="map-wrapper"):
        return False

    # Ближайший <section>, который считаем блоком карты
    section = iframe.find_parent("section")
    if section and "map-section" not in (section.get("class") or []):
        section["class"] = (section.get("class") or []) + ["map-section"]
        changed = True

    # div/container вокруг содержимого секции
    if section:
        inner_div = section.find("div", recursive=False)
        if inner_div and "map-container" not in (inner_div.get("class") or []):
            inner_div["class"] = (inner_div.get("class") or []) + ["map-container"]
            changed = True

        # Заголовок секции
        title_tag = section.find(["h2", "h3"])
        if title_tag and "map-title" not in (title_tag.get("class") or []):
            title_tag["class"] = (title_tag.get("class") or []) + ["map-title"]
            changed = True

        # Первый параграф после заголовка — считаем описанием
        if title_tag:
            desc_tag = title_tag.find_next("p")
            if desc_tag and "map-desc" not in (desc_tag.get("class") or []):
                desc_tag["class"] = (desc_tag.get("class") or []) + ["map-desc"]
                changed = True

    # Обёртка непосредственно вокруг iframe
    iframe_parent = iframe.parent
    if iframe_parent and "map-wrapper" not in (iframe_parent.get("class") or []):
        iframe_parent["class"] = (iframe_parent.get("class") or []) + ["map-wrapper"]
        changed = True

    return changed


def find_phone_number(soup: BeautifulSoup) -> str | None:
    tel_link = soup.find("a", href=lambda h: h and h.startswith("tel:"))
    if tel_link:
        return tel_link["href"].replace("tel:", "")
    return None


def add_sticky_bar(soup: BeautifulSoup) -> bool:
    """Добавляет мобильную прилипающую панель звонка перед </body>,
    если её там ещё нет."""
    if soup.find(class_=STICKY_BAR_MARKER_CLASS):
        return False

    phone = find_phone_number(soup)
    if not phone:
        return False  # нет номера на странице — не добавляем панель

    body = soup.find("body")
    if body is None:
        return False

    bar_html = (
        f'<div class="{STICKY_BAR_MARKER_CLASS}">'
        f'<a href="tel:{phone}">📞 Zadzwoń teraz: {phone}</a>'
        f'</div>'
    )
    new_bar = BeautifulSoup(bar_html, "html.parser")
    body.append(new_bar)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skip-sticky-bar", action="store_true",
                         help="Не добавлять мобильную панель звонка (только CSS-ссылка + карта)")
    args = parser.parse_args()

    pages = list(find_all_html(ROOT_DIR))
    if not pages:
        print("HTML-файлы не найдены. Запустите из корня проекта.")
        sys.exit(1)

    print(f"Найдено {len(pages)} html-файлов.\n")

    css_added = 0
    map_wrapped = 0
    sticky_added = 0
    errors = 0

    for path in pages:
        try:
            html = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"[ПРОПУЩЕН, не UTF-8] {path}")
            continue

        soup = BeautifulSoup(html, "html.parser")
        changed = False

        if ensure_css_link(soup):
            css_added += 1
            changed = True

        if wrap_maps_section(soup):
            map_wrapped += 1
            changed = True
            print(f"[КАРТА ОБЁРНУТА] {path}")

        if not args.skip_sticky_bar:
            if add_sticky_bar(soup):
                sticky_added += 1
                changed = True

        if changed and args.apply:
            try:
                path.with_suffix(path.suffix + ".bak").write_text(html, encoding="utf-8")
                path.write_text(str(soup), encoding="utf-8")
            except Exception as e:
                print(f"[ОШИБКА ЗАПИСИ] {path}: {e}")
                errors += 1

    print("\n--- Итог ---")
    print(f"Всего файлов:                    {len(pages)}")
    print(f"Добавлена ссылка на CSS:         {css_added}")
    print(f"Обёрнут блок карты:              {map_wrapped}")
    print(f"Добавлена sticky-панель звонка:  {sticky_added}")
    print(f"Ошибок записи:                   {errors}")

    if not args.apply:
        print("\nЭто сухой прогон. Запустите с --apply, чтобы записать изменения.")


if __name__ == "__main__":
    main()
