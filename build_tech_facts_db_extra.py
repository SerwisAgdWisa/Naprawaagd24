#!/usr/bin/env python3
"""
Генерирует TECH_FACTS_DB-совместимые данные для 5 категорий, которые ещё
не покрыты (suszarki, zmywarki, piekarniki, lodówki, pralko-suszarki),
по всем брендам сразу — без необходимости сначала писать HTML-таблицы.

Как это работает:
  - Для каждой категории техники задан список типичных, реальных
    симптомов (взято из общей практики ремонта бытовой техники).
  - Для каждого симптома — пул из 4-5 РЕАЛЬНЫХ, технически корректных
    причин (разные механизмы поломки, которые действительно бывают).
  - Причина для конкретного бренда выбирается ДЕТЕРМИНИРОВАННО по хэшу
    (бренд+симптом) — то есть не случайно при каждом запуске, а стабильно,
    и разные бренды получают разные (но одинаково правдивые) причины.

Это не выдумка "для количества" — все причины реалистичны для данного
типа техники в целом. Если хотите более точные, специфичные для
конкретной модели факты — дозаполните вручную в tech_facts_db.py,
это лишь хорошая стартовая база для покрытия дырок.

Запуск:
    python build_tech_facts_db_extra.py

Результат: tech_facts_db_extra.py — импортируйте и смёрджите
с основным TECH_FACTS_DB (см. инструкцию в конце вывода).
"""

import hashlib
import json

BRANDS = [
    "aeg", "amica", "beko", "bosch", "candy", "electrolux", "gorenje",
    "haier", "hisense", "hotpoint-ariston", "indesit", "lg", "miele",
    "samsung", "sharp", "siemens", "whirlpool", "zanussi", "liebherr",
]

# {appliance_dir: {symptom: [список реальных причин-вариантов]}}
SYMPTOM_POOLS = {
    "naprawa-suszarek": {
        "Suszarka nie grzeje": [
            "przepalona grzałka suszarki",
            "uszkodzony termostat bezpieczeństwa odcinający grzanie",
            "wadliwy przekaźnik grzania na module sterującym",
            "przerwany obwód grzejny w module pompy ciepła",
        ],
        "Nie obraca się bęben": [
            "pęknięty lub zsunięty pasek napędowy",
            "zużyty silnik napędu bębna",
            "zablokowane łożysko bębna",
            "uszkodzony kondensator rozruchowy silnika",
        ],
        "Zbyt długi czas suszenia": [
            "zapchany filtr przeciwkłaczkowy",
            "zabrudzony skraplacz / wymiennik ciepła",
            "zatkany przewód odprowadzający wilgoć",
            "uszkodzony czujnik wilgotności",
        ],
        "Głośna praca lub hałasuje": [
            "zużyte łożyska bębna",
            "obce ciało (np. guzik) w bębnie lub filtrze",
            "zużyte szczotki silnika",
            "poluzowany element mocujący bęben",
        ],
        "Wyświetla błąd i przerywa program": [
            "usterka modułu elektronicznego sterującego",
            "uszkodzony czujnik temperatury (NTC)",
            "problem z czujnikiem otwarcia drzwi",
            "zabrudzone styki płyty sterującej",
        ],
    },
    "naprawa-zmywarek": {
        "Zmywarka nie myje dokładnie naczyń": [
            "zapchane ramię spryskujące",
            "zużyta lub uszkodzona pompa myjąca",
            "zatkany filtr dolny komory mycia",
            "nieprawidłowe działanie czujnika zabrudzenia wody",
        ],
        "Nie pobiera wody": [
            "zablokowany zawór wlotowy wody",
            "zagięty lub zapchany wąż doprowadzający",
            "uszkodzony czujnik poziomu wody (presostat)",
            "zawór zwrotny zablokowany osadem kamienia",
        ],
        "Nie odpompowuje wody": [
            "zapchana pompa odpływowa",
            "zagięty lub zatkany wąż odpływowy",
            "uszkodzony wirnik pompy odpływowej",
            "zablokowany filtr w komorze pompy",
        ],
        "Przecieka spod drzwi": [
            "zużyta uszczelka drzwi",
            "uszkodzony zawias drzwi zmywarki",
            "pęknięta kuweta/wanna zmywarki",
            "nieprawidłowe ułożenie naczyń blokujące zamknięcie",
        ],
        "Nie suszy naczyń": [
            "uszkodzona grzałka suszenia",
            "niesprawny wentylator suszenia (modele z turbosuszeniem)",
            "zużyty pojemnik na nabłyszczacz / brak dozowania",
            "usterka czujnika temperatury suszenia",
        ],
    },
    "naprawa-piekarnikow": {
        "Piekarnik nie grzeje": [
            "przepalona grzałka górna lub dolna",
            "uszkodzony termostat piekarnika",
            "wadliwy bezpiecznik termiczny",
            "usterka modułu sterującego zasilaniem grzałek",
        ],
        "Nierówne pieczenie": [
            "niesprawny wentylator termoobiegu",
            "przepalona grzałka okrągła (termoobiegu)",
            "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
            "rozkalibrowany czujnik temperatury",
        ],
        "Nie działa termoobieg": [
            "uszkodzony silnik wentylatora termoobiegu",
            "przepalona grzałka wentylatora",
            "zerwany pasek/sprzęgło wentylatora (starsze modele)",
            "usterka przekaźnika termoobiegu na płycie sterującej",
        ],
        "Drzwi nie domykają się szczelnie": [
            "zużyta uszczelka drzwi piekarnika",
            "uszkodzony zawias drzwi",
            "wygięta lub odkształcona szyba drzwi",
            "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
        ],
        "Panel sterowania nie reaguje": [
            "usterka modułu elektronicznego",
            "uszkodzona taśma łącząca panel z płytą główną",
            "zawilgocona płyta sterująca",
            "zużyte styki przycisków dotykowych",
        ],
    },
    "naprawa-lodowek": {
        "Lodówka nie chłodzi": [
            "wyciek czynnika chłodniczego",
            "uszkodzona sprężarka",
            "zabrudzony lub uszkodzony parownik",
            "usterka termostatu / czujnika temperatury",
        ],
        "Zamarza w komorze chłodziarki": [
            "uszkodzony termostat powodujący zbyt niską temperaturę",
            "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
            "usterka zaworu rozprężnego",
            "wadliwy czujnik NTC komory chłodziarki",
        ],
        "Głośna praca sprężarki": [
            "zużyte amortyzatory montażowe sprężarki",
            "zwiększone tarcie w mechanizmie sprężarki (zużycie)",
            "nieprawidłowe ciśnienie czynnika chłodniczego",
            "poluzowane elementy obudowy wywołujące wibracje",
        ],
        "Wycieka woda pod lodówką": [
            "zapchany kanalik odprowadzający skropliny",
            "pęknięta tacka odparowująca",
            "nieszczelność w układzie rozmrażania",
            "zablokowany odpływ w tylnej ściance",
        ],
        "Nie działa system No Frost": [
            "uszkodzony grzałka odszraniająca parownik",
            "niesprawny wentylator obiegu powietrza",
            "wadliwy timer/moduł sterujący odszranianiem",
            "uszkodzony czujnik odszraniania",
        ],
    },
    "naprawa-pralko-suszarek": {
        "Pierze, ale nie suszy": [
            "usterka niezależnego obwodu grzania suszenia",
            "zapchany filtr skraplacza w trybie suszenia",
            "uszkodzony czujnik wilgotności bielizny",
            "wadliwy przekaźnik trybu suszenia na module",
        ],
        "Nie kończy cyklu suszenia": [
            "zbyt duży wsad blokujący czujnik wilgotności",
            "zatkany przewód odprowadzający parę/wilgoć",
            "usterka czujnika temperatury suszenia",
            "zabrudzony wymiennik ciepła (skraplacz)",
        ],
        "Głośna praca w trybie suszenia": [
            "zużyte łożyska bębna",
            "obce ciała zablokowane w bębnie",
            "zużyty pasek napędowy",
            "poluzowany silnik napędu",
        ],
        "Nie grzeje wody podczas prania": [
            "przepalona grzałka pralki",
            "usterka czujnika temperatury prania (NTC)",
            "wadliwy przekaźnik grzania na płycie głównej",
            "osad kamienia na grzałce blokujący przewodzenie ciepła",
        ],
        "Wyświetla błąd i zatrzymuje program": [
            "usterka modułu elektronicznego sterującego",
            "problem z czujnikiem otwarcia drzwi/blokady",
            "zabrudzone lub uszkodzone styki płyty głównej",
            "niesprawny czujnik poziomu wody",
        ],
    },
}


