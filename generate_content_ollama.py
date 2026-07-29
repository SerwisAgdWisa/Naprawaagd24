import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup  # Если нет, поставь: pip install beautifulsoup4

from tech_facts_db import TECH_FACTS_DB

ROOT_DIR = Path(".")
CACHE_FILE = Path("content_cache.json")
MARKER = "<!-- unique-ai-content-block -->"
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}

OLLAMA_MODEL = "llama3.1:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"

APPLIANCE_NAMES = {
    "naprawa-pralek": "pralki",
    "naprawa-lodowek": "lodówki",
    "naprawa-zmywarek": "zmywarki",
    "naprawa-piekarnikow": "piekarniki",
    "naprawa-suszarek": "suszarki",
    "naprawa-pralko-suszarek": "pralko-suszarki",
}

SYSTEM_PROMPT = """Jesteś copywriterem piszącym krótkie, rzeczowe opisy usług serwisowych AGD po polsku.
ZASADY:
- Pisz WYŁĄCZNIE na podstawie podanych faktów. Nie wymyślaj niczego.
- Długość: 2 krótkie akapity (łącznie 60-90 słów).
- Styl: konkretny, rzeczowy.
- Wspomnij nazwy ulic z listy i konkretny kod błędu/objaw.
- Zwróć WYŁĄCZNIE gotowy tekst w języku polskim."""

def normalize_city_slug(folder_name: str) -> str:
    s = folder_name.strip().lower()
    repl = {"ó": "o", "ą": "a", "ę": "e", "ł": "l", "ż": "z", "ź": "z", "ś": "s", "ć": "c", "ń": "n"}
    for a, b in repl.items():
        s = s.replace(a, b)
    return s

def extract_streets_from_html(html_content: str) -> list[str]:
    """Вытаскивает улицы прямо из HTML файла (ищет упоминания ul. Name)"""
    found = re.findall(r'ul\.\s+([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9\s-]+)', html_content)
    cleaned = [f"ul. {s.strip()}" for s in found if len(s.strip()) > 2]
    return list(set(cleaned))[:5]  # берем первые 5 уникальных улиц

def find_pages(root: Path):
    for appliance_dir in APPLIANCE_NAMES.keys():
        base = root / appliance_dir
        if not base.exists():
            continue
        for path in base.glob("*/*.html"):
            if path.stem == "index":
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            yield appliance_dir, path

def generate_with_ollama(prompt: str) -> str:
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res.get("response", "").strip()

def insert_before_footer(content: str, block_html: str) -> str | None:
    if MARKER in content:
        return None
    idx = content.rfind("</footer>")
    if idx == -1:
        idx = content.rfind("</body>")
        if idx == -1:
            return None
    footer_start = content.rfind("<footer", 0, idx)
    insert_at = footer_start if footer_start != -1 else idx
    return content[:insert_at] + block_html + "\n" + content[insert_at:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Вставить текст в HTML")
    args = parser.parse_args()

    cache = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))

    pages = list(find_pages(ROOT_DIR))
    generated = 0
    applied = 0

    for appliance_dir, path in pages:
        city_slug = normalize_city_slug(path.parent.name)
        brand_slug = path.stem.strip().lower()
        cache_key = f"{appliance_dir}/{city_slug}/{brand_slug}"

        try:
            html_content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if cache_key not in cache:
            # Вытаскиваем улицы из самой страницы!
            streets = extract_streets_from_html(html_content)
            streets_text = ", ".join(streets) if streets else "całe miasto"

            brand_tech = TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)
            if not brand_tech or not brand_tech.get("common_errors"):
                continue

            errors = brand_tech["common_errors"]
            errors_text = "\n".join(
                f"- Kod/Objaw: {e['code']}, przyczyna: {e['cause']}, część: {e['part']}"
                for e in errors
            )

            prompt = f"""DANE:
Miasto: {city_slug.capitalize()}
Ulice z serwisu: {streets_text}
Sprzęt: {APPLIANCE_NAMES[appliance_dir]}
Marka: {brand_slug.capitalize()}
Usterki:
{errors_text}

{SYSTEM_PROMPT}"""

            print(f"[OLLAMA ГЕНЕРАЦИЯ] {path} (Улицы вытащены из страницы)...")
            try:
                text = generate_with_ollama(prompt)
                cache[cache_key] = text
                generated += 1
                CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as e:
                print(f"  Ошибка Ollama (убедись, что Ollama запущена): {e}")
                time.sleep(3)
                continue

        if args.apply:
            paragraphs = "\n".join(f"  <p>{p.strip()}</p>" for p in cache[cache_key].split("\n") if p.strip())
            block_html = f"{MARKER}\n<section class='unique-ai-content'>\n{paragraphs}\n</section>\n"

            new_content = insert_before_footer(html_content, block_html)
            if new_content is not None:
                path.write_text(new_content, encoding="utf-8")
                applied += 1

    print(f"\nГотово! Сгенерировано: {generated}, Вставлено в HTML: {applied}")

if __name__ == "__main__":
    main()