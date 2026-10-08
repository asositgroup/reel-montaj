"""hf/index.html — "Ucan Visa" v2 (45.6 s, render 50 fps). So'z vaqtlari analysis/tr2_uz.json (sinxron ovoz).
Yangi uslublar: 11 (plashka, bob raqami, liquid-fill, zoom-out ritm), 12 (skotch yorliqlar + burst), 13 (rangli kartalar,
flash-blur), 14 (3D karusel, 3D brend nishoni), 15 (doimiy sarlavha, logotip plitkalari, CTA), 16 (3D-stiker harflar).
Silliqlik: references/smooth-motion.md. python scripts/compose.py
"""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 45.6
SHOTS = [(0.0, 8.167), (8.167, 18.633), (18.633, 29.233), (29.233, 38.167), (38.167, 45.6)]

CAPS = [
    (5.62, 7.15, "talabalarni ta’lim olishga", ""),
    (7.18, 8.10, "yuborib kelmoqda.", ""),
    (8.30, 9.30, "Shu vaqt davomida biz", "low"),
    (18.66, 19.95, "Endi esa,", "bot"),
    (20.96, 22.45, "tajribalarimizga asoslanib,", "bot"),
    (26.18, 26.84, "Shu sababli,", ""),
    (32.04, 33.45, "maqsadlarida borayotgan bo‘lsangiz,", "bot"),
    (33.54, 35.40, "va sizga viza xizmati kerak bo‘lsa,", ""),
]

# (id, start, end, rows); row = (klass, [(so'z, vaqt, qo'shimcha_klass)])
HEADS = [
    ("h-hook", 2.30, 5.60, [
        ("thin", [("Buyuk", 2.38, ""), ("Britaniyaning", 2.92, "")]),
        ("heavy", [("eng", 3.42, ""), ("nufuzli", 3.64, "g")]),
        ("boldit", [("universitetlariga", 4.02, "")]),
    ]),
    ("h-final", 38.20, 41.32, [
        ("thin", [("Ucan", 38.10, ""), ("Consulting", 38.44, "")]),
        ("heavy", [("10", 39.54, "num"), ("yillik", 39.72, "")]),
        ("boldit", [("tajriba", 40.10, "g"), ("ortida.", 40.44, "")]),
    ]),
]

FLASH = [8.167, 29.233, 38.167]
STICK = "TAYYOR"

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.30, -12), ("impact-bass-1.mp3", 1.28, -8), ("sweep_small.wav", 1.62, -16),
    ("click-soft.mp3", 2.38, -14), ("click-soft.mp3", 3.42, -14), ("click-soft.mp3", 4.02, -15),
    ("riser.mp3", 9.30, -17), ("impact-bass-1.mp3", 10.62, -8), ("sparkle.mp3", 10.9, -18),
    ("pop.mp3", 11.26, -14), ("correct_tone.wav", 13.08, -16),
    ("whoosh-short.mp3", 14.95, -14), ("whoosh-short.mp3", 15.85, -15), ("whoosh-short.mp3", 16.70, -15),
    ("sweep_small.wav", 14.85, -16), ("long_pop.wav", 17.66, -14), ("long_pop.wav", 18.06, -15),
    ("long_pop.wav", 18.46, -15), ("long_pop.wav", 18.86, -16), ("air_woosh.wav", 21.2, -17),
    ("hard_pop_click.wav", 22.54, -11), ("hard_pop_click.wav", 23.06, -11), ("hard_pop_click.wav", 23.76, -11),
    ("impact-bass-2.mp3", 24.56, -8), ("hard_pop_click.wav", 25.22, -12), ("air_woosh.wav", 25.9, -17),
    ("whoosh_deep_impact.wav", 26.92, -11), ("magic_sparkle_whoosh.wav", 27.78, -15), ("ping.mp3", 28.34, -13),
    ("whoosh.mp3", 28.95, -15),
    ("whoosh-short.mp3", 30.00, -13), ("whoosh-short.mp3", 30.76, -13), ("whoosh-short.mp3", 31.60, -13),
    ("select_click.wav", 35.52, -14), ("select_click.wav", 37.12, -14), ("select_click.wav", 37.24, -15),
    ("select_click.wav", 37.36, -15), ("impact-bass-1.mp3", 37.42, -9),
    ("click-soft.mp3", 38.30, -15), ("impact-bass-1.mp3", 39.54, -10),
    ("explainer_pop_whoosh.wav", 41.70, -13), ("select_click.wav", 43.12, -10), ("notification.mp3", 43.26, -15),
] + [("whoosh_fast_transition.wav", t, -11) for t in FLASH] + [("camera_shutter.wav", t + 0.01, -10) for t in FLASH]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def caps_html():
    return "\n      ".join(
        f'<div id="cap{i}" class="clip cap {p}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="20">'
        f'<div class="cap-in">{esc(t)}</div></div>' for i, (a, b, t, p) in enumerate(CAPS))


