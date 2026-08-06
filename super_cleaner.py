#!/usr/bin/env python3
"""
SUPER CLEANER — Полная реконструкция HTML сайта (исправлённая версия).

Изменения:
- ALLOWED_CSS оставляет только premium-theme.css
- добавлена фиксация breadcrumb-nav
- исправлена вставка sticky-bar (используется soup.new_tag)
- добавлена коррекция позиции .unique-ai-content относительно footer
- порядок операций скорректирован для минимизации конфликтов
"""

import argparse
import datetime
from pathlib import Path
import shutil
import re
from bs4 import BeautifulSoup

ROOT = Path(".")
EXCLUDE = {".git", "node_modules", ".vscode", "__pycache__", "_backups"}

# Оставляем ТОЛЬКО новый стиль, чтобы избежать конфликтов
ALLOWED_CSS = {"premium-theme.css"}
PREMIUM_LINK = "/css/premium-theme.css"


def normalize_css_paths(soup):
    changed = False
    for link in soup.find_all("link", href=True):
        href = link["href"]
        clean = href.split("?")[0]

        if "../../css/" in clean:
            link["href"] = href.replace("../../css/", "/css/")
            changed = True
        elif clean.startswith("css/"):
            link["href"] = "/" + href
            changed = True
    return changed


def remove_old_css(soup):
    changed = False
    for link in list(soup.find_all("link", rel=lambda r: r and "stylesheet" in r)):
        href = link.get("href", "") or ""
        clean = href.split("?")[0].split("/")[-1]
        if clean not in ALLOWED_CSS:
            link.decompose()
            changed = True
    return changed


def add_premium_css(soup):
    head = soup.find("head")
    if not head:
        return False

    exists = head.find("link", href=lambda h: h and "premium-theme.css" in h)
    if exists:
        return False

    new_link = soup.new_tag("link", rel="stylesheet", href=PREMIUM_LINK)
    head.append(new_link)
    return True


def remove_all_style_tags(soup):
    changed = False
    for tag in list(soup.find_all("style")):
        tag.decompose()
        changed = True
    return changed


def remove_inline_styles(soup):
    changed = False
    for tag in soup.find_all(attrs={"style": True}):
        try:
            del tag["style"]
            changed = True
        except Exception:
            pass
    return changed


def fix_breadcrumbs(soup):
    changed = False
    for nav in soup.find_all("nav"):
        inner_a = nav.find("a")
        inner_span = nav.find("span")
        text = (nav.get_text(" ") or "").strip()
        looks_like_bc = inner_a is not None and (inner_span is not None or ">" in text or "/" in text)
        if looks_like_bc:
            classes = nav.get("class", [])
            if "breadcrumb-nav" not in classes:
                nav["class"] = classes + ["breadcrumb-nav"]
                changed = True
    return changed


def fix_footer_position(soup):
    changed = False
    footer = soup.find("footer")
    ai_content = soup.find("section", class_="unique-ai-content")
    if footer and ai_content:
        all_nodes = list(soup.find_all())
        try:
            footer_index = all_nodes.index(footer)
            ai_index = all_nodes.index(ai_content)
            if footer_index < ai_index:
                footer.insert_before(ai_content)
                changed = True
        except ValueError:
            pass
    return changed


def wrap_maps(soup):
    iframe = soup.find("iframe", src=lambda s: s and "google.com/maps" in s)
    if not iframe:
        return False

    changed = False

    parent = iframe.parent
    if parent and "map-wrapper" not in (parent.get("class") or []):
        wrapper = soup.new_tag("div")
        wrapper["class"] = ["map-wrapper"]
        iframe.extract()
        wrapper.append(iframe)
        parent.append(wrapper)
        changed = True

    section = iframe.find_parent(["section", "div"])
    if section:
        if "map-section" not in (section.get("class") or []):
            section["class"] = (section.get("class") or []) + ["map-section"]
            changed = True

        container = None
        for child in section.find_all(recursive=False):
            if child.name == "div" and "map-container" in (child.get("class") or []):
                container = child
                break

        if not container:
            container = soup.new_tag("div")
            container["class"] = ["map-container"]
            for child in list(section.contents):
                if getattr(child, "name", None) in ("h1", "h2", "h3", "p"):
                    continue
                container.append(child.extract())
            section.append(container)
            changed = True

        title = section.find(["h1", "h2", "h3"])
        if title and "map-title" not in (title.get("class") or []):
            title["class"] = (title.get("class") or []) + ["map-title"]
            changed = True

        if title:
            desc = title.find_next("p")
            if desc and "map-desc" not in (desc.get("class") or []):
                desc["class"] = (desc.get("class") or []) + ["map-desc"]
                changed = True

    return changed


