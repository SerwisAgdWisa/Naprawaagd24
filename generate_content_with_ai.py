#!/usr/bin/env python3
"""
ШАГ 3: Генерирует уникальный абзац контента для каждой страницы
naprawa-{urzadzenie}/{miasto}/{marka}.html, используя:
  - реальные гео-данные из geo_data.json (шаг 1, fetch_geo_data.py)
  - реальные технические факты из tech_facts_db.py (шаг 2)
  - Claude API — который пишет связный текст СТРОГО на основе этих фактов
    (не выдумывает ничего от себя — факты фиксированы в промпте)

Результат кэшируется в content_cache.json — при повторном запуске
уже сгенерированные страницы не будут пересозданы (и не потратите
API-вызовы повторно). Чтобы перегенерировать — удалите нужный ключ
из content_cache.json вручную.

Требования:
    pip install anthropic --break-system-packages
    export ANTHROPIC_API_KEY=sk-ant-...

Запуск:
    python generate_content_with_ai.py            # сухой прогон (генерирует
                                                       и сохраняет в кэш, но НЕ
                                                       вставляет в html)
    python generate_content_with_ai.py --apply     # вставляет в html-файлы
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Установите библиотеку: pip install anthropic --break-system-packages")
    sys.exit(1)

from tech_facts_db import TECH_FACTS_DB

ROOT_DIR = Path(".")
GEO_DATA_FILE = Path("geo_data.json")
CACHE_FILE = Path("content_cache.json")
MARKER = "<!-- unique-ai-content-block -->"
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}

APPLIANCE_NAMES = {
    "naprawa-pralek": "pralki",
    "naprawa-lodowek": "lodówki",
    "naprawa-zmywarek": "zmywarki",
    "naprawa-piekarnikow": "piekarniki",
    "naprawa-suszarek": "suszarki",
    "naprawa-pralko-suszarek": "pralko-suszarki",
}

SYSTEM_PROMPT = """Jesteś copywriterem piszącym krótkie, rzeczowe opisy usług serwisowych
AGD po polsku dla strony lokalnego serwisu naprawy sprzętu.

ZASADY:
- Pisz WYŁĄCZNIE na podstawie podanych faktów. Nie wymyślaj żadnych dodatkowych
  informacji, cen, adresów ani danych technicznych.
- Długość: 2 krótkie akapity (łącznie 60-90 słów).
- Styl: konkretny, rzeczowy, bez zbędnego marketingowego lania wody,
  bez wykrzykników, bez fraz w stylu "najlepszy serwis w mieście".
- Wspomnij realne nazwy ulic/dzielnic podane w danych — naturalnie, nie jako
  spis, tylko wplecione w zdanie.
- Wspomnij przynajmniej jeden konkretny kod błędu i jego przyczynę z podanych
  danych technicznych.
- Zwróć WYŁĄCZNIE gotowy tekst (bez nagłówków, bez cudzysłowów, bez komentarzy)."""


def normalize_city_slug(folder_name: str) -> str:
    s = folder_name.strip().lower()
    repl = {"ó": "o", "ą": "a", "ę": "e", "ł": "l", "ż": "z", "ź": "z", "ś": "s", "ć": "c", "ń": "n"}
    for a, b in repl.items():
        s = s.replace(a, b)
    return s


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


def build_prompt(appliance_dir: str, city_data: dict, brand_slug: str) -> str | None:
    appliance_name = APPLIANCE_NAMES[appliance_dir]
    brand_display = brand_slug.replace("-", " ").title()

    brand_tech = TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)
    if not brand_tech or not brand_tech.get("common_errors"):
        return None  # нет технических фактов — не генерируем текст "из воздуха"

    errors = brand_tech["common_errors"]
    errors_text = "\n".join(
        f"- Kod {e['code']}: przyczyna — {e['cause']}; wymieniana część — {e['part']} "
        f"(koszt części: {e['price_range_pln']} zł)"
        for e in errors
    )

    streets = city_data.get("streets", [])
    streets_text = ", ".join(streets[:6]) if streets else "brak danych o ulicach"

    prompt = f"""DANE DO WYKORZYSTANIA:

Miasto: {city_data['display_name'].split(',')[0]}
Przykładowe ulice/rejony w mieście: {streets_text}
Kod pocztowy: {city_data.get('postcode', 'brak danych')}

Urządzenie: {appliance_name}
Marka: {brand_display}

Typowe usterki i koszty:
{errors_text}

Napisz opis usługi naprawy {appliance_name} marki {brand_display} w tym mieście,
zgodnie z zasadami systemowymi."""

    return prompt


def generate_content(client: "anthropic.Anthropic", prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text").strip()


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
    parser.add_argument("--apply", action="store_true", help="Вставить сгенерированный текст в html-файлы")
    args = parser.parse_args()

    if not GEO_DATA_FILE.exists():
        print(f"Не найден {GEO_DATA_FILE}. Сначала запустите fetch_geo_data.py")
        sys.exit(1)

    geo_data = json.loads(GEO_DATA_FILE.read_text(encoding="utf-8"))
    cache = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))

    client = anthropic.Anthropic()  # берёт ключ из переменной окружения ANTHROPIC_API_KEY

    pages = list(find_pages(ROOT_DIR))
    if not pages:
        print("Файлы не найдены. Запустите из корня проекта.")
        sys.exit(1)

    generated = 0
    skipped_no_geo = 0
    skipped_no_tech = 0
    applied = 0

    for appliance_dir, path in pages:
        city_slug = normalize_city_slug(path.parent.name)
        brand_slug = path.stem.strip().lower()
        cache_key = f"{appliance_dir}/{city_slug}/{brand_slug}"

        city_data = geo_data.get(city_slug)
        if city_data is None:
            skipped_no_geo += 1
            continue

        if cache_key not in cache:
            prompt = build_prompt(appliance_dir, city_data, brand_slug)
            if prompt is None:
                skipped_no_tech += 1
                print(f"[НЕТ ТЕХ. ФАКТОВ, пропущен] {path}")
                continue

            print(f"[ГЕНЕРАЦИЯ] {path} ...")
            try:
                text = generate_content(client, prompt)
            except Exception as e:
                print(f"  ОШИБКА API: {e}")
                continue

            cache[cache_key] = text
            generated += 1
            # сохраняем прогрессивно
            CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

        if args.apply:
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            paragraphs = "\n".join(f"  <p>{p.strip()}</p>" for p in cache[cache_key].split("\n") if p.strip())
            block_html = f"{MARKER}\n<section class='unique-ai-content'>\n{paragraphs}\n</section>\n"

            new_content = insert_before_footer(content, block_html)
            if new_content is not None:
                path.with_suffix(path.suffix + ".bak").write_text(content, encoding="utf-8")
                path.write_text(new_content, encoding="utf-8")
                applied += 1
                print(f"[ВСТАВЛЕН В HTML] {path}")

    print("\n--- Итог ---")
    print(f"Всего страниц:                {len(pages)}")
    print(f"Сгенерировано новых текстов:  {generated}")
    print(f"Пропущено (нет гео-данных):   {skipped_no_geo}")
    print(f"Пропущено (нет тех. фактов):  {skipped_no_tech}")
    if args.apply:
        print(f"Вставлено в html:             {applied}")
    else:
        print("\nЭто был сухой прогон (только генерация + кэш).")
        print("Проверьте content_cache.json, затем запустите с --apply")
        print("чтобы вставить текст в html-файлы.")


if __name__ == "__main__":
    main()
