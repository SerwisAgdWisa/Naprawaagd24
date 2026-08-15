#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
upgrade_site.py v7.0 - Production Safe Edition
================================================

Массовая безопасная обработка HTML/PHP-файлов сайта.

Что делает:

1. Исправляет:
       window.location.href(url, '_blank')
   на:
       window.open(url, '_blank')

   Только внутри <script>, без изменения комментариев и строк JS.

2. Оборачивает:
       <section>...</section>
       <section id="order">...</section>

   в:

       <div class="dashboard-grid">
           <div class="dashboard-left">...</div>
           <div class="dashboard-right">...</div>
       </div>

3. Заменяет emoji-иконки услуг на SVG:
       <div class="service-icon">...</div>

4. Исправляет известные повреждённые:
       <l<secti>
       </l<secti>

   и только действительно подозрительные двойные <ul>.

5. Улучшает существующую sticky phone panel:
   - НЕ уничтожает весь блок;
   - НЕ меняет существующий tel: URL;
   - сохраняет существующие атрибуты;
   - добавляет SVG только при необходимости;
   - [ФИКС] убирает исходный emoji 📞 из текста, чтобы не получить
     две иконки телефона подряд после прохода replace_loose_emojis.

6. Улучшает существующую WhatsApp-кнопку:
   - НЕ меняет существующий href;
   - НЕ меняет номер;
   - сохраняет атрибуты;
   - добавляет target/rel/aria-label только если их нет;
   - добавляет SVG;
   - [ФИКС] убирает исходный emoji 💬 по той же причине.

7. Заменяет одиночные:
       📞
       💬
   только в текстовом HTML-контенте.

8. Защищает:
   - HTML-комментарии
   - <script>
   - <style>
   - <textarea>
   - <template>
   - PHP <?php ... ?>

9. Сохраняет:
   - UTF-8
   - UTF-8 BOM
   - CP1250
   - CP1251
   - исходные CRLF/LF

10. Перед реальной записью:
   - создаёт backup;
   - пишет во временный файл;
   - fsync;
   - делает os.replace().

11. Полный --self-test (расширен проверкой на дубли иконок в п.5/6).

Примеры:

    python upgrade_site.py --self-test
    python upgrade_site.py C:\\site --dry-run
    python upgrade_site.py C:\\site --dry-run --verbose
    python upgrade_site.py C:\\site
    python upgrade_site.py C:\\site --backup-dir C:\\site_backups
    python upgrade_site.py C:\\site --no-backup

По умолчанию реальные изменения получают backup в:

    <site>/_backups/<timestamp>/

Поддерживаемые файлы:

    .html
    .htm
    .php
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_EXCLUDE_DIRS = {
    "_backups", "backup", "backups", ".old", ".git", ".svn", "node_modules",
}

SUPPORTED_EXTENSIONS = {".html", ".htm", ".php"}

PHONE_SVG = (
    '<svg class="icon-phone" viewBox="0 0 24 24" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2'
    'c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57'
    '.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.61 21 3 13.39 3 4'
    'c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57'
    '3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>'
    '</svg>'
)

WHATSAPP_SVG = (
    '<svg class="icon-whatsapp" viewBox="0 0 32 32" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M16 0C7.163 0 0 7.163 0 16c0 2.825.737 5.607 '
    '2.137 8.048L0 32l8.135-2.135A15.94 15.94 0 0016 32'
    'c8.837 0 16-7.163 16-16S24.837 0 16 0zm0 29.333'
    'c-2.482 0-4.908-.647-7.042-1.872l-.505-.292-5.228 1.372'
    ' 1.395-5.197-.323-.513A13.3 13.3 0 012.667 16'
    'C2.667 8.649 8.649 2.667 16 2.667S29.333 8.649'
    '29.333 16 23.351 29.333 16 29.333z"/>'
    '</svg>'
)

SMALL_PHONE_SVG = (
    '<svg class="icon-inline icon-phone" viewBox="0 0 24 24" '
    'width="16" height="16" fill="currentColor" '
    'style="vertical-align:-3px;margin-right:4px;" '
    'aria-hidden="true">'
    '<path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2'
    'c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57'
    '.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.61 21 3 13.39 3 4'
    'c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57'
    '3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>'
    '</svg>'
)

SMALL_CHAT_SVG = (
    '<svg class="icon-inline icon-chat" viewBox="0 0 24 24" '
    'width="16" height="16" fill="currentColor" '
    'style="vertical-align:-3px;margin-right:4px;" '
    'aria-hidden="true">'
    '<path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14'
    'c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/>'
    '</svg>'
)


URL_ICON_MAP: List[Tuple[str, str, str]] = [
    ("naprawa-pralko-suszarek", "pralko-suszarka.svg", "Naprawa pralko-suszarek"),
    ("pralko-suszar", "pralko-suszarka.svg", "Naprawa pralko-suszarek"),
    ("naprawa-pralek", "pralka.svg", "Naprawa pralek"),
    ("naprawa-zmywarek", "zmywarka.svg", "Naprawa zmywarek"),
    ("naprawa-lodowek", "lodowka.svg", "Naprawa lodówek"),
    ("naprawa-piekarnikow", "piekarnik.svg", "Naprawa piekarników"),
    ("naprawa-suszarek", "suszarka.svg", "Naprawa suszarek"),
]


NON_CONTENT_RE = re.compile(
    r"<!--.*?-->"
    r"|<script\b[^>]*>.*?</script\s*>"
    r"|<style\b[^>]*>.*?</style\s*>"
    r"|<textarea\b[^>]*>.*?</textarea\s*>"
    r"|<template\b[^>]*>.*?</template\s*>"
    r"|<\?php.*?\?>",
    re.IGNORECASE | re.DOTALL,
)

SCRIPT_RE = re.compile(
    r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script\s*>",
    re.IGNORECASE | re.DOTALL,
)

