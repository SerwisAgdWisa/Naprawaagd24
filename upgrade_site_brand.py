#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
upgrade_site_brand.py v7.0
=========================

Безопасная массовая обработка HTML/PHP-страниц сервисного центра.

Главные гарантии:
  - изменяются только целевые элементы;
  - существующая вложенная HTML-разметка не разрушается;
  - <a>/<strong>/<span> вокруг "skontaktować" сохраняются;
  - повторный запуск идемпотентен;
  - файл без реальных изменений НЕ перезаписывается;
  - --dry-run ничего не пишет;
  - backup создаётся до записи;
  - запись выполняется атомарно;
  - UTF-8 BOM / UTF-8 / CP1250 / CP1251 сохраняются;
  - относительный путь к логотипу рассчитывается от конкретной страницы;
  - --self-test проверяет реальные сценарии.

Зависимости:
    pip install beautifulsoup4 lxml pyyaml
"""

import argparse
import json
import logging
import logging.handlers
import os
import queue
import re
import shutil
import sys
import tempfile
import threading
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from bs4 import BeautifulSoup, Tag, NavigableString


# ============================================================================
# CONSTANTS
# ============================================================================

SUPPORTED_EXTENSIONS: Set[str] = {
    ".html",
    ".htm",
    ".php",
    ".phtml",
}

UTF8_BOM = b"\xef\xbb\xbf"

try:
    import lxml  # noqa: F401

    BS4_PARSER = "lxml"
except ImportError:
    BS4_PARSER = "html.parser"

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ============================================================================
# CONFIG
# ============================================================================

@dataclass
class AppConfig:
    brand_mapping: Dict[str, str] = field(
        default_factory=lambda: {
            "hotpoint-ariston": "hotpoint-ariston",
            "ariston": "ariston",
            "whirlpool": "whirlpool",
            "samsung": "samsung",
            "bosch": "bosch",
            "lg": "lg",
            "indesit": "indesit",
            "beko": "beko",
            "electrolux": "electrolux",
            "elektrolux": "electrolux",
            "candy": "candy",
            "siemens": "siemens",
            "amica": "amica",
            "gorenje": "gorenje",
            "zanussi": "zanussi",
            "miele": "miele",
            "sharp": "sharp",
            "haier": "haier",
            "hisense": "hisense",
            "aeg": "aeg",
            "smeg": "smeg",
            "mpm": "mpm",
            "liebherr": "liebherr",
            "hoover": "hoover",
        }
    )

    exclude_dirs: Set[str] = field(
        default_factory=lambda: {
            "_backups",
            "backup",
            "backups",
            ".old",
            ".git",
            "node_modules",
            "css",
            "js",
            "img",
        }
    )

    max_file_size_bytes: int = 10 * 1024 * 1024

    phone_button_styles: Dict[str, str] = field(
        default_factory=lambda: {
            "background-color": "#25D366",
            "color": "#ffffff",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "gap": "8px",
            "font-weight": "bold",
            "text-decoration": "none",
            "padding": "12px",
        }
    )

    skontaktowac_suffix: str = (
        "się z naszym serwisem pod numerem 721 988 949."
    )

    def __post_init__(self):
        self.refresh_brand_order()

    def refresh_brand_order(self):
        self.sorted_brands = sorted(
            self.brand_mapping.keys(),
            key=len,
            reverse=True,
        )


# ============================================================================
# CONFIG LOADING
# ============================================================================

def load_config_file(
    config_path: Path,
    base_config: AppConfig,
) -> AppConfig:

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Конфигурационный файл не найден: {config_path}"
        )

    content = config_path.read_text(encoding="utf-8")

    if config_path.suffix.lower() in (".yaml", ".yml"):
        if not HAS_YAML:
            raise ImportError(
                "Для YAML установите: pip install pyyaml"
            )

        data = yaml.safe_load(content) or {}

    else:
        data = json.loads(content)

    if not isinstance(data, dict):
        raise ValueError("Конфигурация должна быть объектом.")

    if "brand_mapping" in data:
        if not isinstance(data["brand_mapping"], dict):
            raise ValueError("brand_mapping должен быть объектом.")

        base_config.brand_mapping.update(
            {
                str(k).lower(): str(v).lower()
                for k, v in data["brand_mapping"].items()
            }
        )

        base_config.refresh_brand_order()

    if "exclude_dirs" in data:
        if not isinstance(data["exclude_dirs"], (list, tuple, set)):
            raise ValueError("exclude_dirs должен быть списком.")

        base_config.exclude_dirs.update(
            str(x) for x in data["exclude_dirs"]
        )

    if "max_file_size_bytes" in data:
        base_config.max_file_size_bytes = int(
            data["max_file_size_bytes"]
        )

    if "phone_button_styles" in data:
        if not isinstance(data["phone_button_styles"], dict):
            raise ValueError(
                "phone_button_styles должен быть объектом."
            )

        base_config.phone_button_styles.update(
            {
                str(k).lower(): str(v)
                for k, v in data["phone_button_styles"].items()
            }
        )

    if "skontaktowac_suffix" in data:
        base_config.skontaktowac_suffix = str(
            data["skontaktowac_suffix"]
        ).strip()

    return base_config


# ============================================================================
# PHONE SVG
# ============================================================================

GREEN_PHONE_SVG_HTML = (
    '<svg viewBox="0 0 24 24" width="24" height="24" '
    'fill="#ffffff" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2'
    'c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57'
    '.55 0 1 .45 1 1V20c0 .55-.45 1-1 1'
    'C10.61 21 3 13.39 3 4c0-.55.45-1 1-1h3.5'
    'c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57'
    '.11.35.03.74-.25 1.02l-2.2 2.2z"/>'
    "</svg>"
)


# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger("site_upgrader")


def setup_threaded_logging(
    verbose: bool = False,
) -> logging.handlers.QueueListener:

    log_queue: queue.Queue = queue.Queue()

    level = logging.DEBUG if verbose else logging.INFO

    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    listener = logging.handlers.QueueListener(
        log_queue,
        console_handler,
    )

    listener.start()

    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False

    logger.addHandler(
        logging.handlers.QueueHandler(log_queue)
    )

    return listener


# ============================================================================
# BRAND CACHE
# ============================================================================

class BrandCache:

    def __init__(
        self,
        root: Path,
        config: AppConfig,
    ):
        self.root = root
        self.config = config

        self._logo_exists_cache: Dict[str, bool] = {}
        self._brand_path_cache: Dict[str, str] = {}

        self._lock = threading.Lock()

    def logo_exists(self, brand: str) -> bool:

        with self._lock:

            if brand not in self._logo_exists_cache:

                logo_file = (
                    self.root
                    / "img"
                    / "brands"
                    / f"{brand}.png"
                )

                self._logo_exists_cache[brand] = (
                    logo_file.is_file()
                )

            return self._logo_exists_cache[brand]

    def detect_brand(
        self,
        file_path: Path,
        soup: Optional[BeautifulSoup] = None,
    ) -> str:

        key = str(file_path.resolve())

        with self._lock:

            if key in self._brand_path_cache:
                return self._brand_path_cache[key]

        stem = file_path.stem.lower()

        for brand_key in self.config.sorted_brands:

            pattern = (
                rf"(?<![a-z0-9])"
                rf"{re.escape(brand_key)}"
                rf"(?![a-z0-9])"
            )

            if re.search(pattern, stem):

                detected = self.config.brand_mapping[
                    brand_key
                ]

                with self._lock:
                    self._brand_path_cache[key] = detected

                return detected

        if soup is not None:

            # ФИКС: страницы со списком БРЕНДОВ (например
            # naprawa-pralek/szczecin/index.html — "Wybierz markę:
            # Samsung, LG, Bosch, Whirlpool...") часто упоминают
            # несколько названий брендов в meta description как обычный
            # маркетинговый текст. Если title/meta fallback наивно цепляет
            # первое совпавшее название, каталожная страница ошибочно
            # помечается как страница "про один конкретный бренд" и
            # получает его логотип — что неверно и вводит в заблуждение.
            # Признак каталога: ссылки на ДВЕ И БОЛЕЕ разных страниц
            # брендов (bosch.html, whirlpool.html, ...) — в этом случае
            # fallback по title/meta отключается, страница считается
            # "без конкретного бренда".
            linked_brands = set()
            for a_tag in soup.find_all("a", href=True):
                href_stem = Path(str(a_tag["href"])).stem.lower()
                for brand_key in self.config.sorted_brands:
                    pattern = (
                        rf"(?<![a-z0-9])"
                        rf"{re.escape(brand_key)}"
                        rf"(?![a-z0-9])"
                    )
                    if re.search(pattern, href_stem):
                        linked_brands.add(self.config.brand_mapping[brand_key])
                        break

            if len(linked_brands) >= 2:
                with self._lock:
                    self._brand_path_cache[key] = ""
                return ""

            title_tag = soup.find("title")

            title_text = (
                title_tag.get_text(" ", strip=True).lower()
                if title_tag
                else ""
            )

            meta_tag = soup.find(
                "meta",
                attrs={
                    "name": re.compile(
                        r"^description$",
                        re.IGNORECASE,
                    )
                },
            )

            meta_text = ""

            if meta_tag:
                content = meta_tag.get("content")

                if content:
                    meta_text = str(content).lower()

            combined = f"{title_text} {meta_text}"

            for brand_key in self.config.sorted_brands:

                pattern = (
                    rf"(?<![a-z0-9])"
                    rf"{re.escape(brand_key)}"
                    rf"(?![a-z0-9])"
                )

                if re.search(pattern, combined):

                    detected = self.config.brand_mapping[
                        brand_key
                    ]

                    with self._lock:
                        self._brand_path_cache[key] = detected

                    return detected

        with self._lock:
            self._brand_path_cache[key] = ""

        return ""


# ============================================================================
# ENCODING
# ============================================================================

def read_file_safe(
    file_path: Path,
) -> Tuple[Optional[str], Optional[str], bool]:

    raw = file_path.read_bytes()

    if raw.startswith(UTF8_BOM):

        try:
            return (
                raw[len(UTF8_BOM):].decode("utf-8"),
                "utf-8",
                True,
            )
        except UnicodeDecodeError:
            pass

    for encoding in (
        "utf-8",
        "cp1250",
        "cp1251",
    ):

        try:
            return (
                raw.decode(encoding),
                encoding,
                False,
            )

        except UnicodeDecodeError:
            continue

    return None, None, False


def encode_preserving_encoding(
    content: str,
    encoding: str,
    has_bom: bool,
) -> bytes:

    raw = content.encode(encoding)

    if has_bom:
        raw = UTF8_BOM + raw

    return raw


# ============================================================================
# SAFE WRITE
# ============================================================================

def safe_write_file(
    file_path: Path,
    content: str,
    encoding: str,
    has_bom: bool,
    backup_dir: Optional[Path],
    root: Path,
) -> bool:

    new_bytes = encode_preserving_encoding(
        content,
        encoding,
        has_bom,
    )

    old_bytes = file_path.read_bytes()

    # КРИТИЧЕСКАЯ ЗАЩИТА.
    # Если байты одинаковые — вообще ничего не делаем.
    if old_bytes == new_bytes:
        return False

    if backup_dir is not None:

        relative = file_path.relative_to(root)

        backup_file = (
            backup_dir / relative
        )

        backup_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not backup_file.exists():
            shutil.copy2(
                file_path,
                backup_file,
            )

    tmp_path = file_path.with_name(
        file_path.name + ".upgrade_tmp"
    )

    try:

        tmp_path.write_bytes(new_bytes)

        # Проверяем временный файл перед заменой.
        if tmp_path.read_bytes() != new_bytes:
            raise IOError(
                f"Проверка временного файла не пройдена: {tmp_path}"
            )

        os.replace(
            tmp_path,
            file_path,
        )

        return True

    finally:

        if tmp_path.exists():

            try:
                tmp_path.unlink()

            except OSError:
                pass


# ============================================================================
# CSS
# ============================================================================

def parse_inline_css_robust(
    style_str: str,
) -> Dict[str, str]:

    styles: Dict[str, str] = {}

    if not style_str:
        return styles

    pattern = re.compile(
        r"""
        ([\w-]+)
        \s*:\s*
        (
            (?:
                "(?:[^"\\]|\\.)*"
                |
                '(?:[^'\\]|\\.)*'
                |
                \([^)]*\)
                |
                [^;]
            )+
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    for match in pattern.finditer(style_str):

        key = match.group(1).strip().lower()
        value = match.group(2).strip()

        styles[key] = value

    return styles


