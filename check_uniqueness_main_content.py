#!/usr/bin/env python3
"""
Сравнивает страницы ТОЛЬКО по содержательной части — вырезая
<header>, <nav>, <footer>, <script>, <style> перед сравнением.

Если предыдущий отчёт (uniqueness_report.json) считал похожесть по
ВСЕМУ файлу (включая одинаковую навигацию/футер на 630 страницах),
он завышал реальную дубликацию. Этот скрипт даёт куда более честную
картину: что на самом деле отличается в текстах, которые видит и
Google, и живой посетитель, как основной контент страницы.

Требует: pip install beautifulsoup4 --break-system-packages

Запуск:
    python check_uniqueness_main_content.py
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
SIMILARITY_THRESHOLD = 0.5  # показываем пары похожие больше чем на 50%

# Теги, которые считаем "боилерплейтом" — вырезаем перед сравнением
BOILERPLATE_TAGS = ["header", "nav", "footer", "script", "style"]


def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag_name in BOILERPLATE_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Если на странице есть <main> — берём только его, это самый чистый сигнал
    main_tag = soup.find("main")
    if main_tag:
        text = main_tag.get_text(separator=" ", strip=True)
    else:
        text = soup.get_text(separator=" ", strip=True)

    # Схлопываем пробелы
    text = re.sub(r"\s+", " ", text)
    return text


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

    print("Сравниваю пары (это может занять время на 600+ файлах)...\n")

    # Для скорости на больших объёмах сравниваем только файлы с похожей длиной текста
    # (экономия: SequenceMatcher дорогой на больших N^2 сравнениях)
    items = list(texts.items())
    high_similarity_pairs = []

    for (path_a, text_a), (path_b, text_b) in combinations(items, 2):
        # Быстрый предварительный фильтр по длине — если тексты очень разной
        # длины, они точно не похожи, не тратим время на точное сравнение
        len_a, len_b = len(text_a), len(text_b)
        if len_a == 0 or len_b == 0:
            continue
        if min(len_a, len_b) / max(len_a, len_b) < 0.5:
            continue

        sim = similarity(text_a, text_b)
        if sim >= SIMILARITY_THRESHOLD:
            high_similarity_pairs.append((path_a, path_b, sim))

    high_similarity_pairs.sort(key=lambda x: -x[2])

    print(f"Проанализировано файлов: {len(pages)}")
    print(f"Пар с похожестью >= {int(SIMILARITY_THRESHOLD * 100)}% (только осн. контент): "
          f"{len(high_similarity_pairs)}\n")

    for path_a, path_b, sim in high_similarity_pairs[:50]:
        print(f"{sim*100:.1f}%  {path_a}  <->  {path_b}")

    if len(high_similarity_pairs) > 50:
        print(f"\n... и ещё {len(high_similarity_pairs) - 50} пар (показаны первые 50)")

    print(
        "\nЕсли после исключения боилерплейта список сильно короче, чем "
        "в предыдущем отчёте — предыдущая метрика была завышена шаблоном сайта, "
        "а не реальным дублированием контента."
    )


if __name__ == "__main__":
    main()