TAG_RE = re.compile(
    r"<(?P<close>/?)\s*(?P<name>[A-Za-z][A-Za-z0-9:_-]*)\b"
    r"(?P<attrs>[^>]*?)>",
    re.DOTALL,
)

ORDER_ATTR_RE = re.compile(
    r"\bid\s*=\s*(?:([\"'])order\1|order\b)",
    re.IGNORECASE,
)

DASHBOARD_CLASS_RE = re.compile(
    r"\bclass\s*=\s*([\"'])[^\"']*\bdashboard-grid\b[^\"']*\1",
    re.IGNORECASE,
)

WHATSAPP_BUG_RE = re.compile(
    r"window\s*\.\s*location\s*\.\s*href"
    r"\s*\(\s*([^,()]+?)\s*,\s*([\"'])_blank\2\s*\)",
    re.IGNORECASE,
)

BROKEN_LI_RE = re.compile(
    r"</?l<secti>",
    re.IGNORECASE,
)

SUSPICIOUS_PATTERNS = [
    (re.compile(r"<l<\w+>", re.IGNORECASE), "Неизвестный повреждённый открывающий тег"),
    (re.compile(r"</l<\w+>", re.IGNORECASE), "Неизвестный повреждённый закрывающий тег"),
    (re.compile(r"<ul\b[^>]*>\s*<ul\b", re.IGNORECASE), "Подозрительная вложенность <ul>"),
]

SERVICE_ICON_OPEN_RE = re.compile(
    r"<div\b(?P<attrs>[^>]*\bclass\s*=\s*"
    r"([\"'])[^\"']*\bservice-icon\b[^\"']*\2[^>]*)>",
    re.IGNORECASE | re.DOTALL,
)

STICKY_CLASS_RE = re.compile(
    r"\bclass\s*=\s*([\"'])[^\"']*\bsticky-bottom-bar\b[^\"']*\1",
    re.IGNORECASE,
)

WHATSAPP_FLOAT_CLASS_RE = re.compile(
    r"\bclass\s*=\s*([\"'])[^\"']*\bwhatsapp-float\b[^\"']*\1",
    re.IGNORECASE,
)

TEL_RE = re.compile(
    r"\bhref\s*=\s*([\"'])tel:[^\"']*\1",
    re.IGNORECASE,
)

ONLY_WS_COMMENTS_RE = re.compile(
    r"^(?:\s|<!--.*?-->)*$",
    re.DOTALL,
)


@dataclass
class FileData:
    path: Path
    raw: bytes
    text: str
    encoding: str
    bom: bool
    newline: str


@dataclass
class TransformStats:
    whatsapp_fixed: int = 0
    dashboard_wrapped: int = 0
    dashboard_already: int = 0
    dashboard_skipped: int = 0
    icons_replaced: int = 0
    corruption_fixed: int = 0
    buttons_upgraded: int = 0
    loose_emojis: int = 0
    suspicious: List[Tuple[str, str]] = field(default_factory=list)

    def changed_count(self) -> int:
        return (
            self.whatsapp_fixed + self.dashboard_wrapped + self.icons_replaced
            + self.corruption_fixed + self.buttons_upgraded + self.loose_emojis
        )


