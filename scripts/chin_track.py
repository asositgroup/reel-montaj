"""Jag' (iyak) kuzatuvi: har shot uchun yuz shablonini kadrma-kadr qidiradi -> analysis/chin.json
python scripts/chin_track.py   (SHOTS: [t0, t1, ref_kadr, yuz_cx, iyak_y] — iyak_y ref kadrda, 1080x1920)
Natija: {"fps":30, "x":[...], "y":[...]} — har kadr uchun iyak nuqtasi (silliqlangan)."""
import cv2, json, subprocess, numpy as np
SRC = "hf/assets/aroll.mp4"; FPS = 30
SHOTS = [(0.0, 8.167, 100, 500, 820), (8.167, 18.633, 400, 540, 852), (18.633, 29.233, 700, 580, 940),
         (29.233, 38.167, 1000, 540, 848), (38.167, 45.6, 1250, 520, 860)]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-vf", "scale=540:960", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 960, 540); S = 2
X, Y, C = np.zeros(len(V)), np.zeros(len(V)), np.zeros(len(V))
for t0, t1, rf, cx, cy in SHOTS:
    x0, y0 = (cx - 150) // S, (cy - 330) // S; w, h = 300 // S, 310 // S
    T = V[rf][y0:y0 + h, x0:x0 + w]
    for i in range(int(round(t0 * FPS)), min(len(V), int(round(t1 * FPS)))):
        a, b = max(0, x0 - 60), max(0, y0 - 60)
        r = cv2.matchTemplate(V[i][b:y0 + h + 60, a:x0 + w + 60], T, cv2.TM_CCOEFF_NORMED)
        _, m, _, p = cv2.minMaxLoc(r)
        X[i] = cx + (p[0] + a - x0) * S; Y[i] = cy + (p[1] + b - y0) * S; C[i] = m
# silliqlash: har shot ichida markazlashgan Gauss (sigma 3 kadr) — titrashsiz, lekin kechikishsiz
def smooth(v, lo, hi, s=3.0):
    k = np.exp(-0.5 * (np.arange(-9, 10) / s) ** 2); k /= k.sum()
    seg = np.pad(v[lo:hi], 9, mode="edge"); v[lo:hi] = np.convolve(seg, k, "same")[9:-9]
for t0, t1, *_ in SHOTS:
    lo, hi = int(round(t0 * FPS)), min(len(V), int(round(t1 * FPS)))
    smooth(X, lo, hi); smooth(Y, lo, hi)
    print(f"shot {t0:5.2f}-{t1:5.2f}: y {Y[lo:hi].min():.0f}..{Y[lo:hi].max():.0f}  x {X[lo:hi].min():.0f}..{X[lo:hi].max():.0f}  conf min {C[lo:hi].min():.2f}")
json.dump({"fps": FPS, "x": [round(v, 1) for v in X], "y": [round(v, 1) for v in Y]}, open("analysis/chin.json", "w"))
