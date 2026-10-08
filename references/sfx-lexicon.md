# SFX va audio lug'ati (design-library uslub-01..10 §10 dan)

Referens reellarda SFX **kam va vazifali**: faqat ko'rinish/rejim o'zgarganda. Har bir so'zga klik QO'YMA.

| Hodisa | Fayl (assets/sfx) | Nutqqa nisbatan dB | Manba uslub |
|---|---|---|---|
| Huk zoom-out / kirish | whoosh_deep_impact.wav | −10…−12 | 01, 09 |
| Katta so'z / bosh ortida so'z / urg'u so'zi | impact-bass-1.mp3 (+4 dB — bass RMS'da sust eshitiladi) | −7…−11 | 06, 09 |
| Oq/ekspozitsiya chaqnashli kesim | whoosh_fast_transition.wav + camera_shutter.wav (kesim kadrida) | −11 / −9 | 02 |
| Light leak o'tish | air_woosh.wav | −15 | 04, 09 |
| Oddiy kesim / oq-qora B-roll'ga kirish | camera_shutter.wav (+ impact-bass sub) | −10…−13 | 06, 10 |
| Split-ekran ochilishi | sweep_small.wav | −15 | 02, 08 |
| Shisha plashka / ro'yxat bandi | long_pop.wav | −12…−13 | 09 |
| Chizilgan ✓ / tagiga chiziq | sweep_small.wav / correct_tone.wav | −16…−18 | 05 |
| ✕ / xato | select_click.wav + error.mp3 | −13 / −16 | — |
| Hisoblagich (0→100, 100→12) | key-press.mp3 har ~0.12–0.17 s, so'nib boradi | −11…−17 | 01 |
| Ikonka pop | explainer_pop_whoosh.wav | −14…−17 | 10 |
| Bildirishnoma (sotuv, obuna) | ping.mp3 | −14 | 08 |
| Like pop | pop.mp3 (+ sparkle.mp3 −18) | −10…−11 | 08, 10 |
| Kursor bosishi | select_click.wav | −11 | 08 |
| Qora ekranga yakun | whoosh_deep_impact.wav | −16…−17 | 04 |

Joylash: `data-start = hodisa − peak_at` (scripts/sfx_meta.py o'lchaydi), balandlik
`vol = 10^((voice_rms + rel − sfx_rms)/20)`. Har SFX'ga `data-duration` + ALOHIDA `data-track-index`
(aks holda lint `duplicate_audio_track`).

## Nutq va musiqa
- Nutq: `scripts/voice_master.py` (EQ + deesser + kompressor + 2 bosqichli loudnorm) → ~−15 LUFS. Avval `ebur128` bilan o'lcha;
  kamera lav-ovozi ko'pincha −37 LUFS bo'ladi. SNR > 30 dB bo'lsa RNNoise KERAK EMAS.
- Musiqa: Pixabay, **Content ID yo'q** (track sahifasida "Content ID Registered" yo'qligini tekshir).
- **Yagona standart (LUFS emas, nutq-musiqa FARQI o'lchanadi)** — ikki loyihadagi ziddiyatli fikrlar shundan kelib chiqadi:
  Ucan Visa'da musiqa −34..−40 LUFS da "musiqa yo'q" deyildi; Storis'da zarbli trek −20 LUFS da "ovozni to'syapti" deyildi.
  1. Trek: `music_pick.py` bilan sokin, zarbsiz, o'rta chastotasi siyrak trek (bu eng katta ta'sir).
  2. Musiqa zanjiri: `highpass=60` + nutq-polosa o'yig'i `equalizer=f=1200:t=o:w=2.2:g=-6` + loudnorm −25 +
     sidechaincompress (kalit = voice 300–3400 Hz, threshold 0.08, ratio 2.5, attack 60, release 500) — `mix_audio.py` shuni qiladi.
     carve.mjs ishlasa: data-volume bilan bgm ~−25 LUFS, carve 0.25–0.3, EQ o'yig'i saqlansin.
  3. O'lchov (faqat-musiqa stemi, ducking bilan): nutq paytida nutq polosasida nutq − musiqa median ≥19 dB, eng yomon 10% ≥14 dB;
     pauzalarda musiqa −30 LUFS dan past tushmasin (aks holda "musiqa yo'q"). Sokin trekda natija odatda bgm ≈ −27…−25 LUFS.
  4. Foydalanuvchiga 2–3 variant (A/B/C trek) — video `-c:v copy`, faqat ovoz qayta yig'iladi.
- Musiqaning drop'ini videoning eng kuchli lahzasiga mosla: 0.1 s qadamda past chastota energiyasini o'lchab drop vaqtini top,
  bgm'ni `drop − lahza` dan boshlab kes.
- Diniy mavzuda musiqa haqida foydalanuvchidan so'ra (nashid / ambient / musiqasiz).
- Yakunda: `alimiter=limit=0.89` + `loudnorm I=-14 TP=-1.5`, video `-c:v copy`.
