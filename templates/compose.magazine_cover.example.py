"""hf/index.html — "Jurnal muqovasi" (marketing haqida selfi-reel).

python scripts/compose_v3.py
Spiker butun video davomida kesib olingan (subject_full.webm) — orqasida har bo'lim uchun ulkan Anton so'z (jurnal muqovasi).
Old qatlam: iqtibos, vaqt chizig'i (yillar -> tezlik), xarita kartasi (ko'rimsiz vs gavjum joy), so'z chiplari, kengayish to'lqinlari,
"BILMAYDI." qorong'ilik lahzasi, subtitrlar. B-roll: Pexels (yuzsiz). Hamma tween silliq (overshootsiz).
"""
import json, os
from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 62.85
INK, ACC = "#151412", "#d9531e"
# ulkan so'zlar: (id, matn, boshi, oxiri, rang)
WORDS = [("w0", "ZO‘R?", 0.00, 3.30, INK), ("w1", "YILLAR", 3.30, 15.45, INK), ("w2", "TEZLIK", 15.45, 20.15, ACC),
         ("w3", "JOY", 22.60, 33.75, INK), ("w4", "KO‘RINING", 38.35, 43.25, INK), ("w5", "MARKETING", 43.25, 52.20, INK),
         ("w6", "BILMAYDI.", 52.20, 54.25, ACC), ("w7", "TIRIKCHILIK", 54.25, DUR, INK)]
CAPS = [(3.38, 6.80, "Bu gapga qo‘shilaman — uzoq vaqt"), (6.92, 10.20, "bozorda bo‘lsangiz, xizmat ko‘rsatsangiz,"),
        (10.28, 12.20, "kerakli mijozlarni yig‘asiz —"), (12.28, 15.40, "ular yillar davomida kelaveradi."),
        (15.54, 20.04, "Marketingning vazifasi — shu jarayonni tezlashtirish."),
        (28.44, 33.70, "Bu sizga tezroq mijoz yig‘ishga yordam beradi."),
        (33.82, 38.30, "O‘zingizni reklama qilsangiz, ko‘rsatsangiz…"), (40.46, 43.12, "jarayon yana ham tezlashadi."),
        (43.32, 47.10, "Biznesni kengaytirmoqchi bo‘lsangiz —"), (47.24, 52.16, "marketing qiling. Mahsulotingiz eng zo‘r bo‘lsa ham."),
        (52.22, 54.20, "Chunki odamlar bu haqda bilmaydi.")]
BROLL = [("r1_shop", 7.00, 9.60, "full", ""), ("r2_empty", 20.20, 22.60, "full", "KO‘RIMSIZ JOY"),
         ("r3_busy", 23.90, 26.30, "full", "GAVJUM JOY"), ("r5_grow", 45.40, 47.50, "full", "")]
SPLIT = ("r4_ads", 33.85, 38.40)
SFX = [("whoosh_deep_impact.wav", 0.10, -22), ("sweep_small.wav", 3.32, -21), ("whoosh-short.mp3", 15.47, -19), ("sweep_small.wav", 7.00, -22),
       ("camera_shutter.wav", 20.20, -22), ("camera_shutter.wav", 23.90, -22), ("sweep_small.wav", 26.40, -21), ("sweep_small.wav", 33.80, -20),
       ("click-soft.mp3", 38.50, -18), ("click-soft.mp3", 38.75, -18), ("click-soft.mp3", 39.00, -18), ("sweep_small.wav", 43.30, -21),
       ("camera_shutter.wav", 45.40, -22), ("whoosh_deep_impact.wav", 52.20, -19), ("air_woosh.wav", 54.30, -21)]

_F = ImageFont.truetype(os.path.join(ROOT, "hf", "assets", "fonts", "Anton.ttf"), 100)


def fit(t, width=1000, cap=520):
    return min(cap, int(100 * width / _F.getlength(t)))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def words_html():
    return "\n        ".join(
        f'<div id="{i}" class="clip bw" data-layout-allow-overlap data-layout-allow-occlusion data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{2 + k}" '
        f'style="font-size:{fit(t)}px;color:{c}"><span class="bwi" data-layout-allow-overlap data-layout-allow-occlusion>{esc(t)}</span></div>' for k, (i, t, a, b, c) in enumerate(WORDS))


