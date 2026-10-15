#!/usr/bin/env python3
"""Genera il sito statico (IT in radice, EN/DE/FR in sottocartelle).

Uso:  python3 -I tools/build.py            # genera le pagine HTML
      SITE_URL=https://dominio.it python3 -I tools/build.py   # URL assoluti per hreflang / Open Graph

I testi stanno in tools/i18n.py (una sezione per lingua, stesse chiavi).
Componenti condivisi: banner demo, filigrana, header, footer, sprite icone.
"""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image  # noqa: E402
from i18n import S, LANGS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
DEMO = os.environ.get("DEMO", "1") != "0"        # DEMO=0 -> senza banner e filigrana (solo dopo approvazione del cliente)
NOINDEX = os.environ.get("NOINDEX", "1") != "0"  # NOINDEX=0 -> rimuove "noindex, nofollow" (solo alla pubblicazione ufficiale)
TRAMONTIS = "https://tramontis.netlify.app/"
PHONE, MOBILE, MAIL = "+39 0332 960361", "+39 347 7867227", "info@campinglamadunina.com"
PHONE_TEL, MOBILE_TEL = "+390332960361", "+393477867227"
ADDR1, ADDR2 = "Via dei Martiri, 12", "21020 Varano Borghi (VA)"
MAPS_Q = "https://www.google.com/maps/search/?api=1&query=Camping+La+Madunina%2C+Via+dei+Martiri+12%2C+21020+Varano+Borghi"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination=Camping+La+Madunina%2C+Via+dei+Martiri+12%2C+21020+Varano+Borghi"
OSM = "https://www.openstreetmap.org/relation/1314307"
PDF_LOCAL = "assets/docs/listino-originale.pdf"
PDF_ORIG = "https://www.campinglamadunina.com/lis/listino.pdf"

PAGES = ["index", "campeggio", "sistemazioni", "servizi", "galleria", "prezzi", "cartina", "contatti", "faq", "privacy", "note-legali"]
NAV = ["campeggio", "sistemazioni", "servizi", "prezzi", "galleria", "cartina"]
LANG_NAMES = {"it": "Italiano", "en": "English", "de": "Deutsch", "fr": "Français"}
OG_LOCALE = {"it": "it_IT", "en": "en_GB", "de": "de_DE", "fr": "fr_FR"}

CREDITS = {c["slug"]: c for c in json.load(open(ROOT / "tools/commons_sources.json", encoding="utf-8"))}

# ----------------------------------------------------------------------------
# Icone (sprite inline: nessuna richiesta aggiuntiva, funziona anche da file://)
# ----------------------------------------------------------------------------
ICONS = {
    "pool": '<path d="M7 14V6.5a2.5 2.5 0 0 1 5 0M13 14V6.5a2.5 2.5 0 0 1 5 0M7 10h5M13 10h5"/><path d="M2 17.5c2.2 0 2.2-1.6 5-1.6s2.8 1.6 5 1.6 2.8-1.6 5-1.6 2.8 1.6 5 1.6M2 21.5c2.2 0 2.2-1.6 5-1.6s2.8 1.6 5 1.6 2.8-1.6 5-1.6 2.8 1.6 5 1.6"/>',
    "utensils": '<path d="M6 3v6a2.5 2.5 0 0 0 5 0V3M8.5 3v18M17 21V3c-2.4 1.6-3.5 4.2-3.5 7 0 1.6 1 2.5 3.5 2.5"/>',
    "dice": '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><path d="M8.5 8.5h.01M15.5 8.5h.01M12 12h.01M8.5 15.5h.01M15.5 15.5h.01" stroke-width="2.4"/>',
    "swing": '<path d="M4 21 7 3M20 21 17 3M7 3h10M9 3l-.7 12M15 3l.7 12M6.5 15h4M13.5 15h4"/>',
    "ball": '<circle cx="12" cy="12" r="9"/><path d="m12 7.5 3.8 2.8-1.4 4.4H9.6L8.2 10.3zM12 7.5V3.2M15.8 10.3l4-1.2M14.4 14.7l2.5 3.6M9.6 14.7l-2.5 3.6M8.2 10.3l-4-1.2"/>',
    "bike": '<circle cx="6" cy="16" r="3.6"/><circle cx="18" cy="16" r="3.6"/><path d="m6 16 3.8-7.5h5.2L18 16M9.8 8.5 13 16M8 6h3M15 8.5 14 5.5h2.2"/>',
    "wifi": '<path d="M2.5 9a15 15 0 0 1 19 0M5.6 12.6a10 10 0 0 1 12.8 0M8.7 16.1a5.2 5.2 0 0 1 6.6 0M12 19.5h.01" />',
    "shower": '<path d="M4 21V7a3.5 3.5 0 0 1 7 0M11 7h6.5M9 11h11M10.5 14.5v.01M14.5 14.5v.01M18.5 14.5v.01M12.5 18v.01M16.5 18v.01M10.5 21.5v.01M14.5 21.5v.01M18.5 21.5v.01" />',
    "washer": '<rect x="4" y="3" width="16" height="18" rx="2.5"/><circle cx="12" cy="13.5" r="4.2"/><path d="M8 6.5h.01M11 6.5h.01"/>',
    "paw": '<circle cx="5.8" cy="11" r="1.7"/><circle cx="9.8" cy="6.6" r="1.7"/><circle cx="14.2" cy="6.6" r="1.7"/><circle cx="18.2" cy="11" r="1.7"/><path d="M12 12c-3 0-5.2 3-5.2 5.3 0 1.6 1.4 2 2.7 2 1 0 1.5-.6 2.5-.6s1.5.6 2.5.6c1.300 0 2.700-.4 2.700-2C17.200 15 15 12 12 12z"/>',
    "access": '<circle cx="12" cy="4.2" r="1.7"/><path d="M12 8v6h5l2.3 5.5M12 11h5M8.3 10.6a5.6 5.6 0 1 0 7.2 8"/>',
    "caravan": '<path d="M2 17V9.5A2.5 2.5 0 0 1 4.500 7H13a7 7 0 0 1 7 7v3H2z"/><circle cx="9" cy="18.500" r="2" fill="var(--bianco)"/><path d="M5.500 10.500h4.500v3H5.500zM20 17h2"/>',
    "tent": '<path d="m2.500 20.500 9.500-17 9.500 17zM12 3.500v17M9 20.500l3-6 3 6"/>',
    "camper": '<path d="M2 17V8.500A2.500 2.500 0 0 1 4.500 6H15l5 5v6H2z"/><circle cx="7" cy="18" r="2" fill="var(--bianco)"/><circle cx="16.500" cy="18" r="2" fill="var(--bianco)"/><path d="M15 6.500V11h4.500M5.500 9.500h5v3h-5z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.500v2.500M12 19v2.500M2.500 12H5M19 12h2.500M5.300 5.300l1.800 1.800M16.900 16.900l1.800 1.800M5.300 18.700l1.800-1.800M16.900 7.100l1.800-1.800"/>',
    "pin": '<path d="M12 21.500s-7-6-7-11.500a7 7 0 0 1 14 0c0 5.500-7 11.500-7 11.500z"/><circle cx="12" cy="10" r="2.500"/>',
    "phone": '<path d="M5 3.500h3.800l1.900 4.800-2.400 1.600a11.500 11.500 0 0 0 5.800 5.800l1.600-2.400 4.800 1.900V19a2 2 0 0 1-2 2A16.500 16.500 0 0 1 3 5.500a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.500"/><path d="m3.500 7.500 8.500 6 8.500-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.200l3.300 2"/>',
    "waves": '<path d="M2 8c2.200 0 2.200-1.800 5-1.800S9.800 8 12 8s2.800-1.800 5-1.800S19.800 8 22 8M2 13c2.200 0 2.200-1.800 5-1.800S9.800 13 12 13s2.800-1.800 5-1.800S19.800 13 22 13M2 18c2.200 0 2.200-1.800 5-1.800S9.800 18 12 18s2.800-1.800 5-1.800S19.800 18 22 18"/>',
    "tree": '<path d="M12 21.500V16M12 16c-4 0-6-2-6-4.500 0-2 1.500-3 3-3-.5-3 1.500-5.500 3-5.500s3.500 2.500 3 5.500c1.500 0 3 1 3 3 0 2.500-2 4.500-6 4.500z"/>',
    "arrow": '<path d="M4.500 12h15M13.500 6l6 6-6 6"/>',
    "check": '<path d="m4.500 12.500 5 5 10-11"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "chev-l": '<path d="m14.500 5.500-6.500 6.500 6.500 6.500"/>',
    "chev-r": '<path d="m9.500 5.500 6.500 6.500-6.500 6.500"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.800 3 2.800 15 0 18M12 3c-2.800 3-2.800 15 0 18"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.500M12 7.500v.01" stroke-width="2"/>',
    "alert": '<path d="M12 3.500 22 20.500H2z"/><path d="M12 10v4.500M12 17.500v.01" stroke-width="2"/>',
    "download": '<path d="M12 3.500v12M7 11l5 5 5-5M4.500 20.500h15"/>',
    "route": '<circle cx="6" cy="19" r="2.200"/><circle cx="18" cy="5" r="2.200"/><path d="M8.200 19H15a3.500 3.500 0 0 0 0-7H9a3.500 3.500 0 0 1 0-7h6.800"/>',
    "bocce": '<circle cx="8" cy="15" r="5"/><circle cx="18" cy="8" r="2.800"/><circle cx="17" cy="17.500" r="1.800"/>',
    "calendar": '<rect x="3.500" y="5" width="17" height="15.500" rx="2.500"/><path d="M3.500 10h17M8 3v4M16 3v4"/>',
    "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v4.500a1.500 1.500 0 0 1-1.500 1.500h-11A1.500 1.500 0 0 1 4 18.500v-11A1.500 1.500 0 0 1 5.500 6H10"/>',
}


