#!/usr/bin/env python3
"""
upgrade_site.py (v3)
=====================
Комплексный скрипт для всех .html файлов сайта. За один проход:

  1. ЧИНИТ баг кнопки WhatsApp:
         window.location.href(url, '_blank');   ->   window.open(url, '_blank');

  2. СТАТИЧЕСКИ оборачивает блок формы заказа (<section id="order">) и
     предыдущую секцию в <div class="dashboard-grid"> ПРЯМО В HTML.

  3. ЗАМЕНЯЕТ emoji-иконки услуг на настоящие SVG.

  4. ИСПРАВЛЯЕТ и РЕПОРТИТ битые теги (точечные безопасные паттерны).

Требования: только стандартная библиотека Python.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

DEFAULT_EXCLUDE_DIRS = {"_backups", "backup", "backups", ".old", ".git", "node_modules"}

# ---------------------------------------------------------------------------
# 1) WHATSAPP BUTTON BUG
# ---------------------------------------------------------------------------
WHATSAPP_BUG_RE = re.compile(
    r"window\.location\.href\(\s*([^,()]+?)\s*,\s*(['\"]_blank['\"])\s*\)",
)


def fix_whatsapp_bug(text: str) -> Tuple[str, int]:
    count = [0]

    def repl(m: re.Match) -> str:
        count[0] += 1
        return f"window.open({m.group(1)}, {m.group(2)})"

    new_text = WHATSAPP_BUG_RE.sub(repl, text)
    return new_text, count[0]


# ---------------------------------------------------------------------------
# 2) STATIC DASHBOARD WRAPPING (depth-aware)
# ---------------------------------------------------------------------------
SECTION_TAG_RE = re.compile(r"<(/?)section\b([^>]*)>", re.IGNORECASE)
ORDER_ID_RE = re.compile(r'id\s*=\s*"order"', re.IGNORECASE)
ONLY_WHITESPACE_OR_COMMENTS_RE = re.compile(r"(?:\s|<!--.*?-->)*", re.DOTALL)


def top_level_sections(text: str) -> List[Tuple[int, int, str]]:
    spans = []
    depth = 0
    start = None
    start_attrs = None
    for m in SECTION_TAG_RE.finditer(text):
        closing = bool(m.group(1))
        if not closing:
            if depth == 0:
                start = m.start()
                start_attrs = m.group(2)
            depth += 1
        else:
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    spans.append((start, m.end(), start_attrs))
                    start = None
    return spans


def wrap_order_section_statically(text: str) -> Tuple[str, bool, str]:
    spans = top_level_sections(text)

    order_idx = None
    for i, (_, _, attrs) in enumerate(spans):
        if ORDER_ID_RE.search(attrs):
            order_idx = i
            break

    if order_idx is None:
        return text, False, "секция #order не найдена"

    if order_idx == 0:
        return text, False, "перед #order нет другой секции верхнего уровня"

    order_start, order_end, _ = spans[order_idx]
    prev_start, prev_end, _ = spans[order_idx - 1]

    # Идемпотентность: проверяем расширенный контекст перед prev_start
    prefix_context = text[max(0, prev_start - 500):prev_start]
    if 'class="dashboard-left"' in prefix_context or 'class="dashboard-grid"' in prefix_context:
        return text, False, "уже обёрнуто в dashboard-grid ранее — пропущено (идемпотентность)"

    between = text[prev_end:order_start]
    if not ONLY_WHITESPACE_OR_COMMENTS_RE.fullmatch(between):
        return text, False, "между секциями есть посторонний контент — пропущено для безопасности"

    prev_html = text[prev_start:prev_end]
    order_html = text[order_start:order_end]

    wrapped = (
        '<div class="dashboard-grid">'
        f'<div class="dashboard-left">{prev_html}</div>'
        f'<div class="dashboard-right">{order_html}</div>'
        '</div>'
    )

    new_text = text[:prev_start] + wrapped + text[order_end:]
    return new_text, True, ""


# ---------------------------------------------------------------------------
# 3) SERVICE ICONS
# ---------------------------------------------------------------------------
URL_ICON_MAP = [
    ("naprawa-pralko-suszarek", "pralko-suszarka.svg"),
    ("pralko-suszar", "pralko-suszarka.svg"),
    ("naprawa-pralek", "pralka.svg"),
    ("naprawa-zmywarek", "zmywarka.svg"),
    ("naprawa-lodowek", "lodowka.svg"),
    ("naprawa-piekarnikow", "piekarnik.svg"),
    ("naprawa-suszarek", "suszarka.svg"),
]
ICON_DIR = "/icons"

CARD_RE = re.compile(
    r'href="(?P<href>[^"]*)"(?P<a_rest>[^>]*)>'
    r'(?P<gap>(?:\s|<!--.*?-->)*)'
    r'<div(?P<div_attrs>(?=[^>]*\bclass="[^"]*\bservice-icon\b[^"]*")[^>]*)>'
    r'(?P<content>[^<]*)'
    r'</div>',
    re.DOTALL,
)


def pick_icon(href: str, old_content: str) -> Optional[str]:
    href_l = href.lower()
    for key, icon in URL_ICON_MAP:
        if key in href_l:
            return icon
    if ("⚡" in old_content or "\u26a1" in old_content) and (href.startswith("#") or href == ""):
        return "szybki-dojazd.svg"
    return None


def build_img_tag(icon_file: str) -> str:
    alt = icon_file.replace(".svg", "").replace("-", " ").capitalize()
    return (
        f'<img src="{ICON_DIR}/{icon_file}" alt="{alt}" '
        f'class="service-icon-img" width="40" height="40" loading="lazy">'
    )


def fix_icons(text: str):
    changes = []

    def repl(m: re.Match) -> str:
        href = m.group("href")
        old_content = m.group("content")
        icon = pick_icon(href, old_content)
        if icon is None:
            return m.group(0)
        changes.append((href, old_content.strip(), icon))
        return (
            f'href="{href}"{m.group("a_rest")}>'
            f'{m.group("gap")}'
            f'<div{m.group("div_attrs")}>{build_img_tag(icon)}</div>'
        )

    new_text = CARD_RE.sub(repl, text)
    return new_text, changes


# ---------------------------------------------------------------------------
# 4) CORRUPTED TAG FIXING & DETECTION
# ---------------------------------------------------------------------------
BROKEN_LI_OPEN_RE = re.compile(r"<l<\w+>", re.IGNORECASE)
BROKEN_LI_CLOSE_RE = re.compile(r"</l<\w+>", re.IGNORECASE)

DOUBLED_UL_BLOCK_RE = re.compile(
    r"(<ul\b[^>]*>)\s*<ul\b[^>]*>(.*?)</ul>\s*</ul>",
    re.DOTALL | re.IGNORECASE
)


def fix_known_corruption(text: str) -> Tuple[str, int]:
    count = 0

    new_text, n1 = BROKEN_LI_OPEN_RE.subn("<li>", text)
    count += n1
    text = new_text

    new_text, n2 = BROKEN_LI_CLOSE_RE.subn("</li>", text)
    count += n2
    text = new_text

    def ul_repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        return f"{m.group(1)}{m.group(2)}</ul>"

    text, n3 = DOUBLED_UL_BLOCK_RE.subn(ul_repl, text)
    count += n3

    return text, count


CORRUPTION_PATTERNS = [
    (re.compile(r"<l<\w+>", re.IGNORECASE), "разорванный тег вида <l<secti>"),
    (re.compile(r"<(ul|ol|li)\b([^>]*)>\s*<\1\2>", re.IGNORECASE), "задвоенный открывающий тег списка"),
]


def detect_corruption(text: str):
    findings = []
    for pattern, description in CORRUPTION_PATTERNS:
        for m in pattern.finditer(text):
            findings.append((description, m.group(0)[:60]))
    return findings


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def iter_html_files(root: Path, exclude_dirs: set):
    for path in root.rglob("*.html"):
        if any(part in exclude_dirs for part in path.relative_to(root).parts[:-1]):
            continue
        yield path


def main():
    parser = argparse.ArgumentParser(description="Комплексное обновление всех HTML файлов сайта.")
    parser.add_argument("root", help="Корневая папка сайта")
    parser.add_argument("--dry-run", action="store_true", help="Только показать изменения, не сохранять")
    parser.add_argument("--skip-icons", action="store_true", help="Не трогать иконки")
    parser.add_argument("--skip-whatsapp", action="store_true", help="Не чинить баг WhatsApp-кнопки")
    parser.add_argument("--skip-dashboard", action="store_true", help="Не оборачивать в dashboard-grid")
    parser.add_argument("--skip-corruption-check", action="store_true", help="Не искать битые теги")
    parser.add_argument("--exclude", action="append", default=[], help="Папка для исключения (можно несколько раз)")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Папка не найдена: {root}")
        sys.exit(1)

    exclude_dirs = DEFAULT_EXCLUDE_DIRS | set(args.exclude)
    html_files = sorted(iter_html_files(root, exclude_dirs))

    stats = {
        "files_changed": 0,
        "whatsapp_fixed": 0,
        "dashboard_wrapped": 0,
        "dashboard_skipped": 0,
        "icons_replaced": 0,
    }
    corruption_report = []
    dashboard_skip_reasons = []

    for f in html_files:
        try:
            original = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            original = f.read_text(encoding="cp1250", errors="replace")

        text = original
        file_changed = False
        rel = f.relative_to(root)
        log_lines = []

        if not args.skip_whatsapp:
            text, n = fix_whatsapp_bug(text)
            if n:
                stats["whatsapp_fixed"] += n
                file_changed = True
                log_lines.append(f"  WhatsApp-баг исправлен (window.open): {n}")

        if not args.skip_icons:
            text, changes = fix_icons(text)
            if changes:
                stats["icons_replaced"] += len(changes)
                file_changed = True
                log_lines.append(f"  Иконок заменено: {len(changes)}")
                for href, old, icon in changes:
                    shown_old = old if old else "(пусто)"
                    log_lines.append(f"      href={href!r:35} {shown_old!r:10} -> {icon}")

        if not args.skip_dashboard:
            text, wrapped, reason = wrap_order_section_statically(text)
            if wrapped:
                stats["dashboard_wrapped"] += 1
                file_changed = True
                log_lines.append("  dashboard-grid: обёрнуто статически (без JS)")
            elif reason == "уже обёрнуто в dashboard-grid ранее — пропущено (идемпотентность)":
                stats["dashboard_already_done"] = stats.get("dashboard_already_done", 0) + 1
            elif reason != "секция #order не найдена":
                stats["dashboard_skipped"] += 1
                dashboard_skip_reasons.append((rel, reason))

        if not args.skip_corruption_check:
            text, n_fixed = fix_known_corruption(text)
            if n_fixed:
                stats.setdefault("corruption_fixed", 0)
                stats["corruption_fixed"] += n_fixed
                file_changed = True
                log_lines.append(f"  Битые теги исправлены (проверенные паттерны): {n_fixed}")

            remaining = detect_corruption(text)
            for description, snippet in remaining:
                corruption_report.append((rel, description, snippet))

        if file_changed:
            stats["files_changed"] += 1
            print(f"\n{rel}")
            for line in log_lines:
                print(line)
            if not args.dry_run:
                f.write_text(text, encoding="utf-8")

    print("\n" + "=" * 70)
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}Изменено файлов: {stats['files_changed']}")
    print(f"{prefix}WhatsApp-баг исправлен: {stats['whatsapp_fixed']} раз (window.open, новая вкладка)")
    print(f"{prefix}dashboard-grid обёрнуто статически: {stats['dashboard_wrapped']}")
    print(f"{prefix}dashboard-grid уже было обёрнуто ранее (пропущено, это нормально): {stats.get('dashboard_already_done', 0)}")
    print(f"{prefix}dashboard-grid пропущено — требует внимания: {stats['dashboard_skipped']}")
    print(f"{prefix}Иконок заменено: {stats['icons_replaced']}")
    print(f"{prefix}Битых тегов исправлено автоматически: {stats.get('corruption_fixed', 0)}")

    if dashboard_skip_reasons:
        print(f"\nℹ Страницы, где dashboard-обёртка НЕ применена (оставлены как есть):")
        for rel, reason in dashboard_skip_reasons[:30]:
            print(f"    {rel}: {reason}")
        if len(dashboard_skip_reasons) > 30:
            print(f"    ... и ещё {len(dashboard_skip_reasons) - 30}")

    if corruption_report:
        print(f"\n⚠ Осталось подозрений на битые теги (НЕ покрыты автофиксом, только отчёт): {len(corruption_report)}")
        for rel, description, snippet in corruption_report[:30]:
            print(f"    {rel}: {description} -> {snippet!r}")
        if len(corruption_report) > 30:
            print(f"    ... и ещё {len(corruption_report) - 30}")


if __name__ == "__main__":
    main()