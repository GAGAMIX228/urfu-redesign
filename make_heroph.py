"""Фото УрФУ в шестиугольной рамке в шапке внутренних страниц (стиль «Яркий Урал»).
Запуск: python make_heroph.py — можно повторно, старая вставка заменяется. После генераторов страниц, перед make_og.py."""
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PH = {
    'Admission': 'studenty', 'Science': 'it-konferenciya-2026-zal', 'Help': 'volontery-2026', 'Schedule': 'kampus-leto',
    'Program': 'glavnyj-korpus-leto-960', 'News': 'kampus-sverhu', 'Catalog': 'shkolniki', 
    'Events': 'it-konferenciya-2026-slushateli', 'Institute': 'glavnyj-korpus-fasad', 'Cabinet': 'tochka-kipeniya', 'Dorms': 'obshchezhitie-9',
}
PAT = re.compile(r'(<section class="phead[^"]*"[^>]*>\s*<div class="wrap"[^>]*>)')
for page in ['Life']:
    q = page + '.dc.html'; t = open(q, encoding='utf-8').read()
    t = re.sub(r'<div class="ph-hex"[^>]*></div>', '', t).replace('<section class="phead has-ph', '<section class="phead')
    open(q, 'w', encoding='utf-8', newline='').write(t)
for page, img in PH.items():
    p = page + '.dc.html'
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<div class="ph-hex"[^>]*></div>', '', s)
    tag = f'<div class="ph-hex" style="--img:url(\'photos/{img}.webp\')" aria-hidden="true"></div>'
    s, n = PAT.subn(lambda m: m.group(1) + tag, s)
    s = re.sub(r'<section class="phead(?![^"]*has-ph)', '<section class="phead has-ph', s)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print(page, n)
