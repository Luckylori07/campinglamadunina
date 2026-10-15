"""Controllo statico: link interni, ancore, risorse, id duplicati, corrispondenza lingue."""
import pathlib, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
files = sorted([p for p in ROOT.glob("*.html")] + [p for d in ("en", "de", "fr") for p in (ROOT / d).glob("*.html")])

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.refs = []; s.ids = []; s.ext = []; s.alts = []; s.imgs_noalt = []; s.btn = []
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        for k in ("href", "src", "srcset", "imagesrcset"):
            if k in a and a[k]:
                if k.endswith("srcset"):
                    for part in a[k].split(","):
                        s.refs.append((tag, part.strip().split(" ")[0]))
                else:
                    s.refs.append((tag, a[k]))
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"): s.alts.append((a["hreflang"], a["href"]))
        if tag == "img" and "alt" not in a: s.imgs_noalt.append(a.get("src"))

bad = []; n_links = 0; ext = set()
for f in files:
    p = P(); p.feed(f.read_text(encoding="utf-8"))
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup: bad.append(f"{f.relative_to(ROOT)}: id duplicati {dup}")
    if p.imgs_noalt: bad.append(f"{f.relative_to(ROOT)}: img senza alt {p.imgs_noalt}")
    for tag, ref in p.refs:
        if ref.startswith(("mailto:", "tel:", "data:", "#")) and ref != "#":
            if ref.startswith("#") and ref[1:] not in p.ids: bad.append(f"{f.relative_to(ROOT)}: ancora mancante {ref}")
            continue
        u = urlparse(ref)
        if u.scheme in ("http", "https"):
            ext.add(ref); continue
        n_links += 1
        target = (f.parent / unquote(u.path)).resolve() if u.path else f
        if not target.exists():
            bad.append(f"{f.relative_to(ROOT)}: risorsa mancante {ref}")
        elif u.fragment and target.suffix == ".html":
            q = P(); q.feed(target.read_text(encoding="utf-8"))
            if u.fragment not in q.ids: bad.append(f"{f.relative_to(ROOT)}: ancora {ref} non trovata in {target.name}")
    # corrispondenza lingue: stesse pagine per ogni lingua
    for hl, href in p.alts:
        if hl != "x-default" and not (f.parent / href).resolve().exists():
            bad.append(f"{f.relative_to(ROOT)}: hreflang {hl} -> {href} inesistente")

print(f"{len(files)} pagine, {n_links} riferimenti interni controllati")
print("Link esterni distinti:", len(ext))
for e in sorted(ext): print("  ", e)
print("PROBLEMI:" if bad else "OK: nessun link rotto / ancora mancante / id duplicato / img senza alt")
for b in bad: print(" -", b)
sys.exit(1 if bad else 0)
