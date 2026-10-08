"""Yangi reel loyihasi: python ~/.claude/skills/reel-montaj/scripts/new_project.py <slug> "<Mavzu nomi>"

→ AbuDev/reel-<slug>/ {scripts/, analysis/, hf/ (HyperFrames), edit.json}
→ MY - Videos/<Mavzu nomi>/ {1_manba, 2_montajlar, 3_tayyor, README.txt}
"""
import json, os, shutil, subprocess, sys
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HOME = os.path.expanduser("~")
# Windows: OneDrive/Ishchi stol; Mac: Desktop/AI-Videos (birinchisi mavjud bo'lgani olinadi)
_DESK = next((d for d in (os.path.join(_HOME, "OneDrive", "Ishchi stol"), os.path.join(_HOME, "Desktop", "AI-Videos"))
              if os.path.isdir(os.path.join(d, "AbuDev"))), os.path.join(_HOME, "OneDrive", "Ishchi stol"))
ABU = os.environ.get("ABUDEV_DIR", os.path.join(_DESK, "AbuDev"))
MYV = os.environ.get("MYVIDEOS_DIR", os.path.join(_DESK, "MY - Videos"))
slug, title = sys.argv[1], sys.argv[2]
P = os.path.join(ABU, f"reel-{slug}")
os.makedirs(os.path.join(P, "analysis"), exist_ok=True)
subprocess.run(f'npx --yes hyperframes init hf --non-interactive --example=blank --skill=general-video', shell=True, cwd=P, check=True)
shutil.copytree(os.path.join(SK, "scripts"), os.path.join(P, "scripts"), dirs_exist_ok=True)
for f in os.listdir(os.path.join(SK, "templates")):   # hamma andozalar (A, ucanvisa v2/v3, storis_smooth)
    shutil.copy(os.path.join(SK, "templates", f), os.path.join(P, "scripts", f))
for d in ("fonts", "sfx", "emoji", "vendor"):   # vendor = lokal gsap.min.js (CDN uzilsa render yiqilmasin)
    shutil.copytree(os.path.join(SK, "assets", d), os.path.join(P, "hf", "assets", d), dirs_exist_ok=True)
shutil.copytree(os.path.join(SK, "assets", "compositions"), os.path.join(P, "hf", "compositions"), dirs_exist_ok=True)
json.dump({"source": "", "parts": [], "shots": []}, open(os.path.join(P, "edit.json"), "w"), indent=1)
M = os.path.join(MYV, title)
for d in ("1_manba", "2_montajlar", "3_tayyor"):
    os.makedirs(os.path.join(M, d), exist_ok=True)
open(os.path.join(M, "README.txt"), "w", encoding="utf-8").write(
    f"{title}\n\n1_manba/  asl fayllar\n2_montajlar/  oraliq versiyalar\n3_tayyor/  joylashga tayyor fayl\n\nMontaj loyihasi: AbuDev/reel-{slug}/\n")
print("tayyor:", P, "|", M)
