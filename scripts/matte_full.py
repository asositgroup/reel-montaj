"""Butun video bo'yicha spiker kesmasi (u2net_human_seg): niqob 30 fps, har niqob 2 ta 60 fps kadrga qo'llanadi -> VP9 alfa 60 fps.
python scripts/matte_full.py  -> hf/assets/subject_full.webm
"""
import subprocess, numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove
s = new_session("u2net_human_seg")
rd = subprocess.Popen(["ffmpeg","-v","error","-i","hf/assets/aroll.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba","-s","1080x1920","-r","60","-i","-","-c:v","libvpx-vp9",
                       "-pix_fmt","yuva420p","-b:v","5M","-deadline","good","-cpu-used","4","-row-mt","1","-threads","4","hf/assets/subject_full.webm"],stdin=subprocess.PIPE)
fs = 1080*1920*3; i = 0; m = None
while True:
    b = rd.stdout.read(fs)
    if len(b) < fs: break
    fr = np.frombuffer(b, np.uint8).reshape(1920,1080,3)
    if i % 2 == 0:
        small = Image.fromarray(fr).resize((540,960), Image.BILINEAR)
        mk = remove(small, session=s, only_mask=True).resize((1080,1920), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.6))
        m = np.asarray(mk)[...,None]
    wr.stdin.write(np.concatenate([fr, m], 2).tobytes()); i += 1
    if i % 600 == 0: print("kadr", i, flush=True)
wr.stdin.close(); wr.wait(); print("ok", i)
