"""
Дополнительная база фактов для категорий, которые не были
покрыты ручным tech_facts_db.py или auto_tech_facts_db.py.
Сгенерировано build_tech_facts_db_extra.py — причины реалистичны
для типа техники, детерминированно распределены по брендам.
"""

TECH_FACTS_DB_EXTRA = {
    "aeg": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "wadliwy przekaźnik grzania na module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "pęknięty lub zsunięty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zagięty lub zapchany wąż doprowadzający",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "uszkodzony wirnik pompy odpływowej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "zużyta uszczelka drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "uszkodzony termostat piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "zerwany pasek/sprzęgło wentylatora (starsze modele)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zużyta uszczelka drzwi piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "uszkodzona taśma łącząca panel z płytą główną",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "zabrudzony lub uszkodzony parownik",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zużyte amortyzatory montażowe sprężarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "obce ciała zablokowane w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "osad kamienia na grzałce blokujący przewodzenie ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "amica": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "wadliwy przekaźnik grzania na module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zużyty silnik napędu bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zatkany filtr dolny komory mycia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zawór zwrotny zablokowany osadem kamienia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zablokowany filtr w komorze pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "uszkodzona grzałka suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "uszkodzony termostat piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "zerwany pasek/sprzęgło wentylatora (starsze modele)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zużyta uszczelka drzwi piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "zabrudzony lub uszkodzony parownik",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "wadliwy czujnik NTC komory chłodziarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zwiększone tarcie w mechanizmie sprężarki (zużycie)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "obce ciała zablokowane w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "wadliwy przekaźnik grzania na płycie głównej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "beko": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przepalona grzałka suszarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zapchany filtr przeciwkłaczkowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "obce ciało (np. guzik) w bębnie lub filtrze",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "uszkodzony czujnik temperatury (NTC)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zawór zwrotny zablokowany osadem kamienia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zablokowany filtr w komorze pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "uszkodzony zawias drzwi zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "usterka modułu sterującego zasilaniem grzałek",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "uszkodzony zawias drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "uszkodzony termostat powodujący zbyt niską temperaturę",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "poluzowane elementy obudowy wywołujące wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zbyt duży wsad blokujący czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "obce ciała zablokowane w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "zabrudzone lub uszkodzone styki płyty głównej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "bosch": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zapchany filtr przeciwkłaczkowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zatkany filtr dolny komory mycia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "uszkodzony czujnik poziomu wody (presostat)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "uszkodzony zawias drzwi zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "uszkodzona grzałka suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "rozkalibrowany czujnik temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zużyta uszczelka drzwi piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "usterka zaworu rozprężnego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zwiększone tarcie w mechanizmie sprężarki (zużycie)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony grzałka odszraniająca parownik",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "zapchany filtr skraplacza w trybie suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zatkany przewód odprowadzający parę/wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "przepalona grzałka pralki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "zabrudzone lub uszkodzone styki płyty głównej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "candy": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przerwany obwód grzejny w module pompy ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "pęknięty lub zsunięty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "uszkodzony czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "poluzowany element mocujący bęben",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zużyta lub uszkodzona pompa myjąca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "nieprawidłowe ułożenie naczyń blokujące zamknięcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "wygięta lub odkształcona szyba drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "poluzowane elementy obudowy wywołujące wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zablokowany odpływ w tylnej ściance",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zatkany przewód odprowadzający parę/wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "electrolux": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przepalona grzałka suszarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zablokowany filtr w komorze pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "zużyta uszczelka drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "zużyty pojemnik na nabłyszczacz / brak dozowania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "przepalona grzałka okrągła (termoobiegu)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "zerwany pasek/sprzęgło wentylatora (starsze modele)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "uszkodzony zawias drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "wyciek czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "poluzowany silnik napędu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "przepalona grzałka pralki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "gorenje": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "wadliwy przekaźnik grzania na module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "uszkodzony czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "obce ciało (np. guzik) w bębnie lub filtrze",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zatkany filtr dolny komory mycia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "nieprawidłowe ułożenie naczyń blokujące zamknięcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "zużyty pojemnik na nabłyszczacz / brak dozowania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "uszkodzony termostat piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "usterka przekaźnika termoobiegu na płycie sterującej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "zabrudzony lub uszkodzony parownik",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "wadliwy czujnik NTC komory chłodziarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zwiększone tarcie w mechanizmie sprężarki (zużycie)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zablokowany odpływ w tylnej ściance",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "obce ciała zablokowane w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "osad kamienia na grzałce blokujący przewodzenie ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "haier": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zużyty silnik napędu bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zatkany przewód odprowadzający wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "poluzowany element mocujący bęben",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zawór zwrotny zablokowany osadem kamienia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "zużyta uszczelka drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zużyta uszczelka drzwi piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "uszkodzona taśma łącząca panel z płytą główną",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "usterka zaworu rozprężnego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zbyt duży wsad blokujący czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "przepalona grzałka pralki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "hisense": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "wadliwy przekaźnik grzania na module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zatkany przewód odprowadzający wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "obce ciało (np. guzik) w bębnie lub filtrze",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zatkany filtr dolny komory mycia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "uszkodzony czujnik poziomu wody (presostat)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "uszkodzona taśma łącząca panel z płytą główną",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zapchany kanalik odprowadzający skropliny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "zapchany filtr skraplacza w trybie suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "poluzowany silnik napędu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "osad kamienia na grzałce blokujący przewodzenie ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "hotpoint-ariston": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "uszkodzony czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "poluzowany element mocujący bęben",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zablokowany filtr w komorze pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "nieprawidłowe ułożenie naczyń blokujące zamknięcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "zerwany pasek/sprzęgło wentylatora (starsze modele)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "usterka zaworu rozprężnego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "poluzowane elementy obudowy wywołujące wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zapchany kanalik odprowadzający skropliny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "niesprawny wentylator obiegu powietrza",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "usterka niezależnego obwodu grzania suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zatkany przewód odprowadzający parę/wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "poluzowany silnik napędu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "przepalona grzałka pralki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "indesit": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zużyty silnik napędu bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zagięty lub zapchany wąż doprowadzający",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "uszkodzony wirnik pompy odpływowej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "uszkodzony zawias drzwi zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "zużyty pojemnik na nabłyszczacz / brak dozowania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "usterka modułu sterującego zasilaniem grzałek",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "usterka przekaźnika termoobiegu na płycie sterującej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "wygięta lub odkształcona szyba drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "uszkodzony termostat powodujący zbyt niską temperaturę",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zwiększone tarcie w mechanizmie sprężarki (zużycie)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony grzałka odszraniająca parownik",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zbyt duży wsad blokujący czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "wadliwy przekaźnik grzania na płycie głównej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "zabrudzone lub uszkodzone styki płyty głównej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "lg": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "wadliwy przekaźnik grzania na module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "uszkodzony kondensator rozruchowy silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zapchany filtr przeciwkłaczkowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "obce ciało (np. guzik) w bębnie lub filtrze",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "nieprawidłowe ułożenie naczyń blokujące zamknięcie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "wygięta lub odkształcona szyba drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "poluzowane elementy obudowy wywołujące wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "problem z czujnikiem otwarcia drzwi/blokady",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "miele": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przepalona grzałka suszarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "pęknięty lub zsunięty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "obce ciało (np. guzik) w bębnie lub filtrze",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "uszkodzony czujnik poziomu wody (presostat)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "zużyta uszczelka drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "uszkodzona grzałka suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "usterka modułu sterującego zasilaniem grzałek",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "przepalona grzałka okrągła (termoobiegu)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zużyta uszczelka drzwi piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "uszkodzona taśma łącząca panel z płytą główną",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "zabrudzony lub uszkodzony parownik",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "usterka zaworu rozprężnego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "poluzowane elementy obudowy wywołujące wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zapchany kanalik odprowadzający skropliny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zatkany przewód odprowadzający parę/wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "samsung": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "wadliwy przekaźnik grzania na module sterującym",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "pęknięty lub zsunięty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zapchany filtr przeciwkłaczkowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte szczotki silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zagięty lub zapchany wąż doprowadzający",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "uszkodzony zawias drzwi zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "zużyty pojemnik na nabłyszczacz / brak dozowania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "przepalona grzałka okrągła (termoobiegu)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "wygięta lub odkształcona szyba drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "zabrudzony lub uszkodzony parownik",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zablokowany odpływ w tylnej ściance",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "obce ciała zablokowane w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "przepalona grzałka pralki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "zabrudzone lub uszkodzone styki płyty głównej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "sharp": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "uszkodzony kondensator rozruchowy silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "poluzowany element mocujący bęben",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "uszkodzony wirnik pompy odpływowej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "zużyta uszczelka drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "zużyty pojemnik na nabłyszczacz / brak dozowania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zawilgocona płyta sterująca",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "usterka zaworu rozprężnego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "poluzowane elementy obudowy wywołujące wibracje",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony grzałka odszraniająca parownik",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "obce ciała zablokowane w bębnie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "wadliwy przekaźnik grzania na płycie głównej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "zabrudzone lub uszkodzone styki płyty głównej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "siemens": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "uszkodzony kondensator rozruchowy silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "uszkodzony czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zagięty lub zapchany wąż doprowadzający",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "usterka modułu sterującego zasilaniem grzałek",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "rozkalibrowany czujnik temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "problem z czujnikiem otwarcia drzwi/blokady",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "whirlpool": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przerwany obwód grzejny w module pompy ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "uszkodzony kondensator rozruchowy silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "uszkodzony czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "poluzowany element mocujący bęben",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zapchane ramię spryskujące",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "uszkodzony czujnik poziomu wody (presostat)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zablokowany filtr w komorze pompy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "uszkodzona grzałka suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "rozkalibrowany czujnik temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zużyta uszczelka drzwi piekarnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "wyciek czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "usterka zaworu rozprężnego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "niesprawny wentylator obiegu powietrza",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "usterka niezależnego obwodu grzania suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zatkany przewód odprowadzający parę/wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "usterka modułu elektronicznego sterującego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "zanussi": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "uszkodzony termostat bezpieczeństwa odcinający grzanie",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zużyty silnik napędu bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zatkany przewód odprowadzający wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte szczotki silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "uszkodzony czujnik temperatury (NTC)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zawór zwrotny zablokowany osadem kamienia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "usterka modułu sterującego zasilaniem grzałek",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "przepalona grzałka okrągła (termoobiegu)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "usterka przekaźnika termoobiegu na płycie sterującej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "uszkodzony zawias drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zużyte amortyzatory montażowe sprężarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zablokowany odpływ w tylnej ściance",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony czujnik odszraniania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "zapchany filtr skraplacza w trybie suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zbyt duży wsad blokujący czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "poluzowany silnik napędu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "problem z czujnikiem otwarcia drzwi/blokady",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "liebherr": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przerwany obwód grzejny w module pompy ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "pęknięty lub zsunięty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "uszkodzony czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zużyta lub uszkodzona pompa myjąca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "uszkodzony czujnik poziomu wody (presostat)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "uszkodzony zawias drzwi zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "zużyty pojemnik na nabłyszczacz / brak dozowania",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "zablokowany mechanizm zamka drzwi (modele z pirolizą)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zawilgocona płyta sterująca",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "wadliwy czujnik NTC komory chłodziarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zwiększone tarcie w mechanizmie sprężarki (zużycie)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "wadliwy przekaźnik grzania na płycie głównej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "problem z czujnikiem otwarcia drzwi/blokady",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "ariston": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przerwany obwód grzejny w module pompy ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "pęknięty lub zsunięty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zatkany przewód odprowadzający wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte szczotki silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "nieprawidłowe działanie czujnika zabrudzenia wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zawór zwrotny zablokowany osadem kamienia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "uszkodzony zawias drzwi zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "uszkodzona grzałka suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "wadliwy bezpiecznik termiczny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "przepalona grzałka wentylatora",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "wygięta lub odkształcona szyba drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "usterka termostatu / czujnika temperatury",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "nieszczelność w układzie rozmrażania",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "wadliwy timer/moduł sterujący odszranianiem",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "problem z czujnikiem otwarcia drzwi/blokady",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "elektrolux": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przepalona grzałka suszarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "uszkodzony kondensator rozruchowy silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "obce ciało (np. guzik) w bębnie lub filtrze",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "problem z czujnikiem otwarcia drzwi",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zużyta lub uszkodzona pompa myjąca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "uszkodzony czujnik poziomu wody (presostat)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "usterka czujnika temperatury suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "usterka modułu sterującego zasilaniem grzałek",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "uszkodzony silnik wentylatora termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "wygięta lub odkształcona szyba drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "usterka modułu elektronicznego",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "zabrudzony lub uszkodzony parownik",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "uszkodzony termostat powodujący zbyt niską temperaturę",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zużyte amortyzatory montażowe sprężarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zablokowany odpływ w tylnej ściance",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony grzałka odszraniająca parownik",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "wadliwy przekaźnik trybu suszenia na module",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zbyt duży wsad blokujący czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "poluzowany silnik napędu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "osad kamienia na grzałce blokujący przewodzenie ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "gorenie": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przerwany obwód grzejny w module pompy ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "uszkodzony kondensator rozruchowy silnika",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zabrudzony skraplacz / wymiennik ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "zużyte łożyska bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "uszkodzony czujnik temperatury (NTC)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zużyta lub uszkodzona pompa myjąca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zablokowany zawór wlotowy wody",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zagięty lub zatkany wąż odpływowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "zużyta uszczelka drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "uszkodzona grzałka suszenia",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "nieszczelne uszczelnienie drzwi powodujące utratę ciepła",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "usterka przekaźnika termoobiegu na płycie sterującej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "uszkodzony zawias drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "zużyte styki przycisków dotykowych",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "nieszczelna uszczelka drzwi wpuszczająca wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "zużyte amortyzatory montażowe sprężarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "zablokowany odpływ w tylnej ściance",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony grzałka odszraniająca parownik",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "zapchany filtr skraplacza w trybie suszenia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zbyt duży wsad blokujący czujnik wilgotności",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "zużyty pasek napędowy",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "usterka czujnika temperatury prania (NTC)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "zabrudzone lub uszkodzone styki płyty głównej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    },
    "neff": {
        "naprawa-suszarek": {
            "common_errors": [
                {
                    "code": "Suszarka nie grzeje",
                    "cause": "przepalona grzałka suszarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie obraca się bęben",
                    "cause": "zablokowane łożysko bębna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zbyt długi czas suszenia",
                    "cause": "zatkany przewód odprowadzający wilgoć",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca lub hałasuje",
                    "cause": "poluzowany element mocujący bęben",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i przerywa program",
                    "cause": "zabrudzone styki płyty sterującej",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {
                    "code": "Zmywarka nie myje dokładnie naczyń",
                    "cause": "zatkany filtr dolny komory mycia",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie pobiera wody",
                    "cause": "zagięty lub zapchany wąż doprowadzający",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie odpompowuje wody",
                    "cause": "zapchana pompa odpływowa",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Przecieka spod drzwi",
                    "cause": "pęknięta kuweta/wanna zmywarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie suszy naczyń",
                    "cause": "niesprawny wentylator suszenia (modele z turbosuszeniem)",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {
                    "code": "Piekarnik nie grzeje",
                    "cause": "przepalona grzałka górna lub dolna",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nierówne pieczenie",
                    "cause": "niesprawny wentylator termoobiegu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa termoobieg",
                    "cause": "zerwany pasek/sprzęgło wentylatora (starsze modele)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Drzwi nie domykają się szczelnie",
                    "cause": "uszkodzony zawias drzwi",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Panel sterowania nie reaguje",
                    "cause": "uszkodzona taśma łącząca panel z płytą główną",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {
                    "code": "Lodówka nie chłodzi",
                    "cause": "uszkodzona sprężarka",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Zamarza w komorze chłodziarki",
                    "cause": "wadliwy czujnik NTC komory chłodziarki",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca sprężarki",
                    "cause": "nieprawidłowe ciśnienie czynnika chłodniczego",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wycieka woda pod lodówką",
                    "cause": "pęknięta tacka odparowująca",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie działa system No Frost",
                    "cause": "uszkodzony grzałka odszraniająca parownik",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {
                    "code": "Pierze, ale nie suszy",
                    "cause": "uszkodzony czujnik wilgotności bielizny",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie kończy cyklu suszenia",
                    "cause": "zabrudzony wymiennik ciepła (skraplacz)",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Głośna praca w trybie suszenia",
                    "cause": "poluzowany silnik napędu",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Nie grzeje wody podczas prania",
                    "cause": "wadliwy przekaźnik grzania na płycie głównej",
                    "part": "",
                    "price_range_pln": ""
                },
                {
                    "code": "Wyświetla błąd i zatrzymuje program",
                    "cause": "niesprawny czujnik poziomu wody",
                    "part": "",
                    "price_range_pln": ""
                }
            ]
        }
    }
}
