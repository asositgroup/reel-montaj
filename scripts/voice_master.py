"""Nutqni ijtimoiy tarmoq darajasiga olib chiqish (-15 LUFS). Kirish balandligi o'lchanadi — past ham, tayyor manba ham ishlaydi.

python scripts/voice_master.py   → hf/assets/voice.wav (asl nusxa analysis/voice_raw.wav)
"""
import json, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "analysis", "voice_raw.wav")
CLEAN = os.path.join(ROOT, "analysis", "voice_raw_clean.wav")   # wind_clean.py natijasi (bo'lsa)
OUT = os.path.join(ROOT, "hf", "assets", "voice.wav")
if not os.path.exists(RAW):
    shutil.copy(OUT, RAW)

SRC = CLEAN if os.path.exists(CLEAN) else RAW

# Kirish balandligiga qarab kuchaytirish: past lav-ovoz (-37 LUFS) -> +20 dB, tayyor/masterlangan manba (-13 LUFS) -> 0 dB.
# (Qat'iy +20 dB masterlangan manbani ezib yuborardi — Storis 5k->25k, 2026-10-05.)
_m = subprocess.run(["ffmpeg", "-hide_banner", "-i", SRC, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
IN_I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", _m)[-1])
GAIN = max(0.0, min(24.0, -17.0 - IN_I))
print(f"kirish {IN_I:.1f} LUFS -> oldindan kuchaytirish {GAIN:+.1f} dB")

PRE = ("pan=mono|c0=0.5*c0+0.5*c1,highpass=f=85:p=2,"
       "equalizer=f=250:t=q:w=1.1:g=-2,equalizer=f=3200:t=q:w=1.0:g=2.5,highshelf=f=8000:g=1.5,"
       f"deesser=i=0.25:m=0.5:f=0.3,volume={GAIN:.1f}dB,"
       "acompressor=threshold=-24dB:ratio=2.5:attack=10:release=160:makeup=2,alimiter=limit=0.9:attack=5:release=60")
T = "I=-15:TP=-1.5:LRA=9"
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", SRC, "-af", f"{PRE},loudnorm={T}:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", m, re.S).group(0))
ln = (f"loudnorm={T}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-af", f"{PRE},{ln},volume=-2dB,aresample=48000,pan=stereo|c0=c0|c1=c0",
                "-c:a", "pcm_s16le", OUT, "-y"], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", OUT, "-af", "ebur128=peak=true", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
print("natija:", " | ".join(l.strip() for l in r.split("Summary:")[-1].splitlines() if re.match(r"\s*(I:|LRA:|Peak:)", l)))
