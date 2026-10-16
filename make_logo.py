"""Новый логотип «Лента»: заменяет старый знак «У» во всех страницах сайта и в значке вкладки.
Знак — сложенная лента: левая часть фиолетовая, правая розовая, на сгибе тень.
Запуск: python make_logo.py (можно повторно)."""
import glob, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

VB = '10 6 82 94'          # рамка знака: ширина 82, высота 94
RATIO = 82 / 94


def mark(sfx, attrs):
    return (f'<svg {attrs} viewBox="{VB}">'
            f'<defs><linearGradient id="ulA{sfx}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9B5CFF"></stop><stop offset="1" stop-color="#5A1FD1"></stop></linearGradient>'
            f'<linearGradient id="ulB{sfx}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF4D8D"></stop><stop offset="1" stop-color="#C2185B"></stop></linearGradient>'
            f'<linearGradient id="ulF{sfx}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"></stop><stop offset="1" stop-color="#000" stop-opacity="0"></stop></linearGradient></defs>'
            f'<path d="M14 10 L36 10 L60 56 L46 70 Z" fill="url(#ulA{sfx})"></path>'
            f'<path d="M64 10 L88 10 L56 86 C52 95 44 98 30 96 L26 84 C38 84 42 80 46 70 Z" fill="url(#ulB{sfx})"></path>'
            f'<path d="M46 70 L60 56 L54 72 Z" fill="url(#ulF{sfx})"></path></svg>')


OLD = re.compile(r'<svg([^>]*)>(?:(?!</svg>).)*?M1 2 H25(?:(?!</svg>).)*?</svg>', re.S)


def fix_attrs(a):
    a = re.sub(r'\s*viewBox="[^"]*"', '', a)
    h = re.search(r'height="(\d+(?:\.\d+)?)"', a)
    if h:
        hh = float(h.group(1))
        ww = round(hh * RATIO)
        a = re.sub(r'width="\d+(?:\.\d+)?"', f'width="{ww}"', a)
    return a.strip()


total = 0
for f in sorted(glob.glob('*.html')):
    s = open(f, encoding='utf-8').read()
    n = [0]
    def rep(m):
        n[0] += 1
        return mark(f'{n[0]}', fix_attrs(m.group(1)))
    s2 = OLD.sub(rep, s)
    if n[0]:
        open(f, 'w', encoding='utf-8', newline='').write(s2)
        total += n[0]
        print(f, n[0])
open('favicon.svg', 'w', encoding='utf-8').write(
    '<svg xmlns="http://www.w3.org/2000/svg" ' + mark('', '').split('<svg ', 1)[1].replace(f'viewBox="{VB}"', 'viewBox="6 4 90 98"'))
print('всего', total)
