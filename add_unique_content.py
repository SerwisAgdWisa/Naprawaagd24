import argparse
import json
import logging
import os
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
        logging.info(f" Переключение на API ключ #{current_key_index + 1}")

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TEMP = float(os.getenv("GROQ_TEMPERATURE", "0.25"))
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "25"))
DB_PATH = Path(os.getenv("CACHE_DB_PATH", "content_cache.db"))

ROOT_DIR = Path(".")
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

SYSTEM_PROMPT = """Jesteś starszym technikiem serwisu AGD i ekspertem SEO w Polsce.
ZASADY:
- Brak wstępów typu "Szukasz serwisu...". Pisz czystą wiedzę techniczną i lokalną.
- Jeśli podano istniejący tekst SEO (np. tabelę usterek, FAQ) — NIE powtarzaj tych samych informacji.
  Uzupełnij je czymś nowym: inny kąt, inna usterka, inna praktyczna wskazówka.
- Akapit 1: Analiza przyczyn awarii dla podanych kodów błędów (opis mechaniczny: np. zużycie szczotek silnika, zakamieniona grzałka).
- Akapit 2: Specyfika serwisu w danym mieście — podaj ulice/dzielnice oraz czas dojazdu technika.
- Akapit 3: Praktyczna rada dla klienta: co sprawdzić samemu przed wezwaniem fachowca.
- Długość: Ściśle 3 akapity (łącznie 150-200 słów). Zwróć WYŁĄCZNIE gotowy tekst po polsku bez formatowania Markdown.

PRZYKŁAD STRUKTURY:
Akapit 1 (Przyczyny): Awaria kodu E18 w pralkach marki Bosch najczęściej wynika z zablokowanej pompy odpływowej lub zagiętego węża...
Akapit 2 (Lokalizacja): Nasz serwis w Szczecinie dojeżdża do dzielnic Prawobrzeże oraz ul. Mieszka I w czasie do 45 minut...
Akapit 3 (Rada): Zanim wezwiesz technika, odkręć filtr pompy w dolnej części obudowy i sprawdź, czy nie utknęło tam ciało obce..."""

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
            path.rename(backup_path)
        path.write_text(content, encoding="utf-8", errors="replace")
        if backup_path.exists():
            backup_path.unlink()
    except Exception as e:
        if backup_path.exists():
            backup_path.rename(path)
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

def generate_with_groq(prompt: str, model: str = GROQ_MODEL, temp: float = GROQ_TEMP) -> str:
    rate_limiter.wait_if_needed()
    metrics.api_calls += 1

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    for attempt in range(1, len(GROQ_API_KEYS) * 3 + 1):
        api_key = get_current_api_key()
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            "temperature": temp,
            "max_tokens": 350
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if resp.status_code == 429:
                metrics.api_errors += 1
                
                if len(GROQ_API_KEYS) > 1:
                    logging.warning(f"[429 Rate Limit] Лимит ключа #{current_key_index + 1} исчерпан. Ротация...")
                    rotate_api_key()
                    with rate_limiter.lock:
                        rate_limiter.requests.clear()
                    continue
                else:
                    retry_header = resp.headers.get("retry-after")
                    wait_time = float(retry_header) if retry_header else 15.0
                    logging.warning(f"[429 Rate Limit] Ждем {wait_time:.1f} сек...")
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
    for old_tag in soup.find_all(['section', 'div'], class_=['local-info', MARKER_CLASS]):
        old_tag.decompose()

    paragraphs_list = split_into_paragraphs(generated_text)
    paragraphs_html = "".join(f"<p>{p}</p>" for p in paragraphs_list)
    
    h2_title = f"Specyfika serwisu i naprawy {appliance} {brand.capitalize()} w {city.capitalize()}"
    
    new_block_html = f"""
    <section class="{MARKER_CLASS}" style="padding: 25px; background: #f8f9fa; border-radius: 8px; margin: 30px 0;">
        <div class="container">
            <h2 style="font-size: 1.4rem; margin-bottom: 15px;">{h2_title}</h2>
            {paragraphs_html}
        </div>
    </section>
    """
    
    new_section = BeautifulSoup(new_block_html, 'html.parser').find('section')

    main_tag = soup.find('main')
    if main_tag:
        main_tag.append(new_section)
    else:
        footer_tag = soup.find('footer')
        if footer_tag:
            footer_tag.insert_before(new_section)
        elif soup.body:
            soup.body.append(new_section)

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

        brand_tech = (
            TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)
            or AUTO_TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)
        )
        if not brand_tech or not brand_tech.get("common_errors"):
            continue

        cached_text = db.get(cache_key)

        if not cached_text:
            if args.dry_run:
                logging.info(f"[DRY-RUN] Нужна генерация для {path}")
                continue

            existing_seo = extract_existing_seo_text(soup)
            extracted_streets = extract_streets_from_soup(soup)
            streets_text = ", ".join(extracted_streets) if extracted_streets else "całe miasto i okolice"

            errors = brand_tech["common_errors"]
            errors_text = "\n".join(
                f"- Kod: {e['code']}, przyczyna: {e['cause']}, część: {e['part']}" for e in errors
            )

            prompt = f"""DANE TECHNICZNE I LOKALIZACJA:
Miasto: {city_slug.capitalize()}
Obsługiwany rejon / ulice / dzielnice: {streets_text}
Sprzęt: {APPLIANCE_NAMES[appliance_dir]}
Marka: {brand_slug.capitalize()}
Usterki, kody i części:
{errors_text}

ISTNIEJĄCY TEKST SEO DO ROZWINIĘCIA:
{existing_seo if existing_seo else "Brak."}

Napisz 3 zwięzłe akapity techniczne dla serwisu w mieście {city_slug.capitalize()}."""

            try:
                text = generate_with_groq(prompt)
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
                    soup, cached_text, APPLIANCE_NAMES[appliance_dir], city_slug, brand_slug
                )
                safe_write_file(path, str(updated_soup))
                metrics.applied += 1
            except Exception as e:
                logging.error(f"Не удалось безопасно записать {path}: {e}")
                metrics.errors += 1

    metrics.report()

if __name__ == "__main__":
    main()
