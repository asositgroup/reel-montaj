"""Asl fayldan montaj manbasi: virtual kameralar + grading + SINXRON ovoz.

Loyiha ildizida edit.json:
{
  "source": "C:/Users/axihub/Downloads/C8953.MP4",      # ASL kamera fayli (birlashtirilgan emas!)
  "fps": 25,                                             # ixtiyoriy: manba fps (render = fps*2)
  "parts":  [[32.4, 45.0], [101.0, 113.5]],             # asl fayldagi oraliqlar (s); bo'lmasa [[0, <dur>]]
  "shots":  [[0.0, 3.62, 1.0], [3.62, 9.32, 1.35]]      # GLOBAL vaqt (qismlar ketma-ket), zoom (1.0 keng … 1.8 yaqin)
}

python prep.py heads   → analysis/heads.json (har qismda bosh markazi, manba pikselida)
python prep.py test    → analysis/grade_test.jpg (xom / grading, har qism)
python prep.py build   → hf/assets/aroll.mp4 (1080x1920@30), analysis/voice_raw.wav, analysis/shots.json

Har SHOT asl fayldan tasvir+ovoz BIRGA kesiladi → sinxron kafolatlangan. Shot chegaralarini jimlik
joylariga qo'y (transkriptdagi so'zlar orasi). Manba vertikal (9:16) deb hisoblanadi.
"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.getcwd()
CFG = json.load(open(os.path.join(ROOT, "edit.json"), encoding="utf-8"))
O = CFG["source"]
FPS = CFG.get("fps", 30)          # proxy fps; render = FPS*2 (silliqlik)
GRADE = CFG.get("grade", "curves=master='0/0 0.22/0.17 0.5/0.52 0.78/0.83 1/1',eq=saturation=1.28,"
                "colorbalance=rs=-0.03:bs=0.05:rm=0.03:bm=-0.02:rh=0.05:gh=0.01:bh=-0.05,vignette=angle=PI/5.5")


def probe():
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                                   "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", O],
                                  capture_output=True, text=True).stdout)
    s = j["streams"][0]; w, h = s["width"], s["height"]
    rot = next((abs(int(float(d.get("rotation", 0)))) for d in s.get("side_data_list", []) if "rotation" in d), 0)
    if rot in (90, 270):
        w, h = h, w
    return w, h, float(j["format"]["duration"])


SW, SH, SDUR = probe()
PARTS = CFG.get("parts") or [[0.0, SDUR]]
OFF = np.cumsum([0] + [b - a for a, b in PARTS])


def r30(t):
    return round(t * FPS) / FPS


def part_of(t):
    return max(k for k in range(len(PARTS)) if OFF[k] <= t + 1e-6)


def frame(t, w=540, h=960, vf=""):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", O, "-frames:v", "1", "-vf",
                          f"scale={w}:{h}" + (f",{vf}" if vf else ""), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3)


def heads():
    from PIL import Image
    from rembg import new_session, remove
    sess = new_session("u2net_human_seg"); out = []
    for k, (a, b) in enumerate(PARTS):
        bx = []
        for t in np.linspace(a + 0.8, b - 0.3, 4):
            m = np.asarray(remove(Image.fromarray(frame(t)), session=sess, only_mask=True)) > 128
            top = np.where(m.sum(1) > 4)[0][0]
            xs = np.where(m[top:top + 90].any(0))[0]
            bx.append((xs.min(), top, xs.max()))
        bx = np.array(bx); s = SW / 540
        cx = (bx[:, 0].mean() + bx[:, 2].mean()) / 2 * s; top = bx[:, 1].min() * s; hw = (bx[:, 2] - bx[:, 0]).mean() * s
        out.append({"part": k + 1, "head_cx": round(float(cx)), "head_top": round(float(top)), "head_w": round(float(hw)),
                    "face_y": round(float(top + 0.66 * hw))})
        print(out[-1])
    json.dump(out, open(os.path.join(ROOT, "analysis", "heads.json"), "w"), indent=1)


def levels(k):
    a, b = PARTS[k]
    im = frame((a + b) / 2).astype(float) / 255
    lo = np.percentile(im, 0.8, axis=(0, 1)) - 0.01
    hi = np.minimum(np.percentile(im, 99.6, axis=(0, 1)) + 0.01, 1)
    return (f"colorlevels=rimin={lo[0]:.3f}:gimin={lo[1]:.3f}:bimin={lo[2]:.3f}:"
            f"rimax={hi[0]:.3f}:gimax={hi[1]:.3f}:bimax={hi[2]:.3f}")


def crop(z, k, H_):
    W, H = SW / z, SH / z
    hd = H_[k]; cx = hd["head_cx"]; fy = hd["face_y"]
    x = min(max(cx - W / 2, 0), SW - W)
    y = min(max(fy - 0.36 * H, 0), SH - H) if z > 1 else 0
    return int(W) // 2 * 2, int(H) // 2 * 2, int(x) // 2 * 2, int(y) // 2 * 2


def test():
    from PIL import Image
    s = Image.new("RGB", (270 * len(PARTS), 960))
    for k, (a, b) in enumerate(PARTS):
        s.paste(Image.fromarray(frame((a + b) / 2, 270, 480)), (270 * k, 0))
        s.paste(Image.fromarray(frame((a + b) / 2, 270, 480, f"{levels(k)},{GRADE}")), (270 * k, 480))
    s.save(os.path.join(ROOT, "analysis", "grade_test.jpg"), quality=88)
    print("analysis/grade_test.jpg (tepada xom, pastda grading)")


def build():
    H_ = json.load(open(os.path.join(ROOT, "analysis", "heads.json")))
    lv = [levels(k) for k in range(len(PARTS))]
    tmp = os.path.join(ROOT, "analysis", "shots"); os.makedirs(tmp, exist_ok=True)
    os.makedirs(os.path.join(ROOT, "hf", "assets"), exist_ok=True)
    meta, vl, al = [], [], []
    for i, (g0, g1, z) in enumerate(CFG["shots"]):
        g0, g1 = r30(g0), r30(g1); k = part_of(g0)
        src = PARTS[k][0] + (g0 - OFF[k]); dur = g1 - g0
        W, H, x, y = crop(z, k, H_)
        vf = f"crop={W}:{H}:{x}:{y},scale=1080:1920:flags=lanczos,format=rgb24,{lv[k]},{GRADE},fps={FPS},format=yuv420p"
        v = os.path.join(tmp, f"s{i:02d}.mp4"); a = os.path.join(tmp, f"s{i:02d}.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{src:.4f}", "-i", O, "-t", f"{dur + 0.25:.4f}", "-vf", vf,  # -t aniq bo'lsa oxirgi kadr yo'qoladi -> sinxron siljiydi
                        "-frames:v", str(round(dur * FPS)), "-an", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                        "-g", str(FPS), v, "-y"], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{src:.4f}", "-i", O, "-t", f"{dur:.4f}", "-vn", "-ac", "2",
                        "-ar", "48000", "-af", f"apad,atrim=0:{dur:.6f}", "-c:a", "pcm_s16le", a, "-y"], check=True)
        meta.append({"shot": i, "t0": g0, "t1": g1, "zoom": z, "part": k + 1, "src": round(src, 4)})
        vl.append(v); al.append(a)
        print(f"shot {i}: {g0:6.2f}-{g1:6.2f} z={z} qism {k + 1} src {src:.2f}")
    for lst, name, out in ((vl, "v.txt", os.path.join(ROOT, "hf", "assets", "aroll.mp4")),
                           (al, "a.txt", os.path.join(ROOT, "analysis", "voice_raw.wav"))):
        open(os.path.join(tmp, name), "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
        subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", name, "-c", "copy", out, "-y"], check=True, cwd=tmp)
    json.dump(meta, open(os.path.join(ROOT, "analysis", "shots.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "analysis"), exist_ok=True)
    {"heads": heads, "test": test, "build": build}[sys.argv[1] if len(sys.argv) > 1 else "build"]()