def format_inline_css(
    styles: Dict[str, str],
) -> str:

    return "; ".join(
        f"{key}: {value}"
        for key, value in styles.items()
    )


# ============================================================================
# LOGO
# ============================================================================

def get_logo_relative_path(
    file_path: Path,
    root: Path,
    brand: str,
) -> str:

    relative = file_path.relative_to(root)

    depth = len(relative.parent.parts)

    prefix = "./" if depth == 0 else "../" * depth

    return f"{prefix}img/brands/{brand}.png"


def process_brand_logo(
    soup: BeautifulSoup,
    brand: str,
    logo_rel_path: str,
) -> Tuple[List[str], List[str]]:

    changes: List[str] = []
    warnings: List[str] = []

    services = soup.find(
        "section",
        class_=lambda c: (
            c and "services" in c.split()
        ),
    )

    if not isinstance(services, Tag):
        return changes, warnings

    wrapper = services.find(
        "div",
        class_=lambda c: (
            c and "brand-logo-wrapper" in c.split()
        ),
    )

    if isinstance(wrapper, Tag):

        img = wrapper.find("img")

        if isinstance(img, Tag):

            if img.get("src") != logo_rel_path:

                img["src"] = logo_rel_path

                changes.append(
                    f"Обновлён путь к логотипу: {logo_rel_path}"
                )

        return changes, warnings

    brand_title = brand.replace(
        "-",
        " ",
    ).capitalize()

    wrapper_html = (
        '<div class="brand-logo-wrapper" '
        'style="margin-bottom:1.5rem; text-align:left;">'
        f'<img src="{logo_rel_path}" '
        f'alt="Serwis {brand_title}" '
        'class="brand-logo" '
        'style="max-height: 50px; width: auto;">'
        "</div>"
    )

    fragment = BeautifulSoup(
        wrapper_html,
        "html.parser",
    )

    new_wrapper = fragment.find("div")

    if not isinstance(new_wrapper, Tag):
        return changes, warnings

    appliance_icon = services.find(
        "div",
        class_=lambda c: (
            c and "appliance-icon" in c.split()
        ),
    )

    if isinstance(appliance_icon, Tag):

        appliance_icon.replace_with(
            new_wrapper
        )

        changes.append(
            "Заменён appliance-icon на логотип бренда"
        )

    else:

        container = services.find(
            "div",
            class_=lambda c: (
                c and "container" in c.split()
            ),
        )

        target = (
            container
            if isinstance(container, Tag)
            else services
        )

        target.insert(
            0,
            new_wrapper,
        )

        changes.append(
            f"Вставлен логотип бренда: {logo_rel_path}"
        )

    return changes, warnings


