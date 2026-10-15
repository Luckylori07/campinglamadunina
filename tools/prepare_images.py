"""Ottimizza le immagini della demo -> WebP in assets/img/{site,lake}.

Uso: python3 -I tools/prepare_images.py <cartella-con-download-commons>
- site/: foto autentiche del sito ufficiale (originali a bassa risoluzione in
  assets/img/originals/), ritagliate dalle cornici blu e ingrandite con Lanczos.
- lake/: foto del Lago di Comabbio da Wikimedia Commons (vedi IMAGE_SOURCES.md).
"""
import sys, json, pathlib
from PIL import Image, ImageFilter

root = pathlib.Path(__file__).resolve().parent.parent
orig = root / "assets/img/originals"
site = root / "assets/img/site"
lake = root / "assets/img/lake"

# slug: (file, (crop x frac, crop y frac), scale)
SITE = {
    "ingresso": ("ingresso.jpg", (0, 0), 2.2),
    "piazzetta": ("thumbs/la-piazzetta.jpg", (0, 0), 3.5),
    "piazzole": ("thumbs/Le-piazzole.jpg", (0, 0), 3.5),
    "piscina": ("la-Piscina.jpg", (0.09, 0.16), 3.4),
    "ristorante": ("thumbs/Il-ristorante.jpg", (0.09, 0.12), 4.2),
    "servizi-igienici": ("thumbs/bagno.jpg", (0.09, 0.12), 4.2),
    "serata-pista": ("thumbs/giochi.jpg", (0, 0), 3.5),
    "pista-ciclabile": ("thumbs/Il-lago.jpg", (0, 0), 3.6),
    "tramonto": ("tramonto-su-lago.jpg", (0.09, 0.16), 3.4),
}
LAKE = {  # slug: commons file (nome locale), larghezze
    "lago-sponda-fiorita": "Lago_di_Comabbio_4882918177_.jpg",
    "passerella-lago": "Boardwalk_on_Lago_di_Comabbio.jpg",
    "passerella-ternate": "Ternate_Lago_di_Comabbio.jpg",
    "ninfee-lago": "Lake_Comabbio.jpg",
    "tramonto-cigno": "Queen_of_the_Lake_regina_del_lago_al_tramonto.jpg",
    "riflesso-colline": "Lago_Comabbio_riflesso_1.jpg",
    "cigni-pontile": "Cigni_sul_Lago_di_Comabbio.jpg",
    "veduta-aerea": "Aerial_photograph_of_Lago_di_Comabbio.jpg",
    "salice-lago": "Lago_di_Comabbio_4882917585_.jpg",
    "alba-lago": "Lago_di_Comabbio.JPG",
    "canne-ninfee": "CANNE_E_NINFEE_NEL_LAGO_DI_COMABBIO.jpg",
}

def save(im, path, q):
    im.save(path, "WEBP", quality=q, method=6)
    print(path.relative_to(root), im.size, path.stat().st_size // 1024, "KB")

for slug, (f, (fx, fy), s) in SITE.items():
    im = Image.open(orig / f).convert("RGB")
    w, h = im.size
    im = im.crop((round(w * fx), round(h * fy), round(w * (1 - fx)), round(h * (1 - fy))))
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=3))
    save(im, site / f"{slug}.webp", 78)

if len(sys.argv) > 1:
    src = pathlib.Path(sys.argv[1])
    for slug, f in LAKE.items():
        im = Image.open(src / f).convert("RGB")
        for width in (1920, 960):
            if im.width < width:
                continue
            r = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            save(r, lake / f"{slug}-{width}.webp", 74 if width == 1920 else 72)

# Cartine ufficiali: ingrandimento 2x/3x (le originali sono 380x380 e 215x180)
a = Image.open(orig / "cartina.gif").convert("RGB")
a = a.resize((a.width * 2, a.height * 2), Image.LANCZOS)
a.save(site / "cartina-zona.webp", quality=82, method=6)
b = Image.open(orig / "cartina2p.jpg").convert("RGB")
b = b.resize((b.width * 3, b.height * 3), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 70, 2))
b.save(site / "cartina-dettaglio.webp", quality=84, method=6)
