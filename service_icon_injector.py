#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse
import re
import shutil
import sys


# ============================================================
# НАСТРОЙКИ
# ============================================================

TARGETS = {
    "naprawa-lodowek": "lodowka",
    "naprawa-pralek": "pralka",
    "naprawa-piekarnikow": "piekarnik",
    "naprawa-suszarek": "suszarka",
    "naprawa-pralko-suszarek": "pralko-suszarka",
    "naprawa-zmywarek": "zmywarka",
}

ICON_DIR = "icons"


# ============================================================
# КОДИРОВКА
# ============================================================

def decode_file(data: bytes):
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig"), "utf-8-sig"

    try:
        return data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return data.decode("cp1250"), "cp1250"


def encode_file(text: str, encoding: str) -> bytes:
    return text.encode(encoding)


# ============================================================
# BACKUP
# ============================================================

def make_backup(path: Path):
    backup = path.with_suffix(path.suffix + ".bak")

    counter = 1
    while backup.exists():
        backup = path.with_suffix(
            path.suffix + f".bak{counter}"
        )
        counter += 1

    shutil.copy2(path, backup)
    return backup


# ============================================================
# ОПРЕДЕЛЕНИЕ ОТНОСИТЕЛЬНОГО ПУТИ К ИКОНКЕ
# ============================================================

def icon_src_for_file(root: Path, html_path: Path, icon: str) -> str:
    """
    Например:

    /naprawa-lodowek/index.html
        -> ../icons/lodowka.svg

    /naprawa-lodowek/stargard/index.html
        -> ../../icons/lodowka.svg
    """

    html_parent = html_path.parent
    relative_parent = html_parent.relative_to(root)

    depth = len(relative_parent.parts)

    prefix = "../" * depth

    return f"{prefix}{ICON_DIR}/{icon}.svg"


# ============================================================
# ПРОВЕРКА ИКОНКИ
# ============================================================

def is_already_present(text: str, icon_src: str) -> bool:
    """
    Проверяем наличие именно нашей иконки.

    Разрешаем как ../icons/..., так и ../../icons/...
    """

    normalized = icon_src.replace("/", r"\/")

    pattern = rf'<img\b[^>]*src=["\']{normalized}["\']'

    return re.search(
        pattern,
        text,
        re.IGNORECASE,
    ) is not None


# ============================================================
# ВСТАВКА ИКОНКИ
# ============================================================

def insert_icon(text: str, icon_src: str):
    """
    Приоритет:

    1. после первого <h1>...</h1>
    2. если H1 нет — сразу после <body>
    3. если body нет — в начало файла

    Никакой другой HTML не изменяется.
    """

    if is_already_present(text, icon_src):
        return text, False

    insertion = (
        '\n'
        '    <div class="appliance-icon">\n'
        f'        <img src="{icon_src}" '
        'alt="" aria-hidden="true" loading="eager">\n'
        '    </div>'
    )

    # --------------------------------------------------------
    # 1. После H1
    # --------------------------------------------------------

    h1_pattern = re.compile(
        r'(<h1\b[^>]*>.*?</h1>)',
        re.IGNORECASE | re.DOTALL,
    )

    match = h1_pattern.search(text)

    if match:
        new_text = (
            text[:match.end()]
            + insertion
            + text[match.end():]
        )

        return new_text, True

    # --------------------------------------------------------
    # 2. После BODY
    # --------------------------------------------------------

    body_pattern = re.compile(
        r'(<body\b[^>]*>)',
        re.IGNORECASE,
    )

    match = body_pattern.search(text)

    if match:
        new_text = (
            text[:match.end()]
            + insertion
            + text[match.end():]
        )

        return new_text, True

    # --------------------------------------------------------
    # 3. Совсем пустой / нестандартный HTML
    # --------------------------------------------------------

    return insertion.lstrip("\n") + "\n" + text, True


# ============================================================
# ПОИСК ФАЙЛОВ
# ============================================================

def discover_files(root: Path):
    """
    Для каждой категории ищем:

        naprawa-xxx/index.html

    и непосредственно городские:

        naprawa-xxx/*/index.html

    Более глубокие уровни НЕ обрабатываем.
    """

    files = []

    for folder, icon in TARGETS.items():

        category_dir = root / folder

        # ----------------------------------------------------
        # Главная страница категории
        # ----------------------------------------------------

        main_index = category_dir / "index.html"

        if main_index.is_file():
            files.append(
                (main_index, icon)
            )

        # ----------------------------------------------------
        # Городские страницы: ровно один уровень
        # ----------------------------------------------------

        if category_dir.is_dir():

            for child in sorted(category_dir.iterdir()):

                if not child.is_dir():
                    continue

                city_index = child / "index.html"

                if city_index.is_file():
                    files.append(
                        (city_index, icon)
                    )

    return files


