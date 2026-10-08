"""Gastro-kritik manba: 4K vertikal -> 1080x1920@60, virtual kameralar (4K crop) + iliq kino grading + jimlikda tezlik-rampa.

python scripts/build_v2.py [test]
Nutq bo'laklarida vaqt 1:1 (sinxron). Rampa faqat 16.6–22.7 s (gapsiz tatib ko'rish) — manba oralig'i o'sha, faqat ichki tezlik.
"""
import os, subprocess, sys

SRC = "/Users/user/Downloads/IMG_6089.MOV"
W0, H0 = 2160, 3840
FPS = 60
GRADE = ("curves=master='0/0 0.12/0.09 0.5/0.5 0.86/0.9 1/1',eq=saturation=1.14:contrast=1.04,"
         "colorbalance=rs=0.02:gs=0.0:bs=-0.03:rm=0.03:bm=-0.03:rh=0.03:bh=-0.04,vignette=angle=PI/4.6")
# (chiq_boshi, chiq_oxiri, manba_boshi, manba_oxiri, zoom, cx, cy)
SEGS = [
    (0.00, 6.20, 0.00, 6.20, 1.15, 0.50, 0.44),
    (6.20, 11.75, 6.20, 11.75, 1.90, 0.42, 0.57),     # makro: go'sht
    (11.75, 16.60, 11.75, 16.60, 1.30, 0.40, 0.55),
    (16.60, 18.60, 16.60, 17.60, 1.45, 0.48, 0.56),   # rampa: sekin (0.5x)
    (18.60, 20.70, 17.60, 21.70, 1.15, 0.50, 0.55),   # tez (~2x)
    (20.70, 22.70, 21.70, 22.70, 1.45, 0.46, 0.60),   # sekin (0.5x)
    (22.70, 27.585, 22.70, 27.585, 1.15, 0.52, 0.46),
]
OUT = "hf/assets/aroll.mp4"


def crop(z, cx, cy):
    w, h = int(W0 / z) // 2 * 2, int(H0 / z) // 2 * 2
    x = int(min(max(cx * W0 - w / 2, 0), W0 - w)) // 2 * 2
    y = int(min(max(cy * H0 - h / 2, 0), H0 - h)) // 2 * 2
    return f"crop={w}:{h}:{x}:{y}"


def seg(i, a, b, sa, sb, z, cx, cy):
    n = round((b - a) * FPS)
    k = (b - a) / (sb - sa)
    vf = f"trim=duration={sb - sa:.4f},setpts=(PTS-STARTPTS)*{k:.5f},fps={FPS},{crop(z, cx, cy)},scale=1080:1920:flags=lanczos,{GRADE},format=yuv420p"
    o = f"analysis/seg/s{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sa:.4f}", "-i", SRC, "-an", "-vf", vf,
                    "-fps_mode", "cfr", "-r", str(FPS), "-frames:v", str(n), "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-g", "30", o], check=True)
    return o


if __name__ == "__main__":
    os.makedirs("analysis/seg", exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.5", "-i", SRC, "-frames:v", "1", "-filter_complex",
                        f"[0]{crop(1.12, .5, .47)},scale=540:960,split[a][b];[b]{GRADE}[g];[a][g]hstack", "analysis/grade_test.jpg"], check=True)
        sys.exit()
    files = [seg(i, *s) for i, s in enumerate(SEGS)]
    open("analysis/seg/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "../../" + OUT], check=True, cwd="analysis/seg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-vn", "-ac", "2", "-ar", "48000", "-t", "27.585", "-c:a", "pcm_s16le", "analysis/voice_raw.wav"], check=True)
    print("ok", OUT)