def sprite():
    body = "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{body}</defs></svg>'


def ic(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


_dim = {}


def dims(path):
    if path not in _dim:
        with Image.open(ROOT / path) as im:
            _dim[path] = im.size
    return _dim[path]


# ----------------------------------------------------------------------------
class Ctx:
    """Contesto di una pagina: lingua, prefissi dei percorsi, traduzioni."""

    def __init__(self, lang, slug):
        self.lang, self.slug = lang, slug
        self.rel = "" if lang == "it" else "../"

    def t(self, key):
        try:
            return S[self.lang][key]
        except KeyError:
            raise KeyError(f"[{self.lang}] chiave mancante: {key}")

    def href(self, slug, lang=None):
        lang = lang or self.lang
        name = "index.html" if slug == "index" else f"{slug}.html"
        if lang == self.lang:
            return name
        if self.lang == "it":
            return f"{lang}/{name}"
        return f"../{name}" if lang == "it" else f"../{lang}/{name}"

    def asset(self, p):
        return self.rel + p

    # immagini ---------------------------------------------------------------
    def site_img(self, slug, alt, cls="", lazy=True, sizes="(min-width: 900px) 40vw, 92vw"):
        path = f"assets/img/site/{slug}.webp"
        w, h = dims(path)
        return (f'<img src="{self.asset(path)}" width="{w}" height="{h}" alt="{alt}"'
                f'{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{" loading=lazy decoding=async" if lazy else ""}>')

    def lake_img(self, slug, alt, cls="", lazy=True, sizes="(min-width: 900px) 50vw, 100vw", hi=False):
        p9, p19 = f"assets/img/lake/{slug}-960.webp", f"assets/img/lake/{slug}-1920.webp"
        w, h = dims(p9)
        attrs = ' fetchpriority="high"' if hi else (" loading=lazy decoding=async" if lazy else "")
        c = f' class="{cls}"' if cls else ""
        return (f'<img src="{self.asset(p9)}" srcset="{self.asset(p9)} 960w, {self.asset(p19)} 1920w" sizes="{sizes}" '
                f'width="{w}" height="{h}" alt="{alt}"{c}{attrs}>')

    def credit(self, slug, short=False):
        c = CREDITS[slug]
        author = c["author"].split(" from ")[0] if not c["author"].startswith("No machine") else "Bol2030"
        lic = c["license"]
        label = f'{author}, {lic}'
        return f'<a href="{c["page"]}" target="_blank" rel="noopener">{label}</a>'

    def credit_txt(self, slug):
        c = CREDITS[slug]
        author = c["author"].split(" from ")[0] if not c["author"].startswith("No machine") else "Bol2030"
        return f'{author}, {c["license"]} (Wikimedia Commons)'


# ----------------------------------------------------------------------------
# Componenti condivisi
# ----------------------------------------------------------------------------
def tramontis_link(ctx):
    return f'<a href="{TRAMONTIS}" target="_blank" rel="noopener lamadunina">Tramontis</a>'


def banner(c):
    if not DEMO:
        return ""
    return ('<div class="demo-banner" role="note" aria-label="Demo"><p>'
            + c.t("banner").replace("{link}", tramontis_link(c)) + "</p></div>")


def header(c):
    items = "".join(
        f'<a href="{c.href(s)}"{" aria-current=page" if c.slug == s else ""}>{c.t("nav." + s)}</a>' for s in NAV)
    langs = "".join(
        f'<li><a href="{c.href(c.slug, l)}" lang="{l}" hreflang="{l}" data-setlang'
        f'{" aria-current=true" if l == c.lang else ""}>{LANG_NAMES[l]}</a></li>' for l in LANGS)
    return f'''<header class="header">
<div class="header__in">
<a class="brand" href="{c.href("index")}" aria-label="{c.t("brand.aria")}">
<svg class="brand__mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1f3b2d"/><path d="M10 44 32 14l22 30z" fill="#f2b134"/><path d="M32 14v30" stroke="#1f3b2d" stroke-width="3"/><path d="M8 50c5 0 5-3 10-3s5 3 10 3 5-3 10-3 5 3 10 3 5-3 8-3" fill="none" stroke="#bfe0ea" stroke-width="3.200" stroke-linecap="round"/><path d="M8 57c5 0 5-3 10-3s5 3 10 3 5-3 10-3 5 3 10 3" fill="none" stroke="#bfe0ea" stroke-width="3.200" stroke-linecap="round" opacity=".6"/></svg>
<span class="brand__txt"><span class="brand__sub">Camping</span><span class="brand__name">La Madunina</span></span></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="{c.t("js.menuOpen")}"><span></span></button>
<nav id="nav" class="nav" aria-label="{c.t("nav.aria")}">{items}<a class="btn nav__cta" href="{c.href("contatti")}">{c.t("cta.info")}</a></nav>
<details class="lang"><summary aria-label="{c.t("lang.label")}: {LANG_NAMES[c.lang]}">{ic("globe")}<span aria-hidden="true">{c.lang.upper()}</span></summary><ul>{langs}</ul></details>
<a class="btn header__cta" href="{c.href("contatti")}">{c.t("cta.info")}</a>
</div>
</header>'''


def footer(c):
    links = "".join(f'<li><a href="{c.href(s)}">{c.t("nav." + s)}</a></li>' for s in ["campeggio", "sistemazioni", "servizi", "galleria", "faq"])
    langs = "".join(
        f'<a href="{c.href(c.slug, l)}" lang="{l}" hreflang="{l}" data-setlang aria-label="{LANG_NAMES[l]}"'
        f'{" aria-current=true" if l == c.lang else ""}>{l.upper()}</a>' for l in LANGS)
    return f'''<footer class="footer">
<div class="wrap">
<div class="footer__grid">
<div>
<a class="brand" href="{c.href("index")}" aria-label="{c.t("brand.aria")}"><svg class="brand__mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#f2b134"/><path d="M10 44 32 14l22 30z" fill="#1f3b2d"/><path d="M8 51c5 0 5-3 10-3s5 3 10 3 5-3 10-3 5 3 10 3 5-3 8-3" fill="none" stroke="#fff" stroke-width="3.200" stroke-linecap="round"/></svg><span class="brand__txt"><span class="brand__sub">Camping</span><span class="brand__name">La Madunina</span></span></a>
<address>{ADDR1}<br>{ADDR2}</address>
<p class="small" style="margin-top:12px">{c.t("footer.tag")}</p>
</div>
<div><h2>{c.t("footer.explore")}</h2><ul>{links}</ul></div>
<div><h2>{c.t("footer.info")}</h2><ul>
<li><a href="{c.href("prezzi")}">{c.t("footer.prices")}</a></li>
<li><a href="{c.asset(PDF_LOCAL)}" target="_blank" rel="noopener">{c.t("footer.pdf")}</a></li>
<li><a href="{c.href("cartina")}">{c.t("footer.map")}</a></li>
<li><a href="{c.href("contatti")}">{c.t("nav.contatti")}</a></li>
</ul></div>
<div><h2>{c.t("footer.contacts")}</h2><ul>
<li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
<li><a href="tel:{MOBILE_TEL}">{MOBILE}</a></li>
<li><a href="mailto:{MAIL}">{MAIL}</a></li>
</ul>
<h2 style="margin-top:22px">{c.t("lang.label")}</h2><div class="footer__langs">{langs}</div></div>
</div>
<div class="footer__bar">
<p style="margin:0;max-width:none">{c.t("footer.made").replace("{link}", tramontis_link(c))}</p>
<p style="margin:0;max-width:none"><a href="{c.href("privacy")}" style="font-weight:600">{c.t("nav.privacy")}</a> · <a href="{c.href("note-legali")}" style="font-weight:600">{c.t("nav.note-legali")}</a></p>
</div>
</div>
</footer>'''


def head(c, extra=""):
    slug, lang = c.slug, c.lang
    title = c.t(f"{slug}.title")
    desc = c.t(f"{slug}.desc")
    base = SITE_URL + "/" if SITE_URL else ""
    alts = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{(SITE_URL + "/" + ("" if l == "it" else l + "/") + ("index.html" if slug == "index" else slug + ".html")) if SITE_URL else c.href(slug, l)}">\n'
        for l in LANGS)
    xdef = (SITE_URL + "/" + ("index.html" if slug == "index" else slug + ".html")) if SITE_URL else c.href(slug, "it")
    og_img = (SITE_URL + "/assets/img/lake/lago-sponda-fiorita-1920.webp") if SITE_URL else c.asset("assets/img/lake/lago-sponda-fiorita-1920.webp")
    i18n = {k[3:]: v for k, v in S[lang].items() if k.startswith("js.")}
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''}
<meta name="theme-color" content="#1f3b2d">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Camping La Madunina — {c.t("demo.label")}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
{alts}<link rel="alternate" hreflang="x-default" href="{xdef}">
<link rel="icon" href="{c.asset("assets/img/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{c.asset("assets/img/favicon.ico")}" sizes="32x32">
<link rel="apple-touch-icon" href="{c.asset("assets/img/apple-touch-icon.png")}">
<link rel="preload" href="{c.asset("assets/fonts/fraunces-latin-opsz-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{c.asset("assets/fonts/manrope-latin-wght-normal.woff2")}" as="font" type="font/woff2" crossorigin>
{extra}<link rel="stylesheet" href="{c.asset("assets/css/style.css")}">
<script>document.documentElement.classList.add("js");window.LM_I18N={json.dumps(i18n, ensure_ascii=False)};</script>
</head>'''


def wrap_page(c, body, extra_head=""):
    return f'''{head(c, extra_head)}
