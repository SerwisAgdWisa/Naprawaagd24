#!/usr/bin/env python3
"""
ШАГ 1: Добирает РЕАЛЬНЫЕ гео-данные (районы, улицы) для каждого города
через бесплатный Nominatim API (OpenStreetMap).

ВАЖНО — правила использования Nominatim (иначе забанят IP):
  - Не больше 1 запроса в секунду (скрипт это соблюдает через time.sleep)
  - Обязателен свой User-Agent с контактом (см. USER_AGENT ниже)
  - Не использовать для тяжёлого продакшн-трафика — это для одноразового
    сбора данных, не для запроса "на лету" при каждом заходе посетителя

Результат сохраняется в geo_data.json — используется на шаге 2/3.

Запуск:
    pip install requests --break-system-packages
    python fetch_geo_data.py
"""

import json
import time
from pathlib import Path

import requests

# ОБЯЗАТЕЛЬНО замените на реальный контакт — это требование Nominatim
USER_AGENT = "Naprawaagd24-ContentBot/1.0 (kontakt@naprawaagd24.pl)"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Список городов — ключ должен совпадать со слагом папки на сайте
CITIES = {
    "goleniow": "goleniow, Polska",
    "nowogard": "Nowogard, Polska",
    "maszewo": "Maszewo, Polska",
    "szczecin": "Szczecin, Polska",
    "stargard": "Stargard, Polska",
    "police": "Police, Polska",
    "pyrzyce": "Pyrzyce, Polska",
    "gryfino": "Gryfino, Polska",
}

OUTPUT_FILE = Path("geo_data.json")


def fetch_city_data(query: str) -> dict | None:
    """Получает координаты + bounding box города через Nominatim."""
    params = {
        "q": query,
        "format": "jsonv2",
        "addressdetails": 1,
        "limit": 1,
    }
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        return None
    return results[0]


def fetch_nearby_streets(lat: str, lon: str) -> list[str]:
    """
    Ищет объекты типа 'street' рядом с центром города через Overpass API
    (тоже OpenStreetMap, отдельный сервис для сложных запросов).
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    # Радиус 2000 м вокруг центра, ищем именованные улицы (highway=*)
    query = f"""
    [out:json][timeout:25];
    (
      way["highway"]["name"](around:2000,{lat},{lon});
    );
    out tags 50;
    """
    headers = {"User-Agent": USER_AGENT}
    resp = requests.post(overpass_url, data={"data": query}, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    names = []
    seen = set()
    for el in data.get("elements", []):
        name = el.get("tags", {}).get("name")
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return names[:15]  # ограничим до 15 самых частых


def main():
    result = {}

    if OUTPUT_FILE.exists():
        result = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        print(f"Найден существующий {OUTPUT_FILE}, дополняем...")

    for slug, query in CITIES.items():
        if slug in result:
            print(f"[ПРОПУЩЕН, уже есть] {slug}")
            continue

        print(f"[ЗАПРОС] {query} ...")
        try:
            city_info = fetch_city_data(query)
            time.sleep(1.1)  # соблюдаем лимит Nominatim: не чаще 1 req/sec

            if city_info is None:
                print(f"  Не найдено: {query}")
                continue

            lat, lon = city_info["lat"], city_info["lon"]
            streets = fetch_nearby_streets(lat, lon)
            time.sleep(1.1)

            result[slug] = {
                "query": query,
                "display_name": city_info.get("display_name", query),
                "lat": lat,
                "lon": lon,
                "postcode": city_info.get("address", {}).get("postcode", ""),
                "streets": streets,
            }
            print(f"  OK — найдено улиц: {len(streets)}")

        except requests.RequestException as e:
            print(f"  ОШИБКА запроса для {query}: {e}")
            continue

        # Сохраняем прогрессивно, чтобы не потерять данные при сбое
        OUTPUT_FILE.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"\nГотово. Данные сохранены в {OUTPUT_FILE}")
    print("Проверьте вручную — Overpass иногда возвращает служебные/технические")
    print("названия (например, безымянные проезды с обобщённым именем) —")
    print("почистите список streets при необходимости перед использованием.")


if __name__ == "__main__":
    main()
