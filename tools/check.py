#!/usr/bin/env python3
"""Автопроверка сайта K Capital перед публикацией.

Запускает её робот на гитхабе при каждой правке (см. .github/workflows/).
Правка публикуется, только если проверка прошла. Локально:
    python3 tools/check.py            # быстрые проверки файлов
    python3 tools/check.py --browser  # плюс проверка в браузере (нужен playwright)

Что проверяется:
- все страницы на месте;
- ссылки между страницами, якоря (#...), картинки, стили и скрипты ведут на существующее;
- шапка и подвал одинаковые во всех файлах (с поправкой на пометку текущей страницы);
- в браузере: на ширине 390 и 1280 ничего не вылезает за край, картинки загрузились,
  на странице нет ошибок JavaScript.
"""
import re
import sys
import threading
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

SITE = Path(__file__).resolve().parent.parent / "docs"
PAGES = ["index.html", "about.html", "advisory.html", "financing.html",
         "experience.html", "contact.html", "privacy.html"]
WIDTHS = [390, 1280]

errors = []


def err(msg):
    errors.append(msg)


class Refs(HTMLParser):
    """Собирает ссылки на файлы и id элементов страницы."""

    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])
        if a.get("srcset"):
            self.refs += [part.strip().split()[0] for part in a["srcset"].split(",") if part.strip()]


def block(html, tag):
    m = re.search(rf"<{tag}\b[^>]*>.*?</{tag}>", html, re.S)
    return m.group(0) if m else None


def check_files():
    parsed = {}
    for page in PAGES:
        path = SITE / page
        if not path.exists():
            err(f"нет страницы {page}")
            continue
        p = Refs()
        p.feed(path.read_text(encoding="utf-8"))
        parsed[page] = p

    for page, p in parsed.items():
        for ref in p.refs:
            u = urlsplit(ref)
            if u.scheme or ref.startswith("//"):
                continue  # внешние ссылки, mailto: и tel: не проверяем
            target = page if not u.path else u.path
            if not (SITE / target).exists():
                err(f"{page}: ссылка на несуществующий файл {ref}")
                continue
            if u.fragment and target.endswith(".html"):
                ids = parsed[target].ids if target in parsed else set()
                if u.fragment not in ids:
                    err(f"{page}: якорь {ref} никуда не ведёт")

    # Шапка и подвал одинаковые во всех файлах
    for tag in ("header", "footer"):
        variants = {}
        for page in parsed:
            b = block((SITE / page).read_text(encoding="utf-8"), tag)
            if b is None:
                err(f"{page}: нет <{tag}>")
                continue
            b = re.sub(r'\s*aria-current="page"', "", b)
            variants.setdefault(b, []).append(page)
        if len(variants) > 1:
            groups = sorted(variants.values(), key=len)
            odd = [page for g in groups[:-1] for page in g]
            err(f"<{tag}> отличается в файлах: {', '.join(odd)} "
                f"(сравни с {', '.join(groups[-1])}); шапка и подвал должны быть одинаковыми везде")


def check_browser():
    from playwright.sync_api import sync_playwright

    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = partial(Quiet, directory=str(SITE))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for width in WIDTHS:
                page = browser.new_page(viewport={"width": width, "height": 900})
                js_errors = []
                page.on("pageerror", lambda e: js_errors.append(str(e)))
                for name in PAGES:
                    js_errors.clear()
                    page.goto(f"{base}/{name}", wait_until="load")
                    over = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                    if over > 0:
                        err(f"{name} на ширине {width}: вылезает за край экрана на {over}px")
                    broken = page.evaluate(
                        "[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.getAttribute('src'))")
                    for src in broken:
                        err(f"{name} на ширине {width}: не загрузилась картинка {src}")
                    for e in js_errors:
                        err(f"{name}: ошибка JavaScript: {e}")
                page.close()
            browser.close()
    finally:
        server.shutdown()


def main():
    check_files()
    if "--browser" in sys.argv:
        check_browser()
    if errors:
        print("Проверка НЕ пройдена, сайт не публикуется:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("Проверка пройдена" + (" (включая браузер)" if "--browser" in sys.argv else ""))


if __name__ == "__main__":
    main()
