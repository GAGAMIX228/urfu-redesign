"""Ищет рывки в кадрах видео: резкие изменения картинки и вертикальные сдвиги страницы.
python check_jumps.py папка_с_кадрами [номера_кадров_смены_сцен,через,запятую]"""
import glob, os, sys
import numpy as np
from PIL import Image

D = sys.argv[1]
CUTS = set(int(x) for x in sys.argv[2].split(',')) if len(sys.argv) > 2 else set()
fs = sorted(glob.glob(os.path.join(D, '*.png')))
prev = None; rows = []
for i, f in enumerate(fs, 1):
    a = np.asarray(Image.open(f).convert('L').resize((480, 270)), dtype=np.float32)
    if prev is not None:
        diff = float(np.abs(a - prev).mean())
        # вертикальный сдвиг: при каком смещении строки совпадают лучше всего
        pa, pb = a.mean(axis=1), prev.mean(axis=1)
        best, bs = 0, 1e9
        for s in range(-30, 31):
            x = pa[max(0, s):270 + min(0, s)]; y = pb[max(0, -s):270 + min(0, -s)]
            e = float(np.abs(x - y).mean())
            if e < bs: bs, best = e, s
        rows.append((i, diff, best))
    prev = a
print('кадров', len(fs))
print('резкие изменения (не смена сцены):')
for i, d, s in rows:
    if d > 6 and i not in CUTS:
        print(f'  кадр {i} ({i / 25:.1f} с): изменение {d:.1f}, сдвиг {s * 4} px')
# сдвиг туда-обратно за несколько кадров — признак «съезжания»
print('сдвиги туда-обратно:')
for k in range(len(rows) - 6):
    s = [r[2] for r in rows[k:k + 6]]
    if any(v > 0 for v in s) and any(v < 0 for v in s) and max(abs(v) for v in s) >= 2:
        print(f'  кадры {rows[k][0]}–{rows[k + 5][0]} ({rows[k][0] / 25:.1f} с): {[v * 4 for v in s]}')
