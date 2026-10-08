# reel-montaj — Claude Code skill

Talking-head reel (9:16) montaji: sinxron manba, grading, transkript, design-library uslublari, B-roll, SFX, HyperFrames render.

## Boshqa laptopga o'rnatish

**Windows (PowerShell):**
```powershell
git clone https://github.com/asositgroup/reel-montaj.git "$env:USERPROFILE\.claude\skills\reel-montaj"
```

**macOS / Linux:**
```bash
git clone https://github.com/asositgroup/reel-montaj.git ~/.claude/skills/reel-montaj
```

Claude Code'ni qayta oching — `/reel-montaj` paydo bo'ladi.

Yangilash: `cd ~/.claude/skills/reel-montaj && git pull`

## Kerakli narsalar
- Python 3.10+, ffmpeg/ffprobe, Node.js (`npx hyperframes`), `yt-dlp`
- Python paketlari: faster-whisper, rembg, opencv-python, numpy, scipy, pillow (Mac: venv `~/Desktop/AI-Videos/.venv`)
- **design-library** (uslublar, ~3 GB) — bu repoda YO'Q, alohida ko'chiring: `AbuDev/design-library/`
- **Pexels API kaliti** — `AbuDev/remotion-teaser/.env` ichida `PEXELS_API_KEY=...` (repoga qo'yilmaydi)

## Papka yo'llari
Standart: Windows `~/OneDrive/Ishchi stol/{AbuDev,MY - Videos}`, Mac `~/Desktop/AI-Videos/{AbuDev,MY - Videos}` (avtomatik topiladi).
Boshqacha bo'lsa muhit o'zgaruvchilari bilan bering:
```powershell
setx ABUDEV_DIR "D:\AbuDev"
setx MYVIDEOS_DIR "D:\MY - Videos"
```