# ============================================================
# ATOMIC WRITE
# ============================================================

def atomic_write(path: Path, data: bytes):
    tmp = path.with_name(
        path.name + ".tmp"
    )

    try:
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()

        tmp.replace(path)

    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


# ============================================================
# ОБРАБОТКА ФАЙЛА
# ============================================================

def process_file(
    root: Path,
    html_path: Path,
    icon: str,
    dry_run: bool,
):
    icon_path = root / ICON_DIR / f"{icon}.svg"

    print()
    print("=" * 70)

    print(
        f"Файл : "
        f"{html_path.relative_to(root)}"
    )

    print(
        f"Иконка: "
        f"{icon_path.relative_to(root)}"
    )

    # --------------------------------------------------------
    # Проверка HTML
    # --------------------------------------------------------

    if not html_path.is_file():
        print("SKIP: index.html не найден")
        return False

    # --------------------------------------------------------
    # Проверка SVG
    # --------------------------------------------------------

    if not icon_path.is_file():
        raise RuntimeError(
            f"Не найдена иконка: {icon_path}"
        )

    # --------------------------------------------------------
    # Относительный URL
    # --------------------------------------------------------

    icon_src = icon_src_for_file(
        root,
        html_path,
        icon,
    )

    print(
        f"Путь в HTML: {icon_src}"
    )

    # --------------------------------------------------------
    # Чтение
    # --------------------------------------------------------

    original_bytes = html_path.read_bytes()

    original_text, encoding = decode_file(
        original_bytes
    )

    # --------------------------------------------------------
    # Изменение
    # --------------------------------------------------------

    transformed_text, changed = insert_icon(
        original_text,
        icon_src,
    )

    if not changed:
        print(
            "OK: иконка уже присутствует — "
            "файл не изменяется"
        )
        return False

    transformed_bytes = encode_file(
        transformed_text,
        encoding,
    )

    # --------------------------------------------------------
    # DRY RUN
    # --------------------------------------------------------

    if dry_run:

        print(
            "DRY-RUN: файл БУДЕТ изменён"
        )

        print()
        print(
            f'Добавится: '
            f'<img src="{icon_src}" ...>'
        )

        return True

    # --------------------------------------------------------
    # BACKUP
    # --------------------------------------------------------

    backup = make_backup(html_path)

    print(
        f"BACKUP: {backup.name}"
    )

    # --------------------------------------------------------
    # АТОМАРНАЯ ЗАПИСЬ
    # --------------------------------------------------------

    atomic_write(
        html_path,
        transformed_bytes,
    )

    # --------------------------------------------------------
    # ПРОВЕРКА ПОСЛЕ ЗАПИСИ
    # --------------------------------------------------------

    actual_bytes = html_path.read_bytes()

    if actual_bytes != transformed_bytes:
        raise RuntimeError(
            "Проверка записи не пройдена: "
            f"{html_path.relative_to(root)}"
        )

    actual_text, _ = decode_file(
        actual_bytes
    )

    if not is_already_present(
        actual_text,
        icon_src,
    ):
        raise RuntimeError(
            "Иконка не найдена после записи: "
            f"{html_path.relative_to(root)}"
        )

    print(
        "OK: иконка добавлена"
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Добавляет иконки на главные и "
            "городские страницы naprawa-*."
        )
    )

    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help=(
            "Корень сайта "
            "(по умолчанию текущая папка)"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Только показать, "
            "что будет изменено"
        ),
    )

    args = parser.parse_args()

    root = Path(
        args.root
    ).resolve()

    if not root.is_dir():

        print(
            f"ОШИБКА: каталог не найден: {root}"
        )

        return 1

    print("=" * 70)
    print(
        "NAPRAWA AGD — ДОБАВЛЕНИЕ ИКОНОК"
    )
    print("=" * 70)

    print(
        f"Корень сайта: {root}"
    )

    print()

    if args.dry_run:

        print(
            "*** DRY-RUN: реальные файлы "
            "изменяться НЕ будут ***"
        )

        print()

    # --------------------------------------------------------
    # Поиск файлов
    # --------------------------------------------------------

    files = discover_files(root)

    print(
        f"Найдено файлов для проверки: {len(files)}"
    )

    changed_count = 0

    try:

        for html_path, icon in files:

            changed = process_file(
                root=root,
                html_path=html_path,
                icon=icon,
                dry_run=args.dry_run,
            )

            if changed:
                changed_count += 1

    except Exception as exc:

        print()
        print("=" * 70)
        print("ОШИБКА")
        print("=" * 70)

        print(str(exc))

        return 1

    print()
    print("=" * 70)

    if args.dry_run:

        print(
            f"Будет изменено файлов: "
            f"{changed_count}"
        )

    else:

        print(
            f"Изменено файлов: "
            f"{changed_count}"
        )

    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())