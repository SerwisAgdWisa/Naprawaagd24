#!/usr/bin/env python3
"""
Находит в content_cache.db записи, обрезанные на полуслове (нет
завершающей точки/знака в конце текста) — обычно из-за старого
max_tokens=350 — и удаляет именно их из кэша.

После удаления просто запустите generate_content_api_v4.py --apply
заново: удалённые ключи перегенерируются с исправленным max_tokens=550,
остальные (нормальные) записи в кэше не тронутся.

Запуск:
    python clean_truncated_cache.py            # сухой прогон — только покажет список
    python clean_truncated_cache.py --apply     # реально удалит найденные ключи
"""

import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path("content_cache.db")


def looks_truncated(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    return stripped[-1] not in ".!?\"”)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Не найден {DB_PATH}. Запустите из корня проекта.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT key, value FROM cache")
    rows = cur.fetchall()

    truncated_keys = [key for key, value in rows if looks_truncated(value)]

    print(f"Всего записей в кэше: {len(rows)}")
    print(f"Обрезанных (без знака в конце): {len(truncated_keys)}\n")

    for key in truncated_keys:
        print(f"  - {key}")

    if args.apply and truncated_keys:
        conn.executemany("DELETE FROM cache WHERE key = ?", [(k,) for k in truncated_keys])
        conn.commit()
        print(f"\nУдалено {len(truncated_keys)} записей из кэша.")
        print("Теперь запустите: python generate_content_api_v4.py --apply")
    elif truncated_keys:
        print("\nЭто сухой прогон. Чтобы удалить — запустите с --apply")
    else:
        print("Обрезанных записей не найдено — всё чисто.")

    conn.close()


if __name__ == "__main__":
    main()
