#!/usr/bin/env python3
"""
add_icons.py
============
Проходит по всем .html файлам сайта и заменяет emoji-иконки в блоках
<div class="service-icon">...</div> на настоящие SVG-иконки
(pralka.svg, zmywarka.svg, lodowka.svg, piekarnik.svg, suszarka.svg,
pralko-suszarka.svg, szybki-dojazd.svg), которые должны лежать в /icons/
в корне сайта (так же, как уже лежат herb-*.svg).

Как это работает:
  Скрипт ищет фрагменты вида:
      href="ЧТО-ТО" ... > [пробелы/комментарии] <div ... class="service-icon" ...>ТЕКСТ</div>
  и по значению href (или по emoji, для "Szybki Dojazd") определяет,
  какая иконка нужна, затем заменяет только содержимое div на <img ...>.

  Всё остальное (переносы строк, комментарии, порядок и набор атрибутов,
  прочие классы на div) сохраняется как было — скрипт ничего не переформатирует.

  Скрипт идемпотентен: если в div уже стоит <img>, повторный запуск
  его не тронет (регулярка не матчит содержимое, где есть теги).

Запуск:
    python3 add_icons.py /путь/к/корню/сайта
    python3 add_icons.py /путь/к/корню/сайта --dry-run
    python3 add_icons.py /путь/к/корню/сайта --exclude _backups --exclude old_version

По умолчанию скрипт пропускает папки: _backups, backup, backups, .git,
node_modules, .old — плюс всё, что передано через --exclude.

Требования: только стандартная библиотека Python (re, pathlib, argparse).
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

# Порядок важен: более специфичные ключи проверяются первыми.
URL_ICON_MAP = [
    ("naprawa-pralko-suszarek", "pralko-suszarka.svg"),
    ("pralko-suszar", "pralko-suszarka.svg"),
    ("naprawa-pralek", "pralka.svg"),
    ("naprawa-zmywarek", "zmywarka.svg"),
    ("naprawa-lodowek", "lodowka.svg"),
    ("naprawa-piekarnikow", "piekarnik.svg"),
    ("naprawa-suszarek", "suszarka.svg"),
]

ICON_DIR = "/icons"  # куда скопированы pralka.svg, zmywarka.svg и т.д.

DEFAULT_EXCLUDE_DIRS = {"_backups", "backup", "backups", ".old", ".git", "node_modules"}

# Регулярка:
#   group(1) href
#   group(2) остальные атрибуты <a ...>
#   group(3) всё, что стоит между ">" открывающего <a> и открывающим <div ...> —
#            пробелы, переносы строк, HTML-комментарии. Сохраняется как есть.
#   group(4) атрибуты самого <div ...> (порядок/набор атрибутов не важен,
#            главное чтобы где-то был class="...service-icon...")
#   group(5) старое содержимое div (emoji / пробел / пусто).
#            [^<]* — не матчит, если внутри уже есть теги (напр. <img>),
#            это и даёт идемпотентность.
CARD_RE = re.compile(
    r'href="(?P<href>[^"]*)"(?P<a_rest>[^>]*)>'
    r'(?P<gap>(?:\s|<!--.*?-->)*)'
    r'<div(?P<div_attrs>(?=[^>]*\bclass="[^"]*\bservice-icon\b[^"]*")[^>]*)>'
    r'(?P<content>[^<]*)'
    r'</div>',
    re.DOTALL,
)


def pick_icon(href: str, old_content: str) -> Optional[str]:
    """Возвращает имя файла иконки для данного href/old_content, либо None."""
    href_l = href.lower()

    for key, icon in URL_ICON_MAP:
        if key in href_l:
            return icon

    # "Szybki Dojazd" на главной странице — ссылка на #order с ⚡
    if "⚡" in old_content and (href.startswith("#") or href == ""):
        return "szybki-dojazd.svg"

    return None


def build_img_tag(icon_file: str) -> str:
    alt = icon_file.replace(".svg", "").replace("-", " ").capitalize()
    return (
        f'<img src="{ICON_DIR}/{icon_file}" alt="{alt}" '
        f'class="service-icon-img" width="40" height="40" loading="lazy">'
    )


def process_text(text: str):
    """Возвращает (новый_текст, список_замен) для одного файла."""
    changes = []

    def repl(m: "re.Match[str]") -> str:
        href = m.group("href")
        old_content = m.group("content")
        icon = pick_icon(href, old_content)
        if icon is None:
            return m.group(0)  # иконка не распознана — не трогаем фрагмент

        changes.append((href, old_content.strip(), icon))

        # Реконструируем фрагмент, сохранив ВСЁ как было (пробелы/переносы/
        # комментарии/прочие атрибуты div), заменив только содержимое.
        return (
            f'href="{href}"{m.group("a_rest")}>'
            f'{m.group("gap")}'
            f'<div{m.group("div_attrs")}>{build_img_tag(icon)}</div>'
        )

    new_text = CARD_RE.sub(repl, text)
    return new_text, changes


def iter_html_files(root: Path, exclude_dirs: set):
    for path in root.rglob("*.html"):
        if any(part in exclude_dirs for part in path.relative_to(root).parts[:-1]):
            continue
        yield path


def main():
    parser = argparse.ArgumentParser(description="Добавляет SVG-иконки услуг во все HTML файлы сайта.")
    parser.add_argument("root", help="Корневая папка сайта (там где лежит index.html)")
    parser.add_argument("--dry-run", action="store_true", help="Только показать изменения, не сохранять файлы")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Имя папки, которую нужно пропустить (можно указывать несколько раз)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Папка не найдена: {root}")
        sys.exit(1)

    exclude_dirs = DEFAULT_EXCLUDE_DIRS | set(args.exclude)

    html_files = sorted(iter_html_files(root, exclude_dirs))
    skipped = sorted(set(root.rglob("*.html")) - set(html_files))

    total_files_changed = 0
    total_replacements = 0

    for f in html_files:
        try:
            original = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            original = f.read_text(encoding="cp1250", errors="replace")

        new_text, changes = process_text(original)

        if changes:
            total_files_changed += 1
            total_replacements += len(changes)
            rel = f.relative_to(root)
            print(f"\n{rel}  ({len(changes)} иконок)")
            for href, old, icon in changes:
                shown_old = old if old else "(пусто)"
                print(f"    href={href!r:35}  {shown_old!r:12} -> {icon}")

            if not args.dry_run:
                f.write_text(new_text, encoding="utf-8")

    print("\n" + "=" * 60)
    if args.dry_run:
        print(f"[DRY RUN] Было бы изменено файлов: {total_files_changed}, иконок: {total_replacements}")
    else:
        print(f"Готово. Изменено файлов: {total_files_changed}, добавлено/заменено иконок: {total_replacements}")

    if skipped:
        print(f"\nПропущено (исключённые папки: {sorted(exclude_dirs)}): {len(skipped)} файлов")
        for s in skipped[:10]:
            print(f"    - {s.relative_to(root)}")
        if len(skipped) > 10:
            print(f"    ... и ещё {len(skipped) - 10}")


if __name__ == "__main__":
    main()