<body>
<a class="skip" href="#main">{c.t("skip")}</a>
{sprite()}
{'<div class="wm" aria-hidden="true"></div>' if DEMO else ''}
<div class="top">
{banner(c)}
{header(c)}
</div>
<main id="main">
{body}
</main>
{footer(c)}
<script src="{c.asset("assets/js/main.js")}" defer></script>
</body>
</html>
'''


# ----------------------------------------------------------------------------
# Blocchi riusabili
# ----------------------------------------------------------------------------
def page_hero(c, img_slug, alt_key, h1_key, lead_key=None):
    lead = f'<p class="lead">{c.t(lead_key)}</p>' if lead_key else ""
    return f'''<section class="hero hero--page" aria-labelledby="h1">
{c.lake_img(img_slug, c.t(alt_key), cls="hero__img", lazy=False, sizes="100vw", hi=True)}
<div class="hero__lines" aria-hidden="true"></div>
<div class="wrap hero__body"><h1 id="h1">{c.t(h1_key)}</h1>{lead}</div>
<p class="hero__credit">{c.t("img.illustrative")} {c.credit(img_slug)}</p>
<span class="wave" aria-hidden="true"></span>
</section>'''


def plain_hero(c, h1_key, lead_key=None):
    lead = f'<p class="lead">{c.t(lead_key)}</p>' if lead_key else ""
    return f'''<section class="hero hero--page" aria-labelledby="h1" style="min-height:clamp(260px,34svh,380px);background:var(--bosco)">
