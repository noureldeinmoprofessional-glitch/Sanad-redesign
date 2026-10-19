"""Bundle site/index.html into one self-contained file for sharing.

Inlines every assets/* image as a data URI and writes
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
html = re.sub(r'(src=)"(assets/[^"]+)"', inline, html)
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT.relative_to(SITE.parent)} ({OUT.stat().st_size // 1024} KB)")
