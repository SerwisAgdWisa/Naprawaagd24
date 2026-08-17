import argparse
import logging
import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("upgrade_v8.log", encoding="utf-8")
    ]
)

EXCLUDE_DIRS = {"_backups", "backup", "backups", ".old", ".git", "node_modules", "css", "js", "img"}

BRANDS = [
    "whirlpool", "samsung", "bosch", "lg", "indesit", "beko", 
    "electrolux", "candy", "siemens", "amica", "ariston", "gorenje"
]

APPLIANCE_ICONS = {
    "naprawa-pralek": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#f97316"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3zm0 11c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>',
    "naprawa-zmywarek": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#f97316"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm0 12c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>',
    "naprawa-lodowek": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#f97316"><path d="M17 2H7c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 8H8V4h8v6zm0 10H8v-8h8v8z"/></svg>',
    "naprawa-piekarnikow": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#f97316"><path d="M19 4H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H5V8h14v10z"/></svg>',
    "naprawa-suszarek": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#f97316"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>',
    "naprawa-pralko-suszarek": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#f97316"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>'
}

GREEN_PHONE_SVG = '<svg viewBox="0 0 24 24" width="24" height="24" fill="#ffffff" xmlns="http://www.w3.org/2000/svg"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>'
WHATSAPP_SVG = '<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 0c-8.837 0-16 7.163-16 16 0 2.825 0.737 5.607 2.137 8.048l-2.137 7.952 8.135-2.135c2.372 1.3 5.060 1.987 7.865 1.987 8.837 0 16-7.163 16-16s-7.163-16-16-16zM16 29.333c-2.482 0-4.908-0.647-7.042-1.872l-0.505-0.292-5.228 1.372 1.395-5.197-0.323-0.513c-1.345-2.138-2.053-4.607-2.053-7.163 0-7.351 5.982-13.333 13.333-13.333s13.333 5.982 13.333 13.333-5.982 13.333-13.333 13.333zM22.502 19.332c-0.357-0.178-2.112-1.042-2.438-1.162-0.327-0.118-0.565-0.178-0.803 0.178s-0.922 1.162-1.131 1.4c-0.208 0.238-0.417 0.268-0.773 0.089s-1.503-0.554-2.863-1.767c-1.059-0.944-1.774-2.11-1.982-2.467s-0.022-0.55 0.156-0.728c0.161-0.16 0.357-0.417 0.536-0.625 0.178-0.208 0.238-0.357 0.357-0.595 0.118-0.238 0.059-0.446-0.030-0.625s-0.803-1.933-1.101-2.647c-0.29-0.696-0.585-0.601-0.803-0.612l-0.684-0.010c-0.238 0-0.625 0.089-0.952 0.446s-1.25 1.22-1.25 2.976 1.28 3.45 1.458 3.688c0.178 0.238 2.518 3.845 6.1 5.392 0.852 0.368 1.518 0.588 2.037 0.753 0.855 0.272 1.634 0.233 2.25 0.141 0.688-0.103 2.112-0.862 2.41-1.696 0.298-0.833 0.298-1.547 0.208-1.696-0.089-0.148-0.327-0.238-0.684-0.417z"/></svg>'

def safe_write_file(path: Path, content: str):
    backup_path = path.with_suffix(path.suffix + ".bak")
    try:
        if path.exists():
            os.replace(path, backup_path)
        path.write_text(content, encoding="utf-8", errors="replace")
        if backup_path.exists():
            backup_path.unlink()
    except Exception as e:
        if backup_path.exists():
            os.replace(backup_path, path)
        raise RuntimeError(f"Ошибка записи {path}: {e}")