<div class="hero__lines" aria-hidden="true" style="opacity:.18"></div>
<div class="wrap hero__body"><h1 id="h1">{c.t(h1_key)}</h1>{lead}</div>
<span class="wave" aria-hidden="true"></span>
</section>'''


def cta_final(c, img="tramonto-cigno", alt_key="img.cta.alt"):
    return f'''<section class="cta-final" aria-labelledby="cta-h">
{c.lake_img(img, c.t(alt_key), lazy=True, sizes="100vw")}
<div class="wrap rv"><h2 id="cta-h">{c.t("ctaf.title")}</h2>
<p class="lead">{c.t("ctaf.text")}</p>
<div class="btn-row"><a class="btn" href="{c.href("contatti")}">{c.t("cta.info")} {ic("arrow")}</a><a class="btn btn--light" href="tel:{PHONE_TEL}">{ic("phone")} {PHONE}</a></div></div>
<p class="credit">{c.t("img.illustrative")} {c.credit(img)}</p>
</section>'''


def tag(c, kind):
    return {"off": f'<span class="tag tag--ok">{ic("check","icon")} {c.t("src.off")}</span>',
            "pdf": f'<span class="tag tag--ok">{ic("check","icon")} {c.t("src.pdf")}</span>',
            "third": f'<span class="tag tag--warn">{ic("alert","icon")} {c.t("src.third")}</span>',
            "ask": f'<span class="tag tag--warn">{ic("alert","icon")} {c.t("src.ask")}</span>'}[kind]


def svc_item(c, icon, key, kind, i=0):
    return (f'<li class="rv" style="--i:{i}"><span class="ico">{ic(icon)}</span><h3>{c.t("svc." + key + ".t")}</h3>'
            f'<p>{c.t("svc." + key + ".d")}</p>{tag(c, kind)}</li>')


SERVICES = [  # (icona, chiave, fonte)
    ("pool", "pool", "pdf"), ("utensils", "food", "off"), ("dice", "games", "off"), ("swing", "kids", "off"),
    ("ball", "sport", "off"), ("bike", "bike", "off"), ("wifi", "wifi", "off"), ("shower", "showers", "pdf"),
    ("washer", "washer", "off"), ("waves", "beach", "off"),
    ("paw", "dogs", "third"), ("access", "access", "third"), ("camper", "campersvc", "third"),
]


def practical_dl(c):
    return f'''<dl class="dl">
<div><dt>{ic("pin")}</dt><dd class="label">{c.t("lbl.address")}</dd><dd><a href="{MAPS_Q}" target="_blank" rel="noopener">{ADDR1}<br>{ADDR2}</a></dd></div>
<div><dt>{ic("phone")}</dt><dd class="label">{c.t("lbl.phone")}</dd><dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd></div>
<div><dt>{ic("phone")}</dt><dd class="label">{c.t("lbl.mobile")}</dd><dd><a href="tel:{MOBILE_TEL}">{MOBILE}</a></dd></div>
<div><dt>{ic("mail")}</dt><dd class="label">{c.t("lbl.email")}</dd><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
<div><dt>{ic("clock")}</dt><dd class="label">{c.t("lbl.open")}</dd><dd>{c.t("open.text")}<br><span class="small muted">{c.t("open.note")}</span></dd></div>
</dl>'''


def gallery_items(c):
    """(slug, tipo, categoria, classe, mosaico)"""
    return [
        ("ingresso", "site", "camp", ""), ("piscina", "site", "camp", ""), ("tramonto", "site", "camp", ""),
        ("piazzetta", "site", "camp", ""), ("ristorante", "site", "camp", ""), ("piazzole", "site", "camp", ""),
        ("servizi-igienici", "site", "camp", ""), ("serata-pista", "site", "camp", ""), ("pista-ciclabile", "site", "camp", ""),
        ("lago-sponda-fiorita", "lake", "lake", "wide"), ("passerella-lago", "lake", "lake", ""), ("tramonto-cigno", "lake", "lake", ""),
        ("ninfee-lago", "lake", "lake", ""), ("riflesso-colline", "lake", "lake", ""), ("cigni-pontile", "lake", "lake", "wide"),
        ("passerella-ternate", "lake", "lake", ""), ("alba-lago", "lake", "lake", ""), ("veduta-aerea", "lake", "lake", ""),
        ("salice-lago", "lake", "lake", ""),
    ]


def gitem(c, slug, kind, cat, cls="", mosaic=None):
    cap = c.t("g." + slug)
    if kind == "site":
        full = c.asset(f"assets/img/site/{slug}.webp")
        thumb = c.site_img(slug, cap)
        credit = c.t("img.credit.site")
    else:
        full = c.asset(f"assets/img/lake/{slug}-1920.webp")
        thumb = c.lake_img(slug, cap, sizes="(min-width: 900px) 33vw, 50vw")
        credit = c.t("img.illustrative") + " " + c.credit_txt(slug)
    dcap = f"{cap} — <small>{credit}</small>"
    m = f" {mosaic}" if mosaic else ""
    return (f'<figure class="gitem{(" " + cls) if cls else ""}{m} rv" data-cat="{cat}"><a href="{full}" data-lightbox data-caption="{dcap.replace(chr(34), "&quot;")}">'
            f'{thumb}<span class="cap">{cap}</span></a></figure>')


# ----------------------------------------------------------------------------
# Pagine
# ----------------------------------------------------------------------------
def p_index(c):
    hero_alt = c.t("img.hero.alt")
    pre = (f'<link rel="preload" as="image" href="{c.asset("assets/img/lake/lago-sponda-fiorita-960.webp")}" '
           f'imagesrcset="{c.asset("assets/img/lake/lago-sponda-fiorita-960.webp")} 960w, {c.asset("assets/img/lake/lago-sponda-fiorita-1920.webp")} 1920w" imagesizes="100vw">\n')
    svcs = "".join(svc_item(c, i, k, s, n) for n, (i, k, s) in enumerate(SERVICES[:8]))
    mos = [("ingresso", "site", "camp", "", "g1"), ("passerella-lago", "lake", "lake", "", "g2"), ("piscina", "site", "camp", "", "g3"),
           ("tramonto", "site", "camp", "", "g4"), ("piazzetta", "site", "camp", "", "g5"), ("ninfee-lago", "lake", "lake", "", "g6"),
           ("ristorante", "site", "camp", "", "g7")]
    mosaic = "".join(gitem(c, s, k, ct, cl, m) for s, k, ct, cl, m in mos)
    body = f'''<section class="hero" aria-labelledby="h1">
{c.lake_img("lago-sponda-fiorita", hero_alt, cls="hero__img", lazy=False, sizes="100vw", hi=True)}
<div class="hero__lines" aria-hidden="true"></div>
<div class="wrap hero__body">
<h1 id="h1">{c.t("hero.title")}</h1>
<p class="lead">{c.t("hero.sub")}</p>
<div class="btn-row"><a class="btn" href="{c.href("campeggio")}">{c.t("hero.cta1")} {ic("arrow")}</a><a class="btn btn--light" href="{c.href("contatti")}">{c.t("cta.info")}</a></div>
</div>
<p class="hero__credit">{c.t("img.illustrative")} {c.credit("lago-sponda-fiorita")}</p>
<span class="wave" aria-hidden="true"></span>
</section>

