"""Ovozni videodan alohida yig'ish: voice + SFX (hf/index.html audio teglaridan) + yangi bgm.
python scripts/mix_audio.py <bgm_manba> <bgm_start_s> <out.wav> [bgm_lufs=-25]
"""
import re, subprocess, sys
src, ss, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
LUFS = float(sys.argv[4]) if len(sys.argv) > 4 else -25
h = open("hf/index.html", encoding="utf-8").read()
_all = re.findall(r"<audio [^>]*>", h)
_v = [t for t in _all if 'id="voice"' in t]
assert _v, 'index.html da <audio id="voice"> topilmadi'
DUR = float(re.search(r'data-duration="([\d.]+)"', _v[0]).group(1))   # kompozitsiya davomiyligi = nutq
tags = _v + [t for t in _all if 'id="bgm"' not in t and 'id="voice"' not in t]   # a0 = voice (ducking kaliti)
ins, fl = [], []
for i, t in enumerate(tags):
    g = lambda k: re.search(k + r'="([^"]+)"', t).group(1)
    ins += ["-i", "hf/" + g("src")]
    st, d, v = float(g("data-start")), float(g("data-duration")), float(g("data-volume"))
    fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d:.3f},volume={v:.4f},adelay={int(st*1000)}:all=1[a{i}]")
n = len(tags)
# musiqa: sokin, nutq polosasida o'yiq, yumshoq ducking (kalit = voice)
ins += ["-ss", f"{ss:.2f}", "-t", f"{DUR}", "-i", src]
fl.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=60:p=2,equalizer=f=1200:t=o:w=2.2:g=-6,"
          f"afade=t=in:d=0.6,afade=t=out:st={DUR-2.2}:d=2.2,loudnorm=I={LUFS}:TP=-6:LRA=11[bg]")
fl.append("[a0]asplit=2[vo][key]")
fl.append("[key]highpass=f=300,lowpass=f=3400[k]")
fl.append("[bg][k]sidechaincompress=threshold=0.08:ratio=2.5:attack=60:release=500:makeup=1[bgd]")
fl.append("".join(f"[a{i}]" for i in range(1, n)) + f"[vo][bgd]amix=inputs={n+1}:normalize=0:duration=longest,atrim=0:{DUR}[mx]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[mx]", "-c:a", "pcm_s16le", out], check=True)
print("ok", out)
