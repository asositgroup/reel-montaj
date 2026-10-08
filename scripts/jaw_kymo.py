"""Kimograf: iyak ustidan o'tgan tik kesma vaqt bo'ylab (x=kadr), ustida jag' chizig'i. python scripts/jaw_kymo.py <t0> <t1> <out.png>"""
import json, subprocess, sys, numpy as np, cv2
t0, t1, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
J = json.load(open("analysis/jaw.json")); F = J["fps"]; W, H = 1080, 1920
n0, n1 = int(t0 * F), int(t1 * F)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", "hf/assets/aroll.mp4", "-frames:v", str(n1 - n0), "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
ref = int(np.median(J["y"][n0:n1])); a = ref - 220; cols = []
for i in range(n0, n1):
    g = np.frombuffer(p.stdout.read(W * H), np.uint8).reshape(H, W)
    x = int(J["x"][i]); cols.append(np.median(g[a:a + 400, x - 4:x + 4], axis=1))
im = cv2.cvtColor(np.repeat(np.array(cols, np.uint8).T, 4, axis=1), cv2.COLOR_GRAY2BGR)
for k, i in enumerate(range(n0, n1)):
    cv2.circle(im, (k * 4 + 2, int(J["raw"][i] - a)), 2, (0, 0, 255), -1)
    cv2.circle(im, (k * 4 + 2, int(J["y"][i] - a)), 1, (0, 255, 0), -1)
cv2.imwrite(out, im)
