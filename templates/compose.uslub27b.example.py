"""hf/index.html — "Storis 5 000 -> 25 000", uslub-27 ANIQ nusxa (referens Dd8-UiOMI2x kadrma-kadr tahlili) — v4.

python scripts/compose27b.py   (shablon: scripts/index27b.tpl.html)
Referensdan: matn kadr O'RTASIDA ko'krak ustida (keng kadrda markazga, profil kadrda chapga), ~21 kesim (keng <-> x1.35 punch-in
<-> hujjatli B-roll), birinchi kadr oq-qora, urg'u turlari (kalit so'z, arvoh matn, katta so'z*, [qavs], qo'shtirnoq, qizil
zigzag/aylana/qo'lyozma, cho'zilib kiruvchi qizil so'z, sochilib->yig'iluvchi qator, shisha plashka, doira-niqob, 3D chiqish,
kesimdan o'tib uchuvchi so'z), CTA pill, oq yakun ekran + YouTube-muqova karta. Tween'lar silliq (overshootsiz).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 55.2
F, S = ("50.2% 31.2%", "58.9% 32.3%")      # old / profil kamera: yuz markazi (punch-in pivoti)
# A-roll kadrlari: (boshi, oxiri, zoom, pivot, oq-qora)
SHOTS = [
    (0.00, 1.94, 1.0, F, 1), (6.68, 10.38, 1.0, S, 0), (10.38, 13.12, 1.35, S, 0), (13.12, 15.58, 1.0, F, 0),
    (15.58, 17.16, 1.35, F, 0), (17.16, 19.52, 1.0, F, 0), (22.20, 24.40, 1.0, S, 0), (24.40, 26.56, 1.35, S, 0),
    (26.56, 30.04, 1.0, S, 0), (30.04, 32.44, 1.0, F, 0), (32.44, 35.40, 1.35, F, 0), (35.40, 38.50, 1.0, F, 0),
    (42.96, 45.14, 1.0, S, 0), (45.14, 46.62, 1.35, S, 1), (46.62, 49.62, 1.0, S, 0),
]
BROLL = [("b1_apps_doc", 1.94, 3.62), ("b3_growth_doc", 3.62, 6.68), ("b2_typing_doc", 19.52, 22.20)]
NEG = [6.68, 22.20, 42.96]

# Bloklar: (id, boshi, oxiri, tekislash c|l, top, chiqish blur|fly, qatorlar)
#   qator: kw | w | ghost | big | bigy | bigr | brk | num | sc (sochilib->yig'iladi, 4-maydon = yig'ilish vaqti)
#   so'z belgisi: zz (qizil zigzag) | ring (qizil aylana) | star (sariq *) | it (sariq kursiv) | q0/q1 (qo'shtirnoq)
B = [
    ("a1", 0.02, 1.92, "c", 930, "blur", [("kw", [("Qanday", 0.02, ""), ("qilib", 0.48, "")]),
                                          ("w", [("bir", 0.82, ""), ("ekspertimda", 1.06, "")])]),
    ("a2", 1.96, 3.60, "c", 1240, "blur", [("kw", [("Storislar", 1.96, "")]),
                                           ("w", [("ko‘rishlari", 2.70, "q0zz"), ("sonini", 3.22, "q1")])]),
    ("a3", 3.64, 6.64, "c", 1150, "blur", [("w", [("5 000", 3.64, ""), ("dan", 4.20, "")]),
                                           ("num", [("25 000", 4.40, "ring")]),
                                           ("w", [("ga", 5.54, ""), ("olib", 5.66, ""), ("chiqqanman", 6.08, "")])]),
    ("a5", 10.40, 12.58, "c", 1010, "blur", [("ghost", [("ya’ni", 10.40, ""), ("o‘sha", 10.80, ""), ("auditoriya", 11.08, "")]),
                                             ("big", [("tahlili", 11.92, "star")])]),
    ("a6", 12.62, 15.54, "c", 950, "blur", [("kw", [("Ikkinchi", 12.62, ""), ("navbatda", 13.30, "")]),
                                            ("w", [("shunchaki", 13.98, "")]), ("brk", [("[keys bilan]", 14.62, "")])]),
    ("a7", 15.60, 17.12, "c", 1010, "blur", [("sc", [("cheklanib", 15.60, ""), ("qolmasdan", 16.48, "")], 16.86)]),
    ("a8", 19.54, 22.16, "c", 860, "blur", [("w", [("xabarlarni", 19.54, "")]),
                                            ("kw", [("o‘qib", 21.00, ""), ("chiqqanman", 21.24, "")])]),
    ("a9", 22.24, 24.36, "l", 960, "blur", [("kw", [("Auditoriya", 22.56, "")]),
                                            ("w", [("unga", 23.40, ""), ("asosan", 23.80, "it")])]),
    ("a10", 24.40, 26.52, "l", 1010, "blur", [("w", [("qaysi", 24.42, "q0"), ("muammo", 24.90, "zz"), ("bilan", 25.36, "")]),
                                              ("w", [("murojaat", 25.70, ""), ("qilyapti?", 26.00, "q1")])]),
    ("a11", 26.60, 30.30, "l", 990, "fly", [("ghost", [("aynan", 27.02, ""), ("shu", 27.56, ""), ("muammolarni", 27.86, "")]),
                                            ("big", [("storisga", 28.56, "")])]),
    ("a13", 32.48, 36.34, "c", 1000, "blur", [("w", [("birinchi", 32.48, ""), ("storisni", 33.16, "")]),
                                              ("bigy", [("kuchli", 33.72, ""), ("intriga", 34.32, "")]),
                                              ("w", [("huk", 35.08, "it"), ("bilan", 35.46, ""), ("boshlash", 35.70, "")])]),
    ("a15", 42.98, 44.54, "l", 960, "blur", [("kw", [("Agar", 42.98, ""), ("sizda", 43.24, "")]),
                                             ("w", [("ham", 43.60, ""), ("storislaringizda", 43.90, "")])]),
    ("a16", 44.58, 46.58, "l", 980, "blur", [("w", [("ko‘rishlar", 44.60, ""), ("soni", 45.16, "")]), ("bigr", [("tushib", 45.58, "")]),
                                              ("w", [("ketgan", 45.84, ""), ("bo‘lsa", 46.18, "")])]),
    ("a17", 46.64, 49.56, "l", 940, "blur", [("w", [("shu", 46.64, ""), ("reels", 47.20, "")]), ("kw", [("izohida", 47.44, "")]),
                                             ("bigy", [("«+»", 48.02, "")]), ("w", [("qoldiring", 48.92, "")])]),
]
PLATES = [("p2", 36.40, 38.46, 960, [("bu", 36.38), ("har", 36.76), ("doim", 37.14), ("yaxshi", 37.52), ("ishlaydi", 37.86)])]
# uslub-28 oq karta + 3D emoji: (id, boshi, oxiri, left, top, sarlavha, izoh, emoji, kirish nuqtasi)
CARDS = [("c1", 6.94, 10.36, 30, 1000, "Birinchi navbatda", "keyslar va natijalar", "emoji_chart.png", "90% 100%"),
         ("c2", 17.20, 19.50, 60, 990, "Direct xabarlar", "auditoriya muammosini o‘zi yozadi", "emoji_envelope.png", "60% 100%"),
         ("c3", 30.06, 32.46, 60, 990, "Uchinchisi: huk", "birinchi storis — kuchli intriga", "emoji_hook.png", "60% 100%")]
PUSH_IN = {"a13"}   # kartadan keyin chapdan kirib keladigan blok (konveyer)
# qizil qo'lyozma izohlar: (id, boshi, oxiri, left, top, matn, burchak)
NOTES = [("n1", 2.95, 3.60, 560, 1470, "aynan shu!", -6), ("n2", 5.10, 6.64, 760, 1070, "x5 !", -8),
         ("n3", 21.40, 22.16, 560, 1070, "har birini", -6), ("n4", 35.30, 36.34, 330, 1345, "birinchi soniyada!", -5)]

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.10, -19), ("camera_shutter.wav", 1.94, -20), ("sweep_small.wav", 4.42, -19),
    ("sweep_small.wav", 4.95, -21), ("camera_shutter.wav", 10.38, -21), ("sweep_small.wav", 11.94, -20),
    ("sweep_small.wav", 12.64, -21), ("camera_shutter.wav", 15.58, -21), ("sweep_small.wav", 16.86, -20),
    ("sweep_small.wav", 17.22, -20), ("camera_shutter.wav", 24.40, -21), ("sweep_small.wav", 25.00, -21),
    ("whoosh-short.mp3", 28.58, -18), ("whoosh-short.mp3", 30.02, -18), ("camera_shutter.wav", 32.44, -21),
    ("sweep_small.wav", 33.74, -20), ("sweep_small.wav", 36.40, -20), ("air_woosh.wav", 38.56, -19),
    ("sweep_small.wav", 40.66, -20), ("whoosh-short.mp3", 42.86, -18), ("impact-bass-1.mp3", 45.60, -16),
    ("select_click.wav", 48.36, -16), ("correct_tone.wav", 48.94, -19), ("magic_sparkle_whoosh.wav", 49.66, -20),
    ("sweep_small.wav", 51.90, -20),
] + [("air_woosh.wav", t, -21) for t in NEG]

ZZ = '<svg class="zz" viewBox="0 0 120 14" preserveAspectRatio="none"><path class="draw red" pathLength="1" d="M2 9 L12 3 L22 11 L32 3 L42 11 L52 3 L62 11 L72 3 L82 11 L92 3 L102 11 L118 4"/></svg>'
RING = '<svg class="ring" viewBox="0 0 400 160" preserveAspectRatio="none"><path class="draw red" pathLength="1" d="M210 14 C320 8 392 40 388 82 C384 128 300 152 196 150 C92 148 12 124 12 80 C12 38 96 12 230 20"/></svg>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


# --- referensdan o'lchangan tipografiya (Dd8-UiOMI2x, 1080 px kadr) ---
SIZE = {"kw": (136, 700, -0.02), "w": (66, 600, -0.01), "sc": (66, 600, -0.01), "ghost": (46, 500, 0), "brk": (38, 600, 0),
        "num": (200, 700, -0.03), "big": (210, 700, -0.03), "bigy": (130, 700, -0.02), "bigr": (190, 700, -0.03)}
MAXW = {"c": 960, "l": 880}
from PIL import ImageFont
_FC = {}


def _font(kind):
    if kind not in _FC:
        px, wt, _ = SIZE[kind]
        f = ImageFont.truetype(os.path.join(ROOT, "hf", "assets", "fonts", "Outfit-var.ttf"), px)
        f.set_variation_by_axes([wt]); _FC[kind] = f
    return _FC[kind]


def wlen(kind, w, m=""):
    px, wt, ls = SIZE[kind]
    txt = ("“" if "q0" in m else "") + w + ("”" if "q1" in m else "") + ("*" if "star" in m else "")
    return _font(kind).getlength(txt) + ls * px * max(0, len(txt) - 1)


def row_w(kind, ws):
    gap = 0.26 * SIZE[kind][0]
    return sum(wlen(kind, w, m) for w, _, m in ws) + gap * (len(ws) - 1)


def wrap_rows(rows, al):
    out = []
    for row in rows:
        kind, ws = row[0], row[1]
        cur = []
        for it in ws:
            if cur and row_w(kind, cur + [it]) > MAXW[al]:
                out.append((kind, cur) + tuple(row[2:])); cur = []
            cur.append(it)
        out.append((kind, cur) + tuple(row[2:]))
    return out


B = [(bid, a, b, al, top, ex, wrap_rows(rows, al)) for bid, a, b, al, top, ex, rows in B]


def word_html(bid, r, j, w, m):
    inner = esc(w)
    if "q0" in m: inner = '<span class="qm">“</span>' + inner
    if "q1" in m: inner = inner + '<span class="qm">”</span>'
    if "star" in m: inner = inner + '<span class="star">*</span>'
    extra = (ZZ if "zz" in m else "") + (RING if "ring" in m else "")
    cls = "w" + (" it" if "it" in m else "")
    return f'<span class="{cls}" id="{bid}-{r}-{j}" data-layout-allow-overlap>{inner}{extra}</span>'


def blocks_html():
    out = []
    for k, (bid, a, b, al, top, ex, rows) in enumerate(B):
        rs = "".join(f'<div class="r k-{row[0]}" id="{bid}-r{r}">' + "".join(word_html(bid, r, j, w, m) for j, (w, _, m) in enumerate(row[1])) + "</div>"
                     for r, row in enumerate(rows))
        out.append(f'<div id="{bid}" class="clip blk al-{al}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{30 + k}" '
                   f'style="top:{top}px"><div class="blk-in">{rs}</div></div>')
    return "\n      ".join(out)


def plates_html():
    return "\n      ".join(
        f'<div id="{pid}" class="clip plate" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{55 + k}" style="top:{top}px">'
        f'<div class="pl-bg"></div><div class="pl-t">' + " ".join(f'<span class="w" id="{pid}-{j}">{esc(w)}</span>' for j, (w, _) in enumerate(ws)) +
        '</div></div>' for k, (pid, a, b, top, ws) in enumerate(PLATES))


def notes_html():
    return "\n      ".join(
        f'<div id="{nid}" class="clip note" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{58 + k}" '
        f'style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><span class="note-in">{esc(t)}</span></div>'
        for k, (nid, a, b, x, y, t, rot) in enumerate(NOTES))


def cards_html():
    return "\n      ".join(
        f'<div id="{cid}" class="clip fcard" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{62 + k}" style="left:{x}px;top:{y}px">'
        f'<div class="fc-in" style="transform-origin:{org}"><div class="fc-t">{esc(t)}</div><div class="fc-s">{esc(sub)}</div></div>'
        f'<img class="fc-e" src="assets/img/{em}" alt="" /></div>' for k, (cid, a, b, x, y, t, sub, em, org) in enumerate(CARDS))


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
    # referens: so'z o'z joyida blur 10->0 + opacity, ~6 kadr (0.2 s); katta so'z gorizontal cho'zilib ~8 kadr
    if kind in ("big", "num", "bigy"):
        return (f'tl.fromTo("{sel}",{{opacity:0,scaleX:1.25,scaleY:0.8,filter:"blur(16px)"}},'
                f'{{opacity:1,scaleX:1,scaleY:1,filter:"blur(0px)",duration:0.34,ease:"power3.out"}},{t - 0.06:.3f});')
    if kind == "bigr":
        return (f'tl.fromTo("{sel}",{{opacity:0,scaleY:1.45,filter:"blur(14px)"}},'
                f'{{opacity:1,scaleY:1,filter:"blur(0px)",duration:0.34,ease:"power3.out"}},{t - 0.06:.3f});')
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:1.04,filter:"blur(10px)"}},'
            f'{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{t - 0.06:.3f});')


SCAT = [(-40, -70, -5), (60, 80, 6), (-30, 120, -4), (50, -40, 5)]   # sochilish ofsetlari (x, y, burchak)


def timeline_js():
    js = []
    for i, (a, b, z, piv, gray) in enumerate(SHOTS):
        js.append(f'tl.set("#aroll",{{filter:"{"grayscale(1) contrast(1.14) brightness(1.03)" if gray else "grayscale(0) contrast(1) brightness(1)"}"}},{a:.3f});')
        js.append(f'tl.fromTo("#cam",{{scale:{z},transformOrigin:"{piv}"}},{{scale:{z * 1.035:.4f},duration:{b - a - 0.004:.3f},ease:"sine.inOut",'
                  f'immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
    for t in NEG:
        js.append(f'tl.fromTo("#neg",{{opacity:0}},{{opacity:0.45,duration:0.3,ease:"sine.inOut",immediateRender:false}},{t - 0.3:.3f});')
        js.append(f'tl.to("#neg",{{opacity:0,duration:0.45,ease:"sine.inOut"}},{t:.3f});')
    for bid, a, b, al, top, ex, rows in B:
        for r, row in enumerate(rows):
            kind, ws = row[0], row[1]
            if al == "c" and kind != "sc" and len(ws) > 1:
                wf = row_w(kind, ws)
                js.append(f'tl.set("#{bid}-r{r}",{{x:{(wf - row_w(kind, ws[:1])) / 2:.1f}}},{a:.3f});')
                for k in range(1, len(ws)):
                    tk = max(a + 0.02, ws[k][1])
                    js.append(f'tl.to("#{bid}-r{r}",{{x:{(wf - row_w(kind, ws[:k + 1])) / 2:.1f},duration:0.36,ease:"power3.out"}},{tk - 0.06:.3f});')
            for j, (w, t, m) in enumerate(ws):
                sel = f"#{bid}-{r}-{j}"
                t0 = max(a + 0.02, t)
                if kind == "sc":
                    dx, dy, rot = SCAT[j % len(SCAT)]
                    js.append(f'tl.fromTo("{sel}",{{opacity:0,x:{dx},y:{dy},rotation:{rot},filter:"blur(10px)"}},'
                              f'{{opacity:1,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{t0 - 0.08:.3f});')
                    js.append(f'tl.to("{sel}",{{x:0,y:0,rotation:0,duration:0.6,ease:"power2.inOut"}},{row[2]:.3f});')
                elif bid in PUSH_IN and r == 0:
                    js.append(f'tl.fromTo("{sel}",{{opacity:0,x:-120,filter:"blur(10px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},{t0 - 0.1:.3f});')
                else:
                    js.append(W_in(sel, t0, kind))
                if "zz" in m:
                    js.append(f'tl.fromTo("{sel} .draw",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.5,ease:"power2.inOut"}},{t0 + 0.3:.3f});')
                if "ring" in m:
                    js.append(f'tl.fromTo("{sel} .draw",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.8,ease:"power2.inOut"}},{t0 + 0.55:.3f});')
                if "star" in m:
                    js.append(f'tl.fromTo("{sel} .star",{{opacity:0,scale:0.6,rotation:-40}},{{opacity:1,scale:1,rotation:0,duration:0.6,ease:"expo.out"}},{t0 + 0.3:.3f});')
            if kind == "big":
                js.append(f'tl.to("#{bid}-{r}-0",{{scale:1.06,duration:{max(0.6, b - ws[0][1] - 0.6):.3f},ease:"sine.inOut"}},{ws[0][1] + 0.55:.3f});')
        if ex == "fly":
            js.append(f'tl.to("#{bid} .blk-in",{{rotation:18,x:160,y:240,opacity:0,filter:"blur(10px)",duration:0.62,ease:"power2.inOut"}},{b - 0.62:.3f});')
        else:
            js.append(f'tl.to("#{bid} .blk-in",{{opacity:0,filter:"blur(8px)",duration:0.24,ease:"power2.in"}},{b - 0.24:.3f});')
    for pid, a, b, top, ws in PLATES:
        js.append(f'tl.fromTo("#{pid} .pl-bg",{{scaleX:0.3,opacity:0,filter:"blur(8px)"}},{{scaleX:1,opacity:1,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},{a - 0.06:.3f});')
        for j, (w, t) in enumerate(ws):
            js.append(W_in(f"#{pid}-{j}", max(a + 0.08, t), "w"))
        js.append(f'tl.to("#{pid} > *",{{opacity:0,filter:"blur(8px)",duration:0.4,ease:"power2.inOut"}},{b - 0.4:.3f});')
    for cid, a, b, x, y, t, sub, em, org in CARDS:   # silliq: scale 0.85->1 + blur, chiqish o'ngga push
        js.append(f'tl.fromTo("#{cid} .fc-in",{{opacity:0,scale:0.85,x:50,y:-24,filter:"blur(12px)"}},{{opacity:1,scale:1,x:0,y:0,filter:"blur(0px)",duration:0.8,ease:"expo.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#{cid} .fc-e",{{opacity:0,scale:0.6,rotation:-18,filter:"blur(8px)"}},{{opacity:1,scale:1,rotation:0,filter:"blur(0px)",duration:0.8,ease:"expo.out"}},{a + 0.18:.3f});')
        n = max(1, int((b - a - 1.5) / 0.9))
        js.append(f'tl.fromTo("#{cid} .fc-e",{{y:0,rotation:0}},{{y:-12,rotation:7,duration:0.45,ease:"sine.inOut",yoyo:true,repeat:{2 * n - 1},immediateRender:false}},{a + 0.98:.3f});')
        js.append(f'tl.to("#{cid} > *",{{x:760,opacity:0,filter:"blur(8px)",duration:0.6,ease:"power2.inOut"}},{b - 0.5:.3f});')
    for nid, a, b, x, y, t, rot in NOTES:
        js.append(f'tl.fromTo("#{nid} .note-in",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.8,ease:"power2.inOut"}},{a:.3f});')
        js.append(f'tl.to("#{nid} .note-in",{{opacity:0,filter:"blur(6px)",duration:0.4,ease:"power2.inOut"}},{b - 0.4:.3f});')
    return "\n      ".join(js)


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index27b.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{BLOCKS}}", blocks_html()).replace("{{PLATES}}", plates_html()).replace("{{NOTES}}", notes_html() + "\n      " + cards_html())
            .replace("{{BROLL}}", broll_html()).replace("{{AUDIO}}", audio_html()).replace("{{TIMELINE}}", timeline_js())
            .replace("{{DUR}}", str(DUR)))
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