<section class="facts" aria-label="{c.t("facts.aria")}">
<div class="wrap"><div class="facts__grid">
<div class="fact">{ic("pin")}<div><strong>{c.t("lbl.address")}</strong><a href="{MAPS_Q}" target="_blank" rel="noopener">{ADDR1}<br>{ADDR2}</a></div></div>
<div class="fact">{ic("phone")}<div><strong>{c.t("lbl.phone")}</strong><a href="tel:{PHONE_TEL}">{PHONE}</a><a href="tel:{MOBILE_TEL}">{MOBILE}</a></div></div>
<div class="fact">{ic("mail")}<div><strong>{c.t("lbl.email")}</strong><a href="mailto:{MAIL}">{MAIL}</a></div></div>
<div class="fact">{ic("clock")}<div><strong>{c.t("lbl.open")}</strong><span>{c.t("open.text")}</span><small>{c.t("open.note")}</small></div></div>
</div></div>
</section>

<section class="section" id="presentazione" aria-labelledby="pres-h">
<div class="wrap split">
<div class="rv">
<p class="kicker">{ic("waves")} {c.t("pres.kicker")}</p>
<h2 id="pres-h">{c.t("pres.title")}</h2>
<p class="lead">{c.t("pres.lead")}</p>
<p>{c.t("pres.p2")}</p>
<ul class="checklist">
<li>{ic("check")}<span>{c.t("pres.l1")}</span></li>
<li>{ic("check")}<span>{c.t("pres.l2")}</span></li>
<li>{ic("check")}<span>{c.t("pres.l3")}</span></li>
</ul>
<a class="link-arrow" href="{c.href("campeggio")}">{c.t("pres.more")} {ic("arrow")}</a>
</div>
<div class="stack-photos rv" style="--i:2">
<figure class="ph-a">{c.site_img("ingresso", c.t("img.ingresso.alt"))}<figcaption>{c.t("img.credit.site")}</figcaption></figure>
<figure class="ph-b">{c.site_img("piazzetta", c.t("img.piazzetta.alt"))}</figure>
</div>
</div>
</section>

<section class="section section--sage" aria-labelledby="sis-h">
<div class="wrap">
<div class="section-head rv"><h2 id="sis-h">{c.t("acc.title")}</h2><p class="lead">{c.t("acc.lead")}</p></div>
<div class="cards">
<article class="card pitch pitch--sand rv"><div class="pitch__art" aria-hidden="true">{ic("tent")}</div><div class="card__body"><h3>{c.t("acc.tent.t")}</h3><p>{c.t("acc.tent.d")}</p>{tag(c, "ask")}<a class="link-arrow" href="{c.href("sistemazioni")}#tende">{c.t("acc.more")} {ic("arrow")}</a></div></article>
<article class="card pitch rv" style="--i:1"><div class="pitch__art" aria-hidden="true">{ic("camper")}</div><div class="card__body"><h3>{c.t("acc.camper.t")}</h3><p>{c.t("acc.camper.d")}</p>{tag(c, "ask")}<a class="link-arrow" href="{c.href("sistemazioni")}#camper">{c.t("acc.more")} {ic("arrow")}</a></div></article>
<article class="card pitch pitch--lake rv" style="--i:2"><div class="pitch__art" aria-hidden="true">{ic("caravan")}</div><div class="card__body"><h3>{c.t("acc.caravan.t")}</h3><p>{c.t("acc.caravan.d")}</p>{tag(c, "ask")}<a class="link-arrow" href="{c.href("sistemazioni")}#roulotte">{c.t("acc.more")} {ic("arrow")}</a></div></article>
</div>
<p class="small muted rv" style="margin-top:22px">{c.t("acc.note")}</p>
</div>
</section>

<section class="section" aria-labelledby="svc-h">
<div class="wrap">
<div class="section-head rv"><h2 id="svc-h">{c.t("svc.title")}</h2><p class="lead">{c.t("svc.lead")}</p></div>
<ul class="svc">{svcs}</ul>
<p style="margin-top:32px" class="rv"><a class="btn btn--line" href="{c.href("servizi")}">{c.t("svc.all")} {ic("arrow")}</a></p>
</div>
</section>

<section class="section dark" aria-labelledby="nat-h">
<div class="wrap nature">
<figure class="nature__photo rv">{c.lake_img("passerella-lago", c.t("img.passerella.alt"))}<figcaption>{c.t("img.illustrative")} {c.credit("passerella-lago")}</figcaption></figure>
<div class="rv" style="--i:2">
<p class="kicker">{ic("tree")} {c.t("nat.kicker")}</p>
<h2 id="nat-h">{c.t("nat.title")}</h2>
<p class="lead">{c.t("nat.lead")}</p>
<ul class="nature-list">
<li>{ic("waves")}<div><strong>{c.t("nat.1.t")}</strong><span>{c.t("nat.1.d")}</span></div></li>
<li>{ic("bike")}<div><strong>{c.t("nat.2.t")}</strong><span>{c.t("nat.2.d")}</span></div></li>
<li>{ic("sun")}<div><strong>{c.t("nat.3.t")}</strong><span>{c.t("nat.3.d")}</span></div></li>
</ul>
<p class="small muted" style="margin-top:18px">{c.t("nat.note")}</p>
</div>
</div>
</section>

<section class="section" aria-labelledby="gal-h">
<div class="wrap">
<div class="section-head rv"><h2 id="gal-h">{c.t("gal.title")}</h2><p class="lead">{c.t("gal.lead")}</p></div>
<div class="mosaic">{mosaic}</div>
<p style="margin-top:32px" class="rv"><a class="btn btn--line" href="{c.href("galleria")}">{c.t("gal.all")} {ic("arrow")}</a></p>
</div>
</section>

<section class="section section--sand" aria-labelledby="inf-h">
<div class="wrap info-grid">
<div class="rv">
<h2 id="inf-h">{c.t("inf.title")}</h2>
{practical_dl(c)}
<div class="btn-row"><a class="btn" href="{MAPS_DIR}" target="_blank" rel="noopener">{ic("route")} {c.t("inf.directions")}</a><a class="btn btn--line" href="{c.href("cartina")}">{c.t("inf.map")}</a></div>
</div>
<figure class="mapfig rv" style="--i:2"><a href="{c.href("cartina")}">{c.site_img("cartina-zona", c.t("img.cartina.alt"))}</a><figcaption>{c.t("img.cartina.cap")}</figcaption></figure>
</div>
</section>

{cta_final(c)}'''
    return body, pre


def p_campeggio(c):
    pts = [("waves", "p1", "off"), ("pool", "p2", "pdf"), ("utensils", "p3", "off"), ("swing", "p4", "off"), ("bike", "p5", "off"), ("sun", "p6", "ask")]
    pts_html = "".join(svc_item(c, i, k, s, n) for n, (i, k, s) in enumerate(pts)).replace("svc.", "svc.")
    return f'''{page_hero(c, "riflesso-colline", "img.riflesso.alt", "campeggio.h1", "campeggio.lead")}