def heads_html():
    out = []
    for hid, a, b, rows in HEADS:
        rr = "".join(f'<div class="row {k}">' + "".join(f'<span class="w {c}" id="{hid}-{r}-{j}">{esc(w)}</span>'
                                                         for j, (w, _, c) in enumerate(ws)) + "</div>" for r, (k, ws) in enumerate(rows))
        out.append(f'<div id="{hid}" class="clip head" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="30">'
                   f'<div class="head-in">{rr}</div></div>')
    return "\n      ".join(out)


def people_html():
    ppl = json.load(open(os.path.join(ROOT, "analysis", "people.json"), encoding="utf-8"))
    return "".join(f'<div class="pc" id="pc{i}"><img src="assets/people/{p["file"]}" alt="" /><div class="pn">{esc(p["name"])}</div></div>'
                   for i, p in enumerate(ppl))


def logos_html():
    lg = [l for l in json.load(open(os.path.join(ROOT, "analysis", "logos.json"))) if not l["src"].startswith("visa")]
    rows, i = [], 0
    for n in (4, 3, 3, 3):
        rows.append(lg[i:i + n]); i += n
    return "".join('<div class="lrow">' + "".join(f'<div class="lt {l["tile"]}"><img src="assets/logos/{l["file"]}" alt="" /></div>' for l in row)
                   + "</div>" for row in rows if row)


def burst_path(n=14, ro=250, ri=150, ry=0.5):
    pts = []
    for k in range(2 * n):
        r = ro if k % 2 == 0 else ri * (1 + 0.12 * ((k * 7) % 3 - 1))
        a = math.pi * k / n
        pts.append(f"{r * math.cos(a):.1f},{r * math.sin(a) * ry:.1f}")
    return "M" + " L".join(pts) + " Z"


def stick_html():
    return "".join(f'<span id="sk{i}">{c}</span>' for i, c in enumerate(STICK))


def fx_html():
    return "\n      ".join(
        f'<div id="flash{i}" class="fx" data-composition-id="editorial-flash-overlay" data-composition-src="compositions/editorial-flash-overlay.html" '
        f'data-start="{t - .398:.3f}" data-duration="0.6" data-width="1080" data-height="1920" data-track-index="{40 + i}"></div>' for i, t in enumerate(FLASH))


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>',
           f'<audio id="bgm" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="0.34"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX_EVENTS, key=lambda e: e[1])):
        m = meta["sfx"][f]; st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" data-track-index="{60 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def timeline_js():
    js = []
    for hid, a, b, rows in HEADS:
        for r, (k, ws) in enumerate(rows):
            for j, (w, t, c) in enumerate(ws):
                big = k == "heavy" or c == "num"
                d, sc = (0.75, ",scale:1.06") if big else (0.62, "")
                js.append(f'tl.fromTo("#{hid}-{r}-{j}",{{opacity:0,y:40,filter:"blur(12px)"{sc}}},'
                          f'{{opacity:1,y:0,filter:"blur(0px)"{",scale:1" if big else ""},duration:{d},ease:"expo.out"}},{max(a, t - 0.08):.3f});')
        js.append(f'OUT("#{hid} .row",{b - 0.46:.3f},{{stagger:0.03}});')
    for i, (a, b, t, p) in enumerate(CAPS):
        js.append(f'tl.fromTo("#cap{i} .cap-in",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.2,ease:"power2.out"}},{a:.3f});')
        js.append(f'tl.to("#cap{i} .cap-in",{{opacity:0,duration:0.18,ease:"power2.in"}},{b - 0.19:.3f});')
    # 11/13/15 ritm: har kesim 1.32x dan zoom-out, keyin sekin push
    for i, (a, b) in enumerate(SHOTS):
        js.append(f'tl.fromTo("#cam",{{scale:1.32}},{{scale:1.0,duration:1.2,ease:"expo.out",immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
        js.append(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.04,duration:{b - a - 1.204:.3f},ease:"sine.inOut",immediateRender:false}},{a + 1.202:.3f});')
    # 13: flash-blur kesimlar
    for t in FLASH:
        js.append(f'tl.fromTo("#cam",{{filter:"blur(18px) brightness(1.5)"}},{{filter:"blur(0px) brightness(1)",duration:0.55,ease:"power2.out",immediateRender:false}},{t:.3f});')
    return "\n      ".join(js)


def carved_bgm():
    f = os.path.join(ROOT, "scripts", "bgm_carved.html")
    return open(f, encoding="utf-8").read() if os.path.exists(f) else None


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{CAPS}}", caps_html()).replace("{{HEADS}}", heads_html()).replace("{{PEOPLE}}", people_html())
            .replace("{{LOGOS}}", logos_html()).replace("{{FX}}", fx_html()).replace("{{AUDIO}}", audio_html())
            .replace("{{BURST}}", burst_path()).replace("{{STICK}}", stick_html())
            .replace("{{TIMELINE}}", timeline_js()).replace("{{DUR}}", str(DUR)))
    keep = carved_bgm()
    if keep:
        html = re.sub(r'<audio id="bgm".*?</audio>', lambda _: keep, html, count=1, flags=re.S)
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
