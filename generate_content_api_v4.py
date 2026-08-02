import argparse
import json
import logging
import os
import random
import signal
import sqlite3
import sys
import threading
import time
import unicodedata
from contextlib import closing
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from tqdm import tqdm

from tech_facts_db import TECH_FACTS_DB
try:
    from auto_tech_facts_db import AUTO_TECH_FACTS_DB
except ImportError:
    AUTO_TECH_FACTS_DB = {}
try:
    from tech_facts_db_extra import TECH_FACTS_DB_EXTRA
except ImportError:
    TECH_FACTS_DB_EXTRA = {}

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("seo_generator.log", encoding="utf-8")
    ]
)

raw_keys = os.getenv("GROQ_API_KEYS", os.getenv("GROQ_API_KEY", ""))
GROQ_API_KEYS = [k.strip() for k in raw_keys.split(",") if k.strip()]
current_key_index = 0

def get_current_api_key() -> str:
    global current_key_index
    if not GROQ_API_KEYS:
        return ""
    return GROQ_API_KEYS[current_key_index % len(GROQ_API_KEYS)]

def rotate_api_key():
    global current_key_index
    if len(GROQ_API_KEYS) > 1:
        current_key_index = (current_key_index + 1) % len(GROQ_API_KEYS)
        logging.info(f"Переключение на API ключ #{current_key_index + 1}")

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TEMP = float(os.getenv("GROQ_TEMPERATURE", "0.45"))
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "12"))
DB_PATH = Path(os.getenv("CACHE_DB_PATH", "content_cache.db"))
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "https://naprawaagd24.pl")

ROOT_DIR = Path(".")

BRAND_DISPLAY_NAMES = {
    "elektrolux": "Electrolux",
    "gorenie": "Gorenje",
}

def brand_display_name(brand_slug: str) -> str:
    return BRAND_DISPLAY_NAMES.get(brand_slug, brand_slug.replace("-", " ").title())

MARKER_CLASS = "unique-ai-content"
EXCLUDE_DIRS = {".git", "node_modules", ".vscode"}

APPLIANCE_NAMES = {
    "naprawa-pralek": "pralki",
    "naprawa-lodowek": "lodówki",
    "naprawa-zmywarek": "zmywarki",
    "naprawa-piekarnikow": "piekarniki",
    "naprawa-suszarek": "suszarki",
    "naprawa-pralko-suszarek": "pralko-suszarki",
}

DEFAULT_FALLBACK_ERRORS = [
    {"code": "E01 / F01", "cause": "Błąd blokady drzwi lub czujnika zamknięcia", "part": "blokada drzwi / moduł"},
    {"code": "E02 / F02", "cause": "Problem z dopływem wody lub zaworem ssącym", "part": "elektrozawór / filtr"},
    {"code": "E03 / F03", "cause": "Problem z odpływem wody lub zablokowana pompa", "part": "pompa odpływowa / filtr"},
    {"code": "E04 / F04", "cause": "Weryfikacja obwodu grzania i czujnika NTC", "part": "grzałka / czujnik NTC"},
    {"code": "E05 / F05", "cause": "Usterka silnika lub zużycie szczotek węglowych", "part": "szczotki silnika / prądniczka"}
]

PERSPECTIVES = [
    "Jesteś inżynierem elektronikiem specjalizującym się w modułach sterujących AGD.",
    "Jesteś praktycznym mobilnym serwisantem AGD z 15-letnim doświadczeniem w terenie.",
    "Jesteś kierownikiem warsztatu naprawczego AGD w Polsce.",
    "Jesteś specjalistą ds. diagnostyki usterek mechanicznych i hydraulicznych sprzętu AGD."
]

class SEOGeneratorError(Exception): pass
class APIRateLimitError(SEOGeneratorError): pass
class InvalidHTMLStructureError(SEOGeneratorError): pass

class GracefulShutdown:
    def __init__(self):
        self.shutdown_requested = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        logging.warning(f"\n[ВНИМАНИЕ] Получен сигнал прерывания ({signum}). Завершаем текущие операции...")
        self.shutdown_requested = True

shutdown_handler = GracefulShutdown()

class CacheDB:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def get(self, key: str) -> str | None:
        with closing(sqlite3.connect(self.db_path)) as conn:
            cur = conn.execute("SELECT value FROM cache WHERE key = ?", (key,))
            row = cur.fetchone()
            return row[0] if row else None

    def set(self, key: str, value: str):
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.execute("INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)", (key, value))
            conn.commit()