def caps_html():
    return "\n      ".join(
        f'<div id="cap{k}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{40 + k}"><span>{esc(t)}</span></div>'
        for k, (a, b, t) in enumerate(CAPS))


def broll_html():
    out = []
    for k, (s, a, b, mode, lab) in enumerate(BROLL):
        out.append(f'<div id="br{k}" class="brw">'
                   f'<video id="brv{k}" class="clip" src="assets/broll/{s}.mp4" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{25 + k}" muted playsinline></video>'
                   + (f'<div class="brl caps">{esc(lab)}</div>' if lab else "") + '</div>')
    s, a, b = SPLIT
    out.append(f'<div id="split" class="split"><video id="spv" class="clip" src="assets/broll/{s}.mp4" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="30" muted playsinline></video></div>')
    out.append(f'<div id="divd" class="clip divider" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="31"><div class="div-in"></div></div>')
    return "\n      ".join(out)


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX, key=lambda e: e[1])):
        m = meta["sfx"][f]; st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" data-track-index="{70 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def timeline_js():
    js = []
    seg = [0, 7.0, 9.6, 20.2, 22.6, 23.9, 26.3, 33.85, 38.4, 45.4, 47.5, 52.2, 54.25, DUR]
    for i in range(len(seg) - 1):   # kamera: kadrlar navbat bilan sekin yaqinlashadi/uzoqlashadi
        a, b = seg[i], seg[i + 1]; z0, z1 = (1.0, 1.06) if i % 2 == 0 else (1.06, 1.0)
        js.append(f'tl.fromTo("#cam",{{scale:{z0}}},{{scale:{z1},duration:{b - a - 0.004:.3f},ease:"sine.inOut",immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
    for k, (i, t, a, b, c) in enumerate(WORDS):   # so'z bosh ortidan yuqoriga ko'tariladi, chiqishda yuqoriga ketadi
        js.append(f'tl.fromTo("#{i} .bwi",{{yPercent:60,opacity:0,filter:"blur(14px)"}},{{yPercent:0,opacity:1,filter:"blur(0px)",duration:0.9,ease:"expo.out"}},{a + 0.02:.3f});')
        js.append(f'tl.fromTo("#{i} .bwi",{{scale:1}},{{scale:1.05,duration:{max(0.5, b - a - 1.0):.3f},ease:"sine.inOut",immediateRender:false}},{a + 0.9:.3f});')
        if b < DUR - 0.1:
            js.append(f'tl.to("#{i} .bwi",{{yPercent:-40,opacity:0,filter:"blur(12px)",duration:0.5,ease:"power2.inOut"}},{b - 0.5:.3f});')
    for k, (a, b, t) in enumerate(CAPS):
        js.append(f'tl.fromTo("#cap{k} span",{{opacity:0,y:16,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{a - 0.06:.3f});')
        js.append(f'tl.to("#cap{k} span",{{opacity:0,filter:"blur(6px)",duration:0.35,ease:"power2.inOut"}},{b - 0.35:.3f});')
    for k, (s, a, b, mode, lab) in enumerate(BROLL):
        js.append(f'tl.fromTo("#br{k}",{{clipPath:"inset(50% 0% 50% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"expo.out"}},{a:.3f});')
        js.append(f'tl.to("#br{k}",{{clipPath:"inset(0% 0% 100% 0%)",duration:0.4,ease:"power2.inOut"}},{b - 0.4:.3f});')
        if lab:
            js.append(f'tl.fromTo("#br{k} .brl",{{opacity:0,y:20,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.55,ease:"expo.out"}},{a + 0.25:.3f});')
    s, a, b = SPLIT
    js.append(f'split({a:.3f},{b:.3f});')
    return "\n      ".join(js)


HTML = open(os.path.join(ROOT, "scripts", "index_v3.tpl.html"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "scripts", "index_v3.tpl.html")) else ""

if __name__ == "__main__":
    html = (HTML.replace("{{DUR}}", str(DUR)).replace("{{WORDS}}", words_html()).replace("{{CAPS}}", caps_html())
            .replace("{{BROLL}}", broll_html()).replace("{{AUDIO}}", audio_html()).replace("{{TIMELINE}}", timeline_js())
            .replace("{{ACC}}", ACC).replace("{{INK}}", INK))
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html))
