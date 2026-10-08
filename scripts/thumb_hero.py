"""Yakun ekran uchun YouTube-muqova uslubidagi rasm (uslub-27/28 oq yakun ekrani): spiker kesmasi + iliq bokeh fon + orqa yorug'lik.

python scripts/thumb_hero.py <video> <vaqt_s> [chiqish=hf/assets/img/thumb_hero.jpg] [scale=1.15] [y=-190]
- vaqt: spiker kameraga qarab TABASSUM qilgan, ko'zlari ochiq kadr (avval 12–16 nomzodni varaqda ko'r).
- Sarlavha (Anton) HTML'da kartaning pastki qismiga yoziladi -> yuz kartaning yuqori yarmida bo'lsin (y ni moslang:
  iyak 900 px li rasmda ~470 dan yuqori). Instagram post muqovalari past sifatli (360x640, ustida matn) — ishlatmang.
"""
import random, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from rembg import new_session, remove

video, t = sys.argv[1], float(sys.argv[2])
out = sys.argv[3] if len(sys.argv) > 3 else "hf/assets/img/thumb_hero.jpg"
S = float(sys.argv[4]) if len(sys.argv) > 4 else 1.15
Y = int(sys.argv[5]) if len(sys.argv) > 5 else -190
tmp = "analysis/thumb_src.png"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", tmp], check=True)
src = Image.open(tmp).convert("RGB")
W, H = 1600, 900
random.seed(7)
bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
for yy in range(H):
    k = yy / H
    d.line([(0, yy), (W, yy)], fill=(int(28 + 40 * k), int(18 + 18 * k), int(30 - 10 * k)))
bok = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bok)
for _ in range(55):
    r = random.randint(14, 60); x = random.randint(0, W); y = random.randint(0, int(H * 0.8))
    c = random.choice([(255, 170, 70), (255, 205, 120), (255, 120, 60), (250, 230, 180)])
    bd.ellipse((x - r, y - r, x + r, y + r), fill=c + (random.randint(50, 130),))
bg = bg.convert("RGBA"); bg.alpha_composite(bok.filter(ImageFilter.GaussianBlur(11)))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse((W / 2 - 600, -100, W / 2 + 600, 1000), fill=(255, 160, 80, 130))
bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(150)))
mask = remove(src, session=new_session("u2net_human_seg"), only_mask=True).filter(ImageFilter.GaussianBlur(1.0))
cut = src.copy(); cut.putalpha(mask)
sw, shh = src.size
cut = cut.crop((0, int(shh * 0.115), sw, int(shh * 0.74)))           # bosh + yelka (9:16 kadr uchun)
cut = cut.resize((int(cut.width * S), int(cut.height * S)), Image.LANCZOS)
sh = Image.new("RGBA", cut.size, (0, 0, 0, 0))
sh.putalpha(cut.split()[3].filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v * .6)))
x = (W - cut.width) // 2
bg.alpha_composite(sh, (x + 18, Y + 14)); bg.alpha_composite(cut, (x, Y))
ImageEnhance.Contrast(bg.convert("RGB")).enhance(1.05).save(out, quality=93)
print("ok", out)