class RateLimiter:
    def __init__(self, max_requests_per_minute: int = RATE_LIMIT):
        self.max_requests = max_requests_per_minute
        self.requests = []
        self.lock = threading.Lock()

    def wait_if_needed(self):
        with self.lock:
            now = time.time()
            self.requests = [t for t in self.requests if now - t < 60]
            if len(self.requests) >= self.max_requests:
                sleep_time = 60 - (now - self.requests[0])
                if sleep_time > 0:
                    logging.info(f"[RateLimiter] Защита API. Пауза {sleep_time:.1f} сек...")
                    time.sleep(sleep_time)
            self.requests.append(time.time())

class Metrics:
    def __init__(self):
        self.total_pages = 0
        self.generated = 0
        self.applied = 0
        self.errors = 0
        self.api_calls = 0
        self.api_errors = 0
        self.total_tokens_est = 0
        self.start_time = time.time()

    def estimate_cost(self) -> float:
        return (self.total_tokens_est / 1000) * 0.0001

    def report(self):
        duration = time.time() - self.start_time
        logging.info(f"""
        ═══════════════════════════════════════
        СТАТИСТИКА ОБРАБОТКИ
        ═══════════════════════════════════════
        Всего страниц:       {self.total_pages}
        Сгенерировано AI:    {self.generated}
        Записано в HTML:     {self.applied}
        Ошибок:              {self.errors}
        Вызовов API:         {self.api_calls} (Ошибок API: {self.api_errors})
        Оценка токенов:      ~{self.total_tokens_est}
        Оценка стоимости:    ~${self.estimate_cost():.5f}
        Время выполнения:    {duration:.1f} сек.
        ═══════════════════════════════════════
        """)

rate_limiter = RateLimiter()
metrics = Metrics()

def check_api_health() -> bool:
    if not GROQ_API_KEYS:
        logging.critical("Переменная GROQ_API_KEYS не найдена или пуста в .env!")
        return False
    try:
        first_key = get_current_api_key()
        resp = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {first_key}"},
            timeout=10
        )
        return resp.status_code == 200
    except Exception as e:
        logging.error(f"Health-check error: {e}")
        return False

def safe_write_file(path: Path, content: str):
    backup_path = path.with_suffix(path.suffix + ".bak")
    try:
        if path.exists():
            os.replace(path, backup_path)
        
        path.write_text(content, encoding="utf-8", errors="replace")
        
        if backup_path.exists():
            backup_path.unlink()
    except Exception as e:
        if backup_path.exists():
            os.replace(backup_path, path)
        raise SEOGeneratorError(f"Сбой записи в {path}: {e}") from e

def split_into_paragraphs(text: str) -> list[str]:
    if '\n\n' in text:
        p = [p.strip() for p in text.split('\n\n') if p.strip()]
        if len(p) == 3: return p
    if '\n' in text:
        p = [p.strip() for p in text.split('\n') if p.strip()]
        if len(p) == 3: return p

    sentences = text.split('. ')
    paragraphs, current = [], []
    for sent in sentences:
        current.append(sent)
        if len(current) >= 3:
            paragraphs.append('. '.join(current).rstrip('.') + '.')
            current = []
    if current:
        paragraphs.append('. '.join(current).rstrip('.') + '.')
    return paragraphs[:3]

