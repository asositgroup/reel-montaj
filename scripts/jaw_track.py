"""Jag' (soqol pastki cheti) kadrma-kadr: og'iz ochilib-yopilganda jag' harakatini ham ushlaydi.
Kirish: analysis/chin.json (bosh darajasidagi taxmin, chin_track.py). Chiqish: analysis/jaw.json {"fps","x","y","raw"}.
1) Har kadrda iyak x atrofidagi 100 px tasmada yorug'lik profili -> +gradient (qorong'i soqol -> yorug' bo'yin).
2) Har shot ichida vaqt bo'yicha dinamik dasturlash: sum(gradient) - LAM*|dy|, |dy| <= 10 px/kadr —
   lab chizig'iga sakrashlarni yo'qotadi, haqiqiy jag' to'lqini qoladi.
3) Gauss sigma 1.6 kadr (titrash yo'q, og'iz harakati saqlanadi). Tekshiruv: scripts/jaw_kymo.py.
python scripts/jaw_track.py"""
import json, subprocess, numpy as np
SRC, W, H = "hf/assets/aroll.mp4", 1080, 1920
UP, DN, LAM, STEP = 110, 80, 0.6, 10
SHOTS = [0.0, 8.167, 18.633, 29.233, 38.167, 45.6]
DN_SHOT = {1: 22}          # shot indeksi -> pastki chegara (yoqa chizig'i ushlanmasin)
C = json.load(open("analysis/chin.json")); FPS = C["fps"]; N = len(C["y"])
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
R = UP + DN; G = np.zeros((N, R), np.float32); A = np.zeros(N, int)
k = np.exp(-0.5 * (np.arange(-6, 7) / 2.5) ** 2); k /= k.sum()
for i in range(N):
    buf = p.stdout.read(W * H)
    if len(buf) < W * H: G[i:] = G[i - 1]; A[i:] = A[i - 1]; break
    g = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.float32)
    x, y0 = int(C["x"][i]), int(C["y"][i]); a = y0 - UP; A[i] = a
    prof = np.median(g[a - 8:a + R + 8, x - 50:x + 50], axis=1)
    d = np.gradient(np.convolve(prof, k, "same"))[8:8 + R]
    sh = max(j for j in range(len(SHOTS) - 1) if i >= round(SHOTS[j] * FPS))
    d = np.maximum(d, 0); lim = UP + DN_SHOT.get(sh, DN)
    d[lim:] = 0; G[i] = d
p.stdout.close(); p.wait()
raw = np.zeros(N); y = np.zeros(N)
for s0, s1 in zip(SHOTS, SHOTS[1:]):
    lo, hi = int(round(s0 * FPS)), min(N, int(round(s1 * FPS)))
    T = hi - lo; S = np.zeros((T, R)); B = np.zeros((T, R), int); S[0] = G[lo]
    for t in range(1, T):
        sh = A[lo + t] - A[lo + t - 1]            # oyna siljishi (absolyut y bo'yicha jarima)
        best = np.full(R, -1e9); arg = np.zeros(R, int)
        for dr in range(-STEP - abs(sh), STEP + abs(sh) + 1):
            prev = np.roll(S[t - 1], dr)            # prev[r] = S[t-1][r-dr]
            if dr > 0: prev[:dr] = -1e9
            elif dr < 0: prev[dr:] = -1e9
            dy_abs = abs(dr + sh)                   # absolyut y farqi
            if dy_abs > STEP: continue
            cand = prev - LAM * dy_abs
            m = cand > best; best[m] = cand[m]; arg[m] = (np.arange(R) - dr)[m]
        S[t] = best + G[lo + t]; B[t] = arg
    r = int(np.argmax(S[-1])); path = np.zeros(T, int)
    for t in range(T - 1, -1, -1):
        path[t] = r; r = B[t, r]
    raw[lo:hi] = A[lo:hi] + path
    ks = np.exp(-0.5 * (np.arange(-5, 6) / 1.6) ** 2); ks /= ks.sum()
    y[lo:hi] = np.convolve(np.pad(raw[lo:hi], 5, mode="edge"), ks, "same")[5:-5]
    mv = y[lo:hi] - np.array(C["y"][lo:hi])
    print(f"shot {s0:6.2f}: jag'ning boshga nisbatan harakati p5..p95 {np.percentile(mv, 5):+.0f}..{np.percentile(mv, 95):+.0f} px, "
          f"kadrlararo max {np.abs(np.diff(y[lo:hi])).max():.1f} px")
json.dump({"fps": FPS, "x": C["x"], "y": [round(v, 1) for v in y], "raw": [round(float(v), 1) for v in raw]}, open("analysis/jaw.json", "w"))
