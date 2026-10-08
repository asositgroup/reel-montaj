"""Silliq tezlik-rampa: optik oqim (minterpolate 120 fps) + uzluksiz tezlik egri chizig'i (uchlarida 1x, o'rtada ~0.3x).
python scripts/smooth_ramp.py <out.mp4> [c=0.35]
Chiqish oralig'i = manba oralig'i (8.766-12.600), shuning uchun nutq sinxroni buzilmaydi.
f(u) = u + c*(sin(2pi u)/2pi - sin(4pi u)/4pi)  ->  f'(0)=f'(1)=1, f'(0.5)=1-2c
"""
import math, subprocess, sys
import numpy as np
FULL = "/Users/user/Downloads/IMG_6106.MP4"
T0, T1, FPS, IFPS = 8.766, 12.600, 60, 120
OUT = sys.argv[1]; C = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
GRADE = ("curves=master='0/0 0.12/0.09 0.5/0.5 0.86/0.9 1/1',eq=saturation=1.12:contrast=1.04,"
         "colorbalance=rs=0.02:bs=-0.03:rm=0.03:bm=-0.03:rh=0.03:bh=-0.04,vignette=angle=PI/4.6")
W0, H0, z, cx, cy = 1440, 2560, 1.15, 0.50, 0.62
w, h = int(W0 / z) // 2 * 2, int(H0 / z) // 2 * 2
x = int(min(max(cx * W0 - w / 2, 0), W0 - w)) // 2 * 2; y = int(min(max(cy * H0 - h / 2, 0), H0 - h)) // 2 * 2
D = T1 - T0
mid = "analysis/seg3/ramp_interp.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{T0:.4f}", "-i", FULL, "-an", "-vf",
                f"trim=duration={D + 0.2:.4f},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:out_range=tv,"
                f"minterpolate=fps={IFPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                "-c:v", "libx264", "-crf", "12", "-preset", "fast", mid], check=True)
N = round(D * FPS)
# tezlik profili: uchlarida 1x, sekin cho'qqi U0 da (kesimdan keyin — qopqoq ko'tarilishi), qolgan joyda biroz tez (o'rtacha = 1)
U0 = (float(sys.argv[3]) - T0) / D if len(sys.argv) > 3 else 0.63
uu = np.linspace(0, 1, 4001)
G = np.exp(-((uu - U0) / 0.11) ** 2); Wn = np.sin(np.pi * uu) ** 2
k = np.trapz(G, uu) / np.trapz(Wn, uu)
A = (1 - 0.3) / (G.max() - k * Wn[np.argmax(G)])
sp = 1 + A * (k * Wn - G)
F = np.concatenate([[0], np.cumsum((sp[1:] + sp[:-1]) / 2 * np.diff(uu))]); F /= F[-1]
idx = [min(round(np.interp(kk / N, uu, F) * D * IFPS), round(D * IFPS) - 1) for kk in range(N)]
print("min tezlik", round(sp.min(), 2), "max", round(sp.max(), 2))
rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", mid, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
                       "-vf", f"{GRADE},format=yuv420p", "-color_range", "tv", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-g", "30", OUT],
                      stdin=subprocess.PIPE)
fs = 1080 * 1920 * 3; cur, frame = -1, None
for i in idx:
    while cur < i:
        b = rd.stdout.read(fs)
        if len(b) < fs: break
        frame, cur = b, cur + 1
    wr.stdin.write(frame)
wr.stdin.close(); wr.wait(); rd.kill()
print("ok", OUT, N)
