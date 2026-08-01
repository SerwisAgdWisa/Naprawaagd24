#!/usr/bin/env python3
"""
Как check_uniqueness_main_content.py, но вместо списка топ-50 пар
показывает РАСПРЕДЕЛЕНИЕ похожести по диапазонам — чтобы понять,
сколько пар в опасной зоне (90%+), а сколько в относительно
безобидной (50-60%).

Запуск:
    python check_uniqueness_distribution.py
"""

import re
import sys
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Установите: pip install beautifulsoup4 --break-system-packages")
    sys.exit(1)

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}
SIMILARITY_THRESHOLD = 0.5
BOILERPLATE_TAGS = ["header", "nav", "footer", "script", "style"]

BUCKETS = [
    (0.50, 0.60), (0.60, 0.70), (0.70, 0.80),
    (0.80, 0.90), (0.90, 0.95), (0.95, 1.01),
]


def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag_name in BOILERPLATE_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    main_tag = soup.find("main")
    text = main_tag.get_text(separator=" ", strip=True) if main_tag else soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_pages(root: Path):
    for path in root.glob("naprawa-*/*/*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def main():
    pages = list(find_pages(ROOT_DIR))
    if not pages:
        print("Файлы не найдены. Запустите из корня проекта.")
        sys.exit(1)

    print(f"Загружаю и очищаю {len(pages)} файлов...")
    texts = {}
    for path in pages:
        try:
            html = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        texts[path] = extract_main_text(html)

    print("Сравниваю пары...\n")

    items = list(texts.items())
    bucket_counts = {b: 0 for b in BUCKETS}
    bucket_examples = {b: [] for b in BUCKETS}
    index_pairs = 0
    same_brand_pairs = 0
    diff_brand_same_city_pairs = 0
    total_compared_over_threshold = 0

    for (path_a, text_a), (path_b, text_b) in combinations(items, 2):
        len_a, len_b = len(text_a), len(text_b)
        if len_a == 0 or len_b == 0:
            continue
        if min(len_a, len_b) / max(len_a, len_b) < 0.5:
            continue

        sim = similarity(text_a, text_b)
        if sim < SIMILARITY_THRESHOLD:
            continue

        total_compared_over_threshold += 1

        for lo, hi in BUCKETS:
            if lo <= sim < hi:
                bucket_counts[(lo, hi)] += 1
                if len(bucket_examples[(lo, hi)]) < 3:
                    bucket_examples[(lo, hi)].append((sim, path_a, path_b))
                break

        # Классификация типа пары для доп. статистики
        brand_a, city_a = path_a.stem.lower(), path_a.parent.name.lower()
        brand_b, city_b = path_b.stem.lower(), path_b.parent.name.lower()

        if brand_a == "index" and brand_b == "index":
            index_pairs += 1
        elif brand_a == brand_b and city_a != city_b:
            same_brand_pairs += 1
        elif brand_a != brand_b and city_a == city_b:
            diff_brand_same_city_pairs += 1

    print(f"Проанализировано файлов: {len(pages)}")
    print(f"Всего пар с похожестью >= 50%: {total_compared_over_threshold}\n")

    print("=" * 60)
    print("РАСПРЕДЕЛЕНИЕ ПО ДИАПАЗОНАМ ПОХОЖЕСТИ")
    print("=" * 60)
    for lo, hi in BUCKETS:
        label = f"{int(lo*100)}-{int(hi*100) if hi <= 1 else 100}%"
        count = bucket_counts[(lo, hi)]
        bar = "█" * min(count // 20, 60)
        print(f"{label:>10}: {count:>6}  {bar}")

    print("\n" + "=" * 60)
    print("ПРИМЕРЫ ИЗ САМОГО ОПАСНОГО ДИАПАЗОНА (95-100%)")
    print("=" * 60)
    for sim, a, b in bucket_examples[(0.95, 1.01)][:3]:
        print(f"{sim*100:.1f}%  {a}  <->  {b}")
    if not bucket_examples[(0.95, 1.01)]:
        print("(пусто — в этом диапазоне пар нет, это хороший знак)")

    print("\n" + "=" * 60)
    print("КЛАССИФИКАЦИЯ ПАР (среди всех >= 50%)")
    print("=" * 60)
    print(f"index.html <-> index.html (не покрыты AI):        {index_pairs}")
    print(f"Один бренд, разные города (ожидаемо/нормально):    {same_brand_pairs}")
    print(f"Разные бренды, один город (тревожный признак):     {diff_brand_same_city_pairs}")

    if diff_brand_same_city_pairs == 0:
        print(
            "\n0 пар 'разные бренды в одном городе' — значит контент реально "
            "стал бренд-специфичным. Оставшаяся похожесть в основном "
            "объясняется естественным сходством одного бренда между городами "
            "и непокрытыми index.html страницами."
        )


if __name__ == "__main__":
    main()
