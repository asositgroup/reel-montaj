"""hf/index.html — "Ucan Visa" v3 (45.6 s, render 50 fps). So'z vaqtlari analysis/tr2_uz.json, jag' analysis/chin.json.
Asos: v1 (kesimlar, musiqa, pasport muhri). Motion grafikalar 11–16 namunalaridan:
13 gradient plashka + flash-blur + bloom kartalar + avatar CTA, 11/12/13 jag' ostidagi matn, 11 liquid-fill + invert chaqnash,
14 3D nishon, 15 doimiy sarlavha + plitkalar, 12 planshet sahnasi, 16 yoy matn + 3D stiker.
"Vau" (o'lchovli): portretlar halqasi spiker atrofida (matte bilan tanasi ortidan o'tadi), light leak.
python scripts/compose.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 45.6
SHOTS = [(0.0, 8.167), (8.167, 18.633), (18.633, 29.233), (29.233, 38.167), (38.167, 45.6)]

# pastki subtitr — faqat logo sahnasida (jag' plitkalar ostida qoladi)
CAPS = [
    (18.66, 19.20, "Endi esa,"),
]

# jag' ostidagi matn: (id, start, end, rows); row = (klass, [(so'z, vaqt[, qo'shimcha klass])])
CHIN = [
    ("c-hook", 2.30, 5.45, [
        ("thin", [("Buyuk", 2.38), ("Britaniyaning", 2.92)]),
        ("heavy", [("eng", 3.42), ("nufuzli", 3.64, "g")]),
        ("boldit", [("universitetlariga", 4.02)]),
    ]),
    ("c-tal", 5.40, 8.12, [
        ("sm", [("talabalarni", 5.48)]),
        ("big", [("ta’lim", 5.66), ("olishga", 6.08, "g")]),
        ("it", [("yuborib", 6.54), ("kelmoqda.", 7.58)]),
    ]),
    ("c-shu", 8.20, 9.40, [
        ("big", [("Shu", 8.18), ("vaqt", 8.30), ("davomida", 8.58), ("biz", 9.06, "g")]),
    ]),
    ("c-tajr", 19.72, 22.38, [
        ("sm", [("10", 19.80), ("yil", 19.86), ("davomida", 20.04)]),
        ("big", [("to‘plangan", 20.46)]),
        ("boldit", [("tajribalarimizga", 20.96, "g"), ("asoslanib,", 21.72)]),
    ]),
    ("c-sabab", 26.10, 26.95, [
        ("big", [("Shu", 26.18), ("sababli,", 26.38, "g")]),
    ]),
    ("c-maq", 31.95, 33.50, [
        ("sm", [("maqsadlarida", 32.04)]),
        ("big", [("borayotgan", 32.56), ("bo‘lsangiz,", 32.92)]),
    ]),
    ("c-viza", 33.45, 35.40, [
        ("sm", [("va", 33.54), ("sizga", 33.88)]),
        ("big", [("viza", 34.10, "mark"), ("xizmati", 34.56)]),
        ("it", [("kerak", 34.88), ("bo‘lsa,", 35.16)]),
    ]),
    ("c-fin", 38.20, 41.32, [
        ("serif", [("Ucan", 38.10), ("Consulting", 38.44)]),
        ("anton", [("10", 39.54, "big10"), ("yillik", 39.72)]),
        ("serif", [("tajriba", 40.10, "g"), ("ortida.", 40.44)]),
    ]),
    ("c-endi", 41.36, 42.95, [
        ("sm", [("endi", 41.40)]),
        ("heavy", [("Ucan", 41.76), ("Visa", 42.60, "g")]),
    ]),
]

# 12: planshet matni — har so'z harflari tasodifiy tartibda "bosiladi"
BOARD = [("B_ALOHIDA", "ALOHIDA", 22.60), ("B_YONALISH", "YO‘NALISH", 23.12), ("B_SIFATIDA", "SIFATIDA", 23.40),
         ("B_VIZA", "VIZA XIZMATLARI", 23.82), ("B_YOLGA", "YO‘LGA QO‘YDIK", 25.28)]

FLASH = [8.167, 22.42, 26.08, 29.233, 38.167, 42.96]
LEAK = [27.30]
STICK = "TAYYOR"
ARC = "BUYUK BRITANIYA VIZASI"

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.10, -13), ("impact-bass-1.mp3", 1.28, -8), ("sweep_small.wav", 1.62, -16),
    ("click-soft.mp3", 2.38, -15), ("click-soft.mp3", 3.42, -15), ("click-soft.mp3", 4.02, -16),
    ("glitch-2.mp3", 9.36, -17), ("impact-bass-1.mp3", 9.37, -8), ("impact-bass-2.mp3", 10.62, -11), ("sparkle.mp3", 10.9, -19),
    ("pop.mp3", 11.26, -14), ("correct_tone.wav", 13.08, -16),
    ("riser.mp3", 14.30, -19), ("whoosh_deep_impact.wav", 14.86, -12), ("whoosh-short.mp3", 15.86, -14), ("whoosh-short.mp3", 16.60, -14),
    ("air_woosh.wav", 17.30, -16), ("long_pop.wav", 17.66, -14), ("long_pop.wav", 18.06, -15),
    ("long_pop.wav", 18.46, -15), ("long_pop.wav", 18.86, -16), ("air_woosh.wav", 19.10, -17),
    ("key-press.mp3", 22.62, -15), ("key-press.mp3", 23.14, -15), ("key-press.mp3", 23.42, -16), ("key-press.mp3", 23.84, -15),
    ("whoosh_fast_transition.wav", 24.54, -13), ("impact-bass-2.mp3", 24.58, -11), ("sweep_small.wav", 24.66, -16),
    ("key-press.mp3", 25.30, -15), ("select_click.wav", 25.82, -15),
    ("whoosh_deep_impact.wav", 26.92, -11), ("magic_sparkle_whoosh.wav", 27.78, -15), ("ping.mp3", 28.34, -13),
    ("whoosh.mp3", 28.95, -15),
    ("whoosh-short.mp3", 30.00, -13), ("whoosh-short.mp3", 30.76, -13), ("whoosh-short.mp3", 31.60, -13),
    ("sparkle.mp3", 35.48, -19), ("whoosh-short.mp3", 35.46, -15), ("impact-bass-1.mp3", 36.26, -7), ("hard_pop_click.wav", 36.27, -11),
    ("select_click.wav", 37.12, -14), ("select_click.wav", 37.24, -15), ("select_click.wav", 37.36, -15), ("impact-bass-1.mp3", 37.42, -10),
    ("click-soft.mp3", 38.30, -15), ("impact-bass-1.mp3", 39.54, -10), ("click-soft.mp3", 41.78, -15),
    ("explainer_pop_whoosh.wav", 43.06, -14), ("select_click.wav", 44.28, -10), ("notification.mp3", 44.40, -15),
] + [("whoosh_fast_transition.wav", t, -12) for t in FLASH if t not in (22.42, 42.96)] \
  + [("camera_shutter.wav", t + 0.01, -11) for t in FLASH]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def caps_html():
    return "\n      ".join(
        f'<div id="cap{i}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="20">'
        f'<div class="cap-in">{esc(t)}</div></div>' for i, (a, b, t) in enumerate(CAPS))


def chin_html():
    out = []
    for cid, a, b, rows in CHIN:
        rr = "".join(f'<div class="row {k}">' + "".join(f'<span class="w {(w[2] if len(w) > 2 else "")}"{" data-layout-allow-overlap" if cid == "c-fin" else ""} id="{cid}-{r}-{j}">{esc(w[0])}</span>'
                                                         for j, w in enumerate(ws)) + "</div>" for r, (k, ws) in enumerate(rows))
        out.append(f'<div id="{cid}" class="clip chin" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{6 + len(out) % 2}">'
                   f'<div class="chin-in">{rr}</div></div>')
    return "\n        ".join(out)


def ring_html(side):
    ppl = json.load(open(os.path.join(ROOT, "analysis", "people.json"), encoding="utf-8"))
    return "".join(f'<div class="rc" id="r{side}{i}"><img src="assets/people/{p["file"]}" alt="" /><div class="rn">{esc(p["name"])}</div></div>'
                   for i, p in enumerate(ppl))


def logos_html():
    lg = [l for l in json.load(open(os.path.join(ROOT, "analysis", "logos.json"))) if not l["src"].startswith("visa")]
    rows, i = [], 0
    for n in (4, 3, 3, 3):
        rows.append(lg[i:i + n]); i += n
    return "".join('<div class="lrow">' + "".join(f'<div class="lt {l["tile"]}"><img src="assets/logos/{l["file"]}" alt="" /></div>' for l in row)
                   + "</div>" for row in rows if row)


def board_html(key, word):
    return "".join(f'<span class="cc2" data-layout-allow-overlap id="{key}-{i}">{"&nbsp;" if ch == " " else esc(ch)}</span>' for i, ch in enumerate(word))


def board_js():
    js, seed = [], 7
    for key, word, t in BOARD:
        for i, ch in enumerate(word):
            seed = (seed * 1103515245 + 12345) % 2147483648
            d = (seed % 7) / 50                       # 0–6 kadr tasodifiy kechikish (deterministik)
            js.append(f'tl.fromTo("#{key}-{i}",{{opacity:0,scale:1.25,filter:"blur(4px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.22,ease:"power2.out"}},{t - 0.06 + d:.3f});')
    return "\n      ".join(js)


def ruler_html():
    return "".join(f"<span>{n}</span>" for n in range(12, 32))


def stick_html():
    return "".join(f'<span id="sk{i}">{c}</span>' for i, c in enumerate(STICK))


def fx_html():
    out = [f'<div id="flash{i}" class="fx" data-composition-id="editorial-flash-overlay" data-composition-src="compositions/editorial-flash-overlay.html" '
           f'data-start="{t - .398:.3f}" data-duration="0.6" data-width="1080" data-height="1920" data-track-index="{40 + i}"></div>' for i, t in enumerate(FLASH)]
    out += [f'<div id="leak{i}" class="fx" data-composition-id="organic-light-leak-overlay" data-composition-src="compositions/organic-light-leak-overlay.html" '
            f'data-start="{t:.3f}" data-duration="1.6" data-width="1080" data-height="1920" data-track-index="{50 + i}"></div>' for i, t in enumerate(LEAK)]
    return "\n      ".join(out)


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>',
           f'<audio id="bgm" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1.0"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX_EVENTS, key=lambda e: e[1])):
        m = meta["sfx"][f]; st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" data-track-index="{60 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def timeline_js():
    js = []
    for cid, a, b, rows in CHIN:
        for r, (k, ws) in enumerate(rows):
            for j, w in enumerate(ws):
                t, c = w[1], (w[2] if len(w) > 2 else "")
                big = k in ("heavy", "anton") or c == "num"
                d, sc = (0.75, ",scale:1.06") if big else (0.62, "")
                if c == "big10":   # vau: katta raqam uzoqdan, kuchli blur bilan yaqinlashadi
                    js.append(f'tl.fromTo("#{cid}-{r}-{j}",{{opacity:0,scale:1.55,y:-20,filter:"blur(22px)"}},'
                              f'{{opacity:1,scale:1,y:0,filter:"blur(0px)",duration:0.95,ease:"expo.out"}},{max(a, t - 0.12):.3f});')
                    continue
                js.append(f'tl.fromTo("#{cid}-{r}-{j}",{{opacity:0,y:40,filter:"blur(12px)"{sc}}},'
                          f'{{opacity:1,y:0,filter:"blur(0px)"{",scale:1" if big else ""},duration:{d},ease:"expo.out"}},{max(a, t - 0.08):.3f});')
                if c == "mark":
                    js.append(f'tl.fromTo("#{cid}-{r}-{j}",{{backgroundSize:"0% 46%"}},{{backgroundSize:"100% 46%",duration:0.5,ease:"sine.inOut",immediateRender:false}},{t + 0.2:.3f});')
        js.append(f'OUT("#{cid} .row",{b - 0.44:.3f},{{stagger:0.03}});')
    for i, (a, b, t) in enumerate(CAPS):
        js.append(f'tl.fromTo("#cap{i} .cap-in",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.2,ease:"power2.out"}},{a:.3f});')
        js.append(f'tl.to("#cap{i} .cap-in",{{opacity:0,duration:0.18,ease:"power2.in"}},{b - 0.19:.3f});')
    # ritm: har kesim 1.32x dan zoom-out, keyin sekin push (11/13/15)
    for i, (a, b) in enumerate(SHOTS):
        js.append(f'tl.fromTo("#cam",{{scale:1.32}},{{scale:1.0,duration:1.2,ease:"expo.out",immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
        js.append(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.04,duration:{b - a - 1.204:.3f},ease:"sine.inOut",immediateRender:false}},{a + 1.202:.3f});')
    # 13: flash-blur (spiker kadrlariga qaytishda)
    for t in (8.167, 26.08, 29.233, 38.167, 42.96):
        js.append(f'tl.fromTo("#cam",{{filter:"blur(18px) brightness(1.5)"}},{{filter:"blur(0px) brightness(1)",duration:0.55,ease:"power2.out",immediateRender:false}},{t:.3f});')
    return "\n      ".join(js)


def carved_bgm():
    f = os.path.join(ROOT, "scripts", "bgm_carved.html")
    return open(f, encoding="utf-8").read() if os.path.exists(f) else None


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index.tpl.html"), encoding="utf-8").read()
    chin = json.load(open(os.path.join(ROOT, "analysis", "jaw.json"))); chin.pop("raw", None)
    rep = {"{{CAPS}}": caps_html(), "{{CHIN}}": chin_html(), "{{RING_B}}": ring_html("b"), "{{RING_F}}": ring_html("f"),
           "{{LOGOS}}": logos_html(), "{{FX}}": fx_html(), "{{AUDIO}}": audio_html(), "{{RULER}}": ruler_html(),
           "{{BOARD_JS}}": board_js(), "{{STICK}}": stick_html(), "{{ARC}}": ARC, "{{CHINDATA}}": json.dumps(chin, separators=(",", ":")),
           "{{TIMELINE}}": timeline_js()}
    rep.update({"{{" + k + "}}": board_html(k, w) for k, w, _ in BOARD})
    html = tpl
    for k, v in rep.items():
        html = html.replace(k, v)
    html = html.replace("{{DUR}}", str(DUR))
    keep = None   # v11: foydalanuvchi fon musiqasini olib tashlashni so'radi
    if keep:
        html = re.sub(r'<audio id="bgm".*?</audio>', lambda _: keep, html, count=1, flags=re.S)
    html = re.sub(r'\s*<audio id="bgm".*?</audio>', '', html, count=1, flags=re.S)
    assert "{{" not in html, re.findall(r"\{\{\w+\}\}", html)
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
