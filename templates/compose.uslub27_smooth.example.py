"""hf/index.html — "Storis 5 000 -> 25 000", uslub-27 (M oila, @uktamjontuygunovv hujjatli intervyu) — silliq versiya.

python scripts/compose27.py   (shablon: scripts/index27.tpl.html)
Matn: chapga tekis, ikki darajali (sariq kalit so'z Outfit 700 + oq izoh Outfit 600), so'zma-so'z blur kirish.
Oq kostyum sababli bloklar pastdagi to'q stol zonasida (top ~1430+). Yuz zonasi 410-840 px — tegilmaydi.
Hamma tween references/smooth-motion.md ga mos: overshootsiz, kirish >=0.6 s expo.out, chiqish 0.5 s power2.inOut.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 55.2
SHOTS = [0, 6.68, 13.12, 22.2, 30.04, 42.96, 50.76, 55.2]
NEG = [6.68, 13.12, 22.2]                       # negativ chaqnash (silliq, opacity <= 0.5)

# B-roll (to'liq ekran, video vaqtli; ovoz davom etadi)
BROLL = [("b3_growth", 3.62, 6.56), ("b1_apps", 17.16, 19.52), ("b2_typing", 19.52, 21.70)]

# Matn bloklari: (id, boshi, oxiri, top_px, chiqish, [(qator_turi, [(so'z, t, belgi)])])
#   qator_turi: kw (sariq katta) | w (oq izoh) | num (katta oq raqam) | big (katta oq so'z) | ghost (kichik arvoh)
#   belgi: "" | "zz" (qizil zigzag) | "ring" (qizil aylana) | "y" (sariq kursiv so'z) | "q" (sariq qo'shtirnoq ichida)
B = [
    ("k0", 0.00, 3.58, 1430, "blur", [
        ("w", [("Qanday", 0.02, ""), ("qilib", 0.48, ""), ("bir", 0.82, ""), ("ekspertimda", 1.06, "")]),
        ("kw", [("Storis", 1.94, "")]),
        ("w", [("ko‘rishlari", 2.70, ""), ("sonini", 3.22, "")]),
    ]),
    ("k1", 3.64, 6.54, 1180, "blur", [
        ("w", [("5 000", 3.64, ""), ("dan", 4.20, "")]),
        ("num", [("25 000", 4.40, "ring")]),
        ("w", [("ga", 5.54, ""), ("olib", 5.66, ""), ("chiqqanman", 6.08, "")]),
    ]),
    ("k2", 6.92, 12.42, 1450, "blur", [
        ("kw", [("Birinchi", 6.98, "")]),
        ("w", [("navbatda", 7.36, "")]),
        ("w", [("auditoriya", 11.08, ""), ("tahlili", 11.92, "y")]),
    ]),
    ("k3", 12.62, 13.96, 1450, "blur", [
        ("kw", [("Ikkinchi", 12.62, "")]),
        ("w", [("navbatda", 13.30, "")]),
    ]),
    ("k4", 17.18, 21.70, 1330, "blur", [
        ("w", [("ekspertning", 17.18, ""), ("Instagram", 17.94, "")]),
        ("kw", [("Direct’iga", 18.30, "")]),
        ("w", [("kelgan", 19.10, ""), ("xabarlarni", 19.52, "")]),
        ("w", [("o‘qib", 21.00, ""), ("chiqqanman", 21.24, "")]),
    ]),
    ("k5", 21.80, 26.58, 1430, "blur", [
        ("kw", [("Auditoriya", 22.56, "")]),
        ("w", [("qaysi", 24.42, "q0"), ("muammo", 24.90, "zz"), ("bilan", 25.36, "")]),
        ("w", [("murojaat", 25.70, ""), ("qilyapti?", 26.00, "q1")]),
    ]),
    ("k6", 27.00, 30.30, 1400, "fly", [
        ("ghost", [("aynan", 27.02, ""), ("shu", 27.56, ""), ("muammolarni", 27.86, "")]),
        ("big", [("storisga", 28.56, "")]),
    ]),
    ("k7", 30.00, 32.42, 1450, "blur", [
        ("kw", [("Uchinchisi", 30.00, "")]),
        ("w", [("esa", 30.52, "")]),
    ]),
    ("k8", 32.48, 36.32, 1400, "blur", [
        ("w", [("birinchi", 32.48, ""), ("storisni", 33.16, "")]),
        ("kw", [("kuchli", 33.72, ""), ("intriga", 34.32, "")]),
        ("w", [("bilan", 35.46, ""), ("boshlash", 35.70, "")]),
    ]),
    ("k10", 42.98, 46.60, 1430, "blur", [
        ("w", [("Agar", 42.98, ""), ("sizda", 43.24, ""), ("ham", 43.60, "")]),
        ("kw", [("ko‘rishlar", 44.60, "")]),
        ("w", [("soni", 45.16, ""), ("tushib", 45.58, "zz"), ("ketgan", 45.84, ""), ("bo‘lsa", 46.18, "")]),
    ]),
    ("k11", 46.62, 49.56, 1330, "blur", [
        ("w", [("shu", 46.62, ""), ("reels", 47.20, ""), ("izohida", 47.44, "")]),
        ("kw", [("«+»", 48.02, "")]),
        ("w", [("qoldiring", 48.92, "")]),
    ]),
]

# to'q shisha plashka subtitrlari: (id, boshi, oxiri, top, [(so'z, t)])
PLATES = [
    ("p0", 13.98, 17.12, 1470, [("shunchaki", 13.98), ("keys", 14.62), ("bilan", 15.24), ("cheklanib", 15.60), ("qolmasdan,", 16.48)]),
    ("p1", 36.38, 38.46, 1470, [("bu", 36.38), ("har", 36.76), ("doim", 37.14), ("yaxshi", 37.52), ("ishlaydi", 37.86)]),
]

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.10, -19), ("sweep_small.wav", 1.94, -21),
    ("sweep_small.wav", 4.42, -19), ("sweep_small.wav", 4.95, -21),
    ("sweep_small.wav", 6.98, -21), ("sweep_small.wav", 12.64, -21),
    ("sweep_small.wav", 14.00, -20), ("sweep_small.wav", 18.32, -21),
    ("sweep_small.wav", 22.58, -21), ("sweep_small.wav", 25.00, -21),
    ("whoosh-short.mp3", 28.58, -18), ("whoosh-short.mp3", 30.02, -18),
    ("sweep_small.wav", 30.02, -21), ("sweep_small.wav", 34.34, -21), ("sweep_small.wav", 35.10, -21),
    ("sweep_small.wav", 36.40, -20), ("air_woosh.wav", 38.56, -19), ("sweep_small.wav", 40.66, -20),
    ("whoosh-short.mp3", 42.86, -18), ("sweep_small.wav", 44.62, -21), ("sweep_small.wav", 45.70, -21),
    ("select_click.wav", 48.36, -16), ("correct_tone.wav", 48.94, -19),
    ("magic_sparkle_whoosh.wav", 49.66, -20), ("sweep_small.wav", 51.90, -20),
] + [("air_woosh.wav", t, -21) for t in NEG]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


ZZ = '<svg class="zz" viewBox="0 0 120 14" preserveAspectRatio="none"><path class="draw red" pathLength="1" d="M2 9 L12 3 L22 11 L32 3 L42 11 L52 3 L62 11 L72 3 L82 11 L92 3 L102 11 L118 4"/></svg>'
RING = '<svg class="ring" viewBox="0 0 400 160" preserveAspectRatio="none"><path class="draw red" pathLength="1" d="M210 14 C320 8 392 40 388 82 C384 128 300 152 196 150 C92 148 12 124 12 80 C12 38 96 12 230 20"/></svg>'


def word_html(bid, r, j, w, mark):
    inner = esc(w)
    if mark == "q0":
        inner = '<span class="qm">“</span>' + inner
    if mark == "q1":
        inner = inner + '<span class="qm">”</span>'
    extra = ZZ if mark == "zz" else RING if mark == "ring" else ""
    cls = "w" + (" yi" if mark == "y" else "")
    return f'<span class="{cls}" id="{bid}-{r}-{j}" data-layout-allow-overlap>{inner}{extra}</span>'


def blocks_html():
    out = []
    for k, (bid, a, b, top, ex, rows) in enumerate(B):
        rs = "".join(f'<div class="r k-{kind}">' + "".join(word_html(bid, r, j, w, m) for j, (w, _, m) in enumerate(ws)) + "</div>"
                     for r, (kind, ws) in enumerate(rows))
        out.append(f'<div id="{bid}" class="clip blk" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{30 + k}" '
                   f'style="top:{top}px"><div class="blk-in">{rs}</div></div>')
    return "\n      ".join(out)


def plates_html():
    return "\n      ".join(
        f'<div id="{pid}" class="clip plate" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{50 + k}" style="top:{top}px">'
        f'<div class="pl-bg"></div><div class="pl-t">' + " ".join(f'<span class="w" id="{pid}-{j}">{esc(w)}</span>' for j, (w, _) in enumerate(ws)) +
        '</div></div>' for k, (pid, a, b, top, ws) in enumerate(PLATES))


def broll_html():
    return "\n      ".join(
        f'<video id="{s}" class="clip broll" src="assets/broll/{s}.mp4" data-start="{a:.3f}" data-duration="{b - a:.3f}" '
        f'data-track-index="{3 + k}" muted playsinline></video>' for k, (s, a, b) in enumerate(BROLL))


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX_EVENTS, key=lambda e: e[1])):
        m = meta["sfx"][f]
        st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{70 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def W_in(sel, t, kind):
    if kind in ("big", "num"):   # "Shunaqa" turi: gorizontal motion-blur + scale 0.7 -> 1 (overshootsiz)
        return (f'tl.fromTo("{sel}",{{opacity:0,scaleX:1.35,scaleY:0.8,x:-60,filter:"blur(18px)"}},'
                f'{{opacity:1,scaleX:1,scaleY:1,x:0,filter:"blur(0px)",duration:0.75,ease:"expo.out"}},{t - 0.1:.3f});')
    if kind == "kw":
        return (f'tl.fromTo("{sel}",{{opacity:0,x:-28,filter:"blur(12px)"}},'
                f'{{opacity:1,x:0,filter:"blur(0px)",duration:0.65,ease:"expo.out"}},{t - 0.08:.3f});')
    return (f'tl.fromTo("{sel}",{{opacity:0,y:14,filter:"blur(10px)"}},'
            f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},{t - 0.08:.3f});')


def timeline_js():
    js = []
    # kamera: kadrlar navbat bilan 1.0 <-> 1.06 sekin drift (kesimda miqyos sakramaydi)
    for i in range(len(SHOTS) - 1):
        a, b = SHOTS[i], SHOTS[i + 1]
        z0, z1 = (1.0, 1.06) if i % 2 == 0 else (1.06, 1.0)
        js.append(f'tl.fromTo("#cam",{{scale:{z0}}},{{scale:{z1},duration:{b - a - 0.004:.3f},ease:"sine.inOut",immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
    for t in NEG:
        js.append(f'tl.fromTo("#neg",{{opacity:0}},{{opacity:0.45,duration:0.3,ease:"sine.inOut",immediateRender:false}},{t - 0.3:.3f});')
        js.append(f'tl.to("#neg",{{opacity:0,duration:0.45,ease:"sine.inOut"}},{t:.3f});')
    for bid, a, b, top, ex, rows in B:
        for r, (kind, ws) in enumerate(rows):
            for j, (w, t, m) in enumerate(ws):
                sel = f"#{bid}-{r}-{j}"
                js.append(W_in(sel, max(a + 0.02, t), kind))
                if m == "zz":
                    js.append(f'tl.fromTo("{sel} .draw",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.5,ease:"power2.inOut"}},{t + 0.25:.3f});')
                if m == "ring":
                    js.append(f'tl.fromTo("{sel} .draw",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.8,ease:"power2.inOut"}},{t + 0.55:.3f});')
            if kind == "big":   # sekin kattalashish 1 -> 1.08
                js.append(f'tl.to("#{bid}-{r}-0",{{scale:1.08,duration:{b - t - 0.6:.3f},ease:"sine.inOut"}},{t + 0.66:.3f});')
        if ex == "fly":     # burilib, KESIMDAN O'TIB uchib ketadi (silliq)
            js.append(f'tl.to("#{bid} .blk-in",{{rotation:18,x:160,y:240,opacity:0,filter:"blur(10px)",duration:0.62,ease:"power2.inOut"}},{b - 0.62:.3f});')
        else:
            js.append(f'tl.to("#{bid} .blk-in",{{opacity:0,y:-16,filter:"blur(8px)",duration:0.5,ease:"power2.inOut"}},{b - 0.5:.3f});')
    for pid, a, b, top, ws in PLATES:
        js.append(f'tl.fromTo("#{pid} .pl-bg",{{scaleX:0.3,opacity:0,filter:"blur(8px)"}},{{scaleX:1,opacity:1,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},{a - 0.1:.3f});')
        for j, (w, t) in enumerate(ws):
            js.append(W_in(f"#{pid}-{j}", max(a + 0.08, t), "w"))
        js.append(f'tl.to("#{pid} > *",{{opacity:0,y:-12,filter:"blur(8px)",duration:0.5,ease:"power2.inOut"}},{b - 0.5:.3f});')
    return "\n      ".join(js)


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index27.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{BLOCKS}}", blocks_html()).replace("{{PLATES}}", plates_html()).replace("{{BROLL}}", broll_html())
            .replace("{{AUDIO}}", audio_html()).replace("{{TIMELINE}}", timeline_js()).replace("{{DUR}}", str(DUR)))
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
