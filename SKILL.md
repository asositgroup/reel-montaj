---
name: reel-montaj
description: Foydalanuvchining talking-head videosini (O'zbek ekspert/podkast reel, 9:16) design-library'dagi 32 ta o'rganilgan reel uslubi (15 oila A–O: Asror Iskandarov, @mr.maxvolkov, targetolog pop-art, Kasb Markazi 3D karusel, Alstar kollaj, iOS-UI, intervyu, @uktamjontuygunovv UI-kartalar, @smoothbeey 3D sahna, Imona Ahmedova studiya monologi va split-podkast va b.) asosida premium, silliq (overshootsiz) to'liq montaj qilish — sinxron manba (asl fayldan virtual kameralar), grading, transkript, bosh-ortidagi so'z, shisha plashkalar, #N kartalar, telefon/profil maketlari, B-roll (Pexels), SFX lug'ati, Content ID'siz musiqa, musiqa ovozni to'smaydigan miks, smooth_check, HyperFrames render (Windows va Mac). "/reel-montaj", "shu uslubda montaj qil", "videomni montaj qilib ber", "o'rgangan usullaringdan foydalan", "b-roll qo'shib montaj", "musiqani almashtir", "silliqroq qil", "Imona Ahmedova uslubida" so'rovlarida ishlat.
---

# Reel montaj (foydalanuvchining o'rgatgan uslubi)

Ish tili: **o'zbekcha**. Loyihalar: `<ABUDEV>/reel-<slug>/`, natija `<MYVIDEOS>/<Mavzu>/`.
- Windows: `~/OneDrive/Ishchi stol/{AbuDev,MY - Videos}`, CUDA whisper.
- Mac: `~/Desktop/AI-Videos/{AbuDev,MY - Videos}`, Python = `~/Desktop/AI-Videos/.venv/bin/python` (tizim python3'da numpy yo'q),
  whisper CPU int8 (tr.py o'zi aniqlaydi), `carve.mjs` ishlamaydi → `mix_audio.py` (ffmpeg ducking). zsh: filtr ichida `${var}`.
- Linux: Mac bilan bir xil (`~/Desktop/AI-Videos`, `.venv`, `mix_audio.py`); ffmpeg **>= 5.1** shart (`-fps_mode`), Ubuntu 22.04 da statik build;
  NVIDIA bo'lsa `tr.py` CUDA'ni o'zi oladi (`LD_LIBRARY_PATH` -> pip nvidia-cublas/cudnn), Chrome kutubxonalari: `npx hyperframes doctor`.
- `new_project.py` qaysi joyda `AbuDev/` borligini o'zi topadi; boshqa joy bo'lsa `ABUDEV_DIR` / `MYVIDEOS_DIR`.
Uslub manbasi: `AbuDev/design-library/INDEX.md` + `uslub-NN/STYLE.md` (+ keyframes) — 32 uslub, 15 oila (A–O; 01–26 Windows'da, 27–32 Macda). Avval INDEX.md ni o'qi.
Ma'lumotnomalar: `references/sfx-lexicon.md` (ovoz + musiqa standarti), `references/lessons.md` (tuzoqlar — HAR loyihada o'qi), `references/smooth-motion.md` (silliqlik standarti — MAJBURIY).
Agar design-library shu kompyuterda bo'lmasa — uslublarni quyidagi jadval + lessons.md dan loyihala va buni rejada ayt.
Bu skill HyperFrames ustida ishlaydi: `/hyperframes` → `general-video` yo'li (flow: automation) qoidalari amal qiladi.

## Qat'iy qoidalar (foydalanuvchi o'rnatgan)
1. **Reja → tasdiq → montaj.** Transkript + reja jadvalini ko'rsatmaguncha va "boshla" demaguncha qurma. Ishni o'z tashabbusing bilan kengaytirma.
2. **Sinxron birinchi.** Birlashtirilgan faylni manba qilma — asl fayldan qur (lessons.md → Sinxron). Yakunda `av_check.py`.
3. **Yuzga hech narsa tushmaydi** (spikerga ham, B-roll'dagiga ham). Bosh qutisini o'lcha (`prep.py heads`, rembg).
4. **B-roll odamlari:** qora tanlilar faqat gapda aytilsa; diniy mavzuda boshi ochiq ayollar yo'q; yuzsiz kadrlar afzal; muqaddas shaxslar tasvirlanmaydi.
5. **Papka:** `MY - Videos/<Mavzu>/{1_manba,2_montajlar,3_tayyor}` + README. Eski versiyani o'chirmay `2_montajlar/` ga, nomida muammosi bilan.
6. **Taqiqlangan:** ElevenLabs, kie.ai (ruxsatsiz). Musiqa: Pixabay, Content ID yo'q. B-roll: Pexels (kalit `AbuDev/remotion-teaser/.env`).
7. **VIDEODAGI HAMMA NARSA SILLIQ** (foydalanuvchi talabi, 2026-10-05) — har bir element, motion animatsiya va grafika
   (matn, karta, ikonka, chiziq, kamera, o'tish, chaqnash, fon xiralashuvi): `references/smooth-motion.md` qiymatlari.
   Qisqasi: kirish ≥0.5 s `expo.out` + blur, chiqish ≥0.5 s `power2.inOut`, overshoot (`back.out`/`elastic`) va
   qisqa `yoyo` "tepki"lar YO'Q, kamera kesimda sakramaydi, render fps = manba×2. Render qilingach kirish oynalarini
   ketma-ket kadrlarda tekshir — tekshirmay "tayyor" dema.
8. Uzun ish paytida foydalanuvchiga qisqa holat yoz; "tugadi" deyishdan oldin fon jarayonlarini haqiqatda tekshir.
9. **Musiqa ekspert ovozini HECH QACHON to'smaydi** (2026-10-05): sokin, zarbsiz trek (`music_pick.py`), nutq polosasida
   nutq musiqadan median ≥19 dB / eng yomon ≥14 dB, lekin pauzalarda musiqa eshitilsin. Uslub: premium, bachkana emas
   (emoji/komiks effektlari faqat foydalanuvchi so'rasa). 2–3 musiqa variantini faqat ovozni qayta yig'ib taklif qil.

## Ish tartibi

### 0. Loyiha
```bash
python ~/.claude/skills/reel-montaj/scripts/new_project.py <slug> "<Mavzu nomi>"
```
Manba fayllarni `MY - Videos/<Mavzu>/1_manba/` ga ko'chir. Keyingi hamma buyruqlar loyiha ildizidan (`AbuDev/reel-<slug>`).

### 1. Tahlil
- `ffprobe` (rotation, fps, start_time, qismlar), 1.5–2 fps kontakt varaq.
- Birlashtirilgan bo'lsa: asl faylni `Downloads/` da qidir (`find ... -iname "C####*"`), qism nomlaridan oraliqlar.
- Transkript: `ffmpeg -ac 1 -ar 16000` → `python scripts/tr.py audio16k.wav analysis/tr_uz.json uz` (+ kk, tr). Matnni adabiy o'zbekchaga tikla.
- Ekspertning Instagrami berilsa: ommaviy sahifadan ism/handle/bio/obunachi, avatar (og:image), reellar (`yt-dlp`, `--dump-json` → like soni). Login qilma.

### 1b. Yangi referens uslubni o'rganish (foydalanuvchi havola bersa)
> Foydalanuvchi referens BILAN o'z videosini berib "shunday video qilib ber" desa — `reel-uslub` skilli (shu quvur + uslub pasporti,
> `grade_match.py`, `style_compare.py`).
video-use (`~/video-use`, browser-use/video-use) vositalari + bizning whisper bilan HAMMA jihatdan:
```bash
yt-dlp -o "<id>.%(ext)s" --write-info-json "https://www.instagram.com/reel/<id>/"     # design-library/_src/ ga
python ~/.claude/skills/reel-montaj/scripts/ref_analyze.py <id>.mp4                   # -> <id>_an/report.md
```
`report.md` beradi: texnik (LUFS/fps), transkript + video-use `takes_packed.md` (beat'lar), kesimlar va har kesimning nutqqa
munosabati (so'z ichida = J/L-cut / pauzada), kadr uzunligi ritmi, har kadr grade (luma, kontrast, to'yinganlik, iliqlik)
va kamera harakati, audio (nutq vs pauza farqi, musiqa bor-yo'qligi, bas/nutq polosasi, SFX zarbalari kesimga bog'liqmi),
kontakt varaqlar va video-use `timeline_view` (filmstrip + to'lqin + so'zlar) huk/yakun/kesimlarda.
Keyin: `tv_*.png` va `contact_*.jpg` ni KO'R → har element kirishi uchun 18 kadrlik strip → `uslub-NN/STYLE.md`
(report.md 7-bo'limdagi 15 bandning hammasi) → INDEX.md → shu jadvalga yangi qatorlar → lessons.md.
**video-use'ning Scribe transkripsiyasi ishlatilmaydi** (ElevenLabs — qoida 6); undan faqat helpers (timeline_view, pack_transcripts),
kesim hunari (pauzada kesim, 30–200 ms padding, 30 ms audio fade), self-eval tartibi va critic sub-agent g'oyasi olinadi.

### 2. Reja (foydalanuvchiga jadval)
Gap mazmuniga qarab har bo'lim uchun element tanla (INDEX.md "umumiy tizim" + "Oilalarni aralashtirish"). Bitta videoda
asosiy oila (odatda A yoki B) + 1–2 ta boshqa oiladan urg'u bloki — hamma oilani aralashtirma:

| Gap turi | Element | Uslub |
|---|---|---|
| Huk (0–3 s) | bosh ortidagi katta so'z + 3 qatorli ierarxik sarlavha, zoom-out | 07, 05, 03 |
| "#1 / eng muhim" | fon blur + nuqta-to'r, sarlavha chapdan, glitch-chiqish | 02 |
| Ro'yxat (2–4 band) | shisha plashkalar pastdan, ✓ chiziladi | 09, 08 |
| Xato / ogohlantirish | pikselli duotone karta (ffmpeg'da bake) `#N xato` | 06 |
| Raqam / foiz | shisha o'lchagich 0→100 yoki 100→12, tik-tik | 10, 02, 01 |
| Kontent / reels haqida | reel kartalar (ekspertning o'z reellari + ❤ like) | 03 |
| Kurs / sotuv | telefon maketi (kurs sahifasi), "Yangi o'quvchi yozildi" bildirishnomalari | 01, 05, 08 |
| Urg'u xulosasi | krem kursiv sarlavha, nuqta bilan tugaydi ("Tabassum.") | 04, 08, 10 |
| Oddiy gap | `[ so'z ]` qavsli subtitr (split paytida `up`) | 04, 06, 07 |
| B-roll | split-ekran (oq chiziq, spiker yuqoriga suriladi) yoki to'liq ekran oq-qora | 02, 04, 08, 09 |
| CTA | profil kartasi (haqiqiy avatar/raqamlar) + kursor Follow + Like pop | 08, 10 |
| Faktdan xulosa ("demak suv ko'p") | **liquid-fill matn** (rang darajasi ko'tariladi/tushadi) | 11 |
| Sabablar / argumentlar ketma-ket | **pop-art sariq skotch yorliqlar** zinapoya, komiks burst + bass | 12 |
| TOP-N mahsulot / element | rangli **mahsulot kartasi** uchib kiradi (`expo.out` + motion blur), so'zma-so'z to'ladi | 13 |
| Kategoriya ro'yxati (davlat/turi) | **doimiy tepa sarlavha** + nom (bayroq/ikonka) + iOS-squircle plitkalar tokchada | 15 |
| Portfolio / keyslar / ishlar | **3D reel karusel** (bitta uzluksiz `sine.inOut` aylanish + blur, aberratsiya) | 14 |
| "1-2-3 qadam" / xavf / hujjatli | qorong'i kollaj + **3D-stiker "QADAM" sarlavha**, harf-harf stiker, yoy (textPath) matn | 16 |
| Bob raqami | kontur italic raqam + qalin italic so'z ("1 Birinchi") | 11 |
| CTA (B oila) | sariq avatar + @handle pill + "Obuna" → kursor → "Rahmat!" | 11, 13, 15 |
| Ritm (B oila) | har kesim 1.2–1.47× dan 1.0× ga zoom-out, matn zoom qatlami ichida | 11, 13, 15 |
| O'tishlar | editorial flash / light leak / hard cut + shutter / flash-blur (13) | 04, 05, 09, 13 |
| TOP-N reyting (davlat/variant) | **shisha Top-5 jadval** — aytilgan sari pop → o'ringa siljish, #1 oxirigacha bo'sh | 19 |
| Davlat / variant nomi | **3D bayroqli kondensat sarlavha-karta** + glow, chiqishda chapga uchib ketadi | 18 |
| Raqamli taqqoslash | katta oq raqam + qizil glow-chiziq, prujina bilan | 18 |
| Ilova / davlat xizmati / IG | **iOS-UI**: IG savol stikeri, app-ikon pop + yaltirash, IG profil paneli | 17 |
| Oddiy gap (F oila) | plashkasiz oq so'zlar blurdan "suzib/tushib" kiradi, prujina bilan, qator qayta markazlashadi | 17, 18 |
| Intervyu (2–3 kamera) | savolda keng kadr + sariq kalit so'z, javobda yaqin plan; qo'lda chizilgan marker/zigzag | 20, 21 |
| Kuchli urg'u so'zi | katta so'z 3D tushish (predmet/mikrofon ortidan) yoki kondensat slam 1.3→1 `expo.out` + blur 20→0 (tepkisiz) | 21, 23 |
| Statistika huki / "oldin vs hozir" | piksel-mozaika ochilish, kursor qayta yozadi, glitch raqam | 23 |
| TOP-5 energik bo'lim | 3D shisha-oltin raqam yerdan o'sadi + 3D karta flip, glitch o'tish | 22 |
| CTA (F/H oila) | so'zlar tushib ko'krakka 1:1 bog'lanadi (19) yoki avatar-olov + IG pill → ✓ (21) | 19, 21 |
| "N ta joy/sabab" ro'yxat bandi | rangli blob + katta tartib so'z (BIRINCHISI…), neo-brutal plashka `expo.out` (emoji faqat so'ralsa) | 25 |
| Joy/ob'ektga ishora | bosh ustida ko'rsatkich-yorliq ▼, bosh bilan yuradi (jaw/chin track) | 25 |
| Ha/yo'q, kerak/kerak emas saralash | pastda doimiy ikki ustunli taxta, kafel pop → hukmda katakka uchadi | 24, 26 |
| Intervyu savol-javob (M oila) | chapda ikki darajali matn: **sariq kalit so'z** + oq izoh so'zma-so'z; savolda sariq `" "` qo'shtirnoq | 27, 28 |
| Uzun iqtibos / tushuntirish | **to'q shisha plashka** eniga o'sadi, matn so'zma-so'z ichida | 27 |
| Atama / qoida / jarima (fakt kartasi) | **oq karta + 3D emoji** qo'l yonidan o'sadi, keyingi subtitr uni o'ngga "itarib" chiqaradi | 28 |
| Boshqa odam gapi / ogohlantirish | **ogohlantirish kartasi** (to'q-sariq `!` ustun, typewriter) yoki **to'q-sariq pill** + oq ikkinchi qator | 28 |
| Ikki toifa (yashil/sariq ro'yxat) | **marker bo'yoq** so'z ortida chapdan to'ladi, rang ma'noga mos | 28 |
| Sana / raqam urg'usi | **qizil qo'lda chizilgan aylana** so'z atrofida; salbiy so'zga qizil zigzag / qizil qo'lyozma izoh | 27, 28 |
| Sanab o'tish (ritmli gap) | **"sochilib → joylashish"**: so'zlar zinapoya tushadi, gap tugagach qatorga yig'iladi | 28 |
| Bitta qisqa xulosa so'zi ("Shunaqa") | katta oq so'z ko'krakda, chiqishda burilib **kesimdan o'tib** keyingi kadrga uchadi | 27 |
| Pul / boylik misoli | **doira-niqob B-roll** qora fonda + neon-sariq qo'lyozma so'z | 27 |
| TOP-N grafik blok (spikersiz, N oila) | syurreal fon + **3D shisha raqam tepalik ortidan** + **albom kartasi flip**, tepada serif CAPS so'z almashuvi | 29 |
| Huk sarlavhasi (N oila) | tepada Didone CAPS **bitta so'z ko'rinadi, keyingisi o'rnini oladi** + markazda 3D glow so'z | 29 |
| Rejim almashishi (spiker ↔ grafik) | **pikselli eritish** + **oltin solarizatsiya → rang** | 29 |
| CTA (M oila) | avatar + @handle oq pill → to'q-sariq to'lib "obuna bo'ling" ✓ → oq yakun ekran (YouTube anons) | 27, 28 |
| **"Imona Ahmedova uslubida"** → `design-library/oila-O-iman/PASSPORT.md` (4 video birga; bitta spiker → monolog, 2 kishi → split) — kalit ibora | **gradient kondensat CAPS** (to'q sariq→sariq), so'z xira chiqib chapdan o'ngga "to'ladi"; ostida oq kichik subtitr | 31 |
| TOP-3 band boshlanishi (O oila) | KENG kadrga kesim + chapda **katta baland gradient raqam 1/2/3** bo'yiga o'sadi | 31 |
| Ritm (O oila) | 2 kamera (keng ↔ o'rta-yaqin) har ~1.9 s, gap o'rtasida; bitta kadr bo'lsa virtual kamera 1.0 / 1.35; pauzalar olinadi | 31 |
| B-roll ustida (O oila) | kalit ibora CHAP-TEPADA gradient CAPS + oq izoh; ro'yxat aytilsa "arvoh" oltin CAPS qatorlar har kadrda qo'shiladi | 31 |
| Huk (O oila) | oltin metall plashka 2 qator CAPS kinematografik B-roll ustida | 31 |
| 2 kishi suhbati (O oila) | **ikki qavatli split**: tepada gapiruvchi yaqin plan (1.35×), pastda keng kadr; sariq subtitr chegarada | 32 |
| Sanab o'tish (O oila) | **qizil ro'yxat yorliqlari** (to'q qizil + oltin chegara + sariq CAPS) zinapoya | 32 |
| CTA (O oila) | KENG kadr + gradient CAPS "VIDEONI SAQLAB QO'YING / MENGA OBUNA BO'LING" | 31 |

**Uslub manbasidagi overshoot / elastic / tepki / qisqa yoyo → har doim smooth-motion.md ekvivalenti** (rule 7). Ularni faqat
foydalanuvchi aniq so'rasa ishlat. Premium ekspert reeli uchun standart andoza: `templates/*storis_smooth*` (A oila, krem + oltin,
Playfair italic, bob kartalari, DM xabarlar, sanoq, CTA izoh) — hamma tween'lar standartga mos.
O oila (Imona Ahmedova): `templates/iman_elements.html` — gradient CAPS "to'lish", raqam, oq subtitr, split-podkast, qizil yorliqlar
(lint 0 xato, snapshot bilan tekshirilgan) — bloklarni shu fayldan ko'chir.

Virtual kameralar (bitta statik kadr bo'lsa): 4K dan keng 1.0 / o'rta 1.3–1.35 / yaqin 1.7–1.8, kesimlar jimlikda.
Ochiq savollar: ❓ matn joylari, musiqa turi (diniy mavzu), takror gaplar.

### 3. Manba
`edit.json` to'ldir (source, parts, shots) →
```bash
python scripts/prep.py heads && python scripts/prep.py test   # grade_test.jpg ni ko'z bilan tekshir
python scripts/prep.py build && python scripts/voice_master.py   # kirish LUFS'ini o'lchaydi: past lav +20 dB, masterlangan manba 0 dB
ffmpeg -i analysis/voice_raw.wav -ac 1 -ar 16000 analysis/voice16k.wav && python scripts/tr.py analysis/voice16k.wav analysis/tr2_uz.json uz
```
So'z vaqtlarini SINXRON ovozdan (tr2) ol. Bosh qutilari har shot uchun (lessons.md).

### 4. Aktivlar
- Bosh ortidagi so'z: `python scripts/matte.py <t0> <t1> subject_<nom>`.
- B-roll: `python scripts/broll_search.py <slot> "so'rov1" "so'rov2"` → `analysis/broll/<slot>/sheet.jpg` ni KO'R, tanla →
  `scripts/broll_prep.py` PICK ni tahrirla → ishga tushir → tanlangan kadrlarni yana ko'r (ekrandagi odamlar ham qoida bo'yicha).
- Musiqa: Pixabay (brauzer pane, track sahifasi fetch → cdn mp3 + "Content ID Registered" tekshiruvi). 5–7 nomzodni
  `analysis/music/` ga yukla → `python scripts/music_pick.py analysis/music/*.mp3` → `OK` belgililardan tanla
  (nutq polosasi ≤ −7 dB, zarbdorlik < 2). Drop/qaytishni urg'u so'ziga mosla.
- SFX: `python scripts/sfx_meta.py` (assets/sfx + nutq o'lchovi).

### 5. Kompozitsiya
`templates/*storis_smooth*` (A oila premium — standart tanlov), `templates/compose.example.py` + `index.tpl.example.html` (A oila, Ekspert shaxsiyati) yoki `templates/*ucanvisa_v2*` (B–E oilalari: aylanuvchi plashka, liquid-fill, skotch yorliqlar, 3D karusel/nishon, rangli kartalar, 3D-stiker, CTA kursor) — nusxa olib `compose.py` / `index.tpl.html` qil
va shu loyiha gaplariga moslab qayta yoz (bloklar: CAPS, HEADS, LIST, SPLITS, FLASH/LEAK, SFX_EVENTS, maketlar).
```bash
python scripts/compose.py && python scripts/smooth_check.py hf/index.html && cd hf && npx hyperframes lint   # smooth_check 0 bo'lishi shart
npx hyperframes snapshot --at t1,t2,... --no-end --describe false   # har elementning eng ko'rinadigan lahzasi
node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed bgm --voice voice && cd .. && python scripts/save_carve.py && python scripts/compose.py
# carve ishlamasa (Mac): renderdan keyin ovozni alohida yig' — python scripts/mix_audio.py <bgm> <start_s> analysis/mix.wav -25
cd hf && npx hyperframes check   # 0 xato; content_overlap bo'lsa ko'z bilan tekshir
```

### 6. Render va topshirish
```bash
npx hyperframes render -o renders/<nom>_raw.mp4 -q delivery -w 2 -f <manba_fps*2> > ../analysis/render.log 2>&1
ffmpeg -i renders/<nom>_raw.mp4 -c:v copy -af "alimiter=limit=0.89:attack=3:release=50:level=false,loudnorm=I=-14:TP=-1.5:LRA=9" -ar 48000 -c:a aac -b:a 256k -movflags +faststart renders/<nom>_final.mp4
python ../scripts/av_check.py renders/<nom>_final.mp4 <spiker to'liq ko'rinadigan vaqtlar>   # loyiha ildizidan
python scripts/smooth_check.py hf/renders/<nom>_final.mp4                 # keskin yorug'lik sakrashlari (0 bo'lishi kerak)
python scripts/smooth_check.py hf/renders/<nom>_final.mp4 <har kirish/bob/karta vaqti...>   # analysis/smooth/*.jpg ni KO'R
```
Self-eval (video-use uslubida, ko'rsatishdan oldin): renderdan har kesim ±1.5 s ga
`python ~/video-use/helpers/timeline_view.py hf/renders/<nom>_final.mp4 <c-1.5> <c+1.5> --transcript analysis/tr2_uz.json`
— chaqnash/sakrash, to'lqinda "pop", subtitr overlay ostida qolmaganini tekshir; birinchi/oxirgi 2 s va 2–3 o'rta nuqta.
Nashr uchun video bo'lsa foydalanuvchi so'rasa critic sub-agent (referens reellar bilan solishtirib, vaqt kodli muammolar ro'yxati).
Kalit kadrlar varag'ini ko'r → `MY - Videos/<Mavzu>/3_tayyor/<Nom>_v1.mp4` → telefon uchun <30 MB nusxa (SendUserFile).
Hisobotda: davomiylik, LUFS (umumiy + musiqa alohida + nutq/musiqa farqi), sinxron o'lchovi, smooth_check natijasi, ❓ qolgan joylar. Loyiha xotirasini yangila (MEMORY.md).
