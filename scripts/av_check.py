"""Tayyor renderda sinxronni o'lchash (loyiha ildizidan):
python scripts/av_check.py hf/renders/<final>.mp4 [t1 t2 ...]

OVOZ: finaldagi nutq analysis/voice_raw.wav ga nisbatan (5 oynada) — hammasi bir xil bo'lishi kerak (AAC ~+8 ms normal).
TASVIR: final kadri hf/assets/aroll.mp4 dagi qaysi kadrga mos — spiker TO'LIQ ko'rinadigan, grafikasiz vaqtlarni ber
(split/B-roll/blur paytida o'lchov ishonchsiz). 0 ms kutiladi.
"""
import subprocess, sys
import numpy as np
F = sys.argv[1]
TS = [float(x) for x in sys.argv[2:]] or None


def aud(p, sr=8000):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                        capture_output=True).stdout, np.float32).astype(float)


def vid(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "scale=64:114,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 114, 64).astype(np.float32)


e = lambda a: np.convolve(np.abs(a), np.ones(40) / 40, "same")
Fa, Va = e(aud(F)), e(aud("analysis/voice_raw.wav"))
dur = min(len(Fa), len(Va)) / 8000
print("OVOZ (final vs voice_raw):")
for a in np.linspace(0.5, dur - 4, 5):
    s0, s1 = int(a * 8000), int((a + 3) * 8000); x = Va[s0:s1] - Va[s0:s1].mean()
    l = max(((np.dot(x, Fa[s0 + k:s1 + k] - Fa[s0 + k:s1 + k].mean()), k) for k in range(-400, 401, 2)))[1]
    print(f"  {a:5.1f}s: {l / 8:+6.1f} ms")
def fps(p):
    a, b = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", p],
                          capture_output=True, text=True).stdout.strip().split("/")
    return float(a) / float(b)


A, G = vid("hf/assets/aroll.mp4"), vid(F)
fa, fg = fps("hf/assets/aroll.mp4"), fps(F)   # render fps manba x2 bo'lishi mumkin
n = lambda x: (x - x.mean()) / (x.std() + 1e-6)
print("TASVIR (final vs aroll):")
for t in TS or np.linspace(1, len(G) / fg - 1, 6):
    g = int(round(t * fg)); i = int(round(t * fa)); js = range(max(0, i - 6), min(len(A), i + 7))
    d = [np.mean(np.abs(n(G[g][8:60, 10:54]) - n(A[j][8:60, 10:54]))) for j in js]
    print(f"  {t:5.1f}s: {(list(js)[int(np.argmin(d))] - i) * 1000 / fa:+6.1f} ms")
