from pathlib import Path

# Старые ссылки → Новые ссылки
LINK_FIXES = {
    # Города на главной странице
    'href="naprawa-pralek/szczecin/"': 'href="szczecin/"',
    'href="naprawa-pralek/stargard/"': 'href="stargard/"',
    'href="naprawa-pralek/goleniow/"': 'href="goleniow/"',
    'href="naprawa-pralek/nowogard/"': 'href="nowogard/"',
    'href="naprawa-pralek/maszewo/"': 'href="maszewo/"',
    'href="naprawa-pralek/police/"': 'href="police/"',
    'href="naprawa-pralek/pyrzyce/"': 'href="pyrzyce/"',
    
}

def fix_main_page():
    """Исправляет ссылки на главной странице index.html"""
    
    index_file = Path("index.html")
    
    if not index_file.exists():
        print("❌ index.html не найден! Запусти из корня сайта.")
        return
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    for old_link, new_link in LINK_FIXES.items():
        if old_link in content:
            content = content.replace(old_link, new_link)
            changes += 1
            print(f"✅ Заменено: {old_link} → {new_link}")
        else:
            print(f"⚠️  Не найдено: {old_link}")
    
    if changes > 0:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Сохранено! Изменено {changes} ссылок.")
    else:
        print("\n⚠️  Ссылки не найдены. Проверь содержимое index.html")

def fix_city_pages():
    """Исправляет ссылки внутри страниц городов"""
    
    cities = ["szczecin", "stargard", "goleniow", "nowogard", 
              "maszewo", "police", "pyrzyce"]
    services = [
        "naprawa-pralek",
        "naprawa-zmywarek", 
        "naprawa-lodowek",
        "naprawa-piekarnikow",
        "naprawa-suszarek"
    ]
    
    for city in cities:
        city_index = Path(city) / "index.html"
        
        if not city_index.exists():
            print(f"⚠️  {city}/index.html не найден - пропускаю")
            continue
        
        with open(city_index, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes = 0
        
        # Исправляем ссылки на услуги внутри страницы города
        for service in services:
            # Если ссылка ведет без ../ - добавляем
            old = f'href="{service}/{city}/"'
            new = f'href="../{service}/{city}/"'
            if old in content:
                content = content.replace(old, new)
                changes += 1
        
        if changes > 0:
            with open(city_index, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {city}/index.html - исправлено {changes} ссылок")
        else:
            print(f"✅ {city}/index.html - ссылки уже правильные")

def check_all_links():
    """Показывает все ссылки городов на главной странице"""
    
    index_file = Path("index.html")
    if not index_file.exists():
        print("❌ index.html не найден!")
        return
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cities = ["szczecin", "stargard", "goleniow", "nowogard",
              "maszewo", "police", "pyrzyce"]
    
    print("\n📋 ТЕКУЩИЕ ССЫЛКИ НА ГЛАВНОЙ:")
    for city in cities:
        if f'href="{city}/"' in content:
            print(f"   ✅ {city}/ - ПРАВИЛЬНО")
        elif f'href="naprawa-pralek/{city}/"' in content:
            print(f"   ❌ naprawa-pralek/{city}/ - НУЖНО ИСПРАВИТЬ → {city}/")
        else:
            print(f"   ⚠️  {city} - ссылка не найдена")

if __name__ == "__main__":
    print("🔍 ПРОВЕРКА ТЕКУЩИХ ССЫЛОК")
    check_all_links()
    
    print("\n🔨 ИСПРАВЛЯЮ ССЫЛКИ НА ГЛАВНОЙ СТРАНИЦЕ...")
    fix_main_page()
    
    print("\n🔨 ИСПРАВЛЯЮ ССЫЛКИ НА СТРАНИЦАХ ГОРОДОВ...")
    fix_city_pages()
    
    print("\n🔍 ПРОВЕРКА ПОСЛЕ ИСПРАВЛЕНИЯ")
    check_all_links()
    
    print("\n🎉 ГОТОВО!")
    print("\nСтруктура ссылок теперь:")
    print("   Главная → szczecin/")
    print("   szczecin/ → ../naprawa-pralek/szczecin/")
    print("   szczecin/ → ../naprawa-zmywarek/szczecin/")
    print("   szczecin/ → ../naprawa-lodowek/szczecin/")