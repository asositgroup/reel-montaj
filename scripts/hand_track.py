"""Qo'l kuzatuvi: hf/assets/aroll.mp4 -> analysis/hands.json (har 2-kadr, 30 Hz): har qo'l uchun ko'rsatkich barmoq uchi (8) va qo'l tepasi."""
import json, subprocess, numpy as np, mediapipe as mp, os
from mediapipe.tasks.python import vision, BaseOptions
W, H = 1080, 1920
opt = vision.HandLandmarkerOptions(base_options=BaseOptions(model_asset_path=os.path.expanduser("~/.cache/mp/hand_landmarker.task")),
                                   running_mode=vision.RunningMode.VIDEO, num_hands=2, min_hand_detection_confidence=0.3, min_tracking_confidence=0.3)
det = vision.HandLandmarker.create_from_options(opt)
rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "hf/assets/aroll.mp4", "-vf", "fps=30", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
out, i = [], 0
while True:
    b = rd.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.frombuffer(b, np.uint8).reshape(H, W, 3))
    r = det.detect_for_video(img, int(i * 1000 / 30))
    hs = []
    for lm, hd in zip(r.hand_landmarks, r.handedness):
        xs = [p.x * W for p in lm]; ys = [p.y * H for p in lm]
        hs.append({"side": hd[0].category_name, "tip": [round(xs[8]), round(ys[8])], "top": [round(xs[int(np.argmin(ys))]), round(min(ys))],
                   "wrist": [round(xs[0]), round(ys[0])]})
    out.append({"t": round(i / 30, 3), "hands": hs}); i += 1
json.dump(out, open("analysis/hands.json", "w")); print("kadr", i)