def process_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8", errors="replace")
    original_content = content

    # 1. Исправление WhatsApp JS и экранирования \\n -> \n
    content, n1 = re.subn(r"window\.location\.href\(\s*([^,()]+?)\s*,\s*(['\"]_blank['\"])\s*\)", r"window.open(\1, \2)", content)
    content, n2 = re.subn(r'\\\\n', r'\\n', content)
    
    soup = BeautifulSoup(content, 'html.parser')
    modified = (n1 > 0 or n2 > 0 or content != original_content)

    # 2. Исправление домена в Schema.org
    for script in soup.find_all('script', type='application/ld+json'):
        if script.string and 'naprawaagd24.pl' in script.string:
            script.string = script.string.replace('naprawaagd24.pl', 'naprawaagd24.pl')
            modified = True

    # 3. Удаление текстовых эмодзи из шапки
    header_phone = soup.find('a', class_='phone')
    if header_phone and '📞' in header_phone.text:
        header_phone.string = header_phone.text.replace('📞', '').strip()
        modified = True

    # 4. Дедупликация списков <ul> (удаление повторов <li>)
    for ul in soup.find_all('ul'):
        seen = set()
        for li in list(ul.find_all('li', recursive=False)):
            text_norm = re.sub(r'\s+', ' ', li.get_text()).strip().lower()
            if text_norm in seen:
                li.decompose()
                modified = True
            elif text_norm:
                seen.add(text_norm)

    # 5. Подстановка брендового PNG-логотипа или SVG-иконки
    filename = path.stem.lower()
    brand = next((b for b in BRANDS if b in filename), "")
    
    services_sec = soup.find('section', class_='services')
    if services_sec:
        container = services_sec.find('div', class_='container') or services_sec
        old_icon = services_sec.find('div', class_='appliance-icon') or services_sec.find('div', class_='brand-logo-wrapper')
        if old_icon:
            old_icon.decompose()

        if brand:
            rel_depth = len(path.relative_to(Path(".")).parts) - 1
            prefix = "../" * rel_depth
            logo_path = f"{prefix}img/brands/{brand}.png"
            logo_markup = f'<div class="brand-logo-wrapper" style="margin-bottom:1.5rem; text-align:left;"><img src="{logo_path}" alt="Serwis {brand.capitalize()}" class="brand-logo" style="max-height: 50px; width: auto;" onerror="this.style.display=\'none\'"></div>'
            container.insert(0, BeautifulSoup(logo_markup, 'html.parser'))
            modified = True
        else:
            appliance_cat = next((part for part in path.parts if part in APPLIANCE_ICONS), "naprawa-pralek")
            svg_icon = APPLIANCE_ICONS[appliance_cat]
            icon_markup = f'<div class="appliance-icon" style="margin-bottom:1rem;">{svg_icon}</div>'
            container.insert(0, BeautifulSoup(icon_markup, 'html.parser'))
            modified = True

    # 6. Обертка в dashboard-grid
    if not soup.find('div', class_='dashboard-grid'):
        order_sec = soup.find('section', id='order') or soup.find('section', class_='order-section')
        if services_sec and order_sec:
            grid = soup.new_tag('div', **{'class': 'dashboard-grid'})
            left = soup.new_tag('div', **{'class': 'dashboard-left'})
            right = soup.new_tag('div', **{'class': 'dashboard-right'})

            services_sec.wrap(left)
            order_sec.wrap(right)
            left.wrap(grid)
            grid.append(right)
            modified = True

    # 7. Зеленая кнопка вызова внизу
    sticky = soup.find('div', class_='sticky-bottom-bar')
    if sticky:
        phone_btn = sticky.find('a', class_='phone-btn')
        if phone_btn:
            phone_btn['style'] = "background-color: #25D366; color: #ffffff; display: flex; align-items: center; justify-content: center; gap: 8px; font-weight: bold; text-decoration: none; padding: 12px; border-radius: 4px;"
            svg_tag = phone_btn.find('svg')
            if svg_tag:
                svg_tag.decompose()
            phone_btn.insert(0, BeautifulSoup(GREEN_PHONE_SVG, 'html.parser'))
            modified = True

    # 8. Гарантированная вставка плавающей WhatsApp-кнопки
    if not soup.find('a', class_='whatsapp-float'):
        wa_tag = BeautifulSoup(f'<a class="whatsapp-float" href="https://wa.me/48721988949" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">{WHATSAPP_SVG}</a>', 'html.parser')
        if soup.body:
            soup.body.append(wa_tag)
            modified = True

    # 9. Исправление оборванного текста в unique-ai-content
    ai_sec = soup.find('section', class_='unique-ai-content')
    if ai_sec:
        for p in ai_sec.find_all('p'):
            text = p.get_text().strip()
            if text.endswith("skontaktować"):
                p.string = text + " się z naszym serwisem pod numerem 721 988 949."
                modified = True

    if modified:
        safe_write_file(path, str(soup))
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Записать изменения на диск")
    args = parser.parse_args()

    root_dir = Path(".")
    files = [p for p in root_dir.rglob("*.html") if not any(part in EXCLUDE_DIRS for part in p.parts)]

    count = 0
    for path in tqdm(files, desc="Полная обработка файлов v8"):
        if args.apply:
            if process_file(path):
                count += 1

    if args.apply:
        print(f"\n[УСПЕХ] Обновлено файлов: {count}")
    else:
        print("\n[DRY-RUN] Тестовый прогон завершен. Для записи запустите:")
        print("python upgrade_site_v8.py --apply")

if __name__ == "__main__":
    main()