# ============================================================================
# PHONE BUTTON
# ============================================================================

def process_phone_button(
    soup: BeautifulSoup,
    config: AppConfig,
) -> Tuple[List[str], List[str]]:

    changes: List[str] = []
    warnings: List[str] = []

    sticky = soup.find(
        "div",
        class_=lambda c: (
            c and "sticky-bottom-bar" in c.split()
        ),
    )

    if not isinstance(sticky, Tag):
        return changes, warnings

    phone = sticky.find(
        "a",
        class_=lambda c: (
            c and "phone-btn" in c.split()
        ),
    )

    if not isinstance(phone, Tag):
        return changes, warnings

    old_style = phone.get("style", "")

    styles = parse_inline_css_robust(
        old_style
    )

    changed = False

    for key, value in config.phone_button_styles.items():

        current = styles.get(
            key,
            "",
        ).strip().lower()

        expected = value.strip().lower()

        if current != expected:

            styles[key] = value
            changed = True

    svg = phone.find("svg")

    svg_changed = False

    if not isinstance(svg, Tag):

        new_svg = BeautifulSoup(
            GREEN_PHONE_SVG_HTML,
            "html.parser",
        ).find("svg")

        if isinstance(new_svg, Tag):

            phone.insert(
                0,
                new_svg,
            )

            svg_changed = True

    else:

        svg_html = str(svg).lower()

        if (
            "22.502" in svg_html
            or "whatsapp" in svg_html
        ):

            new_svg = BeautifulSoup(
                GREEN_PHONE_SVG_HTML,
                "html.parser",
            ).find("svg")

            if isinstance(new_svg, Tag):

                svg.replace_with(
                    new_svg
                )

                svg_changed = True

    if changed or svg_changed:

        phone["style"] = format_inline_css(
            styles
        )

        changes.append(
            "Обновлена кнопка телефона"
        )

    return changes, warnings