<section class="section" aria-labelledby="c1">
<div class="wrap split">
<div class="rv"><h2 id="c1">{c.t("campeggio.s1.t")}</h2><p class="lead">{c.t("campeggio.s1.lead")}</p><p>{c.t("campeggio.s1.p")}</p><p>{c.t("campeggio.s1.p2")}</p></div>
<div class="stack-photos rv" style="--i:2"><figure class="ph-a">{c.site_img("ingresso", c.t("img.ingresso.alt"))}<figcaption>{c.t("img.credit.site")}</figcaption></figure><figure class="ph-b">{c.site_img("piazzole", c.t("img.piazzole.alt"))}</figure></div>
</div>
</section>
<section class="section section--sage" aria-labelledby="c2">
<div class="wrap">
<div class="section-head rv"><h2 id="c2">{c.t("campeggio.s2.t")}</h2><p class="lead">{c.t("campeggio.s2.lead")}</p></div>
<ul class="svc">{pts_html}</ul>
</div>
</section>
<section class="section" aria-labelledby="c3">
<div class="wrap split split--rev">
<div class="rv"><figure style="margin:0">{c.lake_img("veduta-aerea", c.t("img.aerea.alt"), cls="rounded")}<figcaption>{c.t("img.illustrative")} {c.credit("veduta-aerea")}</figcaption></figure></div>
<div class="rv" style="--i:2"><h2 id="c3">{c.t("campeggio.s3.t")}</h2><p class="lead">{c.t("campeggio.s3.lead")}</p><p>{c.t("campeggio.s3.p")}</p><p><a class="link-arrow" href="{c.href("cartina")}">{c.t("campeggio.s3.link")} {ic("arrow")}</a></p></div>
</div>
</section>
<section class="section section--sand" aria-labelledby="c4">
<div class="wrap info-grid">
<div class="rv"><h2 id="c4">{c.t("inf.title")}</h2>{practical_dl(c)}<div class="btn-row"><a class="btn" href="{c.href("contatti")}">{c.t("cta.info")} {ic("arrow")}</a></div></div>
<div class="rv" style="--i:2"><div class="notice">{ic("alert")}<div><p><strong>{c.t("confirm.title")}</strong></p><ul class="checklist" style="margin:10px 0 0">{"".join(f"<li>{ic('alert')}<span>{c.t('confirm.' + str(n))}</span></li>" for n in range(1, 7))}</ul></div></div></div>
</div>
</section>
{cta_final(c, "passerella-ternate")}'''


def p_sistemazioni(c):
    def block(anchor, icon, key, rev=False, cls=""):
        know = "".join(f"<li>{ic('check')}<span>{c.t(f'sis.{key}.k{n}')}</span></li>" for n in (1, 2))
        ask = "".join(f"<li>{ic('alert')}<span>{c.t(f'sis.{key}.a{n}')}</span></li>" for n in (1, 2))
        return f'''<article class="split{" split--rev" if rev else ""}" id="{anchor}" aria-labelledby="{anchor}-h" style="padding-block:clamp(28px,4vw,52px)">
<div class="card pitch {cls} rv"><div class="pitch__art" style="aspect-ratio:16/9" aria-hidden="true">{ic(icon)}</div></div>
<div class="rv" style="--i:2"><h2 id="{anchor}-h" style="font-size:clamp(1.8rem,1rem+2.4vw,2.6rem)">{c.t(f"sis.{key}.t")}</h2><p class="lead">{c.t(f"sis.{key}.lead")}</p>
<h3 style="font-size:1.05rem;font-family:var(--font-ui);font-weight:800">{c.t("sis.known")}</h3><ul class="checklist" style="margin:10px 0 18px">{know}</ul>
<h3 style="font-size:1.05rem;font-family:var(--font-ui);font-weight:800">{c.t("sis.ask")}</h3><ul class="checklist" style="margin:10px 0 22px">{ask}</ul>
<div class="btn-row"><a class="btn" href="{c.href("contatti")}">{c.t("cta.info")} {ic("arrow")}</a><a class="btn btn--line" href="{c.href("prezzi")}">{c.t("sis.prices")}</a></div></div>
</article>'''
    return f'''{page_hero(c, "salice-lago", "img.salice.alt", "sistemazioni.h1", "sistemazioni.lead")}
<section class="section" aria-labelledby="s0">
<div class="wrap">
<div class="notice rv">{ic("info")}<div><p>{c.t("sis.notice1")}</p><p>{c.t("sis.notice2")}</p></div></div>
<h2 id="s0" class="sr-only">{c.t("sistemazioni.h1")}</h2>
<div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));margin-bottom:24px">
<figure class="rv" style="margin:0">{c.site_img("piazzole", c.t("img.piazzole.alt"), cls="rounded")}<figcaption>{c.t("img.credit.site")} — {c.t("g.piazzole")}</figcaption></figure>
<figure class="rv" style="margin:0;--i:1">{c.site_img("piazzetta", c.t("img.piazzetta.alt"), cls="rounded")}<figcaption>{c.t("img.credit.site")} — {c.t("g.piazzetta")}</figcaption></figure>
</div>
{block("tende", "tent", "tent", False, "pitch--sand")}
{block("camper", "camper", "camper", True)}
{block("roulotte", "caravan", "caravan", False, "pitch--lake")}
<article class="rv" style="margin-top:28px"><div class="notice notice--info">{ic("info")}<div><p><strong>{c.t("sis.other.t")}</strong></p><p>{c.t("sis.other.d")}</p></div></div></article>
<div class="pdf-card rv"><div><h3>{c.t("pdf.title")}</h3><p>{c.t("pdf.sub")}</p></div><div class="btn-row"><a class="btn" href="{c.href("prezzi")}">{c.t("sis.prices")} {ic("arrow")}</a></div></div>
</div>
</section>
{cta_final(c, "ninfee-lago")}'''


def p_servizi(c):
    def group(title_key, items, start=0):
        lis = "".join(svc_item(c, i, k, s, n) for n, (i, k, s) in enumerate(items))
        return f'<h2 class="rv" style="font-size:clamp(1.6rem,1rem+1.8vw,2.3rem);margin:{"0" if start==0 else "56px"} 0 20px">{c.t(title_key)}</h2><ul class="svc">{lis}</ul>'
    S_ = {k: (i, k, s) for i, k, s in SERVICES}
    return f'''{page_hero(c, "ninfee-lago", "img.ninfee.alt", "servizi.h1", "servizi.lead")}
