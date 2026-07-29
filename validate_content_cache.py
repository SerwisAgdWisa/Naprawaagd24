#!/usr/bin/env python3
"""
Проверяет content_cache.json на "сломанные" записи ПЕРЕД тем, как
вставлять их в HTML через --apply.

Использование:
    python validate_content_cache.py          # Только проверка и отчет
    python validate_content_cache.py --clean  # Проверка + удаление битых ключей из кэша
"""

import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path

CACHE_FILE = Path("content_cache.json")
OUTPUT_FILE = Path("broken_keys.json")

MAX_PHRASE_REPEATS = 4
MIN_WORDS = 60
MAX_WORDS = 350


def find_repeated_phrases(text: str, phrase_len: int = 3) -> list[tuple[str, int]]:
    words = text.split()
    phrases = [
        " ".join(words[i:i + phrase_len])
        for i in range(len(words) - phrase_len + 1)
    ]
    counts = Counter(phrases)
    return [(p, c) for p, c in counts.items() if c > MAX_PHRASE_REPEATS]


def looks_truncated(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    last_char = stripped[-1]
    return last_char not in ".!?\"”"


def main():
    parser = argparse.ArgumentParser(description="Валидация и чистка content_cache.json")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Автоматически удалить найденные проблемные ключи из content_cache.json",
    )
    args = parser.parse_args()

    if not CACHE_FILE.exists():
        print(f"Ошибка: файл {CACHE_FILE} не найден.")
        return

    cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    broken = {}

    for key, text in cache.items():
        issues = []

        word_count = len(text.split())
        if word_count < MIN_WORDS:
            issues.append(f"Слишком короткий текст ({word_count} слов)")
        elif word_count > MAX_WORDS:
            issues.append(f"Слишком длинный текст ({word_count} слов) — возможно зацикливание")

        repeats = find_repeated_phrases(text)
        if repeats:
            top = sorted(repeats, key=lambda x: -x[1])[:3]
            examples = "; ".join(f"'{p}' x{c}" for p, c in top)
            issues.append(f"Повторяющиеся фразы (похоже на зацикливание): {examples}")

        if looks_truncated(text):
            issues.append("Текст обрывается без завершающей точки — возможен обрыв генерации")

        if issues:
            broken[key] = {"issues": issues, "preview": text[-150:]}

    print(f"Всего записей в кэше: {len(cache)}")
    print(f"Проблемных записей: {len(broken)}\n")

    if not broken:
        print("Кэш полностью чист. Ошибок не обнаружено.")
        return

    for key, info in broken.items():
        print(f"КЛЮЧ: {key}")
        for issue in info["issues"]:
            print(f"  - {issue}")
        print(f"  ...конец текста: ...{info['preview']}\n")

    OUTPUT_FILE.write_text(json.dumps(broken, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Детализация проблемных ключей сохранена в {OUTPUT_FILE}")

    if args.clean:
        # Создаем бэкап перед мутацией файла
        backup_file = CACHE_FILE.with_suffix(".json.bak")
        shutil.copy(CACHE_FILE, backup_file)
        print(f"\nСоздан бэкап кэша: {backup_file}")

        # Удаляем битые ключи
        clean_cache = {k: v for k, v in cache.items() if k not in broken}
        CACHE_FILE.write_text(json.dumps(clean_cache, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Успешно удалено ключей: {len(broken)}. Обновленный {CACHE_FILE} сохранен.")
    else:
        print(
            "\nДля автоматического удаления запустите скрипт с флагом --clean:\n"
            "  python validate_content_cache.py --clean"
        )


if __name__ == "__main__":
    main()