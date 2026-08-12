import argparse
import logging
import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

EXCLUDE_DIRS = {"_backups", "backup", "backups", ".old", ".git", "node_modules", "css", "js", "img"}

# Зеленый SVG вызова
GREEN_PHONE_SVG = (
    '<svg viewBox="0 0 24 24" width="24" height="24" fill="#ffffff" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 '
    '1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 '
    '0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 '
    '1.02l-2.2 2.2z"/></svg>'
)

# Список поддерживаемых брендов (имя файла в img/brands/)
BRANDS = [
    "whirlpool", "samsung", "bosch", "lg", "indesit", "beko", 
    "electrolux", "candy", "siemens", "amica", "ariston", "gorenje"
]

def get_brand_from_path(path: Path) -> str:
    filename = path.stem.lower()
    for b in BRANDS:
        if b in filename:
            return b
    return ""

def process_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(content, 'html.parser')
    modified = False

    brand = get_brand_from_path(path)

    # 1. Замена обобщенного SVG на PNG-логотип бренда
    if brand:
        services_sec = soup.find('section', class_='services')
        if services_sec:
            # Расчет относительного пути к img/brands/
            rel_depth = len(path.relative_to(Path(".")).parts) - 1
            prefix = "../" * rel_depth
            logo_path = f"{prefix}img/brands/{brand}.png"

            # Удаляем старый контейнер иконки, если он был
            old_icon = services_sec.find('div', class_='appliance-icon')
            if old_icon:
                old_icon.decompose()

            # Вставляем логотип бренда
            logo_soup = BeautifulSoup(
                f'<div class="brand-logo-wrapper" style="margin-bottom:1.5rem; text-align:left;">'
                f'<img src="{logo_path}" alt="Serwis {brand.capitalize()}" class="brand-logo" style="max-height: 50px; width: auto;" onerror="this.style.display=\'none\'">'
                f'</div>', 
                'html.parser'
            )
            container = services_sec.find('div', class_='container') or services_sec
            container.insert(0, logo_soup)
            modified = True

    # 2. Оформление зеленой кнопки вызова в плавающей панели
    sticky = soup.find('div', class_='sticky-bottom-bar')
    if sticky:
        phone_btn = sticky.find('a', class_='phone-btn')
        if phone_btn:
            phone_btn['style'] = "background-color: #25D366; color: #ffffff; display: flex; align-items: center; justify-content: center; gap: 8px; font-weight: bold; text-decoration: none; padding: 12px;"
            # Обновляем внутренний SVG
            svg_tag = phone_btn.find('svg')
            if svg_tag:
                svg_tag.decompose()
            new_svg = BeautifulSoup(GREEN_PHONE_SVG, 'html.parser')
            phone_btn.insert(0, new_svg)
            modified = True

    # 3. Фикс обрыва текста в unique-ai-content
    ai_sec = soup.find('section', class_='unique-ai-content')
    if ai_sec:
        for p in ai_sec.find_all('p'):
            text = p.get_text().strip()
            if text.endswith("skontaktować"):
                p.string = text + " się z naszym serwisem под номером 721 988 949."
                modified = True

    if modified:
        path.write_text(str(soup), encoding="utf-8")
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Записать изменения на диск")
    args = parser.parse_args()

    root_dir = Path(".")
    files = [p for p in root_dir.rglob("*.html") if not any(part in EXCLUDE_DIRS for part in p.parts)]

    count = 0
    for path in tqdm(files, desc="Обновление логотипов и стилей"):
        if args.apply:
            if process_file(path):
                count += 1

    if args.apply:
        print(f"\n[УСПЕХ] Обновлено файлов: {count}")
    else:
        print("\n[DRY-RUN] Для записи выполните: python upgrade_site_v9_brand.py --apply")

if __name__ == "__main__":
    main()