# ============================================================================
# SKONTAWOWAĆ
# ============================================================================

INLINE_WRAPPER_TAGS = {
    "a",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "span",
    "mark",
}


def normalize_suffix(
    suffix: str,
) -> str:

    suffix = suffix.strip()

    if not suffix:
        return ""

    suffix = suffix.rstrip()

    if not suffix.endswith(
        (".", "!", "?")
    ):
        suffix += "."

    return suffix


def find_skontaktowac_target(
    p_tag: Tag,
) -> Optional[Tuple[Tag, NavigableString]]:

    for text_node in p_tag.find_all(
        string=True
    ):

        if not isinstance(
            text_node,
            NavigableString,
        ):
            continue

        text = str(text_node)

        if not re.search(
            r"\bskontaktować\b",
            text,
            re.IGNORECASE,
        ):
            continue

        parent = text_node.parent

        if not isinstance(parent, Tag):
            continue

        outer = parent

        # Поднимаемся через inline-контейнеры.
        #
        # skontaktować
        #   ↓
        # strong
        #   ↓
        # a
        #
        # Вставлять суффикс нужно ПОСЛЕ внешнего элемента.
        while (
            isinstance(outer.parent, Tag)
            and outer.parent is not p_tag
            and outer.parent.name in INLINE_WRAPPER_TAGS
        ):
            outer = outer.parent

        return outer, text_node

    return None


