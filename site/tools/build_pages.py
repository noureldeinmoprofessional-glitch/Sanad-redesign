"""Build the site's pages from site/src.

Each file in site/src/pages is one page: a short front matter block, then the page's own markup
(its <main>, then anything that belongs after the footer, such as dialogs). The builder wraps it in
the shared head, header and footer and writes the page the browser loads:

    site/src/pages/index.html  ->  site/index.html
    site/src/pages/about.html  ->  site/about/index.html

Front matter (between two "---" lines):
    title / title_en           the tab title in Arabic and English
    description                the meta description
    scripts                    page scripts in assets/js, after the shared site.js (space separated)
    nav                        optional: the href of the menu item to mark as the current page

A page can pull in a shared block with <!-- include: name -->, which inserts site/src/partials/name.html.

Run: python3 site/tools/build_pages.py
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent
SRC = SITE / "src"
FONTS = ("https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&family=Aref+Ruqaa:wght@700"
         "&family=El+Messiri:wght@500;600;700&family=Roboto:wght@500;700&display=swap")

PAGE = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-en="{title_en}">{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="{root}assets/css/site.css">
</head>
<body{body_attrs}>

{header}
{content}
{footer}
{after}{scripts}
</body>
</html>
"""


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if line.strip():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def fill(partial, home):
    # the homepage links to its own anchors; every other page lives one folder down and links back home
    values = {"root": "" if home else "/", "logo_href": "#top" if home else "/", "give_href": "#give" if home else "/#give"}
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], partial)


def includes(content, home):
    # <!-- include: give-band --> drops in site/src/partials/give-band.html
    return re.sub(r"<!-- include: ([\w-]+) -->",
                  lambda m: fill((SRC / "partials" / f"{m.group(1)}.html").read_text(encoding="utf-8"), home).rstrip("\n"), content)


def mark_current(header, href):
    if not href:
        return header
    return header.replace(f'href="{href}"', f'href="{href}" aria-current="page"', 1)


def build(path):
    meta, content = parse(path)
    slug = path.stem
    home = slug == "index"
    content = includes(content, home)
    root = "" if home else "/"
    header = mark_current(fill((SRC / "partials/header.html").read_text(encoding="utf-8"), home), meta.get("nav"))
    footer = fill((SRC / "partials/footer.html").read_text(encoding="utf-8"), home)
    scripts = [f'<script src="{root}assets/js/site.js"></script>']
    scripts += [f'<script src="{root}assets/js/{name}"></script>' for name in meta.get("scripts", "").split()]
    # what follows </main> (dialogs, a sticky bar) sits after the footer, as in a hand-written page
    cut = content.index("</main>") + len("</main>")
    content, after = content[:cut], content[cut:].strip("\n")
    body_class = meta.get("body_class")
    html = PAGE.format(
        title=meta["title"], title_en=meta.get("title_en", meta["title"]), description=meta.get("description", ""),
        fonts=FONTS, root=root, header=header.rstrip("\n"), content=content.strip("\n") + "\n",
        footer=footer.rstrip("\n"), after=(after + "\n") if after else "", scripts="\n".join(scripts),
        body_attrs=f' class="{body_class}"' if body_class else "")
    out = SITE / "index.html" if home else SITE / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    for page in sorted((SRC / "pages").glob("*.html")):
        out = build(page)
        print(f"{page.relative_to(SITE)} -> {out.relative_to(SITE)}")
