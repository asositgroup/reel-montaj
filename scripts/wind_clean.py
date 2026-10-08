"""Shamol (past chastotali g'uvillash) ni nutqqa tegmasdan olib tashlash — faqat nol-fazali filtrlar (kechikish 0, lip-sync saqlanadi).
1) 110 Hz dan past: 8-tartibli nol-fazali highpass (sosfiltfilt) — shamol 60–140 Hz da, spiker ovozi asosan 140 Hz dan yuqori.
2) 110–300 Hz: faqat PAUZALARDA -12 dB (kalit = 300–3400 Hz nutq energiyasi, attack 10 ms / release 180 ms);
   gapirganda to'liq ochiq. 300 Hz dan yuqori signal o'zgarmaydi (x - low = aynan asl).
python scripts/wind_clean.py  -> analysis/voice_raw_clean.wav (voice_master shu faylni ishlatadi)"""
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
IN, OUT = "analysis/voice_raw.wav", "analysis/voice_raw_clean.wav"
x, sr = sf.read(IN, always_2d=True); x = x.astype(np.float64)
hp = butter(4, 110, "highpass", fs=sr, output="sos")
lp = butter(4, 300, "lowpass", fs=sr, output="sos")
bp = butter(4, [300, 3400], "bandpass", fs=sr, output="sos")
mono = x.mean(1)
key = sosfiltfilt(bp, mono) ** 2
hop = int(sr * 0.005); env = np.sqrt(np.convolve(key, np.ones(hop * 4) / (hop * 4), "same"))[::hop]
db = 20 * np.log10(env + 1e-9)
thr = np.percentile(db, 30) + 3                     # pauza/nutq chegarasi (o'lchangan)
g_target = np.where(db > thr, 0.0, -12.0)           # dB
a_att, a_rel = np.exp(-hop / (sr * 0.010)), np.exp(-hop / (sr * 0.180))
g = np.zeros_like(g_target); cur = -12.0
for i, t in enumerate(g_target):                    # ochilish tez, yopilish sekin
    a = a_att if t > cur else a_rel
    cur = a * cur + (1 - a) * t; g[i] = cur
# nol-faza uchun oldinga-orqaga: ochilishni nutqdan 10 ms oldin boshlaydi
g2 = np.zeros_like(g); cur = -12.0
for i in range(len(g_target) - 1, -1, -1):
    a = a_att if g_target[i] > cur else a_rel
    cur = a * cur + (1 - a) * g_target[i]; g2[i] = cur
gain_db = np.maximum(g, g2)
gain = 10 ** (np.interp(np.arange(len(mono)), np.arange(len(gain_db)) * hop, gain_db) / 20)
y = np.empty_like(x)
for c in range(x.shape[1]):
    h = sosfiltfilt(hp, x[:, c])
    low = sosfiltfilt(lp, h)
    y[:, c] = (h - low) + low * gain
sf.write(OUT, y.astype(np.float32), sr, subtype="FLOAT")
print(f"yozildi {OUT}; pauza ulushi {np.mean(g_target < 0) * 100:.0f}%")
