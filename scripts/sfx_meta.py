"""hf/assets/sfx/* va nutq uchun o'lchov → analysis/sfx_meta.json

peak_at  — energiya cho'qqisi fayl boshidan (s): data-start = hodisa − peak_at
rms_db   — faol qism (cho'qqidan −20 dB gacha) RMS, dBFS
voice    — nutq faol kadrlari (50 ms) RMS medianasi, dBFS
"""
import glob, json, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 22050


def pcm(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def meta(f):
    a = pcm(f)
    env = np.sqrt(np.convolve(a * a, np.ones(441) / 441, "same"))       # 20 ms RMS konvert
    pk = int(env.argmax())
    act = env > env[pk] * 0.1                                            # cho'qqidan −20 dB gacha
    rms = np.sqrt(np.mean(a[act] ** 2)) if act.any() else 1e-9
    return {"peak_at": round(pk / SR, 3), "dur": round(len(a) / SR, 3), "rms_db": round(float(20 * np.log10(rms + 1e-9)), 1)}


if __name__ == "__main__":
    out = {"sfx": {}}
    for f in sorted(glob.glob(os.path.join(ROOT, "hf", "assets", "sfx", "*"))):
        out["sfx"][os.path.basename(f)] = meta(f)
    v = pcm(os.path.join(ROOT, "hf", "assets", "voice.wav"))
    fr = v[: len(v) // 1102 * 1102].reshape(-1, 1102)                    # 50 ms
    r = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    out["voice_rms_db"] = round(float(np.median(r[r > r.max() - 30])), 1)
    json.dump(out, open(os.path.join(ROOT, "analysis", "sfx_meta.json"), "w"), indent=1)
    print("voice", out["voice_rms_db"])
    for k, m in out["sfx"].items():
        print(f"{k:26s} peak {m['peak_at']:5.3f}  dur {m['dur']:5.2f}  rms {m['rms_db']:6.1f}")
