"""Tanlangan Pexels kliplarini yuklab, joyiga moslab tayyorlaydi → hf/assets/broll/<slot>.mp4

python scripts/broll_prep.py
split  — 1080x958 (pastki panel), full — 1080x1920. bw — oq-qora + kontrast + don (06/07/09), warm — iliq, A-roll'ga mos.
"""
import json, os, subprocess, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hf", "assets", "broll")
os.makedirs(OUT, exist_ok=True)

# slot: (nomzod indeksi, manba boshlanishi s, davomiylik s, rejim, rang)
PICK = {
    "b1_phone":  (2, 2.4, 2.6, "split", "warm"),   # qo'l telefon varaqlaydi (yuzsiz)
    "b2_vlog":   (9, 1.0, 2.6, "split", "warm"),    # kontent yaratuvchi telefonni o'rnatadi
    "b3_mentor": (0, 1.0, 2.8, "split", "warm"),   # ustoz doska oldida
}
GRADE = {
    "warm": "eq=contrast=1.06:saturation=1.08,colorbalance=rs=-0.03:bs=0.04:rh=0.04:bh=-0.03,vignette=angle=PI/5",
    "bw": "hue=s=0,eq=contrast=1.22:brightness=-0.02,noise=alls=7:allf=t,vignette=angle=PI/4.5",
}
SIZE = {"split": (1080, 958), "full": (1080, 1920)}
src_log = []
for slot, (idx, ss, dur, mode, grade, *src) in PICK.items():
    cdir = os.path.join(ROOT, "analysis", "broll", src[0] if src else slot)
    c = json.load(open(os.path.join(cdir, "cand.json")))[idx]
    raw = os.path.join(cdir, f"{c['id']}.mp4")
    if not os.path.exists(raw):
        req = urllib.request.Request(c["link"], headers={"User-Agent": "Mozilla/5.0"})
        open(raw, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    w, h = SIZE[mode]
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},"
          f"{GRADE[grade]},fps=30,format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", raw, "-vf", vf, "-an",
                    "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-g", "15",
                    os.path.join(OUT, slot + ".mp4"), "-y"], check=True)
    src_log.append(f"{slot}.mp4 — Pexels video {c['id']} ({c['page']}), {ss}–{ss + dur} s, {mode}/{grade}")
    print(slot, c["id"], f"{c['w']}x{c['h']}", "→", f"{w}x{h}")
open(os.path.join(OUT, "SOURCES.txt"), "w", encoding="utf-8").write(
    "Pexels License (tijoriy foydalanish bepul, atributsiya shart emas)\n" + "\n".join(src_log) + "\n")
