#!/usr/bin/env python3
"""
Генерирует уникальный контент для index.html страниц (город + категория
техники, без привязки к бренду) — тех самых 52 пар, что остались похожи
после того, как все брендовые страницы уже покрыты.

Переиспользует инфраструктуру из generate_content_api_v4.py (кэш,
ротация ключей, обработка 429), но с отдельным промптом, заточенным
под категорию+город, а не под конкретный бренд.

Запуск:
    python generate_index_content.py --apply
"""

import logging
import re
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup

from generate_content_api_v4 import (
    GROQ_API_KEYS, GROQ_MODEL, GROQ_TEMP, ROOT_DIR, MARKER_CLASS,
    EXCLUDE_DIRS, APPLIANCE_NAMES, CacheDB, rate_limiter, metrics,
    shutdown_handler, check_api_health, safe_write_file,
    normalize_city_slug, validate_soup, extract_streets_from_soup,
    split_into_paragraphs, get_current_api_key, rotate_api_key,
    current_key_index, InvalidHTMLStructureError, SEOGeneratorError,
)
import requests

# Общие (не бренд-специфичные) симптомы по категориям — используются,
# чтобы страница-хаб тоже имела содержательный, а не просто списочный текст.
CATEGORY_SYMPTOMS = {
    "naprawa-pralek": ["pralka nie wiruje", "nie grzeje wody", "nie pobiera wody", "głośna praca"],
    "naprawa-lodowek": ["lodówka nie chłodzi", "zamarza w środku", "głośna praca sprężarki", "wycieka woda"],
    "naprawa-zmywarek": ["nie myje dokładnie naczyń", "nie pobiera wody", "nie odpompowuje wody", "przecieka"],
    "naprawa-piekarnikow": ["nie grzeje", "nierówne pieczenie", "nie działa termoobieg", "drzwi nie domykają się"],
    "naprawa-suszarek": ["nie grzeje", "nie obraca się bęben", "zbyt długi czas suszenia", "hałasuje"],
    "naprawa-pralko-suszarek": ["pierze ale nie suszy", "nie kończy cyklu suszenia", "głośna praca w suszeniu", "nie grzeje wody"],
}

INDEX_SYSTEM_PROMPT = """Jesteś ekspertem SEO piszącym opisy stron-kategorii dla lokalnego
serwisu AGD w Polsce.
ZASADY:
- Strona dotyczy WSZYSTKICH marek danej kategorii sprzętu w jednym mieście — NIE pisz o
  konkretnej jednej marce.
- Brak wstępów typu "Szukasz serwisu...". Pisz konkretnie i rzeczowo.
- Akapit 1: Jakie typowe usterki tej kategorii sprzętu obsługujecie (wymień podane symptomy).
- Akapit 2: Specyfika obsługi w danym mieście — wymień podane ulice/dzielnice i czas dojazdu.
- Akapit 3: Dlaczego warto zgłosić się do serwisu obsługującego wiele marek (jedna wizyta,
  uniwersalna diagnostyka, częściej dostępne terminy).
- Długość: Ściśle 3 akapity (łącznie 120-160 słów). Zwróć WYŁĄCZNIE gotowy tekst po polsku
  bez formatowania Markdown."""


def generate_with_groq_index(prompt: str) -> str:
    """Копия логики генерации из v4, но с системным промптом под index-страницы."""
    rate_limiter.wait_if_needed()
    metrics.api_calls += 1

    url = "https://api.groq.com/openai/v1/chat/completions"

    for attempt in range(1, len(GROQ_API_KEYS) * 3 + 1):
        api_key = get_current_api_key()
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": INDEX_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": GROQ_TEMP,
            "max_tokens": 300,
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)

            if resp.status_code == 429:
                metrics.api_errors += 1
                retry_header = resp.headers.get("retry-after")
                wait_time = float(retry_header) if retry_header else 15.0
                if len(GROQ_API_KEYS) > 1:
                    logging.warning(f"[429] Ротация + пауза {wait_time:.1f} сек...")
                    rotate_api_key()
                else:
                    logging.warning(f"[429] Ждём {wait_time:.1f} сек...")
                with rate_limiter.lock:
                    rate_limiter.requests.clear()
                time.sleep(wait_time)
                continue

            resp.raise_for_status()
            data = resp.json()
            if not data.get("choices"):
                raise SEOGeneratorError("API вернул пустые данные.")

            result_text = data["choices"][0]["message"]["content"].strip()
            usage = data.get("usage", {})
            metrics.total_tokens_est += usage.get("total_tokens", len(prompt.split()) + len(result_text.split()))
            return result_text

        except Exception as e:
            metrics.api_errors += 1
            if attempt == len(GROQ_API_KEYS) * 3:
                raise SEOGeneratorError(f"Сбой API после всех попыток: {e}") from e
            rotate_api_key()
            time.sleep(2)

    raise SEOGeneratorError("Неизвестная ошибка связи с API.")