def normalize_city_slug(folder_name: str) -> str:
    text = unicodedata.normalize('NFD', folder_name.strip().lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    replacements = {"ł": "l", "đ": "d"}
    for a, b in replacements.items():
        text = text.replace(a, b)
    return text

def validate_soup(soup: BeautifulSoup) -> bool:
    if not soup.find('html') or not soup.find('body'):
        raise InvalidHTMLStructureError("Критическая ошибка: отсутствует <html> или <body>")
    return True

def extract_streets_from_soup(soup: BeautifulSoup) -> list[str]:
    streets_or_districts = []
    meta_geo = soup.find('meta', {'name': 'geo.placename'})
    if meta_geo and meta_geo.get('content'):
        streets_or_districts.append(meta_geo['content'])

    for card in soup.find_all('div', class_='city-card'):
        p_tag = card.find('p')
        if p_tag and len(p_tag.text.strip()) > 2:
            streets_or_districts.append(p_tag.text.strip())

    for element in soup.find_all(['p', 'li', 'span']):
        text = element.get_text()
        if 'ul.' in text or 'al.' in text:
            words = text.split()
            for i, word in enumerate(words):
                if word in ['ul.', 'al.'] and i + 1 < len(words):
                    streets_or_districts.append(f"{word} {words[i+1]}".strip(',.'))

    unique_items = list(dict.fromkeys(streets_or_districts))
    return unique_items[:5]

EXISTING_CONTENT_CLASSES = [
    'local-info', MARKER_CLASS,
    'symptoms-table', 'faq-item',
    'expertise-box', 'service-card',
]

def extract_existing_seo_text(soup: BeautifulSoup) -> str:
    extracted = []
    for tag in soup.find_all(['section', 'div', 'table'], class_=EXISTING_CONTENT_CLASSES):
        text = tag.get_text(separator=' ', strip=True)
        if text:
            extracted.append(text)

    if not extracted:
        main_tag = soup.find('main')
        if main_tag:
            text = main_tag.get_text(separator=' ', strip=True)
            if text:
                extracted.append(text)

    combined = " ".join(extracted)
    return combined[:1200] + "..." if len(combined) > 1200 else combined

def ensure_canonical_tag(soup: BeautifulSoup, rel_path: Path) -> BeautifulSoup:
    clean_url = f"{SITE_DOMAIN}/{rel_path.as_posix()}"
    head = soup.find('head')
    if head:
        existing_canonical = head.find('link', {'rel': 'canonical'})
        if existing_canonical:
            existing_canonical['href'] = clean_url
        else:
            new_tag = soup.new_tag('link', rel='canonical', href=clean_url)
            head.append(new_tag)
    return soup

def generate_with_groq(prompt: str, system_prompt: str, model: str = GROQ_MODEL, temp: float = GROQ_TEMP) -> str:
    rate_limiter.wait_if_needed()
    metrics.api_calls += 1

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    for attempt in range(1, len(GROQ_API_KEYS) * 3 + 1):
        api_key = get_current_api_key()
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            "temperature": temp,
            "max_tokens": 550
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if resp.status_code == 429:
                metrics.api_errors += 1
                retry_header = resp.headers.get("retry-after")
                wait_time = float(retry_header) if retry_header else 15.0

                if len(GROQ_API_KEYS) > 1:
                    logging.warning(
                        f"[429 Rate Limit] Ключ #{current_key_index + 1} исчерпан. "
                        f"Ротация + пауза {wait_time:.1f} сек..."
                    )
                    rotate_api_key()
                else:
                    logging.warning(f"[429 Rate Limit] Ждём {wait_time:.1f} сек...")

                with rate_limiter.lock:
                    rate_limiter.requests.clear()
                time.sleep(wait_time)
                continue
            
            resp.raise_for_status()
            data = resp.json()

            if not data.get("choices"):
                raise SEOGeneratorError("API вернул пустые данные 'choices'.")

            result_text = data["choices"][0]["message"]["content"].strip()
            
            usage = data.get("usage", {})
            metrics.total_tokens_est += usage.get("total_tokens", len(prompt.split()) + len(result_text.split()))

            return result_text

        except Exception as e:
            metrics.api_errors += 1
            if attempt == len(GROQ_API_KEYS) * 3:
                raise APIRateLimitError(f"Сбой Groq API после всех попыток: {e}") from e
            rotate_api_key()
            time.sleep(2)
            
    raise SEOGeneratorError("Неизвестная ошибка связи с API.")

def update_html_dom(soup: BeautifulSoup, generated_text: str, appliance: str, city: str, brand: str) -> BeautifulSoup:
    # 1. Удаляем старые генерированные AI-блоки
    for old_tag in soup.find_all(['section', 'div'], class_=['local-info', MARKER_CLASS]):
        old_tag.decompose()

    # 2. Вставляем СВЕЖИЙ AI-контент перед футером или в конец main
    paragraphs = split_into_paragraphs(generated_text)
    p_html = "".join(f"<p style='margin-bottom: 1rem;'>{p}</p>" for p in paragraphs)
    
    new_section_html = f"""
    <section class="{MARKER_CLASS}" style="background: #1a1d20; padding: 2rem; border-radius: 12px; margin: 2rem 0; color: #e1e1e1;">
        <h3 style="color: #3b82f6; margin-bottom: 1rem;">Specyfika serwisu {brand_display_name(brand)} w mieście {city.capitalize()}</h3>
        {p_html}
    </section>
    """
    new_section_soup = BeautifulSoup(new_section_html, 'html.parser')

    main_tag = soup.find('main')
    if main_tag:
        main_tag.append(new_section_soup)
    else:
        soup.body.append(new_section_soup)

    # 3. Безопасная замена мусорных списков ошибок (ПОЛНЫЙ ИСПРАВЛЕННЫЙ МЕХАНИЗМ)
    appliance_type = APPLIANCE_NAMES.get(appliance, appliance)
    errors_list = None
    for db in [TECH_FACTS_DB, AUTO_TECH_FACTS_DB, TECH_FACTS_DB_EXTRA]:
        if isinstance(db, dict) and brand in db:
            val = db[brand]
            if isinstance(val, list):
                errors_list = val
                break
            if isinstance(val, dict):
                for sub_key in [appliance, appliance_type]:
                    if sub_key in val and isinstance(val[sub_key], dict) and "common_errors" in val[sub_key]:
                        errors_list = val[sub_key]["common_errors"]
                        break
                if errors_list:
                    break
                for sub_k, sub_v in val.items():
                    if isinstance(sub_v, dict) and "common_errors" in sub_v:
                        errors_list = sub_v["common_errors"]
                        break
        if errors_list:
            break

    if not errors_list:
        errors_list = DEFAULT_FALLBACK_ERRORS

    # Расширенный список маркеров фейкового/мусорного текста
    garbage_markers = [
        'awaria układu', 'wymaga diagnozy', 'błąd systemowy', 
        'test komputerowy', 'sprawdzenie drożności', 'ułożenie wiązki'
    ]
    
    for ul in soup.find_all(['ul', 'ol']):
        ul_classes = ul.get('class', [])
        ul_text = ul.get_text().lower()
        
        # Точное обнаружение: если есть класс 'error-codes-list' ИЛИ совпадает мусорный текст
        is_garbage = 'error-codes-list' in ul_classes or any(marker in ul_text for marker in garbage_markers)
        
        if is_garbage:
            new_lis = []
            for err in errors_list[:8]:
                code = err.get('code', 'Błąd')
                cause = err.get('cause', 'Wymaga weryfikacji')
                part = err.get('part', 'diagnostyka')
                new_lis.append(
                    f"<li><strong>Kod {code}</strong> – {cause} "
                    f"<span style='color: #9da5b1; font-size: 0.9rem;'>(kontrola: {part})</span>.</li>"
                )
            
            ul_class_str = f" class=\"{' '.join(ul_classes)}\"" if ul_classes else ""
            new_ul_html = f"<ul{ul_class_str}>\n" + "\n".join(new_lis) + "\n</ul>"
            
            ul.clear()
            for child in BeautifulSoup(new_ul_html, 'html.parser').children:
                ul.append(child)

    return soup

def find_pages_generator(root: Path):
    for appliance_dir in APPLIANCE_NAMES.keys():
        base = root / appliance_dir
        if not base.exists(): continue
        for path in base.rglob("*.html"):
            if path.stem == "index" or any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            yield appliance_dir, path

def main():
    parser = argparse.ArgumentParser(description="Industrial Grade SEO Content Generator.")
    parser.add_argument("--apply", action="store_true", help="Записать изменения в HTML-файлы")
    parser.add_argument("--dry-run", action="store_true", help="Симуляция без записи файлов и генерации")
    parser.add_argument("--force", action="store_true", help="Игнорировать кэш и сгенерировать заново")
    args = parser.parse_args()

    if not GROQ_API_KEYS:
        logging.critical("Переменная GROQ_API_KEYS не задана в .env!")
        sys.exit(1)

    logging.info("Выполнение Health-Check для Groq API...")
    if not check_api_health():
        logging.critical("Health-Check НЕ ПРОЙДЕН. Groq API недоступен или неверный ключ.")
        sys.exit(1)
    logging.info("Health-Check успешно пройден!")

    db = CacheDB()
    pages = list(find_pages_generator(ROOT_DIR))

    for appliance_dir, path in tqdm(pages, desc="Обработка страниц", unit="page"):
        if shutdown_handler.shutdown_requested:
            logging.warning("Работа прервана пользователем. Сохраняем статистику...")
            break

        metrics.total_pages += 1
        city_slug = normalize_city_slug(path.parent.name)
        brand_slug = path.stem.strip().lower()
        cache_key = f"{appliance_dir}/{city_slug}/{brand_slug}"

        try:
            html_content = path.read_text(encoding="utf-8")
            soup = BeautifulSoup(html_content, 'html.parser')
            validate_soup(soup)
        except Exception as e:
            logging.error(f"Ошибка HTML в файле {path}: {e}")
            metrics.errors += 1
            continue

        # Гибкий поиск ошибок по брендам и категориям
        appliance_type = APPLIANCE_NAMES.get(appliance_dir, appliance_dir)
        errors_list = None
        for tech_db in [TECH_FACTS_DB, AUTO_TECH_FACTS_DB, TECH_FACTS_DB_EXTRA]:
            if isinstance(tech_db, dict) and brand_slug in tech_db:
                val = tech_db[brand_slug]
                if isinstance(val, list):
                    errors_list = val
                    break
                if isinstance(val, dict):
                    for sub_key in [appliance_dir, appliance_type]:
                        if sub_key in val and isinstance(val[sub_key], dict) and "common_errors" in val[sub_key]:
                            errors_list = val[sub_key]["common_errors"]
                            break
                    if errors_list:
                        break
                    for sub_k, sub_v in val.items():
                        if isinstance(sub_v, dict) and "common_errors" in sub_v:
                            errors_list = sub_v["common_errors"]
                            break
            if errors_list:
                break

        if not errors_list:
            errors_list = DEFAULT_FALLBACK_ERRORS

        cached_text = None if args.force else db.get(cache_key)

        if not cached_text:
            if args.dry_run:
                logging.info(f"[DRY-RUN] Нужна генерация для {path}")
                continue

            existing_seo = extract_existing_seo_text(soup)
            extracted_streets = extract_streets_from_soup(soup)
            streets_text = ", ".join(extracted_streets) if extracted_streets else "całe miasto i okolice"

            errors_to_use = list(errors_list)
            random.shuffle(errors_to_use)
            errors_text = "\n".join(
                f"- Kod/Usterka: {e.get('code', 'Błąd')}, przyczyna: {e.get('cause', 'Weryfikacja')}, część: {e.get('part', 'diagnostyka')}"
                for e in errors_to_use[:5]
            )

            selected_perspective = random.choice(PERSPECTIVES)
            
            system_prompt = f"""{selected_perspective} Piszesz unikalny, profesjonalny tekst SEO w języku polskim dla serwisu AGD.
ZASADY:
- Zakaz szablonowych wstępów ("Szukasz...", "Oferujemy...", "Witamy...").
- Piszesz WYŁĄCZNIE konkretną wiedzę techniczną i lokalną.
- Zachowaj naturalny, zróżnicowany styl zdań.
- Wygeneruj WYŁĄCZNIE 3 akapity (150-200 słów) bez formatowania Markdown."""

            prompt = f"""KONTEKST:
Lokalizacja: {city_slug.capitalize()} (rejon: {streets_text})
Urządzenie: {APPLIANCE_NAMES[appliance_dir]}
Marka: {brand_display_name(brand_slug)}

DANE DIAGNOSTYCZNE:
{errors_text}

STRUKTURA (3 AKAPITY):
1. Techniczna analiza konkretnych usterek i wyzwań dla marki {brand_display_name(brand_slug)}.
2. Logistyka dojazdu serwisu w mieście {city_slug.capitalize()} (czas reakcji, dojazd do klienta).
3. Praktyczna porada diagnostyczna do wykonania przed przyjazdem fachowca.

Zainspiruj się poniższym tekstem, ale NIE POWTARZAJ GO:
{existing_seo if existing_seo else "Brak."}"""

            try:
                text = generate_with_groq(prompt, system_prompt)
                db.set(cache_key, text)
                cached_text = text
                metrics.generated += 1
            except Exception as e:
                logging.error(f"Не удалось сгенерировать контент для {path}: {e}")
                metrics.errors += 1
                continue

        if args.apply and cached_text and not args.dry_run:
            try:
                updated_soup = update_html_dom(
                    soup, cached_text, appliance_dir, city_slug, brand_slug
                )
                updated_soup = ensure_canonical_tag(updated_soup, path)
                
                safe_write_file(path, str(updated_soup))
                metrics.applied += 1
            except Exception as e:
                logging.error(f"Не удалось безопасно записать {path}: {e}")
                metrics.errors += 1

    metrics.report()

if __name__ == "__main__":
    main()