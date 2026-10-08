# Saboqlar va tuzoqlar (real loyihalardan)

## Sinxron (eng muhim)
- Foydalanuvchining birlashtirish vositasi **har safar** ovozni klip chegaralarida kechiktiradi (0→+129 ms, 0→+100 ms).
  Birlashtirilgan faylni manba qilma. Asl kamera faylini top (odatda `Downloads/C####.MP4`), qism oraliqlarini nomlardan ol
  (`1-qism_0-32.4_0-45.mp4` = 32.4–45.0 s) va `prep.py` bilan tasvir+ovozni BIRGA kes.
- Asl fayl yo'q bo'lsa: nutqni har kesilgan klipning O'Z ovozidan, klip tasviri boshlanadigan joyga qo'yib yig'
  (T_k = oldingi kadrlar yig'indisi × kadr davomiyligi).
- Tekshiruv: `av_check.py`. Lab-harakat energiyasi korrelyatsiyasi ishonchsiz (qo'l harakati) — ishlatma.
- Manba `start_time` (masalan 0.0213 s) va 29.97→30 fps ≤1 kadr siljish beradi — sezilmaydi.

## Transkript (o'zbek, shevalar)
- `scripts/tr.py <wav16k> <out.json> uz|kk|tr` (large-v3, int8_float16, CUDA; env `HF_CT=int8_float16`,
  `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`). Uchala rejimni solishtirib adabiy o'zbekchaga tikla; ishonchsiz joylarni
  foydalanuvchiga ❓ bilan ko'rsat. JSON: so'zlar RO'YXATI `[{"text","start","end"}]` (+ `<nom>-segments.json`); video-use uchun `{"words": [...]}` ga o'ra (ref_analyze.py qiladi).
- Xotira: large-v3 ~4.4 GB commit; `Get-Counter '\Memory\Commit Limit','\Memory\Committed Bytes'`.

## HyperFrames
- `snapshot --at a,b,c --no-end --describe false` — BITTA chaqiruv (alohida chaqirsa faqat end-kadr qoladi).
- Kamera wrapper'ida ko'p `fromTo` → keyingilariga `immediateRender:false`; ketma-ket tween chegaralarini 0.002 s qisqartir.
- Video vaqtli element ICHIDA bo'lmasin: vaqtni videoga ber, o'rovchi vaqtsiz (kirish/chiqish tweeni ko'rinishni boshqaradi).
- Matn almashishi: `textContent` tween'i seek-safe emas → ikki qatlam + opacity (grid-area:1/1).
- SVG chizish: `pathLength="1"` + dasharray 1; `vector-effect:non-scaling-stroke` bilan pathLength buziladi → px dasharray (2400).
  Chizilmagan round-cap chiziq nuqta ko'rinadi → opacity 0 dan boshla.
- `check` `content_overlap` — ko'z bilan tekshir; haqiqatan to'g'ri bo'lsa `data-layout-allow-overlap` ni ELEMENTLARNING O'ZIGA qo'y.
- Sarlavha qatorlari line-height ≥1.14 + gap 14px (aks holda content_overlap).
- Render: `-w 2` + to'liq log faylga (`> log 2>&1`); `| tail` exit kodi yolg'on 0 beradi. Render oldidan eski preview'larni to'xtat (RAM).
- Render 30 MB dan katta → telefon uchun `-crf 24 -maxrate 6M` nusxa yubor.

## Bosh ortidagi so'z (text-behind-subject)
- `matte.py <t0> <t1> <nom>` (u2net_human_seg, 540x960 → 1080x1920, VP9 yuva420p). So'z boshni ~80–150 px to'sishi kerak,
  aks holda effekt ko'rinmaydi — snapshot bilan tekshir. Keng so'z uchun shrift ≤ kadr eni (8 harf ~164 px Poppins 800).
- So'z va subject video `#cam` ichida (kamera zoom'i bilan birga).

## Grading
- LOG manba: `prep.py test` — kanal persentillari (0.8/99.6) → colorlevels + curves + saturation 1.28 + teal-orange balance.
- B-roll: `broll_prep.py` warm/bw; oq-qora B-roll ichida kesim qo'yma.

## Tanlov qoidalari (foydalanuvchi)
- B-roll'da qora tanli odamlar — faqat gapda tilga olinsa. Diniy mavzuda boshi ochiq ayollar yo'q (fondagisi ham) —
  kerak bo'lsa toza bo'lakni `minterpolate` bilan sekinlashtir. Imkon bo'lsa yuzsiz kadrlar (qo'l, telefon, predmet).
- Payg'ambarimiz / muqaddas shaxslar hech qanday shaklda tasvirlanmaydi.
- Yuzga hech narsa tushmaydi (B-roll'dagi yuzga ham) — subtitrni `up`/`low` bilan ko'chir.
- ElevenLabs va kie.ai ishlatilmaydi (foydalanuvchi ruxsatisiz). HeyGen CLI yo'q → musiqa Pixabay.

## Ucan Visa (2026-09-30) qo'shimchalari
- Tayyor eksport (Sequence) manba bo'lsa: parts=[[0,dur]], shots = mavjud kesimlar (scene>0.25), zoom 1.0; grading yengil (`"grade"` edit.json'da).
- `tr.py` chiqishidagi qatorlar oldida ko'rinmas belgi bor — `grep "^\["` ishlamaydi, `grep -a "\->"` ishlat.
- Kontur (outline) matn: `color: transparent` → check `text_not_painted`; `rgba(...,.16)` fill ber.
- 3D karusel: proxy obyekt `{k}` tween + `onUpdate` da har kartaga gsap.set (x=d*300, z=-|d|*220, rotationY=-d*34, blur) — seek-safe.
- Logo marquee: plitka rangi logo yorqinligidan (lum>0.55 → to'q plitka), oq fonli logolarda oq fonni shaffof qil.
- Brend logotipini ustun/yozuvga bo'lish: shaffof ustunlar orasidagi eng katta bo'shliqdan kesish.
- Windows konsolida `→` kabi belgilar print'da yiqiladi — skriptlarda ASCII ishlat.

## Jag' ostidagi matn (11/12/13 namunalari) — 2026-09-30
- Namuna 12 o'lchovi: matn yuz bilan vertikal 1:1 (korrelyatsiya 0.97), gorizontal ~0.5 ergashadi; matn jag'dan ~55–65 px PASTDA
  (jag' chizig'ining o'zida emas — foydalanuvchi aniq tuzatdi). Faqat oddiy gap subtitrlari; kartalar/raqamlar joyida qoladi.
- `scripts/chin_track.py`: har shot uchun ref kadrda yuz markazi + iyak y ni qo'l bilan ber (kadr varag'idan), yuz shabloni
  kadrma-kadr matchTemplate → analysis/chin.json (Gauss sigma 3 kadr). Tekshiruv: jag'ga chiziq chizib varaq ko'r.
- HTML: `.chin` elementlar #cam ichida (zoom bilan), bitta proxy tween `follow.t` 0→DUR onUpdate'da gsap.set(x,y) — seek-safe.
  Andoza: templates/*ucanvisa_v3*.
- matte.py: 1080p float niqoblar RAMni to'ldiradi → niqoblar 540x960 uint8, kadr `-ss` bilan bittadan; VP9 `-threads 2`
  (aks holda ffmpeg g'alati exit kod bilan yiqiladi).
- `data-layout-allow-overlap` harf-span'larning O'ZIGA kerak (qator div'iga emas).
- flex `gap` harf-harf span'larga bo'lingan so'zni yoyib yuboradi — gap:0.
- JAG'NING O'ZI (og'iz ochilib-yopilishi) — foydalanuvchi talabi: matn jag' bilan silliq qimirlasin. `chin_track.py` faqat bosh
  harakatini beradi; ustiga `jaw_track.py`: soqol pastki cheti (qorong'i->yorug' +gradient, 100 px tasma) + vaqt bo'yicha dinamik
  dasturlash (|dy|<=10 px/kadr, jarima 0.6) — lab chizig'iga sakrash yo'qoladi; Gauss sigma 1.6 kadr. `jaw_kymo.py <t0> <t1> out.png`
  bilan kimografda tekshir. Yon profil kamerada yoqa chizig'i (bo'yin->oq ko'ylak) kuchliroq — `DN_SHOT` bilan oynani qisqartir.

## Musiqa balandligi (Ucan Visa v5, 2026-10-01)
- Carve (strength 0.45) gapirganda musiqani qo'shimcha ~10 dB bosadi -> eski data-volume 0.34 bilan musiqa -40 LUFS, deyarli eshitilmaydi.
  O'lchov: voice va SFX ni data-volume=0 qilib `-q draft -f 5` bilan "faqat musiqa" render (1 daqiqa) -> nutq paytida nutq-musiqa farqi.
  Maqsad (foydalanuvchi 3 marta "ko'tar" dedi): musiqa ~ -19 LUFS; nutq NUTQ POLOSASIDA (300-3400 Hz) musiqadan >=14 dB (eng yomon >=10).
  Buning uchun musiqaga doimiy EQ dip (equalizer f=1700 w=1.0 g=-4) + yengil carve (0.25) - bas/zarb baland, so'zlar aniq.
  Keng polosali farq (~4 dB) aldamchi: trek energiyasi basda.
  14 dB (-27.5 LUFS) da ham "orqada yaxshi eshitilmayapti" dedi. Ucan Visa v8: bgm -15.1 LUFS (limiter), vol 1.0, carve 0.3.
  20 dB / -34..-37 LUFS da foydalanuvchi "musiqa qo'yilmagan" dedi — juda past! Ucan Visa v7: bgm -16.7 LUFS (limiter), vol 0.7, carve 0.3.
- Faqat ovoz o'zgarsa video qayta render qilinmaydi: `-q draft -f 5` ovoz o'tishi + eski raw tasvir `-map 0:v -map 1:a -c:v copy`.
- 100 ms oynali "pauza vs nutq" o'lchovi ishonchsiz (nutq qoldig'i) — faqat-musiqa render bilan o'lcha.
- Musiqa kesimi: trekdagi qisqa to'xtash -> qaytishni asosiy urg'u so'ziga to'g'rila (to'xtash so'zdan oldingi gapga tushadi — tabiiy "build-up").

## "Shamolga o'xshash" fon ovozi (Ucan Visa v6, 2026-10-01)
- Ikki manba bo'ldi: (1) lav-mikrofondagi shamol 60–140 Hz, (2) tijoriy trekning uzluksiz 808 sub-basi (20–120 Hz) — telefonda nutq ostida g'uvillaydi.
- RNNoise/afftdn bu manbada nutqni yedi (polosalar -3..-5 dB, undoshlar 8–32%) — "ovozga tegma" talabida ishlatma.
- Ishlagani: `scripts/wind_clean.py` — nol-fazali (sosfiltfilt) 110 Hz highpass + 110–300 Hz faqat pauzalarda -12 dB
  (kalit 300–3400 Hz); 300 Hz dan yuqori signal aynan asl. Kechikish 0.00 ms. voice_master `voice_raw_clean.wav` ni oladi.
- Musiqa: `highpass=f=45:p=2,lowshelf=f=110:g=-9` — kuy/zarb qoladi. Yakuniy doimiy <110 Hz poli -28.8 -> -36.6 dBFS.
- O'lchov: yakuniy miksda median (SFX zarbalarini hisobga olmaydi); manbalarni alohida (voice/bgm*vol/SFX yig'indisi) o'lcha.

## Foydalanuvchi ko'rib chiqishi (Ucan Visa v10, 2026-10-01)
- Raqam bloki (1200+) ko'krakning past qismida "juda pas" — jag'dan ~100 px pastdan boshlansin.
- Karusel/halqa: bir nechta "sweep + to'xtash" = "joskiy". Bitta uzluksiz `sine.inOut` aylanish + alohida kattalashish.
- Logotip plitkalari ekranda uzoq turmasin (~1.5 s yetarli); pop 0.7->1 back.out(1.4) 0.6 s, stagger 0.055; ikki bosqichli overshoot yo'q.
- "Vau" sarlavha: kontrastli juftlik — Instrument Serif italic (nafis) + Anton (baland, qalin), katta raqam scale 1.55->1 + blur 22.
  Nozik serif oq ko'ylak ustida — kuchli ko'p qatlamli soya shart.
- CTA: hamma element bitta panjarada (880 px, chap chetlar bir chiziqda); oddiy italic yozuv o'rniga ikki qatlam:
  kichik harf-oralig'li CAPS yorliq + katta serif italic.
- Shrift tanlash: foydalanuvchi "vau shrift" desa — 5–6 nomzodni HAQIQIY kadrda (oq ko'ylak ustida, soya bilan) yonma-yon mock qilib tanla.
  Fraunces "oddiy", Syne 800 "juda qo'pol" deyildi; ma'qul: Playfair Display 700 italic — nafis, lekin og'ir/keng emas.
  Foydalanuvchi didi: nafis kursiv serif (Playfair/Instrument Serif) + soya; og'ir keng grotesk yoqmaydi.

## Kosmetika reytingi (uslub-24, 2026-10-02)
- **prep.py kadr yo'qotish xatosi (tuzatildi):** video kesishda kirish `-t dur` + `-frames:v` -> har shot 1 kadr kam (35 shotda 20 kadr = 333 ms
  lab-sinxron siljishi). Endi `-t dur+0.25`. Har build'dan keyin `aroll` kadr soni == round(DUR*fps) ni tekshir.
- **Bo'laklab render** (`scripts/split_render.py` loyiha shablonida): render ba'zi bo'laklarga +1 kadr qo'shadi -> join'da `trim=end_frame`
  bilan aniq kadrga kesib, bitta kodlashda concat. Ovoz renderdan emas: voice + SFX ffmpeg `adelay/amix` bilan (compose.sfx_events dan).
  Chegara tekshiruvi: final kadr vs aroll kadri (pastki 400 px) farqi — best offset 0 bo'lishi kerak.
- Hech qanday `letterSpacing` tween (lint xato: piksel sakraydi) — scale+blur ishlat.
- Kichik o'zbek brendlari logotipi: rasmiy sayt sarlavhasidagi inline SVG/`img[src*=logo]` ni brauzer panelidan `outerHTML` bilan olish ishladi
  (Bloom, M Cosmetic, IsaDora). Instagram avatar faqat 150 px (imzoli URL, kattalashtirib bo'lmaydi). Noaniq brendga logo qo'yma — nom serifda.

## Musiqa ovozni to'smasin (Storis 5k->25k, 2026-10-05)
- Foydalanuvchi: "musiqa yaxshi tanlanmagan va ekspertning ovozini to'sib qo'yyapti". Sabab: zarbli "luxury fashion" treki
  (o'rta chastotasi zich, percussive) + bgm ~-20 LUFS.
- TREK TANLASH (eshitib bo'lmaganda o'lchov bilan): Pixabay nomzodlarini yuklab, (1) nutq polosasi 300-3400 Hz ulushi
  (full'ga nisbatan; -7 dB va pastroq yaxshi), (2) "percussiveness" (100 ms RMS farqining o'rtachasi; <2 yaxshi) o'lcha.
  Ekspert/ta'lim reelida: sokin ambient / pad / yumshoq pianino, vokalsiz, zarbsiz. Zarbli fashion/trap/EDM — yo'q.
- MIKS: musiqaga keng nutq-polosa o'yig'i `equalizer=f=1200:t=o:w=2.2:g=-6` + `highpass=60` + loudnorm -25 +
  sidechaincompress (kalit = voice 300-3400 Hz, threshold 0.08, ratio 2.5, attack 60, release 500). Natija: bgm ~-27.5 LUFS,
  nutq paytida nutq-musiqa farqi (nutq polosasida) median >=19 dB, eng yomon 10% >=14 dB. Faqat-musiqa stemini
  (ducking bilan) alohida chiqarib o'lcha — "mix minus voice" SFX tufayli aldaydi.
- Bir nechta trek variantini (A/B/C) faqat ovozni qayta yig'ib, video `-c:v copy` bilan berish — tez va foydalanuvchiga tanlov.
  Ovoz `scripts/mix_audio.py` uslubida: index.html audio teglaridan voice+SFX (adelay/amix) + yangi bgm.
- Mac'da carve.mjs ishlamadi (@hyperframes/core yo'q) -> yuqoridagi ffmpeg ducking ishlatildi.

## Skill kuchaytirildi (2026-10-05, Storis tajribasidan)
- `smooth_check.py` 3 rejim: html kod tekshiruvi / vaqtlar bo'yicha kadr varaqlari / butun video yorug'lik sakrashi.
  Storis v2 da topgan xato: birinchi `filter` tween'i `to` bilan → bir kadr qora (smooth-motion.md "Tuzoq").
- `music_pick.py`: trek tanlashni eshitmasdan o'lchov bilan (nutq polosasi ulushi + zarbdorlik).
- `voice_master.py` endi kirish LUFS'iga qarab kuchaytiradi (masterlangan −12.6 LUFS manbani ezmaydi).
- `mix_audio.py` davomiylikni `<audio id="voice">` dan oladi (oldin 55.2 qattiq yozilgan edi).
- `tr.py` CUDA bo'lmasa o'zi CPU int8 ga o'tadi; `new_project.py` Mac yo'lini topadi va hamma andozalarni ko'chiradi.

## Yangi uslublarni o'rganish (2026-10-05, uslub-27..29)
- Yuklash: `yt-dlp -o "<id>.%(ext)s" --write-info-json https://www.instagram.com/reel/<id>/` (stkn parametrini olib tashla, login yo'q).
- Varaqlar: 16 s bo'laklarda `fps=2,scale=200:-1,tile=8x4` (har qator = 4 s) — drawtext ishlatma (Mac ffmpeg'da fontconfig yo'q).
  Kadrma-kadr: `-ss t -t 0.62 ... tile=9x2` → 18 kadr. Avval kontakt varaqdan VAQTNI aniq hisobla (indeks/2), keyin strip — aks holda noto'g'ri joy.
- Kesimlar: `select='gt(scene,0.25)',showinfo`. Rang: kadrdan eng to'yingan pikselni ol (kichik matnda chetga tushadi — taxminiy deb belgila).
- Manbadagi kirishlar odatda 0.17–0.3 s — STYLE.md'da o'lchovni yoz, lekin "Silliqlik moslamasi" bo'limida bizning qiymatlarni ber.
- Referensdagi film parchalari (Social Network va h.k.) — bizda ishlatilmaydi (mualliflik huquqi / Content ID), Pexels bilan almashtir.

## "Referens bilan 1 xil" so'ralganda (Storis v3 -> v4, 2026-10-05)
- v3 rad etildi: "referens videodek qilmagansan, yangicha narsa yo'q, oddiy". Sabab: uslubni faqat STYLE.md + 4 ta kontakt
  varaqdan qurdim, referens VIDEONING O'ZINI ko'rmadim -> matn pastda-chapda, kesimlar kam, urg'u turlari bir xil bo'lib qoldi.
- MAJBURIY: design-library/_src/<id>.mp4 dan 6 s li bo'laklar, 4 fps varaqlar (vaqt yozuvi bilan) chiqar va HAR bo'lakni ko'r:
  `ffmpeg -ss S -t 6 -i ref.mp4 -vf "fps=4,scale=216:-1,drawtext=...%{pts\:hms}..." | tile=8x3`. Keyin jadval tuz:
  referens elementi -> bizning qaysi gapga, qaysi vaqtga. Har element turini kamida bir marta ishlat (bitta blok turini takrorlama).
- Uslub-27 aniq parametrlari (o'lchandi): matn kadr O'RTASIDA (y ~ 900-1150, ko'krak ustida), keng kadrda markazga, profil/yaqin
  kadrda chapga; ~28 kesim / 50 s (keng <-> yaqin <-> B-roll); B-rollda RGB-siljish + halatsiya; urg'ular: kalit so'z, arvoh kichik
  matn + katta so'z*, [qavs], qo'shtirnoq, kursiv sariq, qizil cho'zilgan so'z, sochilib->yig'iluvchi qator, qizil qo'lyozma izoh.
- Bitta kamera/2 burchak bo'lsa ritm uchun: asl kadrdan x1.35 punch-in (yuz markazi pivot) + hujjatli B-roll
  (`rgbashift=rh=-5:bh=5` + gblur screen-blend 0.35 + noise 5). Oq kiyimli spiker: matnga kuchli ko'p qatlamli qora glow-soya.
- Andoza: templates/*uslub27b* (compose27b.py + index27b.tpl.html).
- Uslub-27/28 (M oila) videosida **oq fakt-karta + 3D emoji** SHART (foydalanuvchi: "ashu qismini qo'shmagansan"): har 10–15 s da
  1 ta, fakt/qadam/atama gapida. Karta oq r26, sarlavha Outfit 800 70px qora + izoh 32px kulrang, o'ng padding 118px emoji uchun,
  emoji 156px burchakdan tashqarida (right -34, top -62). Kirish 0.8 s expo.out scale 0.85->1 + blur; chiqish o'ngga push 0.6 s,
  keyingi blok chapdan kiradi. Emoji: Microsoft Fluent 3D (MIT) — raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/<Nom>/3D/<nom>_3d.png;
  tayyorlari assets/emoji/ da (chart, envelope, hook, money).
- Karta "REAL" ko'rinishi (foydalanuvchi: "realdek ko'rinishi kerak", 2026-10-05) — tekis oq vektor karta yopishtirilgandek ko'rinadi.
  Referensdan o'lchangan: ikki qavatli chegara (7px oq hoshiya + ichida och kulrang gradient #fbfaf8 -> #e6e5e2), ichki soya
  (inset 0 -4px 8px .07 + inset 1.5px chiziq), yumshoq tashqi soya (0 16px 34px .30); matn to'q kulrang #2b2b2b, sarlavha 90px 800
  (kartaga nisbatan katta, chetlar zich), izoh 40px 500 #343434 (och kulrang EMAS); emoji 214px, burchakni yopib, drop-shadow;
  emoji DOIM jonli (sine y -12 / rotation 7, 0.45 s yoyo) — qotib qolmasin; karta o'rovchisiga blur(0.35px) — video yumshoqligiga mos.
  Emoji matnni to'smasin: o'ng padding >= emoji eni - (right ofset) + 20 (bu yerda 206px). Referens bilan yonma-yon crop solishtir.
- Render 'sub_timeline_script_failure ... gsap.min.js' = CDN (jsdelivr) DNS uzilishi. Yechim: gsap.min.js lokal (assets/vendor/, new_project.py nusxalaydi), shablonda src="assets/vendor/gsap.min.js".
- CTA pill (M oila): ekspertning HAQIQIY Instagram avatari (ommaviy sahifa, login YO'Q; img alt "profile picture" — 150 px) +
  @handle + ko'k ✓ (agar tasdiqlangan bo'lsa) -> to'q-sariq to'lib CTA matni. Avatar atrofida oq + IG-pushti halqa.
- Yakun ekran rasmi: video kadrdan "frame-crop" yoki IG post muqovasi (360x640, ustida matn) — sifatsiz deb rad etildi
  ("yaxshirog'ini qo'y"). Ishlagani: `scripts/thumb_hero.py <video> <t>` — tabassumli kadrdan rembg kesma + iliq bokeh fon +
  orqa yorug'lik, yuz kartaning yuqori yarmida (Anton sarlavha pastda iyakni yopmasin).

## Uslub-27 tipografiya va animatsiya — O'LCHANGAN (v8, 2026-10-05; foydalanuvchi: "shrift, hajm, chiqish animatsiyasi referensdek emas, CapCut'dek")
- Shrift = **Outfit** (nomzodlar Urbanist/Lexend/Sora/RedHat/Jakarta/Manrope/Figtree/Onest bilan referens crop ustida solishtirildi:
  "Xalqda" kengligi ref 455 px, Outfit 470 px). Tanlashdan oldin HAR DOIM shunday mock-taqqoslash qil (analysis/fonttest/compare.jpg).
- O'lchamlar (1080 px kadr): kalit so'z 136 px 700 ls -0.02em; oq izoh 66 px 600, qator ~72 px; katta so'z ("Shunaqa") ~210 px;
  arvoh 46 px; chap blok x=110. Soya YENGIL: 0 2px 12px .42 + 0 1px 3px .35 — qalin qora glow = "CapCut" hissi, ishlatma.
- So'z kirishi: o'z joyida blur 10->0 + opacity + scale 1.04->1, ~6 kadr (0.26 s power3.out); katta so'z gorizontal cho'zilib 0.34 s.
- **Markaziy qator so'z qo'shilgan sari silliq qayta markazlashadi** (referensning asosiy "imzosi"): qator flex-center, hamma so'zlar
  joy egallaydi, qator x = (W_final - W_k)/2 -> 0, har so'zda 0.36 s power3.out. Kengliklar PIL (Outfit-var, set_variation_by_axes)
  bilan; qator MAXW dan oshsa avtomatik bo'linadi (compose27b.py: SIZE, wrap_rows, row_w).
- Qo'lyozma = **Caveat 700** (ingichka flomaster, kichik harf), Permanent Marker emas. Chiqish 0.24 s (kesimda).
- smooth_check "qisqa tween" ogohlantirishlari bu yerda ATAYLAB (referens tezligi) — overshoot/sakrash baribir yo'q.

## "Instagram dunyosi" uslubi (Storis v9, 2026-10-05) — uslub-27 nusxasi "umuman yoqmadi, kreativlik qo'sh" deyilgach
- Avval TAXMIN QILMA: AskUserQuestion bilan nima yoqmaganini + yo'nalishni so'ra, keyin 3 ta HARAKATSIZ namuna kadr (hf_mock/,
  stillar + snapshot) ko'rsat -> "boshla" -> to'liq qurish. Bu bir urinishda tasdiq oldi.
- Mavzuga bog'langan UI = eng kuchli kreativ: storis haqida video -> butun video IG ichida (progress-bar=bo'limlar, header avatar+@handle ✓,
  IG matn stikerlari qora/oq/gradient bloklar Inter 800, "ko'rishlar" paneli sanoq bilan, savol-stikeri qadam kartalari, Direct chat,
  savol qutisi typewriter, 3D storis karuseli, izohlar oynasi "+", oxirida Direct'da sovg'a).
- KUB o'tishi sinxronsiz: ketayotgan yuz = kesimdan 0.06 s oldingi muzlatilgan kadr (img), kelayotgan = jonli #cam (rotationY 90->0,
  origin chap). Ikkalasi 0.5 s power2.inOut.
- PiP (dumaloq video xabar): #cam ni o'zi kichraytir: transformOrigin = yuz markazi (fromTo "from" ichida — kub boshqa origin qo'ygan
  bo'ladi!), scale .52 + x/y + clipPath circle(26%); gradient halqa DOM'da #cam DAN OLDIN (ustida bo'lsa ichidagi qora doira videoni yopadi).
- Andoza: templates/*instagram_world*.

## video-use bilan referens tahlili (2026-10-06)
- `scripts/ref_analyze.py` = video-use helpers (`~/video-use`: timeline_view, pack_transcripts; Python 3.9 da ishlaydi, librosa shart emas)
  + bizning whisper. video-use'ning Scribe (ElevenLabs) transkripsiyasi ISHLATILMAYDI.
- Whisper so'z chegaralari pauzalarni yeydi (so'zlar ketma-ket yopishadi) -> "pauza 0 ta", hammasi bitta fraza. Tuzatish: nutq polosasi
  energiyasi (10 ms) bo'yicha har so'zni ovozli qismiga qisqartirish; pack `--silence-threshold 0.35` (reel ritmi tez).
- O'zbek+rus aralash nutqda whisper matni buziladi — beat'larni transkript + ekrandagi subtitrlar (kontakt varaq) bilan birga aniqla.
- Kuzatuv: tez intervyu reellarida kesimlarning 2/3 qismi GAP O'RTASIDA (ko'p kamera / B-roll ustiga ovoz) — video-use'ning
  "pauzada kes" qoidasi NUTQNI kesishga tegishli; burchak almashuvi nutq o'rtasida bo'lishi normal.
- Gaplar orasidagi pauzalar butunlay olinadi (>=0.4 s pauza 1–2 ta / 50 s), temp 128–143 so'z/daq.
- UI-element kirishi = SFX zarbasi (karta, pill); kesimga SFX kam (4/17..4/23). Grafik o'tish = musiqa zarbasi kadri.

## Uslub-28 (/reel-uslub, Storis v10, 2026-10-06)
- Shrift = **General Sans** (Fontshare, bepul): 17 nomzod referens crop ustida — to'g'ri dumli y, ikki qavatli a, zich (-0.035em).
  Subtitr: L 80 px 600 / s 54 px 500 / katta 124 px / [qavs] 40 px, chapda x=60, ko'krakda; soya 0 2px 14px .45.
- "Sochilib -> joylashish" = HAR SO'Z o'zi: y ±16..32 + rotation ±2 dan blur bilan chiqadi (0.22 s), 0.26 s dan keyin 0.42 s da
  qatoriga o'tiradi. Gap oxirigacha kutish (katta ofset) = tartibsiz, o'qib bo'lmaydi.
- Marker (yashil #0A9A1A / sariq-yashil #C8D400) so'zdan 0.5 s keyin scaleX; qizil ellips 0.55 s keyin, oxiri ochiq (offset .06).
- Ritm: asl kadrlar + x1.28–1.3 yaqin plan (yuz pivot) + 2 yuzsiz B-roll -> 19 kesim (ref 17). style_compare: ritm/temp/rang OK.
- style_compare "SFX/daq" ovozdagi undoshlarni ham sanaydi; "nutq-pauza" pauzasiz videoda ma'nosiz — ikkalasini ko'z/quloq bilan baholash.
- Andoza: templates/*uslub28*.
- (v11) Foydalanuvchi: "emoji grafikalarni reallariga almashtir" — Fluent 3D emoji "multfilm"dek. Ishlagani: Pexels FOTO (oq fonda
  haqiqiy obyekt) + rembg `isnet-general-use` kesma, bbox crop, kartadan katta (h 420–440 px), burchakdan chiqib turadi, ikki qavat
  drop-shadow. Apple emoji ishlatilmaydi (litsenziya). Tayyorlari: assets/emoji/real_growth.png, real_hook.png.
- (v11) Uslub-28 subtitr kirishi O'LCHANDI (30 fps): so'z joyidan ~45 px PASTDA + vertikal blur (scaleY 1.12, blur 7) -> 0.22 s
  power2.out da joyiga; aylanish/sochilish YO'Q. Blok butun turish davomida y 0 -> -40 (ease none). Chiqish ~5 kadr blur.
  Oldingi "sochilib" talqini xato edi — har doim 30+ ketma-ket kadr strip bilan o'lcha.

## Ovqat sharhi / yuzsiz B-roll ovozli video (Video 2, "Gastro-kritik", 2026-10-06)
- Manba iPhone 4K HEVC 60 fps vertikal (rotation -90): ffmpeg avtorotatsiya qiladi. 4K = virtual kamera zaxirasi: makro 1.9x ham 1080p da tiniq.
  Andoza: templates/compose.gastro_critic.example.py + scripts/build_ramp_4k.example.py.
- **Tezlik-rampa faqat nutqsiz oraliqda** (sinxron saqlanadi): chiqish oralig'i = manba oralig'i, ichida 0.5x / ~2x / 0.5x.
  TUZOQ: `-ss X -i src -t D` + `setpts=PTS*k` sekinlashtirishda kadrlarni ko'paytirmadi (78 o'rniga 120). Ishlagani:
  `trim=duration=D,setpts=(PTS-STARTPTS)*k,fps=60` + `-fps_mode cfr -r 60 -frames:v N`. Har bo'lak kadr sonini tekshir.
- Yuzsiz ovqatda "vau": sarlavha idish ORTIDA (rembg `isnet-general-use` niqob, 30 fps VP9 alfa, 3.6 s), letterbox 240 px -> 0,
  makro kadrga ingichka izoh chiziqlari (nuqta + SVG chiziq + shisha yorliq), kritik kartasi o'lchagich bilan, rampa o'tishlarida light leak.
- (Video 2 v4) Foydalanuvchi: "sekinlashtirish qotib qolyapti, smooth bo'lsin". Sabab: 30 fps manbani 0.5x = 15 noyob kadr/s + tezlik
  pog'onali sakraydi. Yechim `scripts/smooth_ramp.example.py`: avval crop/scale, keyin `minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`,
  so'ng UZLUKSIZ tezlik egri chizig'i (uchlarida 1x, Gauss "sekin cho'qqi" 0.3x, qolgan joyda biroz tez, o'rtacha 1x -> chiqish oralig'i =
  manba oralig'i, sinxron saqlanadi). Sekin cho'qqini manbadagi montaj KESIMIGA qo'yma (interpolyatsiya kesimni "suradi") — kesimdan keyingi harakatga.
  Har doim ikkinchi variant: rampasiz (1x) — foydalanuvchi tanlaydi.

## "Jurnal muqovasi" (Video 3, marketing selfi, 2026-10-06)
- Oddiy fon (devor) + bitta selfi kadr = spikerni BUTUN video bo'yicha kesish (`u2net_human_seg`, niqob 30 fps -> har 2 kadrga, VP9 alfa 60 fps,
  ~10 daq / 63 s) va orqasida har bo'lim uchun ulkan Anton so'z (PIL bilan kenglikka moslab, 1000 px). Yuz hech qachon yopilmaydi.
  Lint `text_occluded` — ataylab: `data-layout-allow-occlusion` so'z elementlariga.
- B-roll o'rovchisi VAQTSIZ bo'lsin (`video_nested_in_timed_element` xatosi), vaqt faqat <video> da; o'rovchiga clipPath kirish/chiqish tweenlari.
- Split-ekran paytida #cam yuqoriga suriladi -> #cam ichidagi ulkan so'z kesiladi: so'zni split tugagach chiqar.
- Og'ir alfa kompozitsiya (60 fps, 63 s) `-w 3` da 77% da "Runtime.callFunctionOn timed out" (RAM) bilan yiqildi -> `-w 2 --protocol-timeout 1500000`.
- Andoza: reel-v3/scripts/compose_v3.py + index_v3.tpl.html (vaqt chizig'i siqilishi, xarita kartasi oqim nuqtalari, chiplar, to'lqinlar, "BILMAYDI." qorong'ilik).

## Yuz retushi va imlo (Video 1 v13, 2026-10-06)
- Foydalanuvchi so'rovi: "subtitrda imloviy xato bo'lmasin, yuzni retush qil". Har topshirishdan oldin HAMMA ekrandagi matnni (SUBS, kartalar,
  pill, yakun) o'zbek lotin imlosi bo'yicha tekshir: so'zlovchi aytgan shaklga mos fe'l ("chiqqanmiz", "chiqdik" emas), yangi gap bosh harf.
- `scripts/retouch.py <in> <out> 0.8`: YuNet (cv2.FaceDetectorYN, model ~/.cache/yunet/face_detection_yunet_2023mar.onnx; opencv 5 da Haar YO'Q)
  -> yuz ellipsi x YCrCb teri niqobi -> 2x bilateral + 35% mayda tuzilish qaytariladi. Kadr soni/fps o'zgarmaydi (sinxron 0 ms).
  TUZOQ: RGB<->YUV aylanishda butun kadr 2 daraja qorayadi va rang belgilari yo'qoladi -> ikkala scale'da
  `in/out_color_matrix=bt709:in/out_range=tv:flags=accurate_rnd+full_chroma_int+bitexact` + `setparams=...bt709`. YUV ni o'lchab tekshir (farq <0.1).
- Render HDR ga o'tib qotsa (log: "HDR auto-promotion triggered by <fayl>") — Pexels klipi HLG bo'lishi mumkin: broll_prep'dan keyin
  `color_transfer` ni tekshir, arib-std-b67 bo'lsa zscale+tonemap bilan bt709 ga o'tkaz.

## Imona Ahmedova uslublari (uslub-31/32, 2026-10-07)
- ref_analyze.py xatosi tuzatildi: ovozsiz so'z bo'lsa `vo[0]` IndexError (operator ustuvorligi) — endi asl vaqt olinadi.
- Gradient CAPS "to'lish": har so'z = xira qatlam + gradient qatlam (`background-clip:text`, `clip-path inset` chapdan o'ngga);
  `color:transparent` o'rniga `rgba(...,.01)` (lint `text_not_painted`). Namuna: `templates/iman_elements.html`.
- Split-podkast: `<video>` vaqtli o'rovchi ichida bo'lmasin (lint `video_nested_in_timed_element`) — o'rovchi vaqtsiz, ko'rinish `tl.set(opacity)`;
  bir xil src+start ikki video = `duplicate_media_discovery_risk` -> ikkinchi panel uchun fayl nusxasi.
- Bitta kameradan split: tepa panel zoom ~1.35× (2× faqat ko'zlar), yuz panel tepasidan ~380 px; matn ko'krak/qo'llarda.
- Referens musiqasi baland (nutq−pauza 5–13 dB) — qoida 9 bo'yicha olinmaydi; style_compare'da QOIDA deb belgilanadi.

## SAT "kerak/kerakmas" (iPhone 4K HEVC 10-bit, 2026-10-07)
- 10-bit manba (yuv420p10le) da `colorlevels` YUV ustida ishlab kadrni QORA qildi (grade_test pastki qatori qop-qora).
  Tuzatildi: prep.py da levels oldidan `format=rgb24` (skill prep.py da ham). `prep.py test` ni har doim ko'z bilan ko'r.
- Kim gapiryapti: kadr ortidagi boshlovchi + spiker savol-javobida lab varag'i (og'iz crop, 8 fps strip) bilan aniqla; pitch (~170 vs ~125 Hz) ham yordam beradi.
  Tuzilma: savolda keng 1.0, javobda 1.3 virtual kamera; kesimlar jimlikda (energiya < -70 dB nuqtalar).
- Savol-javob (quiz) "vau" formati: bosh ortida (matte_full) har mavzuning oltin chiziqli belgisi + mavzu kartasi -> hukm ✓/✕ -> ikki ustunli
  taxtaga uchadi (karta fade+scale 0.42 ustunga, chip 0.22 s keyin expo.out) — andoza reel-vau27/scripts/compose.py + index.tpl.html.
- Ro'yxat hujjatida aytilmagan mavzu nomlarini o'ylab topma — yopiq qatorlar matnsiz chiziq bo'lsin.
- Musiqa mix: threshold 0.08 da eng yomon 10% ~9 dB chiqdi; threshold 0.04 + bgm -27.5 LUFS -> median ~24 / worst ~14 dB.

## Qo'l tepasida element (SAT video 2, 2026-10-08)
- Foydalanuvchi: "qo'li bilan ko'rsatayotganda o'sha qo'lning tepasidan chiqsin". Yechim: `scripts/hand_track.py` (MediaPipe Tasks HandLandmarker,
  model ~/.cache/mp/hand_landmarker.task, `pip install mediapipe`) -> hands.json (30 Hz, qo'l tepasi/barmoq uchi) -> Gauss sigma 2 -> HTML'da
  bitta proxy tween onUpdate bilan element qo'l ustida ergashadi (seek-safe). Ishora so'zdan 0.3–0.6 s keyin cho'qqiga chiqadi — paydo bo'lishni
  qo'l y<1150 bo'lgan birinchi kadrga bog'la. Yuz qutisiga tushsa elementni yonga sur (qoida 3). Element #cam ichida (kamera push bilan birga).
