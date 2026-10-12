"""Делает копии всех страниц с тёмной темой (*.dark.dc.html), ссылки внутри ведут на такие же копии.
Основные страницы не меняются. Запуск: python make_dark_preview.py"""
import glob
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pages = [f for f in glob.glob('*.dc.html') if f.count('.') == 2]  # только основные: Name.dc.html
names = {f[:-len('.dc.html')] for f in pages}

for f in pages:
    s = open(f, encoding='utf-8').read()
    s = s.replace('<link rel="stylesheet" href="site.css">',
                  '<link rel="stylesheet" href="site.css">\n<link rel="stylesheet" href="dark.css">\n<script src="theme.js"></script>', 1)
    # ссылки между страницами — на тёмные копии
    s = re.sub(r'((?:href=|href:)["\'])(%s)\.dc\.html' % '|'.join(sorted(names, key=len, reverse=True)), r'\1\2.dark.dc.html', s)
    s = s.replace("'Search.dc.html' +", "'Search.dark.dc.html' +")  # адрес поиска, собираемый в логике
    s = s.replace('<title>', '<title>[Тёмная тема] ', 1)
    assert 'dark.css' in s, f
    open(f.replace('.dc.html', '.dark.dc.html'), 'w', encoding='utf-8').write(s)
    print(f, '->', f.replace('.dc.html', '.dark.dc.html'))
