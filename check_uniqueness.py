#!/usr/bin/env python3
"""
Скрипт проверки уникальности текстов между всеми HTML-страницами сайта.
Сравнивает страницы по алгоритму шинглирования (Jaccard Similarity).

Запуск:
    python check_uniqueness.py

Результат:
    - Вывод в консоль наименее уникальных страниц.
    - Файл uniqueness_report.json с полным отчетом.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT_DIR = Path(".")
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}
SHINGLE_LEN = 4  # Длина шингла (фраза из N слов)
SIMILARITY_THRESHOLD = 0.60  # Порог дублирования (60% и выше — проблема для SEO)


class HTMLTextExtractor(HTMLParser):
    """Вытаскивает только видимый текст из HTML, игнорируя head, скрипты и стили."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_ignored_tag = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head", "noscript", "svg", "iframe"):
            self.in_ignored_tag += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head", "noscript", "svg", "iframe") and self.in_ignored_tag > 0:
            self.in_ignored_tag -= 1

    def handle_data(self, data):
        if self.in_ignored_tag == 0:
            text = data.strip()
            if text:
                self.result.append(text)

    def get_text(self) -> str:
        return " ".join(self.result)


def clean_text(text: str) -> str:
    """Очищает текст от пунктуации, лишних пробелов и приводит к нижнему регистру."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    return words


def get_shingles(words: list[str], shingle_len: int = SHINGLE_LEN) -> set[str]:
    """Генерирует set шинглов заданной длины."""
    if len(words) < shingle_len:
        return {" ".join(words)}
    return {
        " ".join(words[i:i + shingle_len])
        for i in range(len(words) - shingle_len + 1)
    }


def jaccard_similarity(set1: set, set2: set) -> float:
    """Вычисляет коэффициент сходства Джаккара (от 0.0 до 1.0)."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def find_all_html_files(root: Path) -> list[Path]:
    """Ищет все HTML файлы в проекте, кроме исключенных директорий."""
    html_files = []
    for path in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        html_files.append(path)
    return html_files


def main():
    print("=== АУДИТ УНИКАЛЬНОСТИ СТРАНИЦ САЙТА ===")
    files = find_all_html_files(ROOT_DIR)
    print(f"Найдено HTML-файлов для анализа: {len(files)}\n")

    if not files:
        print("HTML-файлы не найдены.")
        return

    # 1. Сбор и парсинг текстов
    page_data = {}
    print("Извлечение текста и генерация шинглов...")
    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
            parser = HTMLTextExtractor()
            parser.feed(content)
            raw_text = parser.get_text()
            
            words = clean_text(raw_text)
            shingles = get_shingles(words)
            
            page_data[str(path)] = {
                "word_count": len(words),
                "shingles": shingles
            }
        except Exception as e:
            print(f"Ошибка чтения файла {path}: {e}")

    # 2. Сравнение страниц между собой
    print("Сравнение страниц между собой (поиск дублей)...")
    results = []
    keys = list(page_data.keys())
    total_comparisons = len(keys) * (len(keys) - 1) // 2
    processed = 0

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            f1, f2 = keys[i], keys[j]
            s1 = page_data[f1]["shingles"]
            s2 = page_data[f2]["shingles"]

            sim = jaccard_similarity(s1, s2)
            
            if sim >= SIMILARITY_THRESHOLD:
                results.append({
                    "file_1": f1,
                    "file_2": f2,
                    "similarity_percent": round(sim * 100, 2),
                    "unique_percent_1_vs_2": round((1 - sim) * 100, 2)
                })

            processed += 1

    # 3. Сортировка по степени сходства
    results.sort(key=lambda x: -x["similarity_percent"])

    # 4. Вывод критических результатов
    print(f"\nАнализ завершен! Найдено проблемных пар (дублирование >= {int(SIMILARITY_THRESHOLD*100)}%): {len(results)}\n")

    if results:
        print("ТОП-10 самых похожих страниц (высокий риск склейки в Google):")
        print("-" * 75)
        for item in results[:10]:
            print(f"Сходство: {item['similarity_percent']}% (Уникальность: {item['unique_percent_1_vs_2']}%)")
            print(f"  Файл 1: {item['file_1']}")
            print(f"  Файл 2: {item['file_2']}")
            print("-" * 75)

    # 5. Сохранение полного отчета
    report_file = Path("uniqueness_report.json")
    report_data = {
        "total_files_analyzed": len(files),
        "threshold_used": SIMILARITY_THRESHOLD,
        "high_similarity_pairs_count": len(results),
        "pairs": results
    }
    report_file.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nПолный отчет с деталями сохранен в файл: {report_file}")


if __name__ == "__main__":
    main()