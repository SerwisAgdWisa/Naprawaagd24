#!/usr/bin/env python3
"""
Скрипт добавляет ссылку на карту сайта (/mapa-stron.html) в футер
каждой .html страницы проекта, если такой ссылки там ещё нет.

Использование:
    1. Положить этот файл в корень проекта (там же, где mapa-stron.html)
    2. Запустить:  python add_footer_link.py
    3. Проверить вывод — какие файлы изменены
    4. Если всё ок — закоммитить изменения в git

По умолчанию делает "сухой прогон" (dry run) — ничего не меняет,
только показывает, что было бы изменено.
Чтобы реально записать изменения, запустить с флагом --apply:
    python add_footer_link.py --apply

Перед реальной записью создаётся резервная копия каждого изменяемого
файла рядом с оригиналом с расширением .bak
"""

import argparse
import re
import sys
from pathlib import Path

# ---------- НАСТРОЙКИ (при необходимости поправьте) ----------

# Текст ссылки, которая будет добавлена в футер
LINK_HTML = '<p><a href="/mapa-stron.html">Mapa strony (wszystkie usługi i miasta)</a></p>'

# По какому паттерну ищем закрывающий тег футера, куда вставляем ссылку
FOOTER_CLOSE_TAG = "</footer>"

# Папка, с которой начинать поиск .html файлов (корень проекта)
ROOT_DIR = Path(".")

# Какие файлы/папки пропускать
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}

# ---------------------------------------------------------------


def find_html_files(root: Path):
    for path in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def already_has_link(content: str) -> bool:
    # Считаем, что ссылка уже есть, если встречается mapa-stron.html внутри футера
    return "mapa-stron.html" in content


def insert_link(content: str) -> str | None:
    """
    Вставляет LINK_HTML перед последним </footer> в файле.
    Возвращает новый контент или None, если вставить некуда/уже есть.
    """
    if FOOTER_CLOSE_TAG not in content:
        return None  # нет футера на этой странице

    if already_has_link(content):
        return None  # ссылка уже есть, ничего не делаем

    # Вставляем перед последним </footer>, с отступом как у соседних строк
    idx = content.rfind(FOOTER_CLOSE_TAG)

    # Пытаемся подобрать такой же отступ, как у строки с </footer>
    line_start = content.rfind("\n", 0, idx) + 1
    indent = re.match(r"[ \t]*", content[line_start:idx]).group(0)

    insertion = f"{indent}{LINK_HTML}\n"
    new_content = content[:idx] + insertion + content[idx:]
    return new_content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Реально записать изменения (по умолчанию — только показать, что изменится)",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Корневая папка проекта (по умолчанию текущая)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    html_files = list(find_html_files(root))

    if not html_files:
        print("Не найдено ни одного .html файла в", root.resolve())
        sys.exit(1)

    changed = 0
    skipped_no_footer = 0
    skipped_has_link = 0

    for path in html_files:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"[ПРОПУЩЕН, не UTF-8] {path}")
            continue

        if FOOTER_CLOSE_TAG not in content:
            skipped_no_footer += 1
            continue

        if already_has_link(content):
            skipped_has_link += 1
            continue

        new_content = insert_link(content)
        if new_content is None:
            continue

        changed += 1
        print(f"[БУДЕТ ИЗМЕНЁН] {path}")

        if args.apply:
            backup_path = path.with_suffix(path.suffix + ".bak")
            backup_path.write_text(content, encoding="utf-8")
            path.write_text(new_content, encoding="utf-8")

    print("\n--- Итог ---")
    print(f"Всего html файлов найдено:      {len(html_files)}")
    print(f"Будет/было изменено:            {changed}")
    print(f"Пропущено (нет <footer>):       {skipped_no_footer}")
    print(f"Пропущено (ссылка уже есть):    {skipped_has_link}")

    if not args.apply and changed > 0:
        print(
            "\nЭто был сухой прогон (dry run), файлы НЕ изменены.\n"
            "Если всё выглядит корректно, запустите:\n"
            "    python add_footer_link.py --apply\n"
            "Резервные копии (.bak) будут созданы автоматически."
        )


if __name__ == "__main__":
    main()
