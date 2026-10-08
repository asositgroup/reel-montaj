"""Pexels'dan B-roll nomzodlari (video) → analysis/broll/<slot>/cand.json + kontakt-varaq.

python scripts/broll_search.py
Kalit: remotion-teaser/.env PEXELS_API_KEY. Pexels License — tijoriy bepul, atributsiya shart emas.
"""
import io, json, os, re, urllib.parse, urllib.request
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = re.search(r"PEXELS_API_KEY=\"?([^\"\r\n]+)", open(os.path.join(ROOT, "..", "remotion-teaser", ".env")).read()).group(1)
BAN = re.compile(r"christmas|xmas|santa|tree|halloween|wine|beer|alcohol|church|cross|bikini|party", re.I)

SLOTS = {
    "s1_gift": ["hands giving gift box", "offering dates plate hands", "hands giving gift"],
    "s2_crowd": ["crowd walking city serious", "busy street people walking", "people commuting city"],
    "s3_greet": ["friends greeting handshake street", "young men handshake smile", "friends hug greeting"],
    "s4_frown": ["serious man face close up", "frowning man portrait", "sad man face"],
    "s5_smile": ["people smiling greeting", "man smiling handshake", "friends laughing together"],
}


def get(url):
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read()


import sys
if len(sys.argv) > 2:  # python broll_search.py <slot> "so'rov1" "so'rov2" ...
    SLOTS = {sys.argv[1]: sys.argv[2:]}
for slot, queries in SLOTS.items():
    d = os.path.join(ROOT, "analysis", "broll", slot)
    os.makedirs(d, exist_ok=True)
    seen, cands = set(), []
    for q in queries:
        j = json.loads(get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
            {"query": q, "per_page": 8, "size": "medium"})))
        for v in j.get("videos", []):
            txt = v.get("url", "")
            if v["id"] in seen or BAN.search(txt) or v["duration"] < 3:
                continue
            seen.add(v["id"])
            files = sorted([f for f in v["video_files"] if f.get("height") and f["file_type"] == "video/mp4"],
                           key=lambda f: -(f["height"] * f["width"]))
            best = next((f for f in files if max(f["width"], f["height"]) <= 2160), files[-1] if files else None)
            if best:
                cands.append({"id": v["id"], "q": q, "page": txt, "dur": v["duration"], "w": best["width"],
                              "h": best["height"], "link": best["link"], "thumb": v["image"]})
    cands = cands[:10]
    json.dump(cands, open(os.path.join(d, "cand.json"), "w"), indent=1)
    W, H = 240, 300
    sheet = Image.new("RGB", (W * 5, H * 2), "#111")
    for i, c in enumerate(cands):
        im = Image.open(io.BytesIO(get(c["thumb"]))).convert("RGB")
        im.thumbnail((W, H - 30))
        sheet.paste(im, ((i % 5) * W, (i // 5) * H))
        ImageDraw.Draw(sheet).text(((i % 5) * W + 4, (i // 5) * H + H - 26),
                                   f"{i}: {c['id']} {c['w']}x{c['h']} {c['dur']}s", fill="yellow")
    sheet.save(os.path.join(d, "sheet.jpg"), quality=85)
    print(slot, len(cands))
