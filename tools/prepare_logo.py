"""Logo: ritaglia l'ovale dal logo-camp.jpg, lo ingrandisce 4x e ne riallinea i colori alla palette del sito."""
import colorsys, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageChops
root = pathlib.Path(__file__).resolve().parent.parent
src = Image.open(root / "assets/img/originals/logo-camp.jpg").convert("RGB")
S = 4
big = src.resize((src.width * S, src.height * S), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2.2, 90, 2))
# maschera ellittica morbida (l'ovale occupa circa x 6..120, y 9..85 dell'originale)
cx, cy, rx, ry = 63.5 * S, 47.5 * S, 56.2 * S, 37.2 * S
m = Image.new("L", big.size, 0)
ImageDraw.Draw(m).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
m = m.filter(ImageFilter.GaussianBlur(S * 0.9))
# ricolorazione: verde -> verde bosco, rosso -> ambra scuro; bianco invariato; blu residuo -> bosco
px = big.load()
BOSCO = colorsys.rgb_to_hsv(0x2d/255, 0x5a/255, 0x43/255)
AMBRA = colorsys.rgb_to_hsv(0xb8/255, 0x70/255, 0x0c/255)
for y in range(big.height):
    for x in range(big.width):
        r, g, b = px[x, y]
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        if s < 0.16:
            continue  # bianchi / grigi
        deg = h * 360
        if 70 <= deg <= 190:          # verde (e azzurro residuo ai bordi)
            t = min(1, s / 0.6)
            ns = BOSCO[1] * t + s * (1 - t) * 0.4
            nv = BOSCO[2] * (0.75 + 0.5 * v)
            nr, ng, nb = colorsys.hsv_to_rgb(BOSCO[0], min(1, ns), min(1, nv))
        elif deg >= 330 or deg <= 25:  # rosso -> ambra scuro
            nv = AMBRA[2] * (0.78 + 0.35 * v)
            nr, ng, nb = colorsys.hsv_to_rgb(AMBRA[0], min(1, AMBRA[1] * min(1, s / 0.5 + 0.2)), min(1, nv))
        else:
            continue
        px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255))
out = big.convert("RGBA"); out.putalpha(m)
out = out.crop(out.getbbox())
out.save(root / "assets/img/logo-madunina.png", optimize=True)
out.save(root / "assets/img/logo-madunina.webp", quality=90, method=6)
# favicon / apple-touch: l'ovale su quadrato trasparente
def square(size):
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0)); o = out.copy(); o.thumbnail((size, size), Image.LANCZOS)
    c.paste(o, ((size - o.width) // 2, (size - o.height) // 2), o); return c
square(180).save(root / "assets/img/apple-touch-icon.png")
square(64).save(root / "assets/img/favicon.png")
square(48).save(root / "assets/img/favicon.ico", sizes=[(48, 48)])
print(out.size)
