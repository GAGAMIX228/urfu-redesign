"""Покадровое движение в готовом видео: на сколько пикселей сдвинулась страница между соседними кадрами
и насколько изменилась картинка. Помогает найти рывки (сдвиг туда-обратно, скачок, неровная прокрутка).
python check_motion.py видео.mp4"""
import subprocess, sys
import numpy as np
import imageio_ffmpeg

W, H = 960, 540
raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', sys.argv[1], '-vf', f'scale={W}:{H}',
                      '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
# только середина кадра по ширине (подпись и курсор слева/снизу не мешают), без шапки сайта
band = fr[:, 60:460, 240:900].mean(axis=2)
for i in range(1, len(fr)):
    a, b = band[i - 1], band[i]
    best, err = 0, 1e9
    for s in range(-150, 151):
        x = a[max(0, s):400 + min(0, s)]; y = b[max(0, -s):400 + min(0, -s)]
        e = float(np.abs(x - y).mean())
        if e < err: err, best = e, s
    diff = float(np.abs(fr[i] - fr[i - 1]).mean())
    if abs(best) > 0 or diff > 1.5:
        print(f'{i:5d} {i / 25:6.2f} с  сдвиг {best * 2:5d} px  изменение {diff:5.1f}  остаток {err:5.1f}')
