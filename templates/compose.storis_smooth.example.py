"""hf/index.html — "Storis 5 000 -> 25 000" (Editorial Premium uslubi).

python scripts/compose.py
Vaqtlar = aroll.mp4 vaqti = analysis/tr_uz.json (manba to'g'ridan kesilgan, sinxron).
Uslub: krem + iliq oltin + qora, Playfair Display italic + Inter Tight. Yuz zonasi 410-840 px — grafika faqat 1000+ va tepada.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 55.2
SHOTS = [0, 6.68, 13.12, 22.2, 30.04, 42.96, 50.76, 55.2]
BLOOM = [13.12, 30.04, 50.76]          # yumshoq ekspozitsiya chaqnashi (kesimda)

# (boshi, oxiri, matn) — *so'z* = oltin kursiv urg'u
CAPS = [
    (0.02, 1.92, "Qanday qilib bir ekspertimda"),
    (1.94, 3.60, "storislar *ko‘rishlari* sonini"),
    (15.52, 17.10, "keys bilan cheklanib qolmasdan,"),
    (21.80, 23.70, "Ya’ni auditoriya unga"),
    (23.78, 26.54, "asosan qaysi *muammo* bilan yozyapti"),
    (36.38, 38.44, "Bu har doim *yaxshi* ishlaydi."),
    (42.94, 44.58, "Agar sizda ham"),
    (44.60, 46.60, "ko‘rishlar soni *tushib* ketgan bo‘lsa,"),
]

# bob kartalari: (id, boshi, oxiri, raqam, yorliq, sarlavha, fon xiralashuvi oxiri)
CHAPTERS = [
    ("ch1", 6.92, 12.42, "01", "Birinchi navbatda", "Auditoriya<br>tahlili.", 9.30),
    ("ch2", 12.66, 15.50, "02", "Ikkinchi navbatda", "Direct<br>xabarlar.", 14.90),
    ("ch3", 30.00, 32.42, "03", "Uchinchisi", "Kuchli<br>huk.", 32.10),
]

# sarlavha (27.0-29.94)
HEAD = [("sm", [("Aynan", 27.02), ("shu", 27.56)]),
        ("cream", [("muammolar", 27.86)]),
        ("cream", [("—", 28.40), ("storisga.", 28.56)])]
HEAD_T = (27.00, 29.96)

DMS = [("dm0", 18.30, "Storislarim ko‘rilmay qoldi, nima qilay?"),
       ("dm1", 19.10, "Obunachi bor, lekin hech kim yozmaydi"),
       ("dm2", 19.90, "Nimadan boshlashni bilmayapman…")]

SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.30, -14), ("impact-bass-1.mp3", 0.42, -12),
    ("sweep_small.wav", 3.66, -17), ("correct_tone.wav", 6.10, -17), ("sparkle.mp3", 6.14, -20),
    ("whoosh-short.mp3", 6.90, -16), ("impact-bass-2.mp3", 7.00, -14),
    ("whoosh-short.mp3", 12.64, -16), ("impact-bass-2.mp3", 12.74, -14),
    ("sweep_small.wav", 17.95, -17), ("click-soft.mp3", 18.32, -15), ("click-soft.mp3", 19.12, -15), ("click-soft.mp3", 19.92, -15),
    ("select_click.wav", 21.02, -16),
    ("click-soft.mp3", 27.88, -15), ("impact-bass-1.mp3", 28.58, -13),
    ("whoosh-short.mp3", 29.98, -16), ("impact-bass-2.mp3", 30.08, -14),
    ("sweep_small.wav", 32.48, -16), ("explainer_pop_whoosh.wav", 34.34, -17), ("explainer_pop_whoosh.wav", 35.10, -17),
    ("long_pop.wav", 39.56, -15), ("sweep_small.wav", 40.62, -18), ("long_pop.wav", 40.70, -15),
    ("sweep_small.wav", 41.20, -18), ("long_pop.wav", 41.28, -15),
    ("sweep_small.wav", 44.62, -17), ("error.mp3", 45.62, -21),
    ("sweep_small.wav", 46.64, -17), ("key-press.mp3", 48.04, -13), ("select_click.wav", 48.92, -13), ("pop.mp3", 49.08, -14),
    ("magic_sparkle_whoosh.wav", 49.80, -18), ("impact-bass-1.mp3", 51.90, -12), ("correct_tone.wav", 54.40, -18),
    ("whoosh_deep_impact.wav", 54.95, -18),
] + [("key-press.mp3", 3.80 + i * 0.16, -15 - i * 0.35) for i in range(13)] \
  + [("air_woosh.wav", t, -19) for t in BLOOM]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def cap_text(t):
    return re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', esc(t))


def caps_html():
    return "\n      ".join(
        f'<div id="cap{i}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="20">'
        f'<span class="cap-in">{cap_text(t)}</span></div>' for i, (a, b, t) in enumerate(CAPS))


def chapters_html():
    return "\n      ".join(
        f'<div id="{cid}" class="clip chap" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{30 + k}">'
        f'<div class="ch-num">{n}</div>'
        f'<div class="ch-lab"><span class="ch-rule"></span>{esc(lab)}</div>'
        f'<div class="ch-title">{title}</div></div>'
        for k, (cid, a, b, n, lab, title, _) in enumerate(CHAPTERS))


def head_html():
    rows = "".join(f'<div class="row {k}">' + "".join(f'<span class="w" id="hd-{r}-{j}">{esc(w)}</span>'
                                                     for j, (w, _) in enumerate(ws)) + "</div>" for r, (k, ws) in enumerate(HEAD))
    a, b = HEAD_T
    return (f'<div id="hd" class="clip head" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="34">'
            f'<div class="head-in">{rows}</div></div>')


def dm_html():
    items = "".join(f'<div class="dm" id="{i}"><span class="dm-av"></span><span class="dm-b glass">{esc(t)}</span></div>' for i, _, t in DMS)
    return (f'<div id="dmbox" class="clip" data-start="17.90" data-duration="3.78" data-track-index="35">'
            f'<div class="dm-head glass" id="dmh"><svg viewBox="0 0 24 24"><path d="M3 11.5 21 3l-7.5 18-2.6-7.4z" fill="none" stroke="#e8c48a" stroke-width="1.7" stroke-linejoin="round"/></svg>'
            f'<b>Direct</b><span>3 ta yangi xabar</span></div>{items}'
            f'<div class="dm-seen" id="dmseen">Ko‘rildi ✓</div></div>')


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>',
           f'<audio id="bgm" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="0.75"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX_EVENTS, key=lambda e: e[1])):
        m = meta["sfx"][f]
        st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{60 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def W(sel, t, d=0.62, y=40, blur=12, extra=""):
    """silliq kirish (smooth-motion.md)"""
    return (f'tl.fromTo("{sel}",{{opacity:0,y:{y},filter:"blur({blur}px)"{extra and "," + extra.split("|")[0]}}},'
            f'{{opacity:1,y:0,filter:"blur(0px)"{extra and "," + extra.split("|")[1]},duration:{d},ease:"expo.out"}},{t:.3f});')


def OUT(sel, t, d=0.5):
    return f'tl.to("{sel}",{{opacity:0,y:-16,filter:"blur(8px)",duration:{d},ease:"power2.inOut"}},{t:.3f});'


def timeline_js():
    js = []
    # kamera: har kadrda sekin "nafas" push, kesimda sakrashsiz (har kadr 1.0 dan boshlanadi — kesim o'zi yangi kadr)
    for i in range(1, len(SHOTS) - 1):
        a, b = SHOTS[i], SHOTS[i + 1]
        z0, z1 = (1.0, 1.035) if i % 2 else (1.035, 1.0)
        js.append(f'tl.fromTo("#cam",{{scale:{z0}}},{{scale:{z1},duration:{b - a - 0.004:.3f},ease:"sine.inOut",immediateRender:false}},{a:.3f});')
    for t in BLOOM:
        js.append(f'tl.fromTo("#bloom",{{opacity:0}},{{opacity:0.22,duration:0.3,ease:"sine.inOut",immediateRender:false}},{t - 0.3:.3f});')
        js.append(f'tl.to("#bloom",{{opacity:0,duration:0.7,ease:"sine.inOut"}},{t:.3f});')
    # subtitrlar
    for i, (a, b, _) in enumerate(CAPS):
        js.append(f'tl.fromTo("#cap{i} .cap-in",{{opacity:0,y:14,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.45,ease:"expo.out"}},{a - 0.06:.3f});')
        js.append(f'tl.to("#cap{i} .cap-in",{{opacity:0,filter:"blur(6px)",duration:0.3,ease:"power2.inOut"}},{b - 0.3:.3f});')
    # bob kartalari + fon xiralashuvi
    for k, (cid, a, b, n, lab, title, unblur) in enumerate(CHAPTERS):
        js.append(f'tl.to("#cam",{{filter:"blur(7px) brightness(0.72)",duration:0.7,ease:"sine.inOut"}},{a - 0.15:.3f});')
        js.append(f'tl.to("#cam",{{filter:"blur(0px) brightness(1)",duration:0.8,ease:"sine.inOut"}},{unblur:.3f});')
        js.append(f'tl.fromTo("#{cid} .ch-num",{{opacity:0,x:-80,filter:"blur(16px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:0.8,ease:"expo.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#{cid} .ch-rule",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power3.inOut"}},{a + 0.18:.3f});')
        js.append(W(f"#{cid} .ch-lab", a + 0.22, 0.6, 20, 8))
        js.append(W(f"#{cid} .ch-title", a + 0.36, 0.75, 40, 14, "scale:1.06|scale:1"))
        js.append(OUT(f"#{cid} > *", b - 0.52))
        js.append(f'prog({k},{a:.3f});')
    # sarlavha
    for r, (k, ws) in enumerate(HEAD):
        for j, (w, t) in enumerate(ws):
            js.append(W(f"#hd-{r}-{j}", max(HEAD_T[0], t - 0.08), 0.75 if k == "cream" else 0.62, 40, 12, "scale:1.06|scale:1" if k == "cream" else ""))
    js.append(OUT("#hd .head-in", HEAD_T[1] - 0.52))
    # Direct
    js.append(W("#dmh", 17.92, 0.6, 24, 10))
    for i, t, _ in DMS:
        js.append(W(f"#{i}", t - 0.08, 0.7, 60, 12))
    js.append(f'tl.fromTo("#dmseen",{{opacity:0}},{{opacity:1,duration:0.5,ease:"sine.inOut"}},20.92);')
    js.append(OUT("#dmbox > *", 21.16))
    return "\n      ".join(js)


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{CAPS}}", caps_html()).replace("{{CHAPTERS}}", chapters_html()).replace("{{HEAD}}", head_html())
            .replace("{{DM}}", dm_html()).replace("{{AUDIO}}", audio_html()).replace("{{TIMELINE}}", timeline_js())
            .replace("{{DUR}}", str(DUR)))
    f = os.path.join(ROOT, "scripts", "bgm_carved.html")
    if os.path.exists(f):
        keep = open(f, encoding="utf-8").read()
        html = re.sub(r'<audio id="bgm".*?</audio>', lambda _: keep, html, count=1, flags=re.S)
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