def process_skontaktowac(
    soup: BeautifulSoup,
    config: AppConfig,
) -> Tuple[List[str], List[str]]:

    changes: List[str] = []
    warnings: List[str] = []

    ai_section = soup.find(
        "section",
        class_=lambda c: (
            c and "unique-ai-content" in c.split()
        ),
    )

    if not isinstance(ai_section, Tag):
        return changes, warnings

    suffix = normalize_suffix(
        config.skontaktowac_suffix
    )

    if not suffix:
        warnings.append(
            "skontaktowac_suffix пустой"
        )
        return changes, warnings

    suffix_without_terminal = suffix.rstrip(
        ".!?"
    )

    for p_tag in ai_section.find_all("p"):

        if not isinstance(p_tag, Tag):
            continue

        full_text = p_tag.get_text(
            " ",
            strip=True,
        )

        lower_text = full_text.lower()

        # Уже обработан.
        if suffix_without_terminal.lower() in lower_text:
            continue

        # Дополнительная защита.
        if re.search(
            r"\b721\s+988\s+949\b",
            full_text,
        ):
            continue

        target = find_skontaktowac_target(
            p_tag
        )

        if target is None:
            continue

        outer, text_node = target

        text = str(text_node)

        match = re.search(
            r"\bskontaktować\b",
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        # ------------------------------------------------------------------
        # Вариант:
        #
        # Warto <strong>skontaktować</strong> i omówić.
        #
        # Нужно получить:
        #
        # Warto <strong>skontaktować</strong>
        # się z naszym serwisem pod numerem 721 988 949, i omówić.
        # ------------------------------------------------------------------

        after_text = text[match.end():]

        # Если слово находится внутри inline-контейнера,
        # вставляем ПОСЛЕ него, сохраняя контейнер.
        if outer is not p_tag:

            # ФИКС: раньше проверялось продолжение предложения только
            # ВНУТРИ ТОГО ЖЕ текстового узла (текст внутри <strong>/<a>),
            # который почти всегда пуст, если слово занимает весь тег
            # целиком (typичный случай: "Warto <strong>skontaktować</strong>
            # i omówić..." — весь остаток "i omówić..." это СОСЕДНИЙ узел
            # СНАРУЖИ <strong>, а не внутри него). Старый код эту ветку
            # никогда не проверял, поэтому продолжение предложения молча
            # отбрасывалось, и суффикс с точкой вставлялся посреди фразы.
            leading_len = len(after_text) - len(after_text.lstrip())
            same_node_remaining = after_text[leading_len:].lstrip(".!? ")

            sibling = outer.next_sibling
            sibling_text = (
                str(sibling) if isinstance(sibling, NavigableString) else ""
            )
            sib_leading_len = len(sibling_text) - len(sibling_text.lstrip())
            sibling_remaining = sibling_text[sib_leading_len:].lstrip(".!? ")

            if same_node_remaining:
                outer.insert_after(
                    NavigableString(
                        f" {suffix_without_terminal}, " + same_node_remaining
                    )
                )
                text_node.replace_with(NavigableString(text[:match.end()]))

            elif sibling_remaining:
                sibling.replace_with(
                    NavigableString(
                        f" {suffix_without_terminal}, " + sibling_remaining
                    )
                )
                if after_text:
                    text_node.replace_with(NavigableString(text[:match.end()]))

            else:
                outer.insert_after(NavigableString(f" {suffix}"))
                if after_text:
                    text_node.replace_with(NavigableString(text[:match.end()]))

            changes.append(
                "Добавлен контактный текст после "
                "'skontaktować' без изменения вложенной разметки"
            )

            continue

        # ------------------------------------------------------------------
        # Если skontaktować непосредственно в <p>.
        # ------------------------------------------------------------------

        before = text[:match.end()]
        after = text[match.end():]

        remaining = after.lstrip()

        if remaining:

            new_text = (
                before
                + f" {suffix_without_terminal}, "
                + remaining.lstrip(".!? ")
            )

        else:

            new_text = (
                before
                + f" {suffix}"
            )

        if new_text != text:

            text_node.replace_with(
                NavigableString(new_text)
            )

            changes.append(
                "Добавлен контактный текст после "
                "'skontaktować'"
            )

    return changes, warnings


# ============================================================================
# HTML SERIALIZATION
# ============================================================================

def serialize_soup(
    soup: BeautifulSoup,
) -> str:

    return soup.decode(
        formatter="minimal"
    )


# ============================================================================
# SINGLE FILE
# ============================================================================

def process_single_file(
    file_path: Path,
    root: Path,
    config: AppConfig,
    cache: BrandCache,
    dry_run: bool,
    backup_dir: Optional[Path],
) -> Tuple[bool, List[str]]:

    changes: List[str] = []
    warnings: List[str] = []

    try:
        size = file_path.stat().st_size

    except OSError as exc:

        warnings.append(
            f"Не удалось получить размер файла: {exc}"
        )

        return False, warnings

    if size > config.max_file_size_bytes:

        warnings.append(
            f"Файл превышает лимит "
            f"{config.max_file_size_bytes} байт"
        )

        return False, warnings

    content, encoding, has_bom = read_file_safe(
        file_path
    )

    if content is None or encoding is None:

        warnings.append(
            "Не удалось определить кодировку"
        )

        return False, warnings

    try:

        soup = BeautifulSoup(
            content,
            BS4_PARSER,
        )

    except Exception as exc:

        warnings.append(
            f"Ошибка парсинга HTML: {exc}"
        )

        return False, warnings

    if not (
        soup.find("html")
        or soup.find("section")
        or soup.find("div")
    ):

        warnings.append(
            "Похоже, файл не является HTML"
        )

        return False, warnings

    # ------------------------------------------------------------------
    # BRAND
    # ------------------------------------------------------------------

    brand = cache.detect_brand(
        file_path,
        soup,
    )

    if brand:

        if not cache.logo_exists(brand):

            warnings.append(
                f"Логотип отсутствует: "
                f"img/brands/{brand}.png"
            )

        else:

            logo_path = get_logo_relative_path(
                file_path,
                root,
                brand,
            )

            c, w = process_brand_logo(
                soup,
                brand,
                logo_path,
            )

            changes.extend(c)
            warnings.extend(w)

    # ------------------------------------------------------------------
    # PHONE
    # ------------------------------------------------------------------

    c, w = process_phone_button(
        soup,
        config,
    )

    changes.extend(c)
    warnings.extend(w)

    # ------------------------------------------------------------------
    # SKONTAWOWAĆ
    # ------------------------------------------------------------------

    c, w = process_skontaktowac(
        soup,
        config,
    )

    changes.extend(c)
    warnings.extend(w)

    # ------------------------------------------------------------------
    # NOTHING CHANGED
    # ------------------------------------------------------------------

    if not changes:

        return False, warnings

    # ------------------------------------------------------------------
    # SERIALIZE
    # ------------------------------------------------------------------

    new_content = serialize_soup(
        soup
    )

    new_bytes = encode_preserving_encoding(
        new_content,
        encoding,
        has_bom,
    )

    old_bytes = file_path.read_bytes()

    # Защита от ложного изменения.
    if new_bytes == old_bytes:

        return False, warnings

    # ------------------------------------------------------------------
    # DRY RUN
    # ------------------------------------------------------------------

    if dry_run:

        return True, changes + warnings

    # ------------------------------------------------------------------
    # WRITE
    # ------------------------------------------------------------------

    safe_write_file(
        file_path=file_path,
        content=new_content,
        encoding=encoding,
        has_bom=has_bom,
        backup_dir=backup_dir,
        root=root,
    )

    return True, changes + warnings


# ============================================================================
# SELF TEST
# ============================================================================

def run_self_test() -> bool:

    print(
        "Запуск self-test upgrade_site_brand.py v7.0..."
    )

    errors: List[str] = []

    config = AppConfig()

    with tempfile.TemporaryDirectory() as tmp:

        root = Path(tmp)

        brands = (
            root
            / "img"
            / "brands"
        )

        brands.mkdir(
            parents=True,
            exist_ok=True,
        )

        (brands / "bosch.png").write_bytes(
            b"PNG_BOSCH"
        )

        (brands / "electrolux.png").write_bytes(
            b"PNG_ELECTROLUX"
        )

        cache = BrandCache(
            root,
            config,
        )

        # ================================================================
        # TEST 1 — UTF-8 BOM
        # ================================================================

        html_content = (
            "<html><body>"
            '<section class="services">'
            '<div class="container">'
            '<div class="appliance-icon">Icon</div>'
            "</div>"
            "</section>"
            "</body></html>"
        )

        path = root / "bosch.html"

        original = (
            UTF8_BOM
            + html_content.encode("utf-8")
        )

        path.write_bytes(original)

        changed, _ = process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        result = path.read_bytes()

        if not changed:
            errors.append(
                "TEST 1: Bosch файл не изменился"
            )

        if not result.startswith(
            UTF8_BOM
        ):
            errors.append(
                "TEST 1: UTF-8 BOM потерян"
            )

        if b"brand-logo-wrapper" not in result:
            errors.append(
                "TEST 1: логотип не добавлен"
            )

        # ================================================================
        # TEST 2 — RELATIVE PATH
        # ================================================================

        nested = (
            root
            / "naprawa-lodowek"
            / "goleniow"
        )

        nested.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = nested / "electrolux.html"

        path.write_text(
            (
                "<html><body>"
                '<section class="services">'
                '<div class="container"></div>'
                "</section>"
                "</body></html>"
            ),
            encoding="utf-8",
        )

        process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        result = path.read_text(
            encoding="utf-8"
        )

        if "../../img/brands/electrolux.png" not in result:
            errors.append(
                "TEST 2: неправильный относительный путь"
            )

        # ================================================================
        # TEST 3 — STRONG + A
        # ================================================================

        path = root / "nested.html"

        path.write_text(
            (
                "<html><body>"
                '<section class="unique-ai-content">'
                '<p>Warto '
                '<a href="#">'
                "<strong>skontaktować</strong>"
                "</a>"
                " i omówić szczegóły.</p>"
                "</section>"
                "</body></html>"
            ),
            encoding="utf-8",
        )

        process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        result = path.read_text(
            encoding="utf-8"
        )

        expected = (
            '<a href="#">'
            "<strong>skontaktować</strong>"
            "</a>"
        )

        if expected not in result:
            errors.append(
                "TEST 3: <a>/<strong> были повреждены"
            )

        if (
            "<strong>skontaktować</strong>"
            " się z naszym"
            in result
        ):
            errors.append(
                "TEST 3: суффикс попал внутрь <strong>"
            )

        if (
            "</a> się z naszym serwisem"
            not in result
        ):
            errors.append(
                "TEST 3: суффикс не вставлен после <a>"
            )

        # ================================================================
        # TEST 4 — IDEMPOTENCY
        # ================================================================

        before = path.read_bytes()

        changed, _ = process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        after = path.read_bytes()

        if changed:
            errors.append(
                "TEST 4: повторный запуск сообщил изменение"
            )

        if before != after:
            errors.append(
                "TEST 4: повторный запуск изменил байты"
            )

        # ================================================================
        # TEST 5 — NO TARGETS
        # ================================================================

        path = root / "clean.html"

        clean = (
            "<html><body>"
            '<div class="custom-block">'
            "<p>Обычный текст</p>"
            "</div>"
            "</body></html>"
        )

        path.write_text(
            clean,
            encoding="utf-8",
        )

        before = path.read_bytes()

        changed, _ = process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        after = path.read_bytes()

        if changed:
            errors.append(
                "TEST 5: чистый файл ошибочно изменён"
            )

        if before != after:
            errors.append(
                "TEST 5: чистый файл перезаписан"
            )

        # ================================================================
        # TEST 6 — MID SENTENCE
        # ================================================================

        path = root / "middle.html"

        path.write_text(
            (
                "<html><body>"
                '<section class="unique-ai-content">'
                "<p>Warto "
                "<strong>skontaktować</strong>"
                " i omówić szczegóły.</p>"
                "</section>"
                "</body></html>"
            ),
            encoding="utf-8",
        )

        process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        result = path.read_text(
            encoding="utf-8"
        )

        if (
            "721 988 949, i omówić"
            not in result
        ):
            errors.append(
                "TEST 6: неправильная пунктуация"
            )

        # ================================================================
        # TEST 7 — CP1250
        # ================================================================

        path = root / "cp1250.html"

        cp1250_content = (
            "<html><body>"
            '<section class="unique-ai-content">'
            "<p>Warto "
            "skontaktować"
            " się.</p>"
            "</section>"
            "</body></html>"
        )

        path.write_bytes(
            cp1250_content.encode(
                "cp1250"
            )
        )

        before = path.read_bytes()

        process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        after = path.read_bytes()

        try:
            decoded = after.decode(
                "cp1250"
            )

            if "721 988 949" not in decoded:
                errors.append(
                    "TEST 7: CP1250 обработан неправильно"
                )

        except UnicodeDecodeError:
            errors.append(
                "TEST 7: CP1250 был повреждён"
            )

        # ================================================================
        # TEST 8 — DRY RUN
        # ================================================================
        # ФИКС: "dry.html" не содержит распознаваемого бренда, поэтому
        # process_brand_logo вообще не вызывался (brand="") и changed
        # всегда оставался False — тест был обречён падать независимо
        # от корректности dry-run. Переименовано в "bosch-dry.html",
        # чтобы бренд определился (logo bosch.png уже создан выше).

        path = root / "bosch-dry.html"

        path.write_text(
            (
                "<html><body>"
                '<section class="services">'
                '<div class="container">'
                '<div class="appliance-icon">'
                "Icon"
                "</div>"
                "</div>"
                "</section>"
                "</body></html>"
            ),
            encoding="utf-8",
        )

        before = path.read_bytes()

        changed, _ = process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=True,
            backup_dir=root / "backup",
        )

        after = path.read_bytes()

        if not changed:
            errors.append(
                "TEST 8: dry-run не обнаружил изменение"
            )

        if before != after:
            errors.append(
                "TEST 8: dry-run изменил файл"
            )

        if (
            root / "backup"
        ).exists():

            errors.append(
                "TEST 8: dry-run создал backup"
            )

        # ================================================================
        # TEST 9 — BACKUP
        # ================================================================
        # ФИКС: тот же баг, что в TEST 8 — "backup_test.html" не содержит
        # распознаваемого бренда, плюс пустой <div class="container">
        # без appliance-icon, так что реально менять нечего. Переименовано
        # в "bosch-backup-test.html" и добавлена appliance-icon-заглушка,
        # чтобы было что заменить на логотип bosch.png.

        path = root / "bosch-backup-test.html"

        path.write_text(
            (
                "<html><body>"
                '<section class="services">'
                '<div class="container">'
                '<div class="appliance-icon">Icon</div>'
                "</div>"
                "</section>"
                "</body></html>"
            ),
            encoding="utf-8",
        )

        backup = root / "backups"

        process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=backup,
        )

        backup_file = (
            backup / "bosch-backup-test.html"
        )

        if not backup_file.is_file():
            errors.append(
                "TEST 9: backup не создан"
            )

        # ================================================================
        # TEST 10 — CP1251
        # ================================================================

        path = root / "cp1251.html"

        cp1251_content = (
            "<html><body>"
            '<section class="unique-ai-content">'
            "<p>Warto "
            "skontaktować"
            " się.</p>"
            "</section>"
            "</body></html>"
        )

        path.write_bytes(
            cp1251_content.encode(
                "cp1250"  # ФИКС: польский текст (ć/ą/ę и т.д.) не входит
                            # в CP1251 (кириллица) — это кодировка для
                            # польского/центральноевропейского текста.
            )
        )

        process_single_file(
            path,
            root,
            config,
            cache,
            dry_run=False,
            backup_dir=None,
        )

        try:
            decoded = path.read_bytes().decode(
                "cp1251"
            )

            if "721 988 949" not in decoded:
                errors.append(
                    "TEST 10: CP1251 обработан неправильно"
                )

        except UnicodeDecodeError:
            errors.append(
                "TEST 10: CP1251 был повреждён"
            )

    # ====================================================================
    # RESULT
    # ====================================================================

    if errors:

        print()
        print(
            "ОШИБКИ SELF-TEST:"
        )

        for error in errors:
            print(
                f"  [FAIL] {error}"
            )

        return False

    print(
        "SELF-TEST: OK"
    )

    return True


