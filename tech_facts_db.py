#!/usr/bin/env python3
"""
РАСШИРЕННАЯ БАЗА ТЕХНИЧЕСКИХ ФАКТОВ: 
Бренд -> Тип техники -> Коды ошибок, визуальные/звуковые сигналы -> Причина -> Запчасть.
"""

TECH_FACTS_DB = {
    "bosch": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "E18 / F18", "cause": "problem z odpompowaniem wody, zapchany filtr lub pompa", "part": "pompa odpływowa", "price_range_pln": "120-250"},
                {"code": "E23 / F23", "cause": "aktywacja systemu Aquastop, wyciek wody na tace", "part": "czujnik Aquastop / uszczelnienie", "price_range_pln": "90-180"},
                {"code": "E61 / F61", "cause": "brak podgrzewania wody, uszkodzona grzałka lub czujnik NTC", "part": "grzałka z czujnikiem NTC", "price_range_pln": "110-210"},
                {"code": "E21 / F21", "cause": "błąd silnika lub zużyte szczotki węglowe", "part": "szczotki silnika / moduł", "price_range_pln": "100-230"},
                {"code": "Miganie kluczyka (blokada)", "cause": "uszkodzenie zamka drzwi lub aktywna blokada rodzicielska", "part": "elektroblokada drzwi", "price_range_pln": "85-160"}
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {"code": "Czerwony napis ALARM / Sygnał dźwiękowy", "cause": "wzrost temperatury w komorze, wyciek czynnika lub awaria agregatu", "part": "usunięcie nieszczelności / sprężarka", "price_range_pln": "250-550"},
                {"code": "E2 / E3", "cause": "uszkodzony czujnik temperatury NTC w chłodziarce", "part": "czujnik NTC", "price_range_pln": "80-150"},
                {"code": "E1", "cause": "usterka czujnika temperatury parownika No-Frost", "part": "czujnik parownika", "price_range_pln": "90-160"},
                {"code": "Miganie wskaźnika temperatury", "cause": "niedokręcony wentylator lub oblodzenie parownika", "part": "grzałka odmrażania / wentylator", "price_range_pln": "120-240"}
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {"code": "E15 (Miga kranik)", "cause": "woda na dnie urządzenia, zadziałał czujnik pływakowy Aquastop", "part": "uszczelka misy / uszczelnienie", "price_range_pln": "100-220"},
                {"code": "E09 / E19", "cause": "brak grzania wody, uszkodzona grzałka zespolona z pompą", "part": "pompo-grzałka", "price_range_pln": "280-450"},
                {"code": "E22", "cause": "zapchany filtr mesh lub zator w układzie odpływowym", "part": "czyszczenie / czujnik ciśnienia", "price_range_pln": "80-150"},
                {"code": "E24", "cause": "błąd odpompowania, zablokowany wirnik pompy spustowej", "part": "pompa spustowa", "price_range_pln": "110-210"}
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {"code": "E011", "cause": "zablokowany lub zwarty przycisk na panelu dotykowym", "part": "moduł sterujący / panel", "price_range_pln": "150-350"},
                {"code": "E305", "cause": "brak komunikacji między płytami elektronicznymi", "part": "wiązka przewodów / moduł mocy", "price_range_pln": "200-400"},
                {"code": "Miganie zegara / Symbolu klucza", "cause": "błąd blokady pyrolizy lub przerwa w zasilaniu", "part": "rygiel drzwi pyrolizy", "price_range_pln": "130-260"}
            ]
        },
        "naprawa-suszarek": {
            "common_errors": [
                {"code": "E06 / Miga ikonka filtra", "cause": "problem z nagrzewaniem lub niedrożny wymiennik ciepła", "part": "czujnik NTC / czyszczenie pompy ciepła", "price_range_pln": "120-280"},
                {"code": "Miga pojemnik na wodę", "cause": "uszkodzenie pompki skroplin lub mikrowyłącznika", "part": "pompka skroplin", "price_range_pln": "110-220"}
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {"code": "E18", "cause": "niedrożny układ odpływowy podczas suszenia lub prania", "part": "pompa odpływowa", "price_range_pln": "130-260"},
                {"code": "E13", "cause": "wyciek wody w kanale suszenia", "part": "uszczelka kanału / wąż", "price_range_pln": "100-200"}
            ]
        }
    },

    "samsung": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "4E / 4C", "cause": "brak dopływu wody, zapchany filtr elektrozaworu", "part": "zawór wlewowy wody", "price_range_pln": "90-160"},
                {"code": "5E / 5C", "cause": "problem z odpływem wody, zablokowany filtr pompy", "part": "pompa magnesowa", "price_range_pln": "110-200"},
                {"code": "3E / 3C", "cause": "przeciążenie silnika lub awaria czujnika tacho Digital Inverter", "part": "czujnik Tacho / silnik", "price_range_pln": "110-280"},
                {"code": "UE / UB", "cause": "nierównomierne rozłożenie wsadu lub zużycie krzyżaka bębna", "part": "amortyzatory / krzyżak", "price_range_pln": "140-350"},
                {"code": "HE1 / HE2", "cause": "przegrzanie lub brak grzania – awaria czujnika temperatury", "part": "grzałka / czujnik NTC", "price_range_pln": "100-210"}
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {"code": "Miganie kreski na wyświetlaczu / Błąd 22E", "cause": "uszkodzenie wentylator parownika lub silnika zamrażalnika", "part": "wentylator parownika", "price_range_pln": "120-220"},
                {"code": "Sygnał piskowy / Miganie temperatury", "cause": "zablokowany odpływ skroplin, oblodzenie parownika No-Frost", "part": "grzałka rozmrażania / czujnik defrost", "price_range_pln": "130-250"},
                {"code": "5E / 5C", "cause": "błąd czujnika rozmrażania w chłodziarce", "part": "czujnik defrost", "price_range_pln": "90-170"},
                {"code": "RD", "cause": "zablokowanie przepustnicy powietrza (Damper)", "part": "przepustnica powietrza", "price_range_pln": "140-240"}
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {"code": "LE / LC (Sygnał dźwiękowy)", "cause": "wykryto wyciek wody pod urządzeniem na tacy", "part": "czujnik wycieku / wąż", "price_range_pln": "90-190"},
                {"code": "HE / HC", "cause": "problem z podgrzewaniem wody w zmywarce", "part": "grzałka przepływowa", "price_range_pln": "160-290"},
                {"code": "4E / 4C", "cause": "brak poboru wody, zawór dopływowy zatkany", "part": "elektrozawór", "price_range_pln": "95-170"}
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {"code": "C-21 / C-20", "cause": "przegrzanie wnętrza, uszkodzony czujnik temperatury", "part": "termostat / czujnik NTC", "price_range_pln": "100-200"},
                {"code": "C-d1", "cause": "błąd blokady drzwi Dual Cook", "part": "silnik zamka drzwi", "price_range_pln": "130-250"}
            ]
        },
        "naprawa-suszarek": {
            "common_errors": [
                {"code": "HC / tC", "cause": "przegrzanie lub błąd czujnika temperatury suszenia", "part": "termostat / czujnik NTC", "price_range_pln": "110-220"},
                {"code": "3C", "cause": "błąd obrotów bębna suszarki", "part": "pasek / silnik", "price_range_pln": "100-240"}
            ]
        },
        "naprawa-pralko-suszarek": {
            "common_errors": [
                {"code": "FE", "cause": "problem z wentylatorem suszenia lub kanałem powietrznym", "part": "silnik wentylatora / czyszczenie", "price_range_pln": "150-270"}
            ]
        }
    },

    "whirlpool": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "F08 / F12 (Czerwony klucz)", "cause": "awaria układu grzewczego lub przekaźnika na płycie", "part": "grzałka / przekaźnik", "price_range_pln": "90-180"},
                {"code": "F06", "cause": "brak sygnału z obrotomierza silnika 6-ty Zmysł", "part": "czujnik tacho / silnik", "price_range_pln": "90-170"},
                {"code": "F05 / Miganie kranika", "cause": "zablokowana pompa odpływowa lub czujnik NTC", "part": "pompa odpływowa", "price_range_pln": "85-160"},
                {"code": "Service / Czerwona dioda serwisu", "cause": "błąd krytyczny modułu sterującego lub wyciek", "part": "moduł główny", "price_range_pln": "150-320"}
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {"code": "ALARM + Pisk / Dioda trójkąta", "cause": "zbyt wysoka temperatura, awaria sprężarki lub wyciek freonu", "part": "termostat / napełnienie układu", "price_range_pln": "200-500"},
                {"code": "AL02", "cause": "usterka czujnika NTC parownika", "part": "czujnik temperatury", "price_range_pln": "70-140"}
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {"code": "F6 / E4 (Miga dioda start)", "cause": "brak dopływu wody do komory zmywarki", "part": "zawór dopływowy / AquaStop", "price_range_pln": "85-160"},
                {"code": "F8 / E1", "cause": "zablokowany filtr lub czujnik zmętnienia wody OWI", "part": "czujnik OWI / czyszczenie", "price_range_pln": "110-200"},
                {"code": "F12 / E2", "cause": "błąd komunikacji płytki sterującej", "part": "moduł sterowania", "price_range_pln": "160-300"}
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {"code": "F03 / F04", "cause": "błąd czujnika temperatury lub przegrzanie", "part": "sonda temperatury", "price_range_pln": "90-180"}
            ]
        },
        "naprawa-suszarek": {
            "common_errors": [
                {"code": "F04 / Czerwona dioda filtra", "cause": "błąd czujnika wilgotności lub zapchany wymiennik", "part": "czujnik wilgotności", "price_range_pln": "100-190"}
            ]
        }
    },

    "beko": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "E01 / Miga ikonka drzwi", "cause": "uszkodzona blokada drzwi pralki", "part": "elektroblokada drzwiczek", "price_range_pln": "60-120"},
                {"code": "E04", "cause": "ciągłe pobieranie wody, uszkodzony hydrostat", "part": "czujnik poziomu wody", "price_range_pln": "70-130"},
                {"code": "E08 / E09", "cause": "brak poboru wody lub błąd wylewania", "part": "elektrozawór / pompa", "price_range_pln": "75-150"},
                {"code": "E11", "cause": "błąd silnika lub zużycie szczotek", "part": "szczotki węglowe", "price_range_pln": "80-160"}
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {"code": "Wykrzyknik w trójkącie (!)", "cause": "wzrost temperatury w zamrażarce, awaria układu No-Frost", "part": "grzałka / wentylator No-Frost", "price_range_pln": "110-230"},
                {"code": "E4", "cause": "usterka grzałki odmrażania No-Frost", "part": "grzałka parownika", "price_range_pln": "110-200"},
                {"code": "E9", "cause": "awaria kostkarki lub czujnika temperatury", "part": "czujnik NTC", "price_range_pln": "80-150"}
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {"code": "Er 1 / Er 2 (Sygnał piskowy)", "cause": "wyciek wody lub błąd czujnika zalania w misie", "part": "pływak / czujnik wycieku", "price_range_pln": "75-150"},
                {"code": "Er 3", "cause": "problem z nagrzewaniem wody", "part": "grzałka przepływowa", "price_range_pln": "120-220"}
            ]
        },
        "naprawa-piekarnikow": {
            "common_errors": [
                {"code": "Er 0 / Er 2", "cause": "błąd czujnika temperatury lub elektroniki", "part": "termopara / moduł", "price_range_pln": "80-170"}
            ]
        }
    },

    "electrolux": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "E20 / E21 / C2", "cause": "problem z odpływem wody, zablokowany filtr lub pompa", "part": "pompa spustowa", "price_range_pln": "90-180"},
                {"code": "E40 / E41", "cause": "problem z zamknięciem drzwi pralki", "part": "zamek drzwi", "price_range_pln": "80-150"},
                {"code": "E10 / C1", "cause": "brak poboru wody w wyznaczonym czasie", "part": "zawór wlewowy", "price_range_pln": "85-160"},
                {"code": "E60 / E61", "cause": "błąd grzania wody, uszkodzony element grzejny", "part": "grzałka", "price_range_pln": "95-180"}
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {"code": "i20 / 2 piski", "cause": "niedrożny tor odpływowy zmywarki lub uszkodzony hydrostat", "part": "czyszczenie / pompa", "price_range_pln": "100-190"},
                {"code": "i30 / 3 piski", "cause": "zadziałał system przeciwzalaniowy AquaControl", "part": "uszczelka / wąż", "price_range_pln": "90-210"},
                {"code": "i10 / 1 pisk", "cause": "problem z pobieraniem воды", "part": "zawór AquaControl", "price_range_pln": "95-180"}
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {"code": "Miganie ikonki Warning / Pisk", "cause": "zbyt высокая температура w komorze", "part": "czujnik NTC / agregat", "price_range_pln": "120-350"},
                {"code": "błąd b1-b4", "cause": "uszkodzenie czujnika temperatury parownika", "part": "czujnik NTC", "price_range_pln": "85-160"}
            ]
        }
    },

    "lg": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "OE", "cause": "brak odpływu wody w wyznaczonym czasie", "part": "pompa odpływowa", "price_range_pln": "95-190"},
                {"code": "IE", "cause": "błąd dopływu wody, zatkany filtr siatkowy", "part": "zawór wlewowy", "price_range_pln": "85-160"},
                {"code": "UE / LE", "cause": "błąd przeciążenia silnika Direct Drive lub czujnika Halla", "part": "czujnik Halla (Hall sensor)", "price_range_pln": "110-220"},
                {"code": "dE / dE1", "cause": "problem z zamknięciem drzwiczek", "part": "blokada drzwi", "price_range_pln": "80-150"},
                {"code": "tE", "cause": "błąd termistora (czujnika temperatury)", "part": "termistor", "price_range_pln": "75-140"}
            ]
        },
        "naprawa-lodowek": {
            "common_errors": [
                {"code": "Er FF", "cause": "awaria wentylatora zamrażalnika No-Frost", "part": "silnik wentylatora", "price_range_pln": "130-220"},
                {"code": "Er dH", "cause": "błąd rozmrażania parownika", "part": "grzałka defrost / bezpiecznik", "price_range_pln": "120-210"},
                {"code": "Er CF", "cause": "błąd wentylatora skraplacza z tyłu", "part": "wentylator skraplacza", "price_range_pln": "110-200"}
            ]
        }
    },

    "siemens": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "E18 / F18", "cause": "niedrożność pompy spustowej", "part": "pompa odpływowa", "price_range_pln": "120-250"},
                {"code": "E23", "cause": "aktywacja AquaStop przy wycieku", "part": "czujnik AquaStop", "price_range_pln": "100-200"}
            ]
        },
        "naprawa-zmywarek": {
            "common_errors": [
                {"code": "E15", "cause": "aktywacja czujnika zalania w misie", "part": "uszczelka pompy", "price_range_pln": "110-230"},
                {"code": "E09", "cause": "awaria pompy myjącej z grzałką", "part": "pompo-grzałka", "price_range_pln": "290-460"}
            ]
        }
    },

    "indesit": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "F05 / Miganie diody szybkiego prania", "cause": "zablokowana pompa odpływowa lub hydrostat", "part": "pompa / hydrostat", "price_range_pln": "70-140"},
                {"code": "F01", "cause": "zwarcie w obwodzie silnika", "part": "triak / moduł", "price_range_pln": "110-220"},
                {"code": "F06 / Miganie diody blokady", "cause": "błąd zamka drzwi lub przycisków", "part": "zamek drzwi", "price_range_pln": "65-130"}
            ]
        }
    },

    "candy": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "E03 / E3", "cause": "problem ze spuszczaniem wody w wyznaczonym czasie", "part": "pompa odpływu", "price_range_pln": "75-145"},
                {"code": "E02 / E2", "cause": "błąd pobierania wody", "part": "elektrozawór", "price_range_pln": "70-135"}
            ]
        }
    },

    "amica": {
        "naprawa-piekarnikow": {
            "common_errors": [
                {"code": "E05", "cause": "uszkodzenie czujnika temperatury PT1000", "part": "czujnik temperatury", "price_range_pln": "70-130"},
                {"code": "Miganie AUTO / Zegara", "cause": "reset программатора po zaniku napięcia", "part": "programator / zegar", "price_range_pln": "80-150"}
            ]
        },
        "naprawa-pralek": {
            "common_errors": [
                {"code": "E07", "cause": "wyciek wody do podstawy, zadziałał pływak", "part": "czujnik pływakowy", "price_range_pln": "65-130"}
            ]
        }
    },

    "gorenje": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "F3", "cause": "błąd poziomu wody / hydrostatu", "part": "hydrostat", "price_range_pln": "80-150"},
                {"code": "F7", "cause": "problem z odpływem wody", "part": "pompa spustowa", "price_range_pln": "85-160"}
            ]
        }
    },

    "ariston": {
        "naprawa-pralek": {
            "common_errors": [
                {"code": "F02", "cause": "zablokowany silnik lub czujnik tacho", "part": "czujnik obrotów", "price_range_pln": "85-160"},
                {"code": "F08", "cause": "sklejenie przekaźnika grzałki", "part": "grzałka / модул", "price_range_pln": "90-180"}
            ]
        }
    }
}

if __name__ == "__main__":
    print(f"База успешно загружена. Брендов в базе: {len(TECH_FACTS_DB)}")