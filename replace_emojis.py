import os
import re

EMOJI_TO_CITY = {
    '🏙': ('szczecin', 'Szczecin'),
    '🏛': ('stargard', 'Stargard'),
    '✈': ('goleniow', 'Goleniów'),
    '🌳': ('nowogard', 'Nowogard'),
    '🌾': ('maszewo', 'Maszewo'),
    '🏭': ('police', 'Police'),
    '🏘': ('pyrzyce', 'Pyrzyce')
}

processed_count = 0
changed_count = 0

print("🚀 Запуск обработки HTML-файлов...")

SCRIPT_RE = re.compile(r'(<script\b[^>]*>.*?</script>)', flags=re.DOTALL | re.IGNORECASE)

for root, dirs, files in os.walk('.'):
    if '_backups' in root or '.git' in root or 'node_modules' in root:
        continue

    for file in files:
        if not file.endswith('.html'):
            continue

        file_path = os.path.join(root, file)
        processed_count += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[ОШИБКА ЧТЕНИЯ] {file_path}: {e}")
            continue

        parts = SCRIPT_RE.split(content)
        new_parts = []
        file_changed = False

        for part in parts:
            if part.lower().startswith('<script'):
                new_parts.append(part)
                continue

            original_part = part

            for emoji, (slug, name) in EMOJI_TO_CITY.items():
                img_tag = f'<img src="/icons/herb-{slug}.svg" alt="{name}" class="city-herb-icon" width="48" height="48" loading="lazy">'
                
                # 1. Замена контейнера с эмодзи целиком (если есть <div class="service-icon">)
                pattern_div = r'<div class="service-icon">\s*' + emoji + r'\ufe0f?\s*</div>'
                part = re.sub(pattern_div, f'<div class="service-icon">{img_tag}</div>', part)

                # 2. Одиночная замена эмодзи, если он вне div
                pattern_single = emoji + r'\ufe0f?'
                part = re.sub(pattern_single, img_tag, part)

            # Исправление опечатки в названии Голенюва
            part = part.replace('<h3>goleniow</h3>', '<h3>Goleniów</h3>')

            if part != original_part:
                file_changed = True

            new_parts.append(part)

        if file_changed:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("".join(new_parts))
                changed_count += 1
                print(f"[ИСПРАВЛЕНО] {file_path}")
            except Exception as e:
                print(f"[ОШИБКА ЗАПИСИ] {file_path}: {e}")

print(f"\n✅ Готово!")
print(f"Всего проверено HTML-файлов: {processed_count}")
print(f"Файлов с изменениями: {changed_count}")