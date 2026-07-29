import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_main_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Вырезаем шапку, футер, навигацию, скрипты и стили (сквозной шум)
    for element in soup(["header", "footer", "nav", "script", "style", "aside"]):
        element.decompose()
        
    # Ищем смысловой блок
    main_content = soup.find('main')
    if main_content:
        text = main_content.get_text(separator=' ')
    else:
        text = soup.body.get_text(separator=' ') if soup.body else soup.get_text(separator=' ')
        
    # Чистим пробелы
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("Собираем файлы...")
pages = list(Path(".").glob("naprawa-*/*/*.html"))

documents = []
file_paths = []

for path in pages:
    if path.stem == "index":
        continue
    try:
        html = path.read_text(encoding="utf-8")
        clean_text = get_main_text(html)
        if len(clean_text) > 50:
            documents.append(clean_text)
            file_paths.append(str(path))
    except Exception:
        continue

print(f"Найдено {len(documents)} текстовых блоков. Считаем TF-IDF сходство...")

if len(documents) < 2:
    print("Ошибка: Найдено меньше 2 файлов для сравнения. Проверь, из той ли папки запускаешь скрипт.")
    exit()

vectorizer = TfidfVectorizer().fit_transform(documents)
cosine_sim = cosine_similarity(vectorizer, vectorizer)

results = []
for i in range(len(file_paths)):
    for j in range(i + 1, len(file_paths)):
        sim = cosine_sim[i][j]
        if sim > 0.4:  # Порог 40%
            results.append((file_paths[i], file_paths[j], sim))

results.sort(key=lambda x: x[2], reverse=True)

print("\n" + "="*60)
print(" ТОП СОВПАДЕНИЙ ПО ЧИСТОМУ ТЕКСТУ (БЕЗ ШАПКИ И ФУТЕРА)")
print("="*60)

if not results:
    print(" Поздравляю! Совпадений выше 40% по чистому тексту НЕ НАЙДЕНО.")
else:
    for file1, file2, score in results[:15]:
        print(f"{score*100:.2f}% | {file1} <---> {file2}")