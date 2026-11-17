"""Bundle site/index.html into one self-contained file for sharing.

Run site/tools/build_pages.py first. Inlines the shared stylesheet and scripts and every assets/* image (including the English story posters) as a data URI and writes
site/dist/sanad-homepage-prototype.html. Run: python3 site/build.py
"""
import base64
import mimetypes
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent
SRC = SITE / "index.html"
OUT = SITE / "dist" / "sanad-homepage-prototype.html"


def inline(match):
    path = SITE / match.group(2)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'{match.group(1)}"data:{mime};base64,{data}"'


html = SRC.read_text(encoding="utf-8")
# the shared stylesheet and scripts go in as text, so the file works on its own
html = re.sub(r'<link rel="stylesheet" href="(assets/css/[^"]+)">',
              lambda m: "<style>\n" + (SITE / m.group(1)).read_text(encoding="utf-8") + "</style>", html)
html = re.sub(r'<script src="(assets/js/[^"]+)"></script>',
              lambda m: "<script>\n" + (SITE / m.group(1)).read_text(encoding="utf-8") + "</script>", html)
html = re.sub(r'((?:src|href|data-en-src)=)"(assets/[^"]+)"', inline, html)
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT.relative_to(SITE.parent)} ({OUT.stat().st_size // 1024} KB)")
