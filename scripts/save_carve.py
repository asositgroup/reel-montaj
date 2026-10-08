"""carve.mjs natijasini saqlash: hf/index.html dagi <audio id="bgm"> (data-fx-carve bilan) → scripts/bgm_carved.html.
compose.py uni har qayta yig'ishda qo'yadi (aks holda carve yo'qoladi). Loyiha ildizidan: python scripts/save_carve.py"""
import re, sys
h = open("hf/index.html", encoding="utf-8").read()
m = re.search(r'<audio id="bgm".*?</audio>', h, re.S)
if not m or "data-fx-carve" not in m.group(0):
    sys.exit("carve topilmadi — avval: cd hf && node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed bgm --voice voice")
open("scripts/bgm_carved.html", "w", encoding="utf-8").write(m.group(0))
print("carve saqlandi: scripts/bgm_carved.html")
