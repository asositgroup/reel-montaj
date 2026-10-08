"""hf/index.html — "Storis 5 000 -> 25 000", USLUB-28 (referens Dd_39GWs0Wy, @uktamjontuygunovv podkast UI kartalar) — v10.

python scripts/compose28.py   (shablon: scripts/index28.tpl.html)
Referensdan o'lchangan: General Sans Semibold, ikki darajali chap subtitr (66/46 px), so'zlar sochilib -> qatorga yig'iladi,
yashil/sariq-yashil marker, qizil qo'lda ellips, sariq “ ” savol, [qavs] iqtibos, oq karta + 3D emoji (o'ngga push),
to'q-sariq pill (punktir) + oq pill typewriter, ogohlantirish kartasi (!) typewriter, CTA pill, oq yakun ekran.
Ritm: ~19 kesim (keng / x1.3 yaqin plan / yuzsiz B-roll). Overshoot yo'q.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 55.2
F, S = "50.2% 31.2%", "58.9% 32.3%"
# A-roll kadrlari: (boshi, oxiri, zoom, pivot)
SHOTS = [(0.00, 1.94, 1.0, F), (1.94, 3.62, 1.28, F), (3.62, 6.68, 1.0, F), (6.68, 10.38, 1.0, S), (10.38, 13.12, 1.3, S),
         (13.12, 15.58, 1.0, F), (15.58, 17.16, 1.28, F), (22.20, 24.40, 1.0, S), (24.40, 26.56, 1.3, S), (26.56, 30.04, 1.0, S),
         (30.04, 32.44, 1.0, F), (36.38, 38.50, 1.28, F), (38.50, 40.62, 1.0, F), (40.62, 42.96, 1.3, F),
         (42.96, 45.14, 1.0, S), (45.14, 46.62, 1.3, S), (46.62, 49.62, 1.0, S)]
BROLL = [("r28_dm", 17.16, 22.20), ("r28_phone", 32.44, 36.38)]

# subtitr bloklari: (id, boshi, oxiri, top, [(tur, [(so'z, t, belgi)])], yig'ilish vaqti)
#  tur: L (katta 66) | s (kichik 46) | B (juda katta 104) | k (qavs 34)
#  belgi: mg (yashil marker) | my (sariq-yashil marker) | ell (qizil ellips) | q0/q1 (sariq qo'shtirnoq)
SUBS = [
    ("b1", 0.02, 1.92, 1010, [("L", [("Qanday", 0.00, ""), ("qilib", 0.48, ""), ("bir", 0.82, "")]), ("s", [("ekspertimda", 1.06, "")])], 1.40),
    ("b2", 1.98, 3.58, 1060, [("L", [("Storislar", 1.98, ""), ("ko‘rishlari", 2.70, "")]), ("s", [("sonini", 3.22, "")])], 3.30),
    ("b3", 6.74, 10.34, 1000, [("L", [("Birinchi", 6.98, ""), ("navbatda", 7.36, "")]), ("k", [("[keyslar va natijalar]", 8.66, "")])], 7.60),
    ("b4", 10.42, 13.08, 1040, [("s", [("ya’ni", 10.40, ""), ("o‘sha", 10.80, ""), ("auditoriya", 11.08, "")]), ("B", [("tahlili", 11.92, "ell")])], 11.40),
    ("b5", 13.16, 15.54, 1000, [("L", [("Ikkinchi", 13.16, ""), ("navbatda", 13.30, "")]), ("s", [("shunchaki", 13.98, ""), ("keys", 14.62, ""), ("bilan", 15.24, "")])], 15.30),
    ("b6", 15.62, 17.12, 1040, [("L", [("cheklanib", 15.60, "")]), ("s", [("qolmasdan", 16.48, "")])], 16.60),
    ("b7", 22.24, 26.52, 980, [("L", [("Auditoriya", 22.56, "q0"), ("unga", 23.40, "")]), ("s", [("qaysi", 24.42, ""), ("muammo", 24.90, ""), ("bilan", 25.36, "")]),
                              ("s", [("murojaat", 25.70, ""), ("qilyapti?", 26.00, "q1")])], 26.10),
    ("b8", 26.60, 29.98, 1000, [("L", [("Aynan", 27.02, ""), ("shu", 27.56, ""), ("muammolarni", 27.86, "mg")]),
                               ("L", [("storisga", 28.56, "my"), ("olib", 29.26, ""), ("chiqdik", 29.42, "")])], 29.50),
    ("b9", 36.42, 38.46, 1040, [("L", [("Bu", 36.38, ""), ("har", 36.76, ""), ("doim", 37.14, "")]), ("L", [("yaxshi", 37.52, "mg"), ("ishlaydi", 37.86, "")])], 37.95),
    ("b10", 38.54, 40.58, 1000, [("s", [("va", 38.52, ""), ("har", 38.74, ""), ("doim", 39.14, "")]), ("L", [("birinchi", 39.54, ""), ("storis", 40.18, "")])], 40.25),
    ("b11", 40.66, 42.92, 1040, [("L", [("ikkinchisini", 40.66, ""), ("sotishga", 41.24, "my")]), ("k", [("[xizmat qilishi kerak]", 41.70, "")])], 41.80),
    ("b12", 43.00, 45.10, 1000, [("L", [("Agar", 42.94, ""), ("sizda", 43.24, ""), ("ham", 43.60, "")]), ("s", [("storislaringizda", 43.90, ""), ("ko‘rishlar", 44.60, "")])], 44.70),
    ("b13", 45.18, 46.58, 1040, [("L", [("soni", 45.16, ""), ("tushib", 45.58, "ell"), ("ketgan", 45.84, "")]), ("s", [("bo‘lsa", 46.18, "")])], 46.25),
    ("b14", 46.66, 49.56, 980, [("L", [("shu", 46.62, ""), ("reels", 47.20, ""), ("izohida", 47.44, "")]), ("L", [("«+»", 48.02, "my"), ("qoldiring", 48.92, "")])], 49.00),
]
# oq karta + 3D emoji: (id, boshi, oxiri, top, sarlavha, izoh, emoji)
CARDS = [("c1", 3.66, 6.64, 980, "5 000 → 25 000", "storis ko‘rishlari", "real_growth.png"),
         ("c2", 30.08, 32.42, 980, "3-usul: kuchli huk", "birinchi soniyadan qiziqtiring", "real_hook.png")]
SCAT = [(0, -26, -2), (0, 22, 2), (0, -16, -1.5), (0, 30, 1.5), (0, -32, 2), (0, 18, -2)]

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.10, -22), ("sweep_small.wav", 1.94, -21), ("long_pop.wav", 3.70, -18), ("sweep_small.wav", 6.40, -20),
    ("sweep_small.wav", 12.30, -21), ("sweep_small.wav", 16.62, -21),
    ("sweep_small.wav", 17.22, -19), ("sweep_small.wav", 19.52, -20), ("sweep_small.wav", 27.88, -20),
    ("sweep_small.wav", 28.58, -20), ("long_pop.wav", 30.10, -18), ("sweep_small.wav", 32.20, -20), ("error.mp3", 32.52, -24),
    ("sweep_small.wav", 41.26, -21), ("sweep_small.wav", 45.60, -20),
    ("select_click.wav", 48.36, -17), ("correct_tone.wav", 48.86, -20), ("whoosh-short.mp3", 49.60, -19), 
] + [("key-press.mp3", 17.40 + i * 0.6, -20 - (i % 2)) for i in range(4)] + [("key-press.mp3", 32.80 + i * 0.7, -20 - (i % 2)) for i in range(4)]

ELL = '<svg class="ell" viewBox="0 0 400 160" preserveAspectRatio="none"><path class="draw" pathLength="1" d="M215 18 C325 10 394 44 388 84 C382 128 296 150 192 148 C88 146 10 122 12 78 C14 36 102 10 240 24"/></svg>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def word(bid, r, j, w, m):
    inner = esc(w)
    if "q0" in m: inner = '<span class="qm">“</span>' + inner
    if "q1" in m: inner = inner + '<span class="qm">”</span>'
    mk = '<span class="mk g"></span>' if "mg" in m else '<span class="mk y"></span>' if "my" in m else ""
    return f'<span class="w" id="{bid}-{r}-{j}">{mk}<span class="wt">{inner}</span>{ELL if "ell" in m else ""}</span>'


def subs_html():
    out = []
    for k, (bid, a, b, top, rows, _) in enumerate(SUBS):
        rs = "".join(f'<div class="r t-{kind}">' + "".join(word(bid, r, j, w, m) for j, (w, _, m) in enumerate(ws)) + "</div>"
                     for r, (kind, ws) in enumerate(rows))
        out.append(f'<div id="{bid}" class="clip sub" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{30 + k}" '
                   f'style="top:{top}px"><div class="sub-in" data-layout-allow-overlap>{rs}</div></div>')
    return "\n      ".join(out)


def cards_html():
    return "\n      ".join(
        f'<div id="{cid}" class="clip fcard" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{50 + k}" style="top:{top}px">'
        f'<div class="fc-in"><div class="fc-t">{esc(t)}</div><div class="fc-s">{esc(s)}</div></div>'
        f'<img class="fc-e" src="assets/img/{em}" alt="" /></div>' for k, (cid, a, b, top, t, s, em) in enumerate(CARDS))


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
                   f'data-track-index="{80 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def timeline_js():
    js = []
    for i, (a, b, z, piv) in enumerate(SHOTS):     # kadr ichida sekin drift (+3%), kesim = yangi kamera burchagi
        js.append(f'tl.fromTo("#cam",{{scale:{z},transformOrigin:"{piv}"}},{{scale:{z * 1.03:.4f},duration:{b - a - 0.004:.3f},ease:"sine.inOut",'
                  f'immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
    n = 0
    for bid, a, b, top, rows, settle in SUBS:
        for r, (kind, ws) in enumerate(rows):
            for j, (w, t, m) in enumerate(ws):
                sel = f"#{bid}-{r}-{j}"; t0 = max(a + 0.02, t - 0.06)
                dx, dy, rot = SCAT[n % len(SCAT)]; n += 1
                # referens (30 fps o'lchandi): so'z joyidan ~45 px PASTDA, vertikal blur bilan chiqadi, ~6 kadrda joyiga ko'tariladi
                js.append(f'tl.fromTo("{sel}",{{opacity:0,y:46,scaleY:1.12,filter:"blur(7px)"}},{{opacity:1,y:0,scaleY:1,filter:"blur(0px)",duration:0.22,ease:"power2.out"}},{t0:.3f});')
                if "mg" in m or "my" in m:
                    js.append(f'tl.fromTo("{sel} .mk",{{scaleX:0}},{{scaleX:1,duration:0.32,ease:"power2.inOut"}},{t0 + 0.3:.3f});')
                if "ell" in m:
                    js.append(f'tl.fromTo("{sel} .draw",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0.06,opacity:1,duration:0.4,ease:"power2.inOut"}},{t0 + 0.3:.3f});')
        js.append(f'tl.fromTo("#{bid} .sub-in",{{y:0}},{{y:-40,duration:{b - a:.3f},ease:"none"}},{a:.3f});')
        js.append(f'tl.to("#{bid} .sub-in",{{opacity:0,filter:"blur(8px)",duration:0.16,ease:"power2.in"}},{b - 0.16:.3f});')
    for cid, a, b, top, t, s, em in CARDS:          # oq karta: qo'l yonidan o'sadi, chiqishda o'ngga surilib ketadi
        js.append(f'tl.fromTo("#{cid} .fc-in",{{opacity:0,scale:0.4,x:180,y:120,filter:"blur(14px)"}},{{opacity:1,scale:1,x:0,y:0,filter:"blur(0px)",duration:0.42,ease:"power3.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#{cid} .fc-e",{{opacity:0,scale:0.5,rotation:-20}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"power3.out"}},{a + 0.12:.3f});')
        js.append(f'tl.fromTo("#{cid} .fc-e",{{y:0,rotation:0}},{{y:-10,rotation:6,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:{max(1, int((b - a - 1.2) / 0.5)) | 1},immediateRender:false}},{a + 0.6:.3f});')
        js.append(f'tl.to("#{cid} > *",{{x:900,opacity:0,filter:"blur(10px)",duration:0.36,ease:"power2.in"}},{b - 0.36:.3f});')
    return "\n      ".join(js)


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index28.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{SUBS}}", subs_html()).replace("{{CARDS}}", cards_html()).replace("{{BROLL}}", broll_html())
            .replace("{{AUDIO}}", audio_html()).replace("{{TIMELINE}}", timeline_js()).replace("{{DUR}}", str(DUR)))
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