def find_phone(soup):
    tel = soup.find("a", href=lambda h: h and h.startswith("tel:"))
    if not tel:
        return None
    num = tel["href"].split(":", 1)[1]
    return re.sub(r"[^\d+]", "", num)


def add_sticky_bar(soup):
    if soup.find(class_="sticky-bottom-bar"):
        return False

    phone = find_phone(soup)
    if not phone:
        return False

    body = soup.find("body")
    if not body:
        return False

    bar = soup.new_tag("div", **{"class": "sticky-bottom-bar"})
    a = soup.new_tag("a", href=f"tel:{phone}")
    a.string = f"📞 Zadzwoń teraz: {phone}"
    bar.append(a)
    body.append(bar)
    return True


def remove_old_buttons(soup):
    changed = False
    for btn in list(soup.find_all("a", class_="floating-call-button")):
        btn.decompose()
        changed = True
    return changed


def remove_duplicate_breadcrumbs(soup):
    crumbs = soup.find_all(class_=lambda c: c and "breadcrumb" in c)
    if len(crumbs) > 1:
        for c in crumbs[1:]:
            c.decompose()
        return True
    return False


def fix_js(soup):
    changed = False
    for script in soup.find_all("script"):
        if script.string and "sendToWhatsApp" in script.string:
            script.string = script.string.replace("window.open", "window.location.href")
            changed = True
    return changed


def process_file(path, apply, backup_dir):
    try:
        html = path.read_text(encoding="utf-8")
    except Exception:
        return False

    soup = BeautifulSoup(html, "html.parser")
    changed = False
    local_changes = []

    if normalize_css_paths(soup):
        changed = True
        local_changes.append("normalize_css_paths")

    if remove_old_css(soup):
        changed = True
        local_changes.append("remove_old_css")

    if add_premium_css(soup):
        changed = True
        local_changes.append("add_premium_css")

    if remove_all_style_tags(soup):
        changed = True
        local_changes.append("remove_all_style_tags")

    if remove_inline_styles(soup):
        changed = True
        local_changes.append("remove_inline_styles")

    if fix_breadcrumbs(soup):
        changed = True
        local_changes.append("fix_breadcrumbs")

    if fix_footer_position(soup):
        changed = True
        local_changes.append("fix_footer_position")

    if wrap_maps(soup):
        changed = True
        local_changes.append("wrap_maps")

    if add_sticky_bar(soup):
        changed = True
        local_changes.append("add_sticky_bar")

    if remove_old_buttons(soup):
        changed = True
        local_changes.append("remove_old_buttons")

    if remove_duplicate_breadcrumbs(soup):
        changed = True
        local_changes.append("remove_duplicate_breadcrumbs")

    if fix_js(soup):
        changed = True
        local_changes.append("fix_js")

    if changed:
        print(f"[ИЗМЕНЕНИЯ] {path}")
        for c in local_changes:
            print("  -", c)

    if changed and apply:
        rel = path.relative_to(ROOT)
        bak = backup_dir / rel
        bak.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, bak)
        path.write_text(str(soup), encoding="utf-8")

    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    pages = [
        p for p in ROOT.rglob("*.html")
        if not any(x in p.parts for x in EXCLUDE)
    ]

    print(f"Найдено {len(pages)} HTML-файлов.")

    backup_dir = None
    if args.apply:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"_backups/full_rebuild_{ts}")

    changed = 0
    for p in pages:
        try:
            if process_file(p, args.apply, backup_dir):
                changed += 1
        except Exception as e:
            print(f"[ОШИБКА] {p}: {e}")

    print(f"\nИТОГ: изменено {changed} файлов.")
    if args.apply:
        print(f"Бэкапы сохранены в {backup_dir}")
    else:
        print("Пробный прогон завершён. Для записи используйте: --apply")


if __name__ == "__main__":
    main()
