"""Карточка ссылки для соцсетей и мессенджеров (Telegram, ВКонтакте): на каждой странице — заголовок, описание и картинка.
Запускать после остальных make_*.py: python make_og.py (можно повторно)."""
import glob, html, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://gagamix228.github.io/urfu-redesign/'
for f in sorted(glob.glob('*.html')):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- og -->.*?<!-- /og -->\n', '', s, flags=re.S)
    t = re.search(r'<title>(.*?)</title>', s)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    lang = re.search(r'<html lang="(\w+)"', s)
    if not t: continue
    title, desc = t.group(1), (d.group(1) if d else '')
    url = SITE + ('' if f == 'index.html' else f)
    tags = ['<!-- og -->',
            '<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="%s">' % ('UrFU redesign' if lang and lang.group(1) == 'en' else 'Редизайн сайта УрФУ'),
            '<meta property="og:title" content="%s">' % title,
            '<meta property="og:description" content="%s">' % desc,
            '<meta property="og:url" content="%s">' % url,
            '<meta property="og:image" content="%sphotos/og-card.jpg">' % SITE,
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
            '<meta property="og:locale" content="%s">' % ('en_US' if lang and lang.group(1) == 'en' else 'ru_RU'),
            '<meta name="twitter:card" content="summary_large_image">',
            '<!-- /og -->']
    s = s.replace('</title>\n', '</title>\n' + '\n'.join(tags) + '\n', 1)
    open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok', f)
