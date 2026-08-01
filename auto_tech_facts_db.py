"""
Автоматически извлечённая база фактов из уже существующих на страницах
таблиц symptoms-table. Сгенерировано extract_facts_from_pages.py.
Формат идентичен ручному TECH_FACTS_DB из tech_facts_db.py.
"""

AUTO_TECH_FACTS_DB = {
    "aeg": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Zatkany filtr pompy - blokada odpływu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Uszkodzony termostat (czujnik NTC) - błędny odczyt",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Obcy przedmiot w bębnie (guzik, moneta) - cykliczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Woda w module sterującym - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Awaria modułu sterującego - brak sygnału",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Nieprawidłowe ustawienie - niestabilność",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "amica": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Przerwany pasek napędowy (w starszych modelach)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Uszkodzony bezpiecznik termiczny grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Poluzowane amortyzatory lub sprężyny - stukanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zablokowany wąż odpływowy - zgięcie, zator",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Woda w module sterującym - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "beko": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Uszkodzone łożyska bębna - charakterystyczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Zablokowany zawór wody - za mało wody w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Błąd presostatu (czujnika poziomu wody) - błędny sygnał",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Zużyte łożyska i krzyżak bębna - metaliczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony silnik - zwarcie uzwojeń",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "bosch": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Błąd elektroniki - uszkodzony moduł sterujący",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Zablokowany zawór wody - za mało wody w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Błąd presostatu (czujnika poziomu wody) - błędny sygnał",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Poluzowane amortyzatory lub sprężyny - stukanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zatkany filtr pompy - dostęp z przodu urządzenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony przewód zasilający - izolacja",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Awaria modułu sterującego - brak sygnału",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "candy": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Błąd elektroniki - uszkodzony moduł sterujący",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Zablokowany zawór wody - za mało wody w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Luźny pasek napędowy - piski, trzaski",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zatkany syfon lub kanalizacja - odwrotny ciąg",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Woda w module sterującym - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Uszkodzone amortyzatory - brak tłumienia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "electrolux": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Zablokowana pompa odpływowa (brak odpompowania)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Awaria modułu sterującego - brak zasilania grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Za niskie ciśnienie wody w instalacji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Nierówne ustawienie pralki - wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zablokowany wąż odpływowy - zgięcie, zator",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony silnik - zwarcie uzwojeń",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Woda w bębnie - blokada bezpieczeństwa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Nierównomierny rozkład prania - wyważenie",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "gorenje": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Przerwany pasek napędowy (w starszych modelach)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Awaria modułu sterującego - brak zasilania grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Za niskie ciśnienie wody w instalacji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Luźny pasek napędowy - piski, trzaski",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Błąd elektroniki - brak zasilania pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony silnik - zwarcie uzwojeń",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "haier": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Błąd czujnika Halla (tachometr) - brak sygnału obrotów",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Spalona grzałka - brak rezystancji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Zatkany filtr wody wlotowej - brak ciśnienia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Zużyte łożyska i krzyżak bębna - metaliczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zatkany syfon lub kanalizacja - odwrotny ciąg",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Woda w module sterującym - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Woda w bębnie - blokada bezpieczeństwa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Uszkodzone amortyzatory - brak tłumienia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "hisense": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Zatkany filtr pompy - blokada odpływu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Spalona grzałka - brak rezystancji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Za niskie ciśnienie wody w instalacji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Nierówne ustawienie pralki - wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Błąd elektroniki - brak zasilania pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony przewód zasilający - izolacja",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Awaria modułu sterującego - brak sygnału",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "hotpoint-ariston": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Uszkodzone łożyska bębna - charakterystyczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Błąd przekaźnika grzałki w module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Uszkodzony elektrozawór - brak otwarcia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Uszkodzony silnik - nierówna praca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony silnik - zwarcie uzwojeń",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Wysoka temperatura w bębnie - blokada termiczna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Uszkodzone amortyzatory - brak tłumienia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "indesit": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Błąd czujnika Halla (tachometr) - brak sygnału obrotów",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Zablokowany zawór wody - za mało wody w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Nierówne ustawienie pralki - wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Spięta grzałka - zwarcie do masy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Zablokowana zamknięcie drzwi - mechanizm",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Nierównomierny rozkład prania - wyważenie",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "lg": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Uszkodzone łożyska bębna - charakterystyczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Awaria modułu sterującego - brak zasilania grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Uszkodzony elektrozawór - brak otwarcia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Poluzowane amortyzatory lub sprężyny - stukanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zatkany filtr pompy - dostęp z przodu urządzenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Woda w module sterującym - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Woda w bębnie - blokada bezpieczeństwa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Nierównomierny rozkład prania - wyważenie",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "miele": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Błąd elektroniki - uszkodzony moduł sterujący",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Uszkodzony bezpiecznik termiczny grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Uszkodzony elektrozawór - brak otwarcia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Zużyte łożyska i krzyżak bębna - metaliczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zatkany syfon lub kanalizacja - odwrotny ciąg",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony przewód zasilający - izolacja",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "samsung": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Błąd elektroniki - uszkodzony moduł sterujący",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Awaria modułu sterującego - brak zasilania grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Obcy przedmiot w bębnie (guzik, moneta) - cykliczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Błąd kondensatora silnika - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Zużyte łożyska - luz bębna",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "sharp": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Awaria modułu sterującego silnikiem - brak napięcia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Spalona grzałka - brak rezystancji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Poluzowane amortyzatory lub sprężyny - stukanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Zatkany filtr pompy - dostęp z przodu urządzenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Uszkodzony przewód zasilający - izolacja",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Wysoka temperatura w bębnie - blokada termiczna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Nieprawidłowe ustawienie - niestabilność",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "siemens": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Przerwany pasek napędowy (w starszych modelach)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Uszkodzony termostat (czujnik NTC) - błędny odczyt",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Awaria modułu sterującego - brak impulsu do zaworu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Luźny pasek napędowy - piski, trzaski",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Spięta grzałka - zwarcie do masy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Wysoka temperatura w bębnie - blokada termiczna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "whirlpool": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Zatkany filtr pompy - blokada odpływu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Spalona grzałka - brak rezystancji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Zablokowany wąż dopływowy - kamień, zanieczyszczenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Poluzowane amortyzatory lub sprężyny - stukanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Spięta grzałka - zwarcie do masy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Zablokowana zamknięcie drzwi - mechanizm",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Uszkodzone amortyzatory - brak tłumienia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "zanussi": {
        "naprawa-pralek": {
            "common_errors": [
                {
                    "code": "Pralka nie wiruje",
                    "cause": "Przerwany pasek napędowy (w starszych modelach)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie grzeje wody",
                    "cause": "Awaria modułu sterującego - brak zasilania grzałki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka nie pobiera wody",
                    "cause": "Za niskie ciśnienie wody w instalacji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka hałasuje i stuka",
                    "cause": "Zużyte łożyska i krzyżak bębna - metaliczny hałas",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Woda zostaje w pralce",
                    "cause": "Uszkodzona pompa odpływowa - brak wirnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka wywala bezpieczniki",
                    "cause": "Błąd kondensatora silnika - zwarcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi pralki zablokowane",
                    "cause": "Błąd microswitcha - czujnik pozycji",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Pralka skacze podczas wirowania",
                    "cause": "Poluzowane sprężyny - nadmierny ruch",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    }
}
