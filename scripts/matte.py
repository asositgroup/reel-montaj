"""Spiker kesmasi (hukda matn bosh ORTIDA turishi uchun) + har klipda bosh qutisi.

python scripts/matte.py
  hf/assets/subject_hook.webm   — 0..HOOK_END s, VP9 yuva420p (fon shaffof)
  analysis/headbox.json         — klip bo'yicha bosh qutisi (1080x1920 koordinatada)
"""
import json, os, subprocess
import numpy as np
from PIL import Image
from rembg import new_session, remove

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "hf", "assets", "aroll.mp4")
W, H = 1080, 1920
FPS = round(eval(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hf', 'assets', 'aroll.mp4')], capture_output=True, text=True).stdout.strip() or '30'))
HOOK_END = 5.5
CUTS = [0, 5.3266, 7.7290, 13.7350, 18.7400, 24.7460, 32.03]
session = new_session("u2net_human_seg")


def read(n0, n1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"select=between(n\\,{n0}\\,{n1})",
                          "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def read1(n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{n / FPS:.4f}", "-i", SRC, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3)


def mask(rgb):
    m = remove(Image.fromarray(rgb).resize((540, 960), Image.BILINEAR), session=session, only_mask=True)
    m = np.asarray(m.resize((W, H), Image.BILINEAR), np.float32) / 255
    return np.clip((m - 0.12) / 0.76, 0, 1)


def headbox(m):
    """Yuqoridan skan: kenglik bosh kengligining 2x idan oshgan qator = yelka."""
    rows = np.where((m > 0.5).sum(1) > 8)[0]
    if len(rows) == 0:
        return None
    top = rows[0]
    widths = [(m[y] > 0.5).sum() for y in range(top, min(H, top + 700))]
    headw = np.median(widths[20:120]) if len(widths) > 120 else max(widths)
    sh = next((i for i, w in enumerate(widths[60:], 60) if w > 2.0 * headw), len(widths) - 1)
    ys = slice(top, top + sh)
    xs = np.where((m[ys] > 0.5).any(0))[0]
    return [int(xs.min()), int(top), int(xs.max()), int(top + sh)]


def matte_range(t0, t1, name):
    """[t0,t1) oraliq uchun spiker kesmasi -> hf/assets/<name>.webm (media-start 0 = t0).
    Xotira tejamkor: niqoblar 540x960 uint8 da saqlanadi, kadrlar bittadan o'qiladi."""
    n0, n1 = round(t0 * FPS), round(t1 * FPS)
    small = []
    for n in range(n0, n1):
        rgb = read1(n)
        m = remove(Image.fromarray(rgb).resize((540, 960), Image.BILINEAR), session=session, only_mask=True)
        small.append(np.asarray(m, np.uint8))
    d = os.path.join(ROOT, "analysis", "matte_" + name)
    os.makedirs(d, exist_ok=True)
    for i in range(len(small)):
        a = (0.25 * small[max(0, i - 1)].astype(np.float32) + 0.5 * small[i] + 0.25 * small[min(len(small) - 1, i + 1)]) / 255
        a = np.clip((a - 0.12) / 0.76, 0, 1)
        al = Image.fromarray((a * 255 + .5).astype(np.uint8)).resize((W, H), Image.BILINEAR)
        rgb = read1(n0 + i)
        im = Image.fromarray(rgb).convert("RGBA"); im.putalpha(al); im.save(f"{d}/{i:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-framerate", str(FPS), "-i", f"{d}/%04d.png", "-c:v", "libvpx-vp9",
                    "-pix_fmt", "yuva420p", "-b:v", "6M", "-auto-alt-ref", "0", "-g", "30", "-threads", "2",
                    os.path.join(ROOT, "hf", "assets", name + ".webm"), "-y"], check=True)
    print(name, "matte:", n0, "..", n1 - 1, flush=True)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:  # python matte.py <t0> <t1> <nom>
        matte_range(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
        raise SystemExit
    # 1) hook kesmasi
    n1 = round(HOOK_END * FPS)
    rgb = read(0, n1 - 1)
    ms = [mask(f) for f in rgb]
    d = os.path.join(ROOT, "analysis", "matte")
    os.makedirs(d, exist_ok=True)
    for i in range(len(ms)):
        a = 0.25 * ms[max(0, i - 1)] + 0.5 * ms[i] + 0.25 * ms[min(len(ms) - 1, i + 1)]
        Image.fromarray(np.dstack([rgb[i], (a * 255 + .5).astype(np.uint8)]), "RGBA").save(f"{d}/{i:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-framerate", str(FPS), "-i", f"{d}/%04d.png", "-c:v", "libvpx-vp9",
                    "-pix_fmt", "yuva420p", "-b:v", "6M", "-auto-alt-ref", "0", "-g", "30", "-threads", "2",
                    os.path.join(ROOT, "hf", "assets", "subject_hook.webm"), "-y"], check=True)
    print("hook matte:", len(ms), "kadr", flush=True)

    # 2) har klipda 5 kadrdan bosh qutisi (birlashma)
    boxes = []
    for c in range(6):
        t0, t1 = CUTS[c], CUTS[c + 1]
        bs = []
        for t in np.linspace(t0 + .2, t1 - .2, 5):
            n = round(t * FPS)
            b = headbox(mask(read(n, n)[0]))
            if b: bs.append(b)
        bs = np.array(bs)
        box = [int(bs[:, 0].min()), int(bs[:, 1].min()), int(bs[:, 2].max()), int(bs[:, 3].max())]
        boxes.append({"clip": c + 1, "t0": t0, "t1": t1, "head": box})
        print(c + 1, box, flush=True)
    json.dump(boxes, open(os.path.join(ROOT, "analysis", "headbox.json"), "w"), indent=1)