def extract_brands_from_index(soup: BeautifulSoup) -> list[str]:
    """Собирает названия брендов, перечисленных на странице-хабе (из ссылок)."""
    brands = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        m = re.search(r'/?([a-z0-9-]+)\.html$', href.lower())
        if m and m.group(1) not in ("index",):
            name = m.group(1).replace("-", " ").title()
            if name not in brands:
                brands.append(name)
    return brands[:10]


def update_index_dom(soup: BeautifulSoup, generated_text: str, appliance: str, city: str) -> BeautifulSoup:
    for old_tag in soup.find_all(["section", "div"], class_=["local-info", MARKER_CLASS]):
        old_tag.decompose()

    paragraphs_list = split_into_paragraphs(generated_text)
    paragraphs_html = "".join(f"<p>{p}</p>" for p in paragraphs_list)
    h2_title = f"Serwis {appliance} wszystkich marek w {city.capitalize()}"

    new_block_html = f"""
    <section class="{MARKER_CLASS}" style="padding: 25px; background: #f8f9fa; border-radius: 8px; margin: 30px 0;">
        <div class="container">
            <h2 style="font-size: 1.4rem; margin-bottom: 15px;">{h2_title}</h2>
            {paragraphs_html}
        </div>
    </section>
    """
    new_section = BeautifulSoup(new_block_html, "html.parser").find("section")

    main_tag = soup.find("main")
    if main_tag:
        main_tag.append(new_section)
    else:
        footer_tag = soup.find("footer")
        if footer_tag:
            footer_tag.insert_before(new_section)
        elif soup.body:
            soup.body.append(new_section)
    return soup


def find_index_pages(root: Path):
    for appliance_dir in APPLIANCE_NAMES.keys():
        base = root / appliance_dir
        if not base.exists():
            continue
        for path in base.glob("*/index.html"):
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            yield appliance_dir, path


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not GROQ_API_KEYS:
        logging.critical("GROQ_API_KEYS не задан в .env!")
        sys.exit(1)

    logging.info("Выполнение Health-Check для Groq API...")
    if not check_api_health():
        logging.critical("Health-Check НЕ ПРОЙДЕН.")
        sys.exit(1)
    logging.info("Health-Check успешно пройден!")

    db = CacheDB()
    pages = list(find_index_pages(ROOT_DIR))
    logging.info(f"Найдено {len(pages)} index.html страниц")

    generated = applied = errors = 0

    for appliance_dir, path in pages:
        if shutdown_handler.shutdown_requested:
            logging.warning("Прервано пользователем.")
            break

        city_slug = normalize_city_slug(path.parent.name)
        cache_key = f"{appliance_dir}/{city_slug}/index"

        try:
            html_content = path.read_text(encoding="utf-8")
            soup = BeautifulSoup(html_content, "html.parser")
            validate_soup(soup)
        except Exception as e:
            logging.error(f"Ошибка HTML в {path}: {e}")
            errors += 1
            continue

        cached_text = db.get(cache_key)

        if not cached_text:
            symptoms = CATEGORY_SYMPTOMS.get(appliance_dir, [])
            symptoms_text = ", ".join(symptoms)
            streets = extract_streets_from_soup(soup)
            streets_text = ", ".join(streets) if streets else "całe miasto i okolice"
            brands = extract_brands_from_index(soup)
            brands_text = ", ".join(brands) if brands else "wszystkich popularnych marek"

            prompt = f"""DANE:
Miasto: {city_slug.capitalize()}
Kategoria sprzętu: {APPLIANCE_NAMES[appliance_dir]}
Typowe usterki tej kategorii: {symptoms_text}
Obsługiwane ulice/dzielnice: {streets_text}
Obsługiwane marki na tej stronie: {brands_text}

Napisz 3 akapity dla strony kategorii "{APPLIANCE_NAMES[appliance_dir]}" w mieście {city_slug.capitalize()}."""

            try:
                text = generate_with_groq_index(prompt)
                db.set(cache_key, text)
                cached_text = text
                generated += 1
                logging.info(f"[СГЕНЕРИРОВАНО] {path}")
            except Exception as e:
                logging.error(f"Не удалось сгенерировать для {path}: {e}")
                errors += 1
                continue

        if args.apply and cached_text:
            try:
                updated_soup = update_index_dom(soup, cached_text, APPLIANCE_NAMES[appliance_dir], city_slug)
                safe_write_file(path, str(updated_soup))
                applied += 1
                logging.info(f"[ЗАПИСАНО] {path}")
            except Exception as e:
                logging.error(f"Не удалось записать {path}: {e}")
                errors += 1

    logging.info(f"\nВсего: {len(pages)}, сгенерировано: {generated}, записано: {applied}, ошибок: {errors}")


if __name__ == "__main__":
    main()