<section class="section" aria-labelledby="sv0">
<div class="wrap">
<div class="notice rv">{ic("info")}<div><p>{c.t("servizi.notice")}</p></div></div>
<div class="rv" style="margin-bottom:28px"><span class="tag tag--ok">{ic("check")} {c.t("src.off")}</span> <span class="tag tag--ok">{ic("check")} {c.t("src.pdf")}</span> <span class="tag tag--warn">{ic("alert")} {c.t("src.third")}</span></div>
<h2 id="sv0" class="sr-only">{c.t("servizi.h1")}</h2>
{group("servizi.g1", [S_[k] for k in ("pool", "food", "games", "kids", "sport", "bike", "beach")])}
{group("servizi.g2", [S_[k] for k in ("showers", "washer", "wifi")], 1)}
{group("servizi.g3", [S_[k] for k in ("dogs", "access", "campersvc")], 1)}
<div class="notice rv" style="margin-top:44px">{ic("alert")}<div><p><strong>{c.t("servizi.na.t")}</strong></p><p>{c.t("servizi.na.d")}</p></div></div>
</div>
</section>
{cta_final(c, "cigni-pontile")}'''


def p_galleria(c):
    items = "".join(gitem(c, s, k, ct, cl) for s, k, ct, cl in gallery_items(c))
    n = len(gallery_items(c))
    return f'''{page_hero(c, "alba-lago", "img.alba.alt", "galleria.h1", "galleria.lead")}
<section class="section" aria-labelledby="g0">
<div class="wrap">
<h2 id="g0" class="sr-only">{c.t("galleria.h1")}</h2>
<div class="filters" role="group" aria-label="{c.t("gal.filter")}">
<button class="chip" type="button" data-filter="all" aria-pressed="true">{c.t("gal.f.all")}</button>
<button class="chip" type="button" data-filter="camp" aria-pressed="false">{c.t("gal.f.camp")}</button>
<button class="chip" type="button" data-filter="lake" aria-pressed="false">{c.t("gal.f.lake")}</button>
</div>
<p class="sr-only" id="gcount" aria-live="polite" role="status"></p>
<div class="gallery">{items}</div>
<div class="notice notice--info gnote-box" style="margin-top:32px">{ic("info")}<div><p>{c.t("gal.note1")}</p><p>{c.t("gal.note2")}</p></div></div>
</div>
</section>
{cta_final(c, "tramonto-cigno")}'''


def p_prezzi(c):
    rows = [("adult", "8,00", None), ("child", "7,00", None), ("pitch", "10,00", None), ("dog", "3,00", None),
            ("tax", "0,50", None), ("guest", "7,00", None), ("showers", None, "free")]
    tr = ""
    for k, v, f in rows:
        note = c.t(f"price.{k}.n") if f"price.{k}.n" in S[c.lang] else ""
        small = f"<small>{note}</small>" if note else ""
        cell = f'<td class="num">{v}</td>' if v else f'<td class="num free">{c.t("price.free")}</td>'
        tr += f'<tr><th scope="row">{c.t(f"price.{k}.l")}{small}</th>{cell}</tr>'
    return f'''{page_hero(c, "canne-ninfee", "img.canne.alt", "prezzi.h1", "prezzi.lead")}
<section class="section" aria-labelledby="pr0">
<div class="wrap--narrow" style="width:min(940px,100% - 2*var(--gutter));margin-inline:auto">
<div class="notice rv">{ic("alert")}<div><p><strong>{c.t("prezzi.warn.t")}</strong></p><p>{c.t("prezzi.warn.d")}</p></div></div>
<div class="table-wrap rv">
<table class="prices">
<caption id="pr0">{c.t("prezzi.caption")}</caption>
<thead><tr><th scope="col">{c.t("prezzi.col.item")}</th><th scope="col" style="text-align:right">{c.t("prezzi.col.amount")}</th></tr></thead>
<tbody>{tr}</tbody>
</table>
</div>
<p class="small muted rv" style="margin:-12px 0 28px">{c.t("prezzi.unit")}</p>
<h2 class="rv" style="font-size:clamp(1.6rem,1rem+1.8vw,2.2rem)">{c.t("prezzi.terms")}</h2>
<ul class="terms rv">
<li>{ic("pool")}<span>{c.t("prezzi.t1")}</span></li>
<li>{ic("calendar")}<span>{c.t("prezzi.t2")}</span></li>
<li>{ic("info")}<span>{c.t("prezzi.t3")}</span></li>
<li>{ic("info")}<span>{c.t("prezzi.t4")}</span></li>
</ul>
<div class="pdf-card rv"><div><h3>{c.t("pdf.title")}</h3><p>{c.t("prezzi.pdf.meta")}</p></div>
<div class="btn-row"><a class="btn" href="{c.asset(PDF_LOCAL)}" target="_blank" rel="noopener">{ic("download")} {c.t("prezzi.pdf.open")}</a><a class="btn btn--light" href="{PDF_ORIG}" target="_blank" rel="noopener">{ic("ext")} {c.t("prezzi.pdf.orig")}</a></div></div>
<p class="small muted rv" style="margin-top:22px">{c.t("prezzi.source")}</p>
<div class="btn-row rv" style="margin-top:28px"><a class="btn" href="{c.href("contatti")}">{c.t("prezzi.ask")} {ic("arrow")}</a></div>
</div>
</section>'''


def p_cartina(c):
    return f'''{page_hero(c, "veduta-aerea", "img.aerea.alt", "cartina.h1", "cartina.lead")}
<section class="section" aria-labelledby="m0">
<div class="wrap">
<h2 id="m0" class="sr-only">{c.t("cartina.h1")}</h2>
<div class="maps-two">
<figure class="mapfig rv"><a href="{c.asset("assets/img/site/cartina-zona.webp")}" data-lightbox data-caption="{c.t("img.cartina.cap")}">{c.site_img("cartina-zona", c.t("img.cartina.alt"))}</a><figcaption>{c.t("img.cartina.cap")}</figcaption></figure>
<figure class="mapfig rv" style="--i:2"><a href="{c.asset("assets/img/site/cartina-dettaglio.webp")}" data-lightbox data-caption="{c.t("img.dettaglio.cap")}">{c.site_img("cartina-dettaglio", c.t("img.dettaglio.alt"))}</a><figcaption>{c.t("img.dettaglio.cap")}</figcaption></figure>
</div>
<p class="small muted rv" style="margin-top:12px">{c.t("cartina.zoom")}</p>
<div class="info-grid" style="margin-top:56px">
<div class="rv"><h2 style="font-size:clamp(1.8rem,1rem+2.4vw,2.6rem)">{c.t("cartina.how")}</h2>
<p class="lead">{c.t("cartina.how.lead")}</p>
<ol class="steps"><li><span>{c.t("cartina.s1")}</span></li><li><span>{c.t("cartina.s2")}</span></li><li><span>{c.t("cartina.s3")}</span></li></ol>
<p class="small muted">{c.t("cartina.how.note")}</p>
<div class="btn-row"><a class="btn" href="{MAPS_DIR}" target="_blank" rel="noopener">{ic("route")} {c.t("inf.directions")}</a><a class="btn btn--line" href="{MAPS_Q}" target="_blank" rel="noopener">{ic("pin")} {c.t("cartina.gmaps")}</a><a class="btn btn--line" href="{OSM}" target="_blank" rel="noopener">{ic("ext")} OpenStreetMap</a></div>
<p class="small muted" style="margin-top:14px">{c.t("cartina.extnote")}</p></div>
<div class="rv" style="--i:2"><h2 style="font-size:clamp(1.8rem,1rem+2.4vw,2.6rem)">{c.t("inf.title")}</h2>{practical_dl(c)}</div>
</div>
</div>
</section>
{cta_final(c, "riflesso-colline")}'''


def p_contatti(c):
    return f'''{page_hero(c, "cigni-pontile", "img.cigni.alt", "contatti.h1", "contatti.lead")}
