import os

icons = {
    # 1. Стиральная машина (Washig machite -> Naprawa Pralek)
    "pralka.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
            <linearGradient id="doorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#475569"/>
                <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
        </defs>
        <!-- Корпус -->
        <rect x="15" y="10" width="70" height="95" rx="8" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4"/>
        <!-- Панель управления -->
        <line x1="15" y1="32" x2="85" y2="32" stroke="#1e293b" stroke-width="3"/>
        <rect x="22" y="17" width="22" height="10" rx="3" fill="#cbd5e1" stroke="#1e293b" stroke-width="2"/>
        <circle cx="58" cy="22" r="4" fill="#1e293b"/>
        <circle cx="70" cy="20" r="2" fill="#1e293b"/>
        <circle cx="76" cy="20" r="2" fill="#1e293b"/>
        <!-- Люк c объемом -->
        <circle cx="50" cy="68" r="24" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
        <circle cx="50" cy="68" r="18" fill="url(#doorGrad)" stroke="#1e293b" stroke-width="3"/>
        <path d="M 40 60 A 10 10 0 0 1 58 60" fill="none" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
        <!-- Ножки -->
        <rect x="22" y="105" width="10" height="5" rx="1" fill="#1e293b"/>
        <rect x="68" y="105" width="10" height="5" rx="1" fill="#1e293b"/>
    </svg>''',

    # 2. Посудомоечная машина (Dishwasher -> Naprawa Zmywarek)
    "zmywarka.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
        </defs>
        <!-- Корпус -->
        <rect x="15" y="10" width="70" height="95" rx="8" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4"/>
        <!-- Панель управления -->
        <line x1="15" y1="28" x2="85" y2="28" stroke="#1e293b" stroke-width="3"/>
        <circle cx="25" cy="19" r="2" fill="#1e293b"/>
        <circle cx="31" cy="19" r="2" fill="#1e293b"/>
        <circle cx="37" cy="19" r="2" fill="#1e293b"/>
        <rect x="62" y="15" width="14" height="8" rx="2" fill="#1e293b"/>
        <!-- Линия дверцы -->
        <line x1="15" y1="34" x2="85" y2="34" stroke="#1e293b" stroke-width="2"/>
        <!-- Ручка -->
        <rect x="30" y="42" width="40" height="6" rx="3" fill="#cbd5e1" stroke="#1e293b" stroke-width="2.5"/>
        <!-- Ножки -->
        <rect x="22" y="105" width="10" height="5" rx="1" fill="#1e293b"/>
        <rect x="68" y="105" width="10" height="5" rx="1" fill="#1e293b"/>
    </svg>''',

    # 3. Холодильник (Refrigerator -> Naprawa Lodówek)
    "lodowka.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#cbd5e1"/>
            </linearGradient>
        </defs>
        <!-- Корпус -->
        <rect x="22" y="6" width="56" height="106" rx="7" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4"/>
        <!-- Разделение морозилки и холодильника -->
        <line x1="22" y1="48" x2="78" y2="48" stroke="#1e293b" stroke-width="4"/>
        <!-- Ручка верхняя -->
        <rect x="28" y="20" width="4" height="18" rx="2" fill="#1e293b"/>
        <!-- Ручка нижняя -->
        <rect x="28" y="58" width="4" height="24" rx="2" fill="#1e293b"/>
    </svg>''',

    # 4. Духовой шкаф / Плита (Oven -> Naprawa Piekarników)
    "piekarnik.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
            <linearGradient id="glassGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#334155"/>
                <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
        </defs>
        <!-- Корпус -->
        <rect x="15" y="10" width="70" height="95" rx="8" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4"/>
        <!-- Ручки конфорок -->
        <circle cx="26" cy="22" r="4" fill="#1e293b"/>
        <circle cx="38" cy="22" r="4" fill="#1e293b"/>
        <circle cx="50" cy="22" r="4" fill="#1e293b"/>
        <circle cx="62" cy="22" r="4" fill="#1e293b"/>
        <circle cx="74" cy="22" r="4" fill="#1e293b"/>
        <line x1="15" y1="34" x2="85" y2="34" stroke="#1e293b" stroke-width="3"/>
        <!-- Дверца духовки -->
        <rect x="22" y="42" width="56" height="52" rx="5" fill="url(#glassGrad)" stroke="#1e293b" stroke-width="3"/>
        <!-- Ручка духовки -->
        <rect x="28" y="47" width="44" height="5" rx="2" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
    </svg>''',

    # 5. Сушильная машина (Dryer -> Naprawa Suszarek)
    "suszarka.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
        </defs>
        <rect x="15" y="10" width="70" height="95" rx="8" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4"/>
        <line x1="15" y1="32" x2="85" y2="32" stroke="#1e293b" stroke-width="3"/>
        <circle cx="28" cy="21" r="5" fill="#1e293b"/>
        <rect x="55" y="17" width="18" height="8" rx="2" fill="#cbd5e1" stroke="#1e293b" stroke-width="2"/>
        <!-- Люк сушки -->
        <circle cx="50" cy="68" r="24" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
        <circle cx="50" cy="68" r="18" fill="#94a3b8" opacity="0.3" stroke="#1e293b" stroke-width="3"/>
        <path d="M 42 68 Q 50 58 58 68 T 50 78" fill="none" stroke="#f97316" stroke-width="4" stroke-linecap="round"/>
        <rect x="22" y="105" width="10" height="5" rx="1" fill="#1e293b"/>
        <rect x="68" y="105" width="10" height="5" rx="1" fill="#1e293b"/>
    </svg>''',

    # 6. Стирально-сушильная машина
    "pralko-suszarka.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
            <linearGradient id="doorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#334155"/>
                <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
        </defs>
        <rect x="15" y="10" width="70" height="95" rx="8" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4"/>
        <line x1="15" y1="32" x2="85" y2="32" stroke="#1e293b" stroke-width="3"/>
        <circle cx="30" cy="21" r="4" fill="#1e293b"/>
        <circle cx="42" cy="21" r="4" fill="#1e293b"/>
        <circle cx="50" cy="68" r="24" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
        <circle cx="50" cy="68" r="18" fill="url(#doorGrad)" stroke="#1e293b" stroke-width="3"/>
        <path d="M 42 62 A 8 8 0 0 1 58 62" fill="none" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
    </svg>''',

    # 7. Szybki Dojazd
    "szybki-dojazd.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
        </defs>
        <path d="M 10 50 L 55 50 L 72 68 L 90 68 L 90 90 L 10 90 Z" fill="url(#bodyGrad)" stroke="#1e293b" stroke-width="4" stroke-linejoin="round"/>
        <rect x="56" y="56" width="14" height="12" rx="2" fill="#94a3b8" stroke="#1e293b" stroke-width="2"/>
        <circle cx="30" cy="90" r="10" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
        <circle cx="30" cy="90" r="4" fill="#1e293b"/>
        <circle cx="72" cy="90" r="10" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
        <circle cx="72" cy="90" r="4" fill="#1e293b"/>
    </svg>'''
}

os.makedirs("icons", exist_ok=True)
for name, code in icons.items():
    with open(f"icons/{name}", "w", encoding="utf-8") as f:
        f.write(code.strip())

print("Все 7 иконок созданы с объемом и точной геометрией макета.")