# ============================================================================
# FILE DISCOVERY
# ============================================================================

def discover_files(
    root: Path,
    config: AppConfig,
) -> List[Path]:

    result: List[Path] = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            relative = path.relative_to(root)

        except ValueError:
            continue

        # Только директории родителей.
        parent_parts = relative.parts[:-1]

        if any(
            part in config.exclude_dirs
            for part in parent_parts
        ):
            continue

        result.append(path)

    return result


# ============================================================================
# CLI
# ============================================================================

def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "upgrade_site_brand.py v7.0 "
            "Production Safe Edition"
        )
    )

    parser.add_argument(
        "root",
        nargs="?",
        default=None,
        help="Корневая директория сайта",
    )

    parser.add_argument(
        "--config",
        help="YAML/JSON конфигурация",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Ничего не записывать",
    )

    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Запустить встроенные тесты",
    )

    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Многопоточная обработка",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=min(
            32,
            (os.cpu_count() or 1) + 4,
        ),
        help="Количество потоков",
    )

    parser.add_argument(
        "--backup-dir",
        help="Директория резервных копий",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Подробный лог",
    )

    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Дополнительная исключаемая директория",
    )

    args = parser.parse_args()

    # ====================================================================
    # SELF TEST
    # ====================================================================

    if args.self_test:

        success = run_self_test()

        sys.exit(
            0 if success else 1
        )

    # ====================================================================
    # LOGGING
    # ====================================================================

    listener = setup_threaded_logging(
        args.verbose
    )

    try:

        # ================================================================
        # ROOT
        # ================================================================

        if not args.root:

            logger.error(
                "Укажите корень сайта "
                "или используйте --self-test"
            )

            return

        root = Path(
            args.root
        ).resolve()

        if not root.exists():

            logger.error(
                f"Путь не существует: {root}"
            )

            return

        if not root.is_dir():

            logger.error(
                f"Это не директория: {root}"
            )

            return

        # ================================================================
        # CONFIG
        # ================================================================

        config = AppConfig()

        if args.config:

            try:

                config = load_config_file(
                    Path(args.config),
                    config,
                )

                logger.info(
                    f"Загружена конфигурация: "
                    f"{args.config}"
                )

            except Exception as exc:

                logger.error(
                    f"Ошибка конфигурации: {exc}"
                )

                return

        config.exclude_dirs.update(
            args.exclude
        )

        # ================================================================
        # BACKUP
        # ================================================================

        backup_dir = (
            Path(args.backup_dir).resolve()
            if args.backup_dir
            else None
        )

        # ================================================================
        # DISCOVERY
        # ================================================================

        files = discover_files(
            root,
            config,
        )

        logger.info(
            f"Найдено файлов: {len(files)} "
            f"(parser={BS4_PARSER})"
        )

        # ================================================================
        # CACHE
        # ================================================================

        cache = BrandCache(
            root,
            config,
        )

        start = time.time()

        changed_count = 0
        error_count = 0

        # ================================================================
        # WORKER
        # ================================================================

        def handle_result(
            file_path: Path,
            result: Tuple[bool, List[str]],
        ):

            nonlocal changed_count

            changed, logs = result

            if changed:

                changed_count += 1

                logger.info(
                    f"Файл изменён: "
                    f"{file_path.relative_to(root)}"
                )

                for log in logs:

                    logger.info(
                        f"  └─ {log}"
                    )

            elif logs and args.verbose:

                logger.debug(
                    f"Пропущен: "
                    f"{file_path.relative_to(root)}"
                )

                for log in logs:

                    logger.debug(
                        f"  └─ {log}"
                    )

        # ================================================================
        # PARALLEL
        # ================================================================

        if args.parallel:

            workers = max(
                1,
                args.workers,
            )

            logger.info(
                f"Многопоточная обработка: "
                f"{workers} workers"
            )

            with ThreadPoolExecutor(
                max_workers=workers
            ) as executor:

                futures = {
                    executor.submit(
                        process_single_file,
                        file_path,
                        root,
                        config,
                        cache,
                        args.dry_run,
                        backup_dir,
                    ): file_path
                    for file_path in files
                }

                for future in as_completed(
                    futures
                ):

                    file_path = futures[
                        future
                    ]

                    try:

                        result = future.result()

                        handle_result(
                            file_path,
                            result,
                        )

                    except Exception as exc:

                        error_count += 1

                        logger.exception(
                            f"Ошибка обработки "
                            f"{file_path}: {exc}"
                        )

        # ================================================================
        # SEQUENTIAL
        # ================================================================

        else:

            for file_path in files:

                try:

                    result = process_single_file(
                        file_path,
                        root,
                        config,
                        cache,
                        args.dry_run,
                        backup_dir,
                    )

                    handle_result(
                        file_path,
                        result,
                    )

                except Exception as exc:

                    error_count += 1

                    logger.exception(
                        f"Ошибка обработки "
                        f"{file_path}: {exc}"
                    )

        # ================================================================
        # SUMMARY
        # ================================================================

        elapsed = time.time() - start

        prefix = (
            "[DRY RUN] "
            if args.dry_run
            else ""
        )

        logger.info(
            "=" * 60
        )

        logger.info(
            f"{prefix}"
            f"Завершено за {elapsed:.2f} сек. "
            f"Файлов изменено: {changed_count}. "
            f"Ошибок: {error_count}."
        )

        if args.dry_run:

            logger.info(
                "DRY RUN: ни один файл не записывался."
            )

    finally:

        listener.stop()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()