<section class="section" aria-labelledby="k0">
<div class="wrap form-grid">
<div class="rv">
<h2 id="k0" style="font-size:clamp(1.8rem,1rem+2.4vw,2.6rem)">{c.t("contatti.direct")}</h2>
<div class="contact-big">
<a class="c" href="tel:{PHONE_TEL}">{ic("phone")}<div><span>{c.t("lbl.phone")}</span><strong>{PHONE}</strong></div></a>
<a class="c" href="tel:{MOBILE_TEL}">{ic("phone")}<div><span>{c.t("lbl.mobile")}</span><strong>{MOBILE}</strong></div></a>
<a class="c" href="mailto:{MAIL}">{ic("mail")}<div><span>{c.t("lbl.email")}</span><strong>{MAIL}</strong></div></a>
<a class="c" href="{MAPS_Q}" target="_blank" rel="noopener">{ic("pin")}<div><span>{c.t("lbl.address")}</span><strong>{ADDR1}, {ADDR2}</strong></div></a>
</div>
<p class="small muted" style="margin-top:18px">{c.t("contatti.hours")}</p>
<p><a class="link-arrow" href="{c.href("cartina")}">{c.t("inf.map")} {ic("arrow")}</a></p>
</div>
<form class="form rv" id="contact-form" style="--i:2" action="mailto:{MAIL}" method="post" enctype="text/plain" aria-labelledby="f0">
<h2 id="f0" style="font-size:1.6rem;margin:0">{c.t("form.title")}</h2>
<div class="notice notice--info" style="margin:0">{ic("info")}<div><p>{c.t("form.demo")}</p></div></div>
<div class="field"><label for="f-name">{c.t("form.name")}</label><input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="err-name"><span class="err" id="err-name" aria-live="polite"></span></div>
<div class="field"><label for="f-email">{c.t("form.email")}</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="err-email"><span class="err" id="err-email" aria-live="polite"></span></div>
<div class="field"><label for="f-period">{c.t("form.period")} <span class="opt">({c.t("form.optional")})</span></label><input id="f-period" name="period" type="text" placeholder="{c.t("form.period.ph")}" aria-describedby="err-period"><span class="err" id="err-period"></span></div>
<div class="field"><label for="f-msg">{c.t("form.message")}</label><textarea id="f-msg" name="message" required aria-describedby="err-message"></textarea><span class="err" id="err-message" aria-live="polite"></span></div>
<div class="field"><label class="check" for="f-priv"><input id="f-priv" name="privacy" type="checkbox" required aria-describedby="err-privacy"><span>{c.t("form.privacy").replace("{link}", f'<a href="{c.href("privacy")}">{c.t("nav.privacy")}</a>')}</span></label><span class="err" id="err-privacy" aria-live="polite"></span></div>
<button class="btn" type="submit">{ic("mail")} {c.t("form.submit")}</button>
<p class="form__status" id="form-status" role="status" aria-live="polite"></p>
<p class="small muted" style="margin:0">{c.t("form.after")}</p>
</form>
</div>
</section>'''


FAQ_N = 9


def p_faq(c):
    qa = ""
    for n in range(1, FAQ_N + 1):
        qa += f'<details class="rv"><summary>{c.t(f"faq.q{n}")}</summary><div class="ans"><p>{c.t(f"faq.a{n}")}</p></div></details>'
    return f'''{page_hero(c, "passerella-ternate", "img.ternate.alt", "faq.h1", "faq.lead")}
<section class="section" aria-labelledby="q0">
<div class="wrap--narrow faq" style="width:min(860px,100% - 2*var(--gutter));margin-inline:auto">
<h2 id="q0" class="sr-only">{c.t("faq.h1")}</h2>
{qa}
<div class="btn-row rv" style="margin-top:32px"><a class="btn" href="{c.href("contatti")}">{c.t("cta.info")} {ic("arrow")}</a><a class="btn btn--line" href="{c.href("prezzi")}">{c.t("nav.prezzi")}</a></div>
</div>
</section>'''


def legal_body(c, key, n_sections):
    secs = ""
    for n in range(1, n_sections + 1):
        secs += f'<h2 style="font-size:1.5rem;margin-top:36px">{c.t(f"{key}.s{n}.t")}</h2>{c.t(f"{key}.s{n}.d")}'
    return secs


def p_privacy(c):
    return f'''{plain_hero(c, "privacy.h1")}
<section class="section" aria-labelledby="h1">
<div class="wrap--narrow" style="width:min(820px,100% - 2*var(--gutter));margin-inline:auto">
<div class="notice">{ic("alert")}<div><p><strong>{c.t("legal.draft.t")}</strong></p><p>{c.t("legal.draft.d")}</p></div></div>
{legal_body(c, "privacy", 6)}
</div>
</section>'''


def p_note(c):
    credits = "".join(
        f'<li>{ic("check")}<span><strong>{c.t("g." + s)}</strong> — {c.credit(s)}</span></li>'
        for s in CREDITS)
    return f'''{plain_hero(c, "note-legali.h1")}
<section class="section" aria-labelledby="h1">
<div class="wrap--narrow" style="width:min(820px,100% - 2*var(--gutter));margin-inline:auto">
<div class="notice">{ic("alert")}<div><p><strong>{c.t("legal.draft.t")}</strong></p><p>{c.t("legal.draft.d")}</p></div></div>
{legal_body(c, "note-legali", 5)}
<h2 style="font-size:1.5rem;margin-top:36px">{c.t("legal.credits.t")}</h2>
<p>{c.t("legal.credits.d")}</p>
<ul class="checklist" style="margin-top:12px">{credits}</ul>
</div>
</section>'''


BUILDERS = {"index": p_index, "campeggio": p_campeggio, "sistemazioni": p_sistemazioni, "servizi": p_servizi, "galleria": p_galleria,
            "prezzi": p_prezzi, "cartina": p_cartina, "contatti": p_contatti, "faq": p_faq, "privacy": p_privacy, "note-legali": p_note}


def main():
    count = 0
    for lang in LANGS:
        out_dir = ROOT if lang == "it" else ROOT / lang
        out_dir.mkdir(exist_ok=True)
        for slug in PAGES:
            c = Ctx(lang, slug)
            res = BUILDERS[slug](c)
            body, extra = res if isinstance(res, tuple) else (res, "")
            name = "index.html" if slug == "index" else f"{slug}.html"
            (out_dir / name).write_text(wrap_page(c, body, extra), encoding="utf-8")
            count += 1
    print(f"Generate {count} pagine.")


if __name__ == "__main__":
    main()
