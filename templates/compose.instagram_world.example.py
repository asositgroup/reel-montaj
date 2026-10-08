"""hf/index.html — "Storis 5 000 -> 25 000", INSTAGRAM DUNYOSI uslubi (v9).

python scripts/compose_ig.py
Butun video Instagram ichida: storis ramkasi (progress-bar + header), IG matn stikerlari, "ko'rishlar" paneli, qadam-kartalar
(savol stikeri uslubi), Direct chat (spiker dumaloq PiP), savol qutisi, 3D storis-karusel, izohlar oynasi, Direct'da sovg'a.
Bo'limlar orasida storis KUB o'tishi (ketayotgan yuz = muzlatilgan kadr, kelayotgan = jonli video -> sinxron buzilmaydi).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 55.2
SEG = [0, 6.68, 13.12, 22.2, 30.04, 42.96, DUR]          # storislar (progress-bar segmentlari) = kamera kesimlari
CUBE = [6.68, 13.12, 22.2, 30.04, 42.96]

# IG matn stikerlari: (id, kirish, chiqish, top, burchak, [(matn, uslub, vaqt)])  uslub: blk | wht | grad | red
STK = [
    ("s1", 0.02, 3.56, 1040, -3, [("Qanday qilib", "blk", 0.02), ("bir ekspertimda", "wht", 0.82), ("storis ko‘rishlarini", "grad", 1.94)]),
    ("s2", 10.40, 12.56, 1080, 2, [("ya’ni", "blk", 10.40), ("auditoriya tahlili", "wht", 11.08)]),
    ("s3", 15.56, 17.10, 1080, -2, [("keys bilan cheklanib", "blk", 15.60), ("qolmasdan", "wht", 16.48)]),
    ("s4", 26.60, 29.98, 1060, -3, [("aynan shu muammolarni", "blk", 27.02), ("storisga", "grad", 28.56)]),
    ("s5", 32.48, 36.32, 1040, -2, [("birinchi storisni", "wht", 32.48), ("kuchli intriga", "grad", 33.72), ("huk bilan boshlash", "blk", 35.08)]),
    ("s6", 36.38, 38.44, 1100, 2, [("bu har doim", "blk", 36.38), ("yaxshi ishlaydi ✓", "wht", 37.52)]),
    ("s7", 42.98, 46.58, 1040, -3, [("agar sizda ham", "blk", 42.98), ("ko‘rishlar soni", "wht", 44.60), ("tushib ketgan bo‘lsa 📉", "red", 45.58)]),
    ("s8", 20.96, 21.62, 1180, -2, [("hammasini o‘qib chiqdim", "wht", 21.00)]),
]
# qadam kartalari (IG savol-stikeri uslubi): (id, kirish, chiqish, top, sarlavha, matn, emoji)
STEPS = [("q1", 6.96, 10.36, 1060, "1-QADAM", "Keyslar va natijalar", "📊"),
         ("q2", 13.16, 15.50, 1060, "2-QADAM", "Direct’ni o‘qing", "📩"),
         ("q3", 30.08, 32.44, 1060, "3-QADAM", "Kuchli huk", "🪝")]

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.10, -20), ("click-soft.mp3", 0.04, -15), ("click-soft.mp3", 0.84, -15), ("click-soft.mp3", 1.96, -15),
    ("sweep_small.wav", 3.66, -17), ("correct_tone.wav", 6.02, -19),
    ("click-soft.mp3", 6.98, -15), ("click-soft.mp3", 10.42, -16), ("click-soft.mp3", 11.10, -16), ("click-soft.mp3", 13.18, -15),
    ("click-soft.mp3", 15.62, -16), ("click-soft.mp3", 16.50, -16),
    ("sweep_small.wav", 17.20, -17), ("ping.mp3", 18.32, -17), ("ping.mp3", 19.12, -17), ("ping.mp3", 19.92, -17),
    ("click-soft.mp3", 21.02, -16), ("sweep_small.wav", 21.62, -18),
    ("long_pop.wav", 22.56, -17), ("click-soft.mp3", 27.04, -16), ("click-soft.mp3", 28.58, -14),
    ("click-soft.mp3", 30.10, -15), ("click-soft.mp3", 32.50, -16), ("click-soft.mp3", 33.74, -15), ("click-soft.mp3", 35.10, -16),
    ("click-soft.mp3", 36.40, -16), ("click-soft.mp3", 37.54, -16), ("sweep_small.wav", 38.52, -17),
    ("sweep_small.wav", 40.66, -18), ("sweep_small.wav", 41.24, -18),
    ("click-soft.mp3", 43.00, -16), ("click-soft.mp3", 44.62, -16), ("error.mp3", 45.62, -22),
    ("sweep_small.wav", 46.64, -17), ("select_click.wav", 48.90, -15), ("pop.mp3", 49.02, -16),
    ("sweep_small.wav", 49.64, -17), ("notification.mp3", 50.30, -17), ("correct_tone.wav", 54.36, -19),
] + [("whoosh-short.mp3", t, -18) for t in CUBE] + [("key-press.mp3", 24.90 + i * 0.13, -16 - (i % 3)) for i in range(9)] \
  + [("key-press.mp3", 48.02, -14)]

VER = ('<svg class="ver" viewBox="0 0 24 24"><path d="M12 1.6l2.6 1.9 3.2-.1 1 3 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3-3.2-.1L12 22.4l-2.6-1.9-3.2.1-1-3-2.6-1.9 1-3.1-1-3.1 2.6-1.9 1-3 3.2.1z" fill="#3897f0"/>'
       '<path d="M7.6 12.3l3 3 5.8-6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
EYE = ('<svg viewBox="0 0 24 24"><path d="M12 5C6.5 5 2.7 9.4 1.6 12c1.1 2.6 4.9 7 10.4 7s9.3-4.4 10.4-7C21.3 9.4 17.5 5 12 5z" fill="none" stroke="#fff" stroke-width="1.8"/>'
       '<circle cx="12" cy="12" r="3.6" fill="none" stroke="#fff" stroke-width="1.8"/></svg>')
HEART = ('<svg viewBox="0 0 24 24"><path d="M12 21.3 10.6 20C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.6 11.5L12 21.3z"/></svg>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def stickers_html():
    out = []
    for k, (sid, a, b, top, rot, lines) in enumerate(STK):
        ls = "".join(f'<span class="ln {st}" id="{sid}-{j}">{esc(t)}</span>' for j, (t, st, _) in enumerate(lines))
        out.append(f'<div id="{sid}" class="clip stk" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{40 + k}" '
                   f'style="top:{top}px"><div class="stk-in" style="transform:rotate({rot}deg)">{ls}</div></div>')
    return "\n      ".join(out)


def steps_html():
    return "\n      ".join(
        f'<div id="{qid}" class="clip step" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{50 + k}" style="top:{top}px">'
        f'<div class="st-in"><div class="st-h"><img src="assets/img/ig_avatar.jpg" alt="" /><span>{esc(h)}</span></div>'
        f'<div class="st-b"><span class="st-e">{em}</span>{esc(t)}</div></div></div>'
        for k, (qid, a, b, top, h, t, em) in enumerate(STEPS))


def cube_html():
    return "\n      ".join(
        f'<img id="cb{k}" class="clip cubeface" src="assets/img/cube/c_{t}.jpg" data-start="{t:.3f}" data-duration="0.52" data-track-index="{5 + k}" alt="" />'
        for k, t in enumerate(CUBE))


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX_EVENTS, key=lambda e: e[1])):
        m = meta["sfx"][f]
        st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{80 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def timeline_js():
    js = []
    # progress-barlar: har storis o'z segmentida to'ladi
    for i in range(len(SEG) - 1):
        a, b = SEG[i], SEG[i + 1]
        js.append(f'tl.fromTo("#pb{i}",{{scaleX:0}},{{scaleX:1,duration:{b - a:.3f},ease:"none"}},{a:.3f});')
    # kub o'tishi: ketayotgan yuz (muzlatilgan kadr) chap tomonga buriladi, jonli sahna o'ngdan kiradi
    for k, t in enumerate(CUBE):
        js.append(f'tl.fromTo("#cb{k}",{{rotationY:0,x:0,transformOrigin:"100% 50%"}},{{rotationY:-90,x:-1080,duration:0.5,ease:"power2.inOut"}},{t:.3f});')
        js.append(f'tl.fromTo("#cam",{{rotationY:90,x:1080,transformOrigin:"0% 50%"}},{{rotationY:0,x:0,duration:0.5,ease:"power2.inOut",immediateRender:false}},{t:.3f});')
    # stikerlar: har qator "pop" (overshootsiz), qator vaqtida
    for sid, a, b, top, rot, lines in STK:
        for j, (t, st, tt) in enumerate(lines):
            js.append(f'tl.fromTo("#{sid}-{j}",{{opacity:0,scale:0.86,y:24,filter:"blur(8px)"}},{{opacity:1,scale:1,y:0,filter:"blur(0px)",duration:0.32,ease:"power3.out"}},{max(a, tt - 0.06):.3f});')
        js.append(f'tl.to("#{sid} .stk-in",{{opacity:0,scale:0.94,filter:"blur(6px)",duration:0.25,ease:"power2.in"}},{b - 0.25:.3f});')
    for qid, a, b, top, h, t, em in STEPS:
        js.append(f'tl.fromTo("#{qid} .st-in",{{opacity:0,scale:0.8,y:40,filter:"blur(10px)"}},{{opacity:1,scale:1,y:0,filter:"blur(0px)",duration:0.45,ease:"power3.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#{qid} .st-e",{{scale:0.6,rotation:-20}},{{scale:1,rotation:0,duration:0.5,ease:"power3.out"}},{a + 0.12:.3f});')
        js.append(f'tl.to("#{qid} .st-in",{{opacity:0,scale:0.92,filter:"blur(6px)",duration:0.26,ease:"power2.in"}},{b - 0.26:.3f});')
    return "\n      ".join(js)


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index_ig.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{STICKERS}}", stickers_html()).replace("{{STEPS}}", steps_html()).replace("{{CUBE}}", cube_html())
            .replace("{{AUDIO}}", audio_html()).replace("{{TIMELINE}}", timeline_js()).replace("{{DUR}}", str(DUR))
            .replace("{{VER}}", VER).replace("{{EYE}}", EYE).replace("{{HEART}}", HEART))
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
