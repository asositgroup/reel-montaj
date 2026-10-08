"""hf/index.html ni ma'lumotdan yig'adi — "Ekspert shaxsiyati" (C8953).

python scripts/compose.py
Vaqtlar = kompozitsiya soniyasi = aroll.mp4 vaqti. So'z vaqtlari analysis/tr2_uz.json (sinxron ovozdan).
Uslub manbalari: design-library/uslub-01..10 (INDEX.md).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 43.1

# ---------- kameralar (prep.py SHOTS bilan bir xil) ----------
SHOTS = [(0.0, 3.633, 1.0), (3.633, 9.333, 1.35), (9.333, 12.6, 1.8), (12.6, 20.0, 1.3), (20.0, 23.1, 1.0),
         (23.1, 25.1, 1.8), (25.1, 30.133, 1.35), (30.133, 34.8, 1.7), (34.8, 39.5, 1.35), (39.5, 43.1, 1.0)]

# ---------- [ subtitr ]: (boshi, oxiri, matn, joy) — joy: "" pastki, "up" split paytida yuqori yarmda ----------
CAPS = [
    (0.05, 1.27, "Instagramda blogini", ""),
    (3.71, 5.15, "Kursingizga yozilmoqchi", "up"),
    (5.17, 5.90, "bo‘lgan o‘quvchi", "up"),
    (25.64, 26.95, "Shuning uchun ekspert kontentlarini", "up"),
    (26.98, 28.06, "ko‘p qo‘yishni to‘xtatib,", "up"),
    (30.10, 31.22, "Sababi, inson sizga", "up"),
    (31.24, 32.38, "ustoz sifatida ishonsa,", "up"),
    (32.74, 33.86, "kurslaringizni sotishda", ""),
    (33.88, 34.72, "qiynalmaysiz.", ""),
    (34.74, 35.80, "Agar inson sizni", ""),
    (35.82, 37.18, "ustoz sifatida tanlasa,", ""),
]

# ---------- sarlavha bloklari (04/08/10): (id, boshi, oxiri, [(tur, [(so'z, t)])]) ----------
HEADS = [
    ("h-hook", 1.29, 3.58, [
        ("sm", [("ustoz", 1.31), ("sifatida", 1.59), ("yuritadiganlar", 1.95)]),
        ("cream", [("buni", 2.59), ("bilishmaydi.", 3.13)]),
    ]),
    ("h-share", 17.50, 19.95, [
        ("sm", [("Shu", 17.52), ("haqida", 17.80), ("ko‘proq", 18.08)]),
        ("cream", [("blogingizda", 18.38), ("ulashing.", 18.80)]),
    ]),
    ("h-shax", 28.10, 30.05, [
        ("sm", [("O‘z", 28.14)]),
        ("cream2", [("shaxsiyatingizni", 28.66), ("oching.", 29.18)]),
    ]),
]

# ---------- shisha ro'yxat (09/08) ----------
LIST = [("q1", 13.20, 1140, "01", "Qadriyatlaringiz"), ("q2", 14.26, 1300, "02", "Nimalarni yoqtirasiz"),
        ("q3", 15.56, 1460, "03", "Sohaga qanday kelgansiz")]
LIST_END = 17.40

# ---------- split-ekran B-roll ----------
SPLITS = [("b1_phone", 3.66, 5.93), ("b2_vlog", 25.62, 28.06), ("b3_mentor", 30.14, 32.38)]

# ---------- o'tishlar ----------
FLASH = [3.633, 12.6, 25.1, 39.5]
LEAK = [20.0, 34.8]

# ---------- SFX: (fayl, hodisa, nutqqa nisbatan dB) — referens "ovoz lug'ati" ----------
SFX_EVENTS = [
    ("whoosh_deep_impact.wav", 0.50, -12), ("impact-bass-1.mp3", 1.31, -9),
    ("click-soft.mp3", 1.95, -14), ("click-soft.mp3", 2.59, -14),
    ("long_pop.wav", 5.97, -12), ("select_click.wav", 7.45, -13), ("error.mp3", 7.62, -16), ("click-soft.mp3", 8.60, -13),
    ("whoosh_deep_impact.wav", 9.35, -10), ("impact-bass-1.mp3", 10.79, -7), ("camera_shutter.wav", 11.29, -13),
    ("long_pop.wav", 13.22, -13), ("long_pop.wav", 14.28, -13), ("long_pop.wav", 15.58, -13),
    ("sweep_small.wav", 13.75, -18), ("sweep_small.wav", 14.81, -18), ("sweep_small.wav", 16.11, -18),
    ("click-soft.mp3", 18.80, -13),
    ("explainer_pop_whoosh.wav", 20.07, -15), ("explainer_pop_whoosh.wav", 20.27, -15), ("whoosh-short.mp3", 21.50, -16),
    ("camera_shutter.wav", 23.10, -10), ("impact-bass-1.mp3", 23.11, -10), ("hard_pop_click.wav", 24.22, -13),
    ("click-soft.mp3", 28.66, -14), ("impact-bass-1.mp3", 29.18, -12),
    ("camera_shutter.wav", 30.133, -13), ("sweep_small.wav", 32.40, -15), ("correct_tone.wav", 33.92, -16),
    ("ping.mp3", 37.24, -14), ("ping.mp3", 37.60, -14), ("ping.mp3", 37.88, -14), ("ping.mp3", 38.28, -14),
    ("sweep_small.wav", 39.58, -15), ("select_click.wav", 42.28, -11), ("pop.mp3", 42.62, -10), ("sparkle.mp3", 42.70, -18),
    ("whoosh_deep_impact.wav", 42.95, -16),
] + [(f, t, -11) for t in FLASH for f in ("whoosh_fast_transition.wav",)] \
  + [("camera_shutter.wav", t + 0.01, -9) for t in FLASH] \
  + [("air_woosh.wav", t, -15) for t in LEAK] \
  + [("sweep_small.wav", a + 0.06, -15) for _, a, _ in SPLITS] \
  + [("key-press.mp3", 32.50 + i * 0.17, -13 - i * 0.3) for i in range(8)]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def caps_html():
    return "\n      ".join(
        f'<div id="cap{i}" class="clip cap {pos}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="20">'
        f'<span class="br">[</span> {esc(t)} <span class="br">]</span></div>' for i, (a, b, t, pos) in enumerate(CAPS))


def heads_html():
    out = []
    for hid, a, b, lines in HEADS:
        rows = "".join(f'<div class="row {k}">' + "".join(f'<span class="w" id="{hid}-{r}-{j}">{esc(w)}</span>'
                                                          for j, (w, _) in enumerate(ws)) + "</div>" for r, (k, ws) in enumerate(lines))
        out.append(f'<div id="{hid}" class="clip head" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="30">'
                   f'<div class="head-in">{rows}</div></div>')
    return "\n      ".join(out)


def list_html():
    return "\n      ".join(
        f'<div id="{i}" class="clip li-slot" data-start="{a:.3f}" data-duration="{LIST_END - a:.3f}" data-track-index="31" style="top:{y}px">'
        f'<div class="li"><span class="li-n">{n}</span><span class="li-t">{esc(t)}</span>'
        f'<svg class="li-c" viewBox="0 0 24 24" aria-hidden="true"><path class="draw gold" pathLength="1" d="M4 12.5l5 5L20 6.5"/></svg></div></div>'
        for i, a, y, n, t in LIST)


def splits_html():
    out = []
    for k, (slot, a, b) in enumerate(SPLITS):
        out.append(f'<div id="split{k}" class="split"><video id="br{k}" class="clip" src="assets/broll/{slot}.mp4" '
                   f'data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="6" muted playsinline></video></div>')
        out.append(f'<div id="div{k}" class="clip divider" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="7"><div class="div-in"></div></div>')
    return "\n      ".join(out)


def fx_html():
    out = [f'<div id="flash{i}" class="fx" data-composition-id="editorial-flash-overlay" data-composition-src="compositions/editorial-flash-overlay.html" '
           f'data-start="{t - .398:.3f}" data-duration="0.6" data-width="1080" data-height="1920" data-track-index="{40 + i}"></div>' for i, t in enumerate(FLASH)]
    out += [f'<div id="leak{i}" class="fx" data-composition-id="organic-light-leak-overlay" data-composition-src="compositions/organic-light-leak-overlay.html" '
            f'data-start="{t - .32:.3f}" data-duration="1.0" data-width="1080" data-height="1920" data-track-index="{46 + i}"></div>' for i, t in enumerate(LEAK)]
    return "\n      ".join(out)


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>',
           f'<audio id="bgm" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="0.34"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX_EVENTS, key=lambda e: e[1])):
        m = meta["sfx"][f]
        st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{60 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def timeline_js():
    js = []
    for hid, a, b, lines in HEADS:
        for r, (k, ws) in enumerate(lines):
            for j, (w, t) in enumerate(ws):
                d = 0.75 if k.startswith("cream") else 0.62   # silliq: references/smooth-motion.md
                js.append(f'tl.fromTo("#{hid}-{r}-{j}",{{opacity:0,y:40,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{d},ease:"expo.out"}},{max(a, t - 0.08):.3f});')
        js.append(f'tl.to("#{hid} .head-in",{{opacity:0,y:-16,filter:"blur(8px)",duration:0.4,ease:"power2.inOut"}},{b - 0.42:.3f});')
    for i, (a, b, t, pos) in enumerate(CAPS):
        js.append(f'tl.fromTo("#cap{i}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.2,ease:"power2.out"}},{a:.3f});')
        js.append(f'tl.to("#cap{i}",{{opacity:0,duration:0.18,ease:"power2.in"}},{b - 0.19:.3f});')
    for i, a, y, n, t in LIST:
        js.append(f'tl.fromTo("#{i} .li",{{y:150,opacity:0,filter:"blur(12px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:0.9,ease:"expo.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#{i} .draw",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.4,ease:"power2.inOut"}},{a + 0.55:.3f});')
        js.append(f'tl.to("#{i} .li",{{opacity:0,scale:0.96,duration:0.2,ease:"power2.in"}},{LIST_END - 0.22:.3f});')
    for k, (slot, a, b) in enumerate(SPLITS):
        js.append(f'split("#split{k}","#div{k}",{a:.3f},{b:.3f});')
    # kamera: har kadrda sekin "nafas" push (04/09), kesimlar prep'da virtual kamera bilan
    for i, (a, b, z) in enumerate(SHOTS):
        js.append(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.045,duration:{b - a - 0.002:.3f},ease:"sine.inOut",immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
    return "\n      ".join(js)


STAR = ('<svg viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.3L12 17.1l-5.7 3.1 1.2-6.3L2.8 9.5l6.4-.8z"/></svg>')
HEART = ('<svg viewBox="0 0 24 24"><path fill="#ff5a6e" d="M12 21.3 10.6 20C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 '
         '3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.6 11.5L12 21.3z"/></svg>')
CARDS = [("c0", "r0", "4 034", 20.05, 21.50, 150), ("c1", "r1", "1 247", 20.25, 21.60, 570),
         ("c2", "r2", "135", 21.50, 23.00, 150), ("c3", "r3", "67", 21.60, 23.00, 570)]
TOASTS = [37.24, 37.60, 37.88, 38.28]
CAP_IC = ('<svg viewBox="0 0 24 24"><path d="M2 9l10-5 10 5-10 5z" fill="#16191c"/><path d="M6 11.2V16c0 1.4 2.7 3 6 3s6-1.6 6-3v-4.8" '
          'fill="none" stroke="#16191c" stroke-width="2"/></svg>')


def cards_html():
    # video vaqtli (clip), o'rovchi karta vaqtsiz — ko'rinishini kirish/chiqish tweenlari boshqaradi
    return "\n      ".join(
        f'<div id="{cid}" class="card" style="left:{x}px"><div class="card-in">'
        f'<video id="{cid}-v" class="clip" src="assets/ig/{src}.mp4" data-start="{a:.3f}" data-duration="{b - a + 0.1:.3f}" '
        f'data-track-index="34" muted playsinline></video>'
        f'<div class="likes">{HEART}{likes}</div></div></div>' for cid, src, likes, a, b, x in CARDS)


def toasts_html():
    return "\n      ".join(
        f'<div id="t{i}" class="clip toast" data-start="{t:.3f}" data-duration="{39.40 - t:.3f}" data-track-index="37" style="top:{1040 + i * 150}px">'
        f'<div class="t-in glass"><div class="t-ic">{CAP_IC}</div><div class="t-tx"><b>Yangi o‘quvchi yozildi</b>'
        f'<span>Kontent marketing kursi</span></div><div class="t-time">hozir</div></div></div>' for i, t in enumerate(TOASTS))


def carved_bgm():
    f = os.path.join(ROOT, "scripts", "bgm_carved.html")
    return open(f, encoding="utf-8").read() if os.path.exists(f) else None


def build():
    tpl = open(os.path.join(ROOT, "scripts", "index.tpl.html"), encoding="utf-8").read()
    html = (tpl.replace("{{CAPS}}", caps_html()).replace("{{HEADS}}", heads_html()).replace("{{LIST}}", list_html())
            .replace("{{SPLITS}}", splits_html()).replace("{{FX}}", fx_html()).replace("{{AUDIO}}", audio_html())
            .replace("{{TIMELINE}}", timeline_js()).replace("{{DUR}}", str(DUR))
            .replace("{{STARS}}", STAR * 5).replace("{{CARDS}}", cards_html()).replace("{{TOASTS}}", toasts_html()))
    keep = carved_bgm()
    if keep:
        html = re.sub(r'<audio id="bgm".*?</audio>', lambda _: keep, html, count=1, flags=re.S)
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html), "bayt")


if __name__ == "__main__":
    build()