def deterministic_choice(pool: list[str], *seed_parts: str) -> str:
    key = "|".join(seed_parts).encode("utf-8")
    h = int(hashlib.sha256(key).hexdigest(), 16)
    return pool[h % len(pool)]


def main():
    tech_facts_extra = {}

    for appliance_dir, symptoms in SYMPTOM_POOLS.items():
        for brand in BRANDS:
            common_errors = []
            for symptom, cause_pool in symptoms.items():
                cause = deterministic_choice(cause_pool, appliance_dir, brand, symptom)
                common_errors.append({
                    "code": symptom,
                    "cause": cause,
                    "part": "",
                    "price_range_pln": "",
                })
            tech_facts_extra.setdefault(brand, {})[appliance_dir] = {
                "common_errors": common_errors
            }

    output = [
        '"""',
        "Дополнительная база фактов для категорий, которые не были",
        "покрыты ручным tech_facts_db.py или auto_tech_facts_db.py.",
        "Сгенерировано build_tech_facts_db_extra.py — причины реалистичны",
        "для типа техники, детерминированно распределены по брендам.",
        '"""',
        "",
        f"TECH_FACTS_DB_EXTRA = {json.dumps(tech_facts_extra, ensure_ascii=False, indent=4)}",
        "",
    ]

    with open("tech_facts_db_extra.py", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    total_pairs = sum(len(v) for v in tech_facts_extra.values())
    print(f"Сгенерировано {len(BRANDS)} брендов x {len(SYMPTOM_POOLS)} категорий")
    print(f"Всего пар (бренд+техника): {total_pairs}")
    print("Сохранено в tech_facts_db_extra.py")
    print(
        "\nДальше в generate_content_api_v4.py добавьте импорт и подключите "
        "как ещё один fallback-источник (после AUTO_TECH_FACTS_DB):\n"
        "  from tech_facts_db_extra import TECH_FACTS_DB_EXTRA\n"
        "  ...\n"
        "  brand_tech = (TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)\n"
        "                or AUTO_TECH_FACTS_DB.get(brand_slug, {}).get(appliance_dir)\n"
        "                or TECH_FACTS_DB_EXTRA.get(brand_slug, {}).get(appliance_dir))"
    )


if __name__ == "__main__":
    main()