def get_html_attr(attrs_str: str, attr_name: str) -> Optional[str]:
    pattern = re.compile(
        rf"\b{re.escape(attr_name)}\s*=\s*"
        rf"(?:(['\"])(.*?)\1|([^\s>]+))",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(attrs_str)
    if not match:
        return None
    if match.group(1):
        return match.group(2)
    return match.group(3)


def has_class(attrs: str, class_name: str) -> bool:
    value = get_html_attr(attrs, "class") or ""
    return re.search(
        rf"(?<![\w-]){re.escape(class_name)}(?![\w-])", value, re.IGNORECASE,
    ) is not None


def add_class_to_open_tag(open_tag: str, class_name: str) -> str:
    if has_class(open_tag, class_name):
        return open_tag
    class_re = re.compile(r"(\bclass\s*=\s*)([\"'])(.*?)(\2)", re.IGNORECASE | re.DOTALL)
    match = class_re.search(open_tag)
    if match:
        current = match.group(3)
        replacement = (
            match.group(1) + match.group(2) + current
            + (" " if current and not current.endswith(" ") else "")
            + class_name + match.group(4)
        )
        return open_tag[:match.start()] + replacement + open_tag[match.end():]
    pos = open_tag.rfind(">")
    if pos < 0:
        return open_tag
    before = open_tag[:pos]
    if before.rstrip().endswith("/"):
        slash_pos = len(before.rstrip()) - 1
        return open_tag[:slash_pos] + f' class="{class_name}"' + open_tag[slash_pos:]
    return open_tag[:pos] + f' class="{class_name}"' + open_tag[pos:]


def mask_non_content_zones(text: str) -> str:
    chars = list(text)
    for match in NON_CONTENT_RE.finditer(text):
        for i in range(match.start(), match.end()):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def detect_newline(raw: bytes) -> str:
    if b"\r\n" in raw:
        return "\r\n"
    if b"\n" in raw:
        return "\n"
    if b"\r" in raw:
        return "\r"
    return "\n"


def normalize_newline(text: str, newline: str) -> str:
    if newline == "\r\n":
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return text.replace("\n", "\r\n")
    if newline == "\r":
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return text.replace("\n", "\r")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def encoding_hint(raw: bytes) -> Optional[str]:
    head = raw[:8192].lower()
    if b"windows-1251" in head or b"cp1251" in head:
        return "cp1251"
    if b"windows-1250" in head or b"cp1250" in head:
        return "cp1250"
    if b"utf-8" in head:
        return "utf-8"
    return None


def decode_file(path: Path) -> Optional[FileData]:
    raw = path.read_bytes()
    newline = detect_newline(raw)

    if raw.startswith(b"\xef\xbb\xbf"):
        try:
            text = raw[3:].decode("utf-8")
            return FileData(path=path, raw=raw, text=text, encoding="utf-8", bom=True, newline=newline)
        except UnicodeDecodeError:
            return None

    try:
        text = raw.decode("utf-8")
        return FileData(path=path, raw=raw, text=text, encoding="utf-8", bom=False, newline=newline)
    except UnicodeDecodeError:
        pass

    hint = encoding_hint(raw)
    candidates = ["cp1250", "cp1251"]
    if hint in candidates:
        candidates.remove(hint)
        candidates.insert(0, hint)

    decoded: List[Tuple[str, str]] = []
    for enc in candidates:
        try:
            decoded.append((enc, raw.decode(enc)))
        except UnicodeDecodeError:
            pass

    if not decoded:
        return None

    if len(decoded) == 1:
        enc, text = decoded[0]
        return FileData(path=path, raw=raw, text=text, encoding=enc, bom=False, newline=newline)

    def score_cp1251(value: str) -> int:
        return sum(1 for char in value if "\u0400" <= char <= "\u04ff")

    def score_cp1250(value: str) -> int:
        polish = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
        return sum(value.count(ch) for ch in polish)

    cp1251_text = next(text for enc, text in decoded if enc == "cp1251")
    cp1250_text = next(text for enc, text in decoded if enc == "cp1250")

    score1 = score_cp1251(cp1251_text)
    score0 = score_cp1250(cp1250_text)

    if score1 > score0:
        enc, text = "cp1251", cp1251_text
    else:
        enc, text = "cp1250", cp1250_text

    return FileData(path=path, raw=raw, text=text, encoding=enc, bom=False, newline=newline)


def encode_file(data: FileData, text: str) -> bytes:
    text = normalize_newline(text, data.newline)
    body = text.encode(data.encoding)
    if data.bom and data.encoding == "utf-8":
        return b"\xef\xbb\xbf" + body
    return body


@dataclass
class ElementSpan:
    start: int
    end: int
    open_end: int
    name: str
    attrs: str


def find_elements(text: str, tag_name: str) -> List[ElementSpan]:
    masked = mask_non_content_zones(text)
    wanted = tag_name.lower()
    stack: List[Tuple[int, int, str]] = []
    result: List[ElementSpan] = []
    for match in TAG_RE.finditer(masked):
        name = match.group("name").lower()
        if name != wanted:
            continue
        closing = bool(match.group("close"))
        raw_tag = match.group(0)
        if closing:
            if not stack:
                continue
            start, open_end, attrs = stack.pop()
            result.append(ElementSpan(start=start, end=match.end(), open_end=open_end, name=wanted, attrs=attrs))
        else:
            if raw_tag.rstrip().endswith("/>"):
                continue
            stack.append((match.start(), match.end(), match.group("attrs") or ""))
    result.sort(key=lambda item: item.start)
    return result


def element_contains(outer: ElementSpan, inner: ElementSpan) -> bool:
    return outer.start <= inner.start and outer.end >= inner.end


def mask_js_non_code(text: str) -> str:
    chars = list(text)
    i = 0
    n = len(text)
    state = "code"
    quote = ""
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if state == "code":
            if c == "/" and nxt == "/":
                chars[i] = " "; chars[i + 1] = " "; i += 2
                while i < n and text[i] not in "\r\n":
                    chars[i] = " "; i += 1
                continue
            if c == "/" and nxt == "*":
                chars[i] = " "; chars[i + 1] = " "; i += 2
                while i < n:
                    if text[i] == "*" and i + 1 < n and text[i + 1] == "/":
                        chars[i] = " "; chars[i + 1] = " "; i += 2
                        break
                    if text[i] != "\n":
                        chars[i] = " "
                    i += 1
                continue
            if c in ("'", '"', "`"):
                quote = c; state = "string"; chars[i] = " "; i += 1
                continue
            i += 1
            continue
        if state == "string":
            if c == "\\":
                if text[i] != "\n":
                    chars[i] = " "
                if i + 1 < n:
                    if text[i + 1] != "\n":
                        chars[i + 1] = " "
                    i += 2
                else:
                    i += 1
                continue
            if c == quote:
                chars[i] = " "; i += 1; state = "code"
                continue
            if c != "\n":
                chars[i] = " "
            i += 1
    return "".join(chars)


def fix_whatsapp_bug(text: str) -> Tuple[str, int]:
    """
    ВАЖНО: ищем паттерн в ИСХОДНОМ (немаскированном) теле скрипта, а не в
    mask_js_non_code(body). Причина: сам целевой вызов
        window.location.href(url, '_blank')
    содержит строковый литерал '_blank' как часть своего нормального
    синтаксиса — если сначала замаскировать все JS-строки (как задумано
    для защиты произвольных строк от случайного совпадения), то и этот
    '_blank' тоже превращается в пробелы, и WHATSAPP_BUG_RE перестаёт
    находить хоть что-то. В исходной версии это приводило к тому, что
    функция ВСЕГДА возвращала 0 совпадений, независимо от содержимого.

    Вместо этого ищем на исходном body (кавычки на месте), а маску
    используем только для ПРОВЕРКИ каждого найденного совпадения: если
    символ начала совпадения ('w' от "window") в маскированной версии
    оказался пробелом — значит весь вызов на самом деле лежит внутри
    чужой строки или комментария, и его нужно пропустить.
    """
    total = 0
    replacements: List[Tuple[int, int, str]] = []
    for script_match in SCRIPT_RE.finditer(text):
        body_start = script_match.start("body")
        body = script_match.group("body")
        masked = mask_js_non_code(body)
        for match in WHATSAPP_BUG_RE.finditer(body):
            if masked[match.start()] == " " and body[match.start()] != " ":
                continue  # совпадение внутри строки/комментария — не трогаем
            arg1 = body[match.start(1):match.end(1)]
            quote = body[match.start(2):match.end(2)]
            replacement = f"window.open({arg1}, {quote}_blank{quote})"
            replacements.append((body_start + match.start(), body_start + match.end(), replacement))
    if not replacements:
        return text, 0
    new_text = text
    for start, end, replacement in reversed(replacements):
        new_text = new_text[:start] + replacement + new_text[end:]
        total += 1
    return new_text, total


def wrap_dashboard_grid(text: str) -> Tuple[str, bool, str]:
    if "dashboard-grid" in text:
        return text, False, "dashboard-grid уже присутствует"
    sections = find_elements(text, "section")
    if not sections:
        return text, False, "section не найдены"
    order_idx: Optional[int] = None
    for i, section in enumerate(sections):
        if ORDER_ATTR_RE.search(section.attrs):
            order_idx = i
            break
    if order_idx is None:
        return text, False, "section #order не найдена"
    if order_idx == 0:
        return text, False, "перед #order нет предыдущей section"
    previous = sections[order_idx - 1]
    order = sections[order_idx]
    between = text[previous.end:order.start]
    if not ONLY_WS_COMMENTS_RE.match(between):
        return text, False, "между section есть посторонний контент"
    previous_html = text[previous.start:previous.end]
    order_html = text[order.start:order.end]
    wrapped = (
        '<div class="dashboard-grid">\n'
        '    <div class="dashboard-left">\n'
        f'{previous_html}\n'
        '    </div>\n'
        '    <div class="dashboard-right">\n'
        f'{order_html}\n'
        '    </div>\n'
        '</div>'
    )
    new_text = text[:previous.start] + wrapped + text[order.end:]
    return new_text, True, ""


def replace_span(text: str, start: int, end: int, replacement: str) -> str:
    return text[:start] + replacement + text[end:]


def fix_service_icons(text: str) -> Tuple[str, int]:
    divs = find_elements(text, "div")
    anchors = find_elements(text, "a")
    candidates: List[Tuple[ElementSpan, Optional[ElementSpan]]] = []
    for div in divs:
        opening = text[div.start:div.open_end]
        if not SERVICE_ICON_OPEN_RE.search(opening):
            continue
        containing_anchors = [a for a in anchors if element_contains(a, div)]
        anchor = None
        if containing_anchors:
            anchor = min(containing_anchors, key=lambda item: item.end - item.start)
        candidates.append((div, anchor))
    if not candidates:
        return text, 0
    replacements: List[Tuple[int, int, str]] = []
    for div, anchor in candidates:
        inner_start = div.open_end
        inner_end = div.end - len("</div>")
        if inner_end < inner_start:
            continue
        content = text[inner_start:inner_end]
        if "service-icon-img" in content:
            continue
        href = ""
        if anchor is not None:
            anchor_open = text[anchor.start:anchor.open_end]
            href = get_html_attr(anchor_open, "href") or ""
        href_lower = href.lower()
        chosen_svg: Optional[str] = None
        alt_text = ""
        for key, svg_file, alt in URL_ICON_MAP:
            if key in href_lower:
                chosen_svg = svg_file
                alt_text = alt
                break
        if chosen_svg is None:
            if "⚡" in content or "\u26a1" in content:
                if href == "" or href == "#" or href.startswith("#"):
                    chosen_svg = "szybki-dojazd.svg"
                    alt_text = "Szybki dojazd"
        if chosen_svg is None:
            continue
        img_tag = (
            f'<img src="/icons/{chosen_svg}" alt="{alt_text}" '
            'class="service-icon-img" width="40" height="40" loading="lazy">'
        )
        replacements.append((inner_start, inner_end, img_tag))
    for start, end, replacement in reversed(replacements):
        text = replace_span(text, start, end, replacement)
    return text, len(replacements)


def apply_masked_regex_replacements(text: str, pattern, replacer) -> Tuple[str, int]:
    masked = mask_non_content_zones(text)
    matches = list(pattern.finditer(masked))
    if not matches:
        return text, 0
    result = text
    for match in reversed(matches):
        replacement = replacer(match, text)
        result = result[:match.start()] + replacement + result[match.end():]
    return result, len(matches)


def fix_corrupted_tags(text: str) -> Tuple[str, int]:
    count = 0

    def li_replacer(match, original):
        token = original[match.start():match.end()]
        if token.lower() == "<l<secti>":
            return "<li>"
        if token.lower() == "</l<secti>":
            return "</li>"
        return token

    text, n = apply_masked_regex_replacements(text, BROKEN_LI_RE, li_replacer)
    count += n

    masked = mask_non_content_zones(text)
    double_ul_re = re.compile(
        r"(?P<outer><ul\b[^>]*>)"
        r"(?P<ws1>\s*)"
        r"(?P<inner><ul\b[^>]*>)"
        r"(?P<content>(?:(?!</?ul\b).)*?)"
        r"(?P<inner_close></ul>)"
        r"(?P<ws2>\s*)"
        r"(?P<outer_close></ul>)",
        re.IGNORECASE | re.DOTALL,
    )
    matches = list(double_ul_re.finditer(masked))
    for match in reversed(matches):
        start = match.start()
        end = match.end()
        original_segment = text[start:end]
        original_match = re.match(
            r"(?P<outer><ul\b[^>]*>)"
            r"(?P<ws1>\s*)"
            r"(?P<inner><ul\b[^>]*>)"
            r"(?P<content>(?:(?!</?ul\b).)*?)"
            r"(?P<inner_close></ul>)"
            r"(?P<ws2>\s*)"
            r"(?P<outer_close></ul>)$",
            original_segment, re.IGNORECASE | re.DOTALL,
        )
        if not original_match:
            continue
        replacement = (
            original_match.group("outer") + original_match.group("ws1")
            + original_match.group("content") + original_match.group("inner_close")
            + original_match.group("ws2")
        )
        text = text[:start] + replacement + text[end:]
        count += 1
    return text, count


def detect_suspicious(text: str) -> List[Tuple[str, str]]:
    masked = mask_non_content_zones(text)
    findings: List[Tuple[str, str]] = []
    for pattern, description in SUSPICIOUS_PATTERNS:
        for match in pattern.finditer(masked):
            snippet = text[max(0, match.start() - 30):min(len(text), match.end() + 50)].replace("\n", " ")
            findings.append((description, snippet))
    return findings


def add_attribute_if_missing(open_tag: str, attr_name: str, value: str) -> str:
    if get_html_attr(open_tag, attr_name) is not None:
        return open_tag
    pos = open_tag.rfind(">")
    if pos < 0:
        return open_tag
    before = open_tag[:pos]
    if before.rstrip().endswith("/"):
        slash_pos = len(before.rstrip()) - 1
        return open_tag[:slash_pos] + f' {attr_name}="{value}"' + open_tag[slash_pos:]
    return open_tag[:pos] + f' {attr_name}="{value}"' + open_tag[pos:]


def upgrade_sticky_phone_bar(text: str) -> Tuple[str, int]:
    bars = find_elements(text, "div")
    target_bars = []
    for bar in bars:
        opening = text[bar.start:bar.open_end]
        if STICKY_CLASS_RE.search(opening):
            target_bars.append(bar)
    if not target_bars:
        return text, 0
    anchors = find_elements(text, "a")
    changed = 0
    for bar in reversed(target_bars):
        inner_anchors = [
            a for a in anchors
            if (element_contains(bar, a) and TEL_RE.search(text[a.start:a.open_end]))
        ]
        if not inner_anchors:
            continue
        anchor = min(inner_anchors, key=lambda item: item.end - item.start)
        open_tag = text[anchor.start:anchor.open_end]
        inner_start = anchor.open_end
        inner_end = anchor.end - len("</a>")
        inner = text[inner_start:inner_end]
        new_open = add_class_to_open_tag(open_tag, "phone-btn")
        if "icon-phone" not in inner:
            # Убираем исходный emoji 📞 перед вставкой SVG — иначе на реальных
            # файлах (где текст кнопки начинается с "📞 Zadzwoń...") получаются
            # ДВЕ иконки телефона: эта SVG + ещё одна от replace_loose_emojis,
            # которая позже заменит оставшийся emoji на маленькую inline-SVG.
            inner = PHONE_SVG + "\n" + inner.replace("📞", "").lstrip()
        if new_open == open_tag and inner == text[inner_start:inner_end]:
            continue
        text = text[:anchor.start] + new_open + text[anchor.open_end:inner_start] + inner + text[inner_end:]
        changed += 1
        anchors = find_elements(text, "a")
    return text, changed


def upgrade_whatsapp_float(text: str) -> Tuple[str, int]:
    anchors = find_elements(text, "a")
    targets = []
    for anchor in anchors:
        opening = text[anchor.start:anchor.open_end]
        if WHATSAPP_FLOAT_CLASS_RE.search(opening):
            targets.append(anchor)
    changed = 0
    for anchor in reversed(targets):
        opening = text[anchor.start:anchor.open_end]
        inner_start = anchor.open_end
        inner_end = anchor.end - len("</a>")
        inner = text[inner_start:inner_end]
        new_open = opening
        new_open = add_attribute_if_missing(new_open, "target", "_blank")
        new_open = add_attribute_if_missing(new_open, "rel", "noopener noreferrer")
        new_open = add_attribute_if_missing(new_open, "aria-label", "WhatsApp")
        if "icon-whatsapp" not in inner:
            # Аналогично убираем исходный emoji 💬, чтобы не получить два
            # значка чата подряд после прохода replace_loose_emojis.
            inner = WHATSAPP_SVG + "\n" + inner.replace("💬", "").lstrip()
        if new_open == opening and inner == text[inner_start:inner_end]:
            continue
        text = text[:anchor.start] + new_open + text[anchor.open_end:inner_start] + inner + text[inner_end:]
        changed += 1
    return text, changed


def replace_loose_emojis(text: str) -> Tuple[str, int]:
    masked = mask_non_content_zones(text)
    replacements: List[Tuple[int, str]] = []
    i = 0
    n = len(text)
    inside_tag = False
    while i < n:
        if masked[i] == " " and text[i] != " ":
            i += 1
            continue
        char = text[i]
        if char == "<":
            inside_tag = True
            i += 1
            continue
        if char == ">" and inside_tag:
            inside_tag = False
            i += 1
            continue
        if not inside_tag:
            if char == "📞":
                replacements.append((i, SMALL_PHONE_SVG))
            elif char == "💬":
                replacements.append((i, SMALL_CHAT_SVG))
        i += 1
    if not replacements:
        return text, 0
    result = text
    for index, replacement in reversed(replacements):
        result = result[:index] + replacement + result[index + 1:]
    return result, len(replacements)


def sanity_check(original: str, modified: str) -> Tuple[bool, str]:
    if original == modified:
        return False, "Изменений нет"
    if "\x00" in modified:
        return False, "В результате обнаружен NUL"
    if len(original) > 500 and len(modified) < len(original) * 0.50:
        return False, f"Результат уменьшился более чем на 50%: {len(original)} -> {len(modified)}"
    if len(original) > 1000 and len(modified) < 100:
        return False, "Итоговый HTML/PHP подозрительно мал"
    lower_original = original.lower()
    lower_modified = modified.lower()
    for tag in ("<html", "<body"):
        if tag in lower_original and tag not in lower_modified:
            return False, f"После обработки исчез {tag}"
    if "<!doctype" in lower_original and "<!doctype" not in lower_modified:
        return False, "После обработки исчез DOCTYPE"
    return True, ""


def make_backup(source: Path, root: Path, backup_root: Path, timestamp: str) -> Path:
    relative = source.relative_to(root)
    destination = backup_root / timestamp / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def atomic_write(path: Path, data: bytes) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            mode = stat.S_IMODE(path.stat().st_mode)
            os.chmod(temp_path, mode)
        except OSError:
            pass
        os.replace(temp_path, path)
        try:
            dir_fd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass
    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def process_text(text: str, args: argparse.Namespace) -> Tuple[str, TransformStats]:
    stats = TransformStats()
    if not args.skip_whatsapp:
        text, count = fix_whatsapp_bug(text)
        stats.whatsapp_fixed += count
    if not args.skip_icons:
        text, count = fix_service_icons(text)
        stats.icons_replaced += count
    if not args.skip_dashboard:
        text, wrapped, reason = wrap_dashboard_grid(text)
        if wrapped:
            stats.dashboard_wrapped += 1
        elif reason == "dashboard-grid уже присутствует":
            stats.dashboard_already += 1
        else:
            stats.dashboard_skipped += 1
    if not args.skip_corruption_check:
        text, count = fix_corrupted_tags(text)
        stats.corruption_fixed += count
        stats.suspicious = detect_suspicious(text)
    if not args.skip_buttons:
        text, count = upgrade_sticky_phone_bar(text)
        stats.buttons_upgraded += count
        text, count = upgrade_whatsapp_float(text)
        stats.buttons_upgraded += count
        text, count = replace_loose_emojis(text)
        stats.loose_emojis += count
    return text, stats


def run_self_test() -> bool:
    print("Запуск SELF-TEST v7.0 (с фиксом дублирования иконок)...")
    errors: List[str] = []

    def check(condition: bool, message: str):
        if not condition:
            errors.append(message)

    js = "\n<script>\nwindow.location.href(url, '_blank');\nwindow.location.href(a, \"_blank\");\n</script>\n"
    fixed, count = fix_whatsapp_bug(js)
    check(count == 2, "JS: ожидалось 2 исправления")
    check("window.open(url, '_blank')" in fixed, "JS: первый вызов не исправлен")
    check('window.open(a, "_blank")' in fixed, "JS: второй вызов не исправлен")

    js_string = '\n<script>\nconst x = "window.location.href(url, \'_blank\')";\n</script>\n'
    fixed_string, count = fix_whatsapp_bug(js_string)
    check(count == 0, "JS: строковый литерал был изменён")
    check(fixed_string == js_string, "JS: строковый литерал повреждён")

    js_comment = "\n<script>\n// window.location.href(url, '_blank')\n</script>\n"
    fixed_comment, count = fix_whatsapp_bug(js_comment)
    check(count == 0, "JS: комментарий был изменён")

    html = '<section>Prev</section><section id="order">Order</section>'
    result, ok, _ = wrap_dashboard_grid(html)
    check(ok, "Dashboard: section не была обёрнута")
    check('class="dashboard-grid"' in result, "Dashboard: отсутствует dashboard-grid")
    check('class="dashboard-left"' in result, "Dashboard: отсутствует dashboard-left")
    check('class="dashboard-right"' in result, "Dashboard: отсутствует dashboard-right")

    html_fake = (
        '<script>var x = "<section id=\\"order\\">fake</section>";</script>'
        '<!-- <section id="order">fake</section> -->'
        '<section>Real Prev</section>'
        '<section id="order">Real Order</section>'
    )
    result, ok, _ = wrap_dashboard_grid(html_fake)
    check(ok, "Dashboard: не найден настоящий #order")
    check("fake" in result, "Dashboard: fake content неожиданно удалён")

    service = '<a href="/naprawa-pralek"><div class="service-icon">🧺</div></a>'
    result, count = fix_service_icons(service)
    check(count == 1, "Service icon: не заменён")
    check("service-icon-img" in result, "Service icon: отсутствует service-icon-img")
    check("/icons/pralka.svg" in result, "Service icon: неправильная иконка")
    result2, count2 = fix_service_icons(result)
    check(count2 == 0 and result2 == result, "Service icon: неидемпотентный результат")

    broken = "<ul><l<secti>Item</l<secti></ul>"
    result, count = fix_corrupted_tags(broken)
    check(count == 2, "Broken LI: ожидалось 2 исправления")
    check(result == "<ul><li>Item</li></ul>", "Broken LI: неправильный результат")

    nested = "<ul><li>Main<ul><li>Sub</li></ul></li></ul>"
    result, count = fix_corrupted_tags(nested)
    check(count == 0, "Nested UL: настоящий вложенный UL был изменён")
    check(result == nested, "Nested UL: содержимое повреждено")

    phone = '<div class="sticky-bottom-bar custom"><a href="tel:+48123456789" data-x="1">Zadzwoń</a></div>'
    result, count = upgrade_sticky_phone_bar(phone)
    check(count == 1, "Sticky: кнопка не обновлена")
    check('href="tel:+48123456789"' in result, "Sticky: исходный номер был изменён")
    check('data-x="1"' in result, "Sticky: существующий атрибут потерян")
    check("icon-phone" in result, "Sticky: SVG не добавлен")
    result2, count2 = upgrade_sticky_phone_bar(result)
    check(count2 == 0 and result2 == result, "Sticky: неидемпотентность")

    # НОВЫЙ ТЕСТ: реальный сценарий с существующим emoji 📞 — не должно
    # получиться ДВЕ иконки телефона после полного пайплайна.
    phone_with_emoji = '<div class="sticky-bottom-bar"><a href="tel:+48721988949">📞 Zadzwoń teraz: +48721988949</a></div>'
    r1, _ = upgrade_sticky_phone_bar(phone_with_emoji)
    r1, _ = replace_loose_emojis(r1)
    check(r1.count("icon-phone") == 1, f"Sticky+emoji: должна остаться ровно 1 иконка телефона, найдено {r1.count('icon-phone')}")
    check("📞" not in r1, "Sticky+emoji: исходный emoji не был убран")

    wa = '<a class="whatsapp-float custom" href="https://wa.me/48123456789" data-track="yes">WhatsApp</a>'
    result, count = upgrade_whatsapp_float(wa)
    check(count == 1, "WhatsApp: кнопка не обновлена")
    check('https://wa.me/48123456789' in result, "WhatsApp: существующий href был изменён")
    check('data-track="yes"' in result, "WhatsApp: существующий атрибут потерян")
    check("icon-whatsapp" in result, "WhatsApp: SVG не добавлен")
    result2, count2 = upgrade_whatsapp_float(result)
    check(count2 == 0 and result2 == result, "WhatsApp: неидемпотентность")

    # НОВЫЙ ТЕСТ: реальный сценарий с существующим emoji 💬
    wa_with_emoji = '<a class="whatsapp-float" href="https://wa.me/48721988949">💬</a>'
    w1, _ = upgrade_whatsapp_float(wa_with_emoji)
    w1, _ = replace_loose_emojis(w1)
    check((w1.count("icon-whatsapp") + w1.count("icon-chat")) == 1, f"WhatsApp+emoji: должна остаться ровно 1 иконка, найдено {w1.count('icon-whatsapp') + w1.count('icon-chat')}")
    check("💬" not in w1, "WhatsApp+emoji: исходный emoji не был убран")

    emoji = '<p>Call 📞 us 💬</p><img alt="📞"><script>var x = "📞";</script><!-- 💬 --><?php echo "📞"; ?>'
    result, count = replace_loose_emojis(emoji)
    check(count == 2, f"Emoji: ожидалось 2 замены, получено {count}")
    check('<img alt="📞">' in result, "Emoji: emoji внутри атрибута был изменён")
    check('<script>var x = "📞";</script>' in result, "Emoji: script был изменён")
    check("<!-- 💬 -->" in result, "Emoji: comment был изменён")
    check('<?php echo "📞"; ?>' in result, "Emoji: PHP был изменён")

    test_text = "Zażółć gęślą jaźń"
    raw_utf8 = test_text.encode("utf-8")
    fake_path = Path("test.html")
    data = FileData(path=fake_path, raw=raw_utf8, text=test_text, encoding="utf-8", bom=False, newline="\n")
    encoded = encode_file(data, test_text)
    check(encoded == raw_utf8, "Encoding: UTF-8 roundtrip failed")

    data_bom = FileData(path=fake_path, raw=b"\xef\xbb\xbf" + raw_utf8, text=test_text, encoding="utf-8", bom=True, newline="\r\n")
    encoded_bom = encode_file(data_bom, test_text + "\n")
    check(encoded_bom.startswith(b"\xef\xbb\xbf"), "Encoding: BOM потерян")
    check(b"\r\n" in encoded_bom, "Encoding: CRLF потерян")

    full = (
        "\n<!DOCTYPE html>\n<html>\n<head>\n<script>\nwindow.location.href(\"https://wa.me/1\", \"_blank\");\n</script>\n</head>\n<body>\n\n"
        '<a href="/naprawa-pralek">\n    <div class="service-icon">🧺</div>\n</a>\n\n'
        "<section>Features</section>\n<section id=\"order\">Order</section>\n\n"
        '<div class="sticky-bottom-bar">\n    <a href="tel:+48123456789">📞 Zadzwoń</a>\n</div>\n\n'
        '<a class="whatsapp-float"\n   href="https://wa.me/48123456789">\n   WhatsApp\n</a>\n\n'
        "<p>Phone: 📞</p>\n\n</body>\n</html>\n"
    )

    args = argparse.Namespace(skip_whatsapp=False, skip_icons=False, skip_dashboard=False, skip_corruption_check=False, skip_buttons=False)

    t1, stats1 = process_text(full, args)
    # Проверяем, что после ПЕРВОГО прохода нет дублей иконок телефона/чата.
    check(t1.count("icon-phone") == 2, f"Full pipeline: ожидалось 2 icon-phone (кнопка услуги + sticky), получено {t1.count('icon-phone')}")
    check(t1.count("📞") == 0, "Full pipeline: остался необработанный emoji 📞")

    t2, stats2 = process_text(t1, args)
    check(t1 == t2, "Full pipeline: второй проход изменил файл")
    check(stats2.changed_count() == 0, "Full pipeline: второй проход сообщил изменения")

    if errors:
        print()
        print("SELF-TEST: FAIL")
        print()
        for error in errors:
            print(f"[FAIL] {error}")
        return False

    print("SELF-TEST: OK")
    return True


def iter_site_files(root: Path, exclude_dirs: Sequence[str]) -> Iterable[Path]:
    exclude = set(exclude_dirs)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in exclude for part in relative.parts[:-1]):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="upgrade_site.py v7.0 - безопасное массовое обновление HTML/PHP")
    parser.add_argument("root", nargs="?", default=None, help="Корневая папка сайта")
    parser.add_argument("--dry-run", action="store_true", help="Показать изменения без записи")
    parser.add_argument("--self-test", action="store_true", help="Запустить встроенные тесты")
    parser.add_argument("--verbose", action="store_true", help="Подробный вывод")
    parser.add_argument("--skip-icons", action="store_true", help="Не менять иконки услуг")
    parser.add_argument("--skip-whatsapp", action="store_true", help="Не исправлять JS WhatsApp")
    parser.add_argument("--skip-dashboard", action="store_true", help="Не оборачивать dashboard-grid")
    parser.add_argument("--skip-corruption-check", action="store_true", help="Не исправлять/проверять битые теги")
    parser.add_argument("--skip-buttons", action="store_true", help="Не менять phone/WhatsApp кнопки и emoji")
    parser.add_argument("--exclude", action="append", default=[], help="Дополнительная папка для исключения")
    parser.add_argument("--backup-dir", default=None, help="Каталог backup. По умолчанию: <root>/_backups")
    parser.add_argument("--no-backup", action="store_true", help="Отключить backup перед записью")

    args = parser.parse_args()

    if args.self_test:
        return 0 if run_self_test() else 1

    if not args.root:
        print("ОШИБКА: укажите корневую папку сайта или используйте --self-test")
        return 1

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ОШИБКА: путь не существует: {root}")
        return 1
    if not root.is_dir():
        print(f"ОШИБКА: это не каталог: {root}")
        return 1

    exclude_dirs = DEFAULT_EXCLUDE_DIRS | set(args.exclude)

    if args.backup_dir:
        backup_root = Path(args.backup_dir).resolve()
    else:
        backup_root = root / "_backups"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_files = sorted(iter_site_files(root, exclude_dirs))

    print()
    print("=" * 70)
    print("upgrade_site.py v7.0")
    print("=" * 70)
    print(f"ROOT:       {root}")
    print(f"FILES:      {len(html_files)}")
    print("MODE:       " + ("DRY-RUN" if args.dry_run else "WRITE"))
    if not args.dry_run and not args.no_backup:
        print(f"BACKUP:     {backup_root / timestamp}")
    elif args.no_backup:
        print("BACKUP:     DISABLED")
    print("=" * 70)

    totals: Dict[str, int] = {
        "files_found": len(html_files), "files_changed": 0, "files_skipped_encoding": 0,
        "files_rejected": 0, "files_written": 0, "files_write_errors": 0, "backups": 0,
        "whatsapp_fixed": 0, "dashboard_wrapped": 0, "dashboard_already": 0, "dashboard_skipped": 0,
        "icons_replaced": 0, "corruption_fixed": 0, "buttons_upgraded": 0, "loose_emojis": 0, "suspicious": 0,
    }
    suspicious_reports: List[Tuple[Path, str, str]] = []

    for path in html_files:
        relative = path.relative_to(root)
        data = decode_file(path)
        if data is None:
            totals["files_skipped_encoding"] += 1
            print(f"[SKIP ENCODING] {relative}")
            continue

        original_text = data.text
        try:
            modified_text, stats = process_text(original_text, args)
        except Exception as exc:
            print(f"[ERROR] {relative}: ошибка обработки: {exc}")
            totals["files_rejected"] += 1
            continue

        totals["whatsapp_fixed"] += stats.whatsapp_fixed
        totals["dashboard_wrapped"] += stats.dashboard_wrapped
        totals["dashboard_already"] += stats.dashboard_already
        totals["dashboard_skipped"] += stats.dashboard_skipped
        totals["icons_replaced"] += stats.icons_replaced
        totals["corruption_fixed"] += stats.corruption_fixed
        totals["buttons_upgraded"] += stats.buttons_upgraded
        totals["loose_emojis"] += stats.loose_emojis
        totals["suspicious"] += len(stats.suspicious)

        for description, snippet in stats.suspicious:
            suspicious_reports.append((relative, description, snippet))

        if modified_text == original_text:
            if args.verbose:
                print(f"[OK]      {relative} (без изменений)")
            continue

        safe, reason = sanity_check(original_text, modified_text)
        if not safe:
            totals["files_rejected"] += 1
            print(f"[REJECT]  {relative}: {reason}")
            continue

        totals["files_changed"] += 1
        print()
        print(f"[CHANGE]  {relative}")
        if stats.whatsapp_fixed:
            print(f"  WhatsApp JS: {stats.whatsapp_fixed}")
        if stats.dashboard_wrapped:
            print("  dashboard-grid: обёрнуто")
        if stats.icons_replaced:
            print(f"  service icons: {stats.icons_replaced}")
        if stats.corruption_fixed:
            print(f"  corrupted tags: {stats.corruption_fixed}")
        if stats.buttons_upgraded:
            print(f"  buttons: {stats.buttons_upgraded}")
        if stats.loose_emojis:
            print(f"  loose emoji: {stats.loose_emojis}")
        if stats.suspicious:
            print(f"  WARNING: {len(stats.suspicious)} suspicious constructions")

        if args.dry_run:
            continue

        try:
            encoded = encode_file(data, modified_text)
            if encoded == data.raw:
                print("  [SKIP] После кодирования байты не изменились")
                continue
            if not args.no_backup:
                backup_path = make_backup(path, root, backup_root, timestamp)
                totals["backups"] += 1
                if args.verbose:
                    print(f"  Backup: {backup_path}")
            atomic_write(path, encoded)
            totals["files_written"] += 1
            if args.verbose:
                print(f"  Written: {len(data.raw)} -> {len(encoded)} bytes [{data.encoding}]")
        except Exception as exc:
            totals["files_write_errors"] += 1
            print(f"  [WRITE ERROR] {relative}: {exc}")

    print()
    print("=" * 70)
    print("[DRY-RUN]" if args.dry_run else "[RESULT]")
    print("=" * 70)
    print(f"Файлов найдено:                 {totals['files_found']}")
    print(f"Файлов с изменениями:           {totals['files_changed']}")
    print(f"Файлов записано:                {totals['files_written']}")
    print(f"Backup создано:                 {totals['backups']}")
    print(f"Пропущено по кодировке:         {totals['files_skipped_encoding']}")
    print(f"Отклонено safety-check:         {totals['files_rejected']}")
    print(f"Ошибок записи:                  {totals['files_write_errors']}")
    print()
    print(f"WhatsApp JS исправлено:         {totals['whatsapp_fixed']}")
    print(f"Dashboard-grid добавлено:       {totals['dashboard_wrapped']}")
    print(f"Dashboard уже существовал:      {totals['dashboard_already']}")
    print(f"Dashboard пропущено:            {totals['dashboard_skipped']}")
    print(f"Service icons заменено:         {totals['icons_replaced']}")
    print(f"Битых тегов исправлено:         {totals['corruption_fixed']}")
    print(f"Кнопок обновлено:               {totals['buttons_upgraded']}")
    print(f"Emoji заменено:                 {totals['loose_emojis']}")
    print(f"Подозрительных конструкций:     {totals['suspicious']}")

    if suspicious_reports:
        print()
        print("ПОДОЗРИТЕЛЬНЫЕ КОНСТРУКЦИИ (ручной просмотр):")
        for relative, description, snippet in suspicious_reports[:50]:
            print(f"  {relative}: {description} -> {snippet!r}")

    print()
    print("=" * 70)
    if args.dry_run:
        print("DRY-RUN завершён. Файлы НЕ изменялись.")
    else:
        print("Обработка завершена.")

    return 1 if totals["files_write_errors"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
