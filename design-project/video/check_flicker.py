"""Мерцание в готовом видео: средняя яркость каждого кадра и скачки между соседними кадрами.
python check_flicker.py видео.mp4 [секунд_с_начала]"""
import subprocess, sys
import numpy as np
import imageio_ffmpeg

src = sys.argv[1]
secs = float(sys.argv[2]) if len(sys.argv) > 2 else 60
W, H = 192, 108
raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-t', str(secs), '-i', src,
                      '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
mean = fr.mean(axis=(1, 2))
print('кадров', len(fr))
# «дыхание»: кадр отличается от соседей в одну сторону (вспышка), а не плавный переход
d = np.abs(fr[1:] - fr[:-1]).mean(axis=(1, 2))
print('самые большие скачки яркости между кадрами (кадр, секунда, разница, средняя яркость до→после):')
for i in np.argsort(-d)[:15]:
    print(f'  {i + 1:5d}  {(i + 1) / 25:5.2f} с  {d[i]:6.2f}  {mean[i]:6.1f} → {mean[i + 1]:6.1f}')
# неподвижные участки: изображение должно стоять, а не «дышать»
print('колебания яркости на неподвижных участках (по секундам):')
for s in range(int(len(fr) / 25)):
    seg = fr[s * 25:(s + 1) * 25]
    if len(seg) < 2: break
    jit = np.abs(seg[1:] - seg[:-1]).mean(axis=(1, 2))
    print(f'  {s:3d} с: среднее изменение {jit.mean():5.2f}, максимум {jit.max():5.2f}')
