"""
build_pdf.py
Łączy stronę tytułową z Sprawozdanie_Szymon_Przybysz.pdf
z treścią sprawozdanie.html (bez wbudowanej okładki) i zapisuje wynik
jako Sprawozdanie_FINAL.pdf.

Wymagania:
    pip install playwright pypdf
    python -m playwright install chromium
"""

import io
import re
import sys
import tempfile
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Zainstaluj playwright:  pip install playwright && python -m playwright install chromium")

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    sys.exit("Zainstaluj pypdf:  pip install pypdf")

# ── ścieżki ───────────────────────────────────────────────────────────────────
BASE         = Path(__file__).resolve().parent
HTML_FILE    = BASE / "sprawozdanie.html"
EXISTING_PDF = BASE / "Sprawozdanie_Szymon_Przybysz.pdf"
OUTPUT_PDF   = BASE / "Sprawozdanie_FINAL.pdf"

# ── 1. Wczytaj HTML ───────────────────────────────────────────────────────────
html_src = HTML_FILE.read_text(encoding="utf-8")

# ── 2. Usuń wbudowaną okładkę (.cover) z HTML ────────────────────────────────
# Wycina blok wraz z poprzedzającym komentarzem sekcji COVER
cover_pattern = re.compile(
    r'<!--\s*[═\-=]+ COVER [═\-=]+\s*-->\s*'
    r'<div class="cover">.*?</div>',
    re.DOTALL,
)
html_no_cover = cover_pattern.sub("", html_src, count=1)

# Fallback – sam div bez komentarza
if html_no_cover == html_src:
    html_no_cover = re.sub(
        r'<div class="cover">.*?</div>',
        "",
        html_src,
        count=1,
        flags=re.DOTALL,
    )

# ── 3. Wstrzyknij print-friendly CSS ─────────────────────────────────────────
# Marginesy jak w Word: 2,54 cm góra/dół, 2,54 cm lewo/prawo (domyślny "Normal")
extra_css = """
<style>
  /* ─── nadpisania dla trybu druku/PDF ─── */
  body  { background: #fff !important; padding: 0 !important; }
  .page {
    max-width: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    /* padding usunięty – marginesy obsługuje @page */
    padding: 0 !important;
  }
  @page {
    size: A4;
    /* Word "Normal": 2,54 cm wszystkie strony */
    margin: 2.54cm 2.54cm 2.54cm 2.54cm;
  }
</style>
"""
html_no_cover = html_no_cover.replace("</head>", extra_css + "\n</head>", 1)

# ── 4. Konwersja HTML → PDF przez Playwright / Chromium ──────────────────────
print("Konwertuję HTML → PDF (Chromium) …")

with tempfile.NamedTemporaryFile(suffix=".html", delete=False, encoding="utf-8", mode="w") as tmp:
    tmp.write(html_no_cover)
    tmp_path = Path(tmp.name)

content_bytes: bytes
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto(tmp_path.as_uri())
    page.wait_for_load_state("networkidle")
    content_bytes = page.pdf(
        format="A4",
        print_background=True,
        # Marginesy przekazane też do Playwright (nadpisują @page w Chromium)
        margin={
            "top":    "2.54cm",
            "right":  "2.54cm",
            "bottom": "2.54cm",
            "left":   "2.54cm",
        },
    )
    browser.close()

tmp_path.unlink(missing_ok=True)

content_pdf = PdfReader(io.BytesIO(content_bytes))
print(f"  Stron z treścią: {len(content_pdf.pages)}")

# ── 5. Wczytaj stronę tytułową z istniejącego PDF ────────────────────────────
if not EXISTING_PDF.exists():
    sys.exit(f"Nie znaleziono pliku: {EXISTING_PDF}")

existing   = PdfReader(str(EXISTING_PDF))
title_page = existing.pages[0]
print(f"Strona tytułowa: {EXISTING_PDF.name}  (strona 1 z {len(existing.pages)})")

# ── 6. Złącz: okładka + treść ────────────────────────────────────────────────
writer = PdfWriter()
writer.add_page(title_page)
for p in content_pdf.pages:
    writer.add_page(p)

# ── 7. Zapisz wynik ──────────────────────────────────────────────────────────
with open(OUTPUT_PDF, "wb") as fh:
    writer.write(fh)

total = 1 + len(content_pdf.pages)
print(f"\n✓  Wygenerowano: {OUTPUT_PDF.name}  ({total} stron)")
