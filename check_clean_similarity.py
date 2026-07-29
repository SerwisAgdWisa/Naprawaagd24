import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Функция извлечения ТОЛЬКО основного текста
def get_main_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Удаляем сквозные блоки, которые одинаковы на всех страницах
    for element in soup(["header", "footer", "nav", "script", "style", "aside"]):
        element.decompose()
        
    # Ищем основной контент (если есть main, берем его, иначе всё оставшееся тело)
    main_content = soup.find('main')
    if main_content:
        text = main_content.get_text(separator=' ')
    else:
        text = soup.body.get_text(separator=' ') if soup.body else soup.get_text(separator=' ')
        
    # Очистка от лишних пробелов и переносов
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 2. Сбор всех страниц вида naprawa-*/*/*.html
pages = list(Path(".").glob("naprawa-*/*/*.html"))
documents = []
file_paths = []

print(f"Сбор данных из {len(pages)} файлов...")
for path in pages:
    if path.stem == "index":
        continue
    try:
        html = path.read_text(encoding="utf-8")
        clean_text = get_main_text(html)
        if len(clean_text) > 50: # Игнорируем пустые файлы
            documents.append(clean_text)
            file_paths.append(str(path))
    except Exception as e:
        continue

# 3. Расчет TF-IDF и косинусного сходства (как это делает Google)
print("Расчет TF-IDF сходства чистого контента...")
vectorizer = TfidfVectorizer().fit_transform(documents)
cosine_sim = cosine_similarity(vectorizer, vectorizer)

# 4. Вывод топ-10 самых похожих страниц
results = []
for i in range(len(file_paths)):
    for j in range(i + 1, len(file_paths)):
        sim = cosine_sim[i][j]
        if sim > 0.5: # Порог 50%
            results.append((file_paths[i], file_paths[j], sim))

results.sort(key=lambda x: x[2], reverse=True)

print("\n--- ТОП СОВПАДЕНИЙ ПО ЧИСТОМУ ТЕКСТУ ---")
for file1, file2, score in results[:15]:
    print(f"{score*100:.2f}% | {file1} <---> {file2}")