"""hf/index.html — "Gastro-kritik" (sho'rva sharhi), premium oziq-ovqat jurnali uslubi.

python scripts/compose_v2.py
Krem/oltin, Playfair Display italic + Inter. Letterbox ochilishi, sarlavha idish ORTIDA, makro go'shtga ingichka izoh chiziqlari,
piyoz kritik kartasi, jimlikda tezlik-rampa + light leak, hukm sarlavhasi, xulosa kartasi. Hamma tween silliq (overshootsiz).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 27.585
CUTS = [0, 6.2, 11.75, 16.6, 18.6, 20.7, 22.7, DUR]
LEAK = [18.45, 20.55]
SFX = [("air_woosh.wav", 0.35, -20), ("sweep_small.wav", 3.70, -21), ("sweep_small.wav", 6.30, -21),
       ("click-soft.mp3", 8.05, -18), ("click-soft.mp3", 9.90, -18), ("sweep_small.wav", 11.90, -21),
       ("sweep_small.wav", 12.40, -22), ("air_woosh.wav", 18.45, -21), ("air_woosh.wav", 20.55, -21),
       ("whoosh_deep_impact.wav", 22.72, -21), ("sweep_small.wav", 25.32, -21), ("correct_tone.wav", 26.10, -23)]


def audio_html():
    meta = json.load(open(os.path.join(ROOT, "analysis", "sfx_meta.json")))
    out = [f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>']
    for i, (f, t, rel) in enumerate(sorted(SFX, key=lambda e: e[1])):
        m = meta["sfx"][f]; st = max(0, t - m["peak_at"]); d = min(m["dur"], DUR - st)
        vol = min(1.0, 10 ** ((meta["voice_rms_db"] + rel - m["rms_db"]) / 20))
        out.append(f'<audio id="sfx{i}" src="assets/sfx/{f}" data-start="{st:.3f}" data-duration="{d:.3f}" data-track-index="{60 + i}" data-volume="{vol:.3f}"></audio>')
    return "\n      ".join(out)


def cam_js():
    js = []
    for i in range(len(CUTS) - 1):
        a, b = CUTS[i], CUTS[i + 1]
        z0, z1 = (1.0, 1.045) if i % 2 == 0 else (1.045, 1.0)
        js.append(f'tl.fromTo("#cam",{{scale:{z0}}},{{scale:{z1},duration:{b - a - 0.004:.3f},ease:"sine.inOut",immediateRender:{"true" if i == 0 else "false"}}},{a:.3f});')
    return "\n      ".join(js)


def leaks_html():
    return "\n      ".join(
        f'<div id="leak{i}" class="fx" data-composition-id="organic-light-leak-overlay" data-composition-src="compositions/organic-light-leak-overlay.html" '
        f'data-start="{t - 0.35:.3f}" data-duration="1.0" data-width="1080" data-height="1920" data-track-index="{40 + i}"></div>' for i, t in enumerate(LEAK))


HTML = r'''<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Gastro-kritik</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Playfair"; src: url("assets/fonts/PlayfairDisplay-var.ttf"); font-weight: 400 900; font-style: normal; }
      @font-face { font-family: "Playfair"; src: url("assets/fonts/PlayfairDisplay-Italic-var.ttf"); font-weight: 400 900; font-style: italic; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/Inter-var.ttf"); font-weight: 100 900; }
      :root { --cream: #f8efdc; --gold: #e3b873; --coral: #ef8a5b; --ink: #fbf7f0; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0b0907; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #0b0907; font-family: "Inter", sans-serif; }
      #cam { position: absolute; inset: 0; transform-origin: 50% 46%; }
      #aroll, #bowl { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .shade-t { position: absolute; left: 0; right: 0; top: 0; height: 520px; background: linear-gradient(180deg, rgba(10,8,6,.55), rgba(10,8,6,0)); pointer-events: none; }
      .shade-b { position: absolute; left: 0; right: 0; bottom: 0; height: 640px; background: linear-gradient(0deg, rgba(10,8,6,.62), rgba(10,8,6,0)); pointer-events: none; }
      .lb { position: absolute; left: 0; right: 0; height: 240px; background: #0b0907; }
      #lbt { top: 0; transform-origin: 50% 0; } #lbb { bottom: 0; transform-origin: 50% 100%; }
      .fx { position: absolute; inset: 0; pointer-events: none; }
      .caps { font-weight: 600; font-size: 28px; letter-spacing: .38em; color: var(--gold); text-transform: uppercase; }
      .sh { text-shadow: 0 4px 30px rgba(0,0,0,.45), 0 1px 3px rgba(0,0,0,.4); }

      /* huk: sarlavha idish ortida */
      #kick { position: absolute; left: 0; right: 0; top: 420px; text-align: center; padding-left: .38em; color: #fff3df; text-shadow: 0 2px 14px rgba(0,0,0,.55); }
      #title { position: absolute; left: 0; right: 0; top: 470px; padding-top: 0; text-align: center; font: italic 700 290px/1 "Playfair", serif; color: var(--cream);
        letter-spacing: -0.03em; text-shadow: 0 10px 50px rgba(0,0,0,.35); }

      /* bob yorlig'i */
      .chap { position: absolute; left: 72px; display: flex; align-items: center; gap: 22px; }
      .chap .n { font: italic 600 74px/1 "Playfair", serif; color: var(--gold); }
      .chap .rl { width: 90px; height: 2px; background: var(--gold); transform-origin: 0 50%; }
      .chap .t { font-weight: 600; font-size: 34px; letter-spacing: .32em; color: var(--ink); }
      .chap .s { display: block; font: italic 400 36px/1.2 "Playfair", serif; letter-spacing: 0; color: rgba(251,247,240,.82); margin-top: 8px; }

      /* makro izohlari */
      .co { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none; overflow: visible; }
      .co line { stroke: var(--cream); stroke-width: 2.5; stroke-dasharray: 1; stroke-dashoffset: 1; }
      .dot { position: absolute; width: 30px; height: 30px; margin: -15px 0 0 -15px; border-radius: 50%; border: 3px solid var(--cream);
        box-shadow: 0 0 0 6px rgba(248,239,220,.22), 0 2px 10px rgba(0,0,0,.4); }
      .dot i { position: absolute; inset: 7px; border-radius: 50%; background: var(--cream); }
      .lab { position: absolute; padding: 18px 26px 20px; border-radius: 18px; background: rgba(16,12,9,.52); border: 1.5px solid rgba(248,239,220,.32);
        backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); }
      .lab small { display: block; font-weight: 600; font-size: 22px; letter-spacing: .3em; color: var(--gold); }
      .lab b { display: block; margin-top: 6px; font: italic 600 46px/1.1 "Playfair", serif; color: var(--cream); white-space: nowrap; }

      /* piyoz kartasi */
      #card { position: absolute; left: 60px; right: 60px; top: 1220px; }
      .cd { border-radius: 36px; padding: 34px 40px 36px; background: rgba(16,12,9,.55); border: 1.5px solid rgba(248,239,220,.28);
        backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); box-shadow: 0 30px 70px rgba(0,0,0,.4); }
      .cd-h { display: flex; justify-content: space-between; align-items: baseline; }
      .cd-h b { font: italic 600 70px/1 "Playfair", serif; color: var(--cream); }
      .cd-h span { font-weight: 600; font-size: 30px; letter-spacing: .24em; color: var(--coral); text-transform: uppercase; }
      .tr { position: relative; height: 12px; border-radius: 6px; background: rgba(255,255,255,.14); margin-top: 26px; }
      .tr i { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 6px; background: linear-gradient(90deg, var(--gold), var(--coral)); transform-origin: 0 50%; }
      .tr em { position: absolute; right: -6px; top: 50%; width: 26px; height: 26px; margin-top: -13px; border-radius: 50%; background: var(--coral); box-shadow: 0 0 22px var(--coral); }
      .ends { display: flex; justify-content: space-between; margin-top: 14px; font-weight: 500; font-size: 24px; color: rgba(251,247,240,.6); letter-spacing: .06em; }
      #q { position: absolute; left: 70px; right: 70px; top: 1560px; font: italic 500 50px/1.25 "Playfair", serif; color: var(--ink); }
      #q .w { display: inline-block; }

      /* rampa yozuvi */
      #taste { position: absolute; left: 0; right: 0; top: 1640px; text-align: center; }

      /* hukm */
      #verd { position: absolute; left: 0; right: 0; top: 1240px; text-align: center; }
      #verd .l1 { font: italic 500 84px/1.1 "Playfair", serif; color: var(--ink); }
      #verd .l2 { font: italic 700 190px/1.12 "Playfair", serif; color: var(--cream); letter-spacing: -0.02em; margin-top: 6px; }

      /* xulosa kartasi */
      #fin { position: absolute; left: 0; right: 0; top: 1180px; display: flex; justify-content: center; }
      .fc { width: 920px; border-radius: 40px; padding: 44px 50px 46px; background: rgba(16,12,9,.62); border: 1.5px solid rgba(227,184,115,.45);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); text-align: center; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .fc .rl2 { width: 120px; height: 2px; background: var(--gold); margin: 24px auto; transform-origin: 50% 50%; }
      .fc p { font: italic 500 58px/1.18 "Playfair", serif; color: var(--cream); }
      .fc p b { font-weight: 700; color: #fff; }
      .fc .sig { margin-top: 24px; font-weight: 500; font-size: 26px; letter-spacing: .3em; color: rgba(251,247,240,.6); }
      #black { position: absolute; inset: 0; background: #0b0907; opacity: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{DUR}}" data-width="1080" data-height="1920">
      <div id="cam">
        <video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{{DUR}}" data-track-index="0" muted playsinline></video>
        <div id="kick" class="clip caps sh" data-layout-allow-overlap data-start="0.20" data-duration="3.30" data-track-index="1">Gastro · sharh</div>
        <div id="title" class="clip" data-start="0.20" data-duration="3.30" data-track-index="2">Sho‘rva</div>
        <video id="bowl" class="clip" src="assets/subject_bowl.webm" data-start="0" data-duration="3.60" data-track-index="3" muted playsinline></video>
      </div>
      <div class="shade-t"></div><div class="shade-b"></div>
      {{LEAKS}}

      <div id="ch1" class="clip chap sh" data-start="3.60" data-duration="2.55" data-track-index="20" style="top:1600px">
        <span class="n">01</span><span class="rl"></span><span class="t">SHO‘RVA<span class="s">birinchi taassurot</span></span></div>
      <div id="ch2" class="clip chap sh" data-start="6.25" data-duration="5.45" data-track-index="21" style="top:250px">
        <span class="n">02</span><span class="rl"></span><span class="t">GO‘SHT</span></div>
      <div id="ch3" class="clip chap sh" data-start="11.80" data-duration="4.75" data-track-index="22" style="top:250px">
        <span class="n">03</span><span class="rl"></span><span class="t">PIYOZ</span></div>

      <div id="co1" class="clip" data-start="7.85" data-duration="3.85" data-track-index="23">
        <svg class="co"><line pathLength="1" x1="430" y1="980" x2="300" y2="700"/></svg>
        <div class="dot" style="left:430px;top:980px"><i></i></div>
        <div class="lab sh" style="left:90px;top:560px"><small>GO‘SHT</small><b>presda mayda to‘g‘ralgan</b></div>
      </div>
      <div id="co2" class="clip" data-start="9.70" data-duration="2.00" data-track-index="24">
        <svg class="co"><line pathLength="1" x1="660" y1="1180" x2="760" y2="1430"/></svg>
        <div class="dot" style="left:660px;top:1180px"><i></i></div>
        <div class="lab sh" style="right:80px;top:1440px"><small>KO‘RINISHI</small><b>piyozga o‘xshab ketgan</b></div>
      </div>

      <div id="card" class="clip" data-start="12.00" data-duration="4.55" data-track-index="25">
        <div class="cd"><div class="cd-h"><b>Piyoz</b><span>juda ko‘p</span></div>
          <div class="tr"><i id="mt"></i><em id="me"></em></div><div class="ends"><span>kam</span><span>me’yor</span><span>ko‘p</span></div></div>
      </div>
      <div id="q" class="clip sh" data-start="12.20" data-duration="4.35" data-track-index="26"><span class="w" id="q0">Ko‘pchilik</span> <span class="w" id="q1">piyozdan</span> <span class="w" id="q2">to‘yib</span> <span class="w" id="q3">ketgan</span> <span class="w" id="q4">bo‘lishi</span> <span class="w" id="q5">mumkin.</span></div>

      <div id="taste" class="clip caps sh" data-start="16.70" data-duration="1.90" data-track-index="27">· tatib ko‘ramiz ·</div>

      <div id="verd" class="clip sh" data-start="22.72" data-duration="2.55" data-track-index="28"><div class="l1" id="v1" data-layout-allow-overlap>Piyozsiz —</div><div class="l2" id="v2" data-layout-allow-overlap>bo‘lmaydi.</div></div>

      <div id="fin" class="clip" data-start="25.30" data-duration="2.285" data-track-index="29">
        <div class="fc" id="fcd"><div class="caps">Xulosa</div><div class="rl2" id="frl"></div>
          <p>Go‘shti mayda, piyozi ko‘p —<br><b>lekin piyozsiz bo‘lmaydi.</b></p><div class="sig">SHO‘RVA · SHARH</div></div>
      </div>

      <div id="lbt" class="lb"></div><div id="lbb" class="lb"></div>
      <div id="black"></div>
      {{AUDIO}}
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.to({}, { duration: {{DUR}} }, 0);
      tl.set("#cam", { filter: "blur(0px) brightness(1)" }, 0);
      {{CAM}}

      // letterbox ochiladi (kino)
      tl.fromTo(["#lbt", "#lbb"], { scaleY: 1 }, { scaleY: 0, duration: 1.6, ease: "power2.inOut" }, 0.25);
      // sarlavha idish ortidan ko'tariladi
      tl.fromTo("#title", { opacity: 0, y: 140, scale: 1.06, filter: "blur(18px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 1.1, ease: "expo.out" }, 0.45);
      tl.fromTo("#kick", { opacity: 0, y: 20, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.8, ease: "expo.out" }, 0.9);
      tl.to(["#title", "#kick"], { opacity: 0, y: -30, filter: "blur(12px)", duration: 0.55, ease: "power2.inOut" }, 2.95);

      function chap(id, t, out) {
        tl.fromTo(id + " .n", { opacity: 0, x: -30, filter: "blur(10px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, t);
        tl.fromTo(id + " .rl", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.inOut" }, t + 0.12);
        tl.fromTo(id + " .t", { opacity: 0, x: -16, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, t + 0.22);
        tl.to(id + " > *", { opacity: 0, filter: "blur(8px)", duration: 0.5, ease: "power2.inOut" }, out - 0.5);
      }
      chap("#ch1", 3.62, 6.15); chap("#ch2", 6.28, 11.70); chap("#ch3", 11.82, 16.55);

      function callout(id, t, out) {
        tl.fromTo(id + " .dot", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, t);
        tl.fromTo(id + " line", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.55, ease: "power2.inOut" }, t + 0.15);
        tl.fromTo(id + " .lab", { opacity: 0, y: 16, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.65, ease: "expo.out" }, t + 0.45);
        tl.to(id + " > *", { opacity: 0, filter: "blur(8px)", duration: 0.5, ease: "power2.inOut" }, out - 0.5);
      }
      callout("#co1", 7.87, 11.70); callout("#co2", 9.72, 11.70);

      // piyoz kartasi: o'lchagich me'yordan oshib to'ladi
      tl.fromTo("#card .cd", { opacity: 0, y: 120, filter: "blur(14px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.8, ease: "expo.out" }, 12.02);
      tl.fromTo("#mt", { scaleX: 0 }, { scaleX: 1, duration: 1.6, ease: "power2.inOut" }, 12.4);
      tl.fromTo("#me", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, 13.85);
      tl.to("#card .cd", { opacity: 0, y: -16, filter: "blur(8px)", duration: 0.5, ease: "power2.inOut" }, 16.05);
      [["#q0", 12.87], ["#q1", 14.01], ["#q2", 14.93], ["#q3", 15.41], ["#q4", 15.73], ["#q5", 16.17]].forEach(([id, t]) =>
        tl.fromTo(id, { opacity: 0, y: 20, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "expo.out" }, t - 0.08));
      tl.to("#q", { opacity: 0, filter: "blur(8px)", duration: 0.45, ease: "power2.inOut" }, 16.15);

      // tatib ko'rish
      tl.fromTo("#taste", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.6, ease: "sine.inOut" }, 16.75);
      tl.to("#taste", { opacity: 0, duration: 0.6, ease: "sine.inOut" }, 18.0);

      // hukm: fon xiralashadi, katta kursiv
      tl.fromTo("#cam", { filter: "blur(0px) brightness(1)" }, { filter: "blur(6px) brightness(0.62)", duration: 0.7, ease: "sine.inOut", immediateRender: false }, 22.6);
      tl.fromTo("#v1", { opacity: 0, y: 30, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, 22.72);
      tl.fromTo("#v2", { opacity: 0, y: 40, scale: 1.08, filter: "blur(18px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.9, ease: "expo.out" }, 23.6);
      tl.to("#verd > *", { opacity: 0, y: -20, filter: "blur(10px)", duration: 0.5, ease: "power2.inOut" }, 24.8);

      // xulosa kartasi
      tl.fromTo("#fcd", { opacity: 0, y: 120, scale: 0.96, filter: "blur(14px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.9, ease: "expo.out" }, 25.32);
      tl.fromTo("#frl", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.inOut" }, 25.7);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }, 26.98);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''


if __name__ == "__main__":
    html = (HTML.replace("{{DUR}}", str(DUR)).replace("{{CAM}}", cam_js()).replace("{{LEAKS}}", leaks_html()).replace("{{AUDIO}}", audio_html()))
    open(os.path.join(ROOT, "hf", "index.html"), "w", encoding="utf-8").write(html)
    print("index.html yozildi:", len(html))
