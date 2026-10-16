"""Рисует карты двух кампусов УрФУ (SVG) по данным OpenStreetMap и вставляет блок «Карта кампусов» в Dorms.dc.html."""
import json, math, os, re, html
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'osm')
SITE = os.path.dirname(os.path.abspath(__file__))
NOM = json.load(open(os.path.join(HERE, 'points.json'), encoding='utf-8'))

# категории: ключ, подпись, цвет пина, цвет текста номера
CAT = {'study': ('Учёба', '#6B2BE8', '#FFFFFF'), 'dorm': ('Общежития', '#E0246F', '#FFFFFF'),
       'sport': ('Спорт', '#00B386', '#16112B'), 'food': ('Еда', '#FFC21A', '#16112B'), 'med': ('Здоровье', '#16112B', '#FFFFFF')}

AREAS = {
 'vtuz': dict(title='Втузгородок', bbox=(56.8352, 60.6395, 56.8470, 60.6640), pts=[
   ('study', 'Главный учебный корпус', 'ул. Мира, 19', 'Уральский федеральный университет имени'),
   ('study', 'ИРИТ-РтФ, учебный корпус № 6', 'ул. Мира, 32', 'ИРИТ-РТФ УрФУ'),
   ('study', 'ФТИ, учебный корпус № 5', 'ул. Мира, 21', 'ФТИ УрФУ'),
   ('study', 'ХТИ и ИНМиТ, учебный корпус № 3', 'ул. Мира, 28', 'ХТИ/ИнМИТ'),
   ('study', 'Институт строительства и архитектуры', 'ул. Мира, 17', 'ИСиА УрФУ'),
   ('study', 'УралЭНИН, учебный корпус № 8', 'ул. Софьи Ковалевской, 5', 'УралЭНИН УрФУ'),
   ('study', 'Институт физической культуры', 'ул. Мира, 29', 'Институт физической культуры УрФУ'),
   ('dorm', 'Общежитие № 3', 'ул. Малышева, 140', 'Общежитие УрФУ №3'),
   ('dorm', 'Общежитие № 5', 'ул. Малышева, 144', 'Общежитие УрФУ №5'),
   ('dorm', 'Общежитие № 7', 'ул. Станислава Набойченко, 3', 'Общежитие УрФУ №7'),
   ('dorm', 'Общежитие № 8', 'ул. Комсомольская, 70', 'Общежитие УрФУ №8'),
   ('dorm', 'Общежитие № 9', 'ул. Фонвизина, 8', 'Общежитие УрФУ №9'),
   ('dorm', 'Общежитие № 10', 'пр. Ленина, 66', '@Общ10'),
   ('dorm', 'Общежитие № 11', 'ул. Фонвизина, 2', 'Общежитие УрФУ № 11'),
   ('dorm', 'Общежитие № 12', 'ул. Фонвизина, 4', 'Общежитие УрФУ № 12'),
   ('dorm', 'Общежитие № 13', 'ул. Комсомольская, 66А', 'Общежитие УрФУ №13'),
   ('dorm', 'Общежитие № 14', 'ул. Станислава Набойченко, 1А', 'Общежитие УрФУ №14'),
   ('dorm', 'Общежитие № 15', 'ул. Коминтерна, 11', 'Общежите УрФУ №15'),
   ('sport', 'Бассейн «Университетский»', 'ул. Коминтерна, 14А', 'Бассейн «Университетский»'),
   ('sport', 'Спорткомплекс игровых видов спорта', 'ул. Станислава Набойченко, 14', 'Спортивный комплекс игровых'),
   ('sport', 'Физкультурно-оздоровительный комплекс', 'ул. Фонвизина, 5', 'Физкуьтурно-оздоровительный'),
   ('sport', 'Манеж УПИ', 'ул. Станислава Набойченко, 4', 'Манеж УПИ'),
   ('food', 'Столовая УрФУ', 'студгородок, рядом с общежитиями', 'Столовая УрФУ'),
   ('food', 'Столовая УралЭНИН', 'ул. Софьи Ковалевской, 5А', 'Столовая ТЭФ УрФУ'),
   ('med', 'Медсанчасть УрФУ', 'ул. Комсомольская, 59', '@МСЧ'),
 ]),
 'nvk': dict(title='Новокольцовский', bbox=(56.7655, 60.7525, 56.7760, 60.7700), pts=[
   ('study', 'Учебный корпус нового кампуса', 'ул. 100-летия Уральского университета, 5', '#5|university'),
   ('study', 'Общественный центр кампуса', 'ул. Универсиады, 7', 'Общественный центр кампуса'),
   ('dorm', 'НВК № 1', 'ул. 100-летия Уральского университета, 6', 'НВК №1'),
   ('dorm', 'НВК № 2', 'ул. 100-летия Уральского университета, 6/2', 'НВК №2'),
   ('dorm', 'НВК № 4', 'ул. 100-летия Уральского университета, 6/4', 'НВК №4'),
   ('dorm', 'НВК № 5', 'ул. 100-летия Уральского университета, 6/5', 'НВК №5'),
   ('sport', 'Дворец водных видов спорта', 'ул. Универсиады, 11', 'Дворец водных видов спорта'),
   ('med', 'Медицинский центр УрФУ', 'ул. 100-летия Уральского университета, 10', 'Медицинский центр УрФУ'),
 ]),
}
W = 1000


def proj(bbox):
    s, w, n, e = bbox
    k = W / ((e - w) * math.cos(math.radians((s + n) / 2)))
    H = (n - s) * k
    return (lambda la, lo: ((lo - w) * math.cos(math.radians((s + n) / 2)) * k, (n - la) * k)), H


def cen(g):
    return sum(p['lat'] for p in g) / len(g), sum(p['lon'] for p in g) / len(g)


ROADW = {'primary': 15, 'secondary': 12, 'tertiary': 10, 'residential': 7, 'unclassified': 7, 'living_street': 6, 'pedestrian': 6, 'service': 4}


def build(key):
    A = AREAS[key]
    d = json.load(open(os.path.join(HERE, key + '.json'), encoding='utf-8'))
    P, H = proj(A['bbox'])
    els = d['elements']
    # найти координаты точек
    pts = []
    for cat, name, addr, look in A['pts']:
        ll = None
        if look.startswith('@'):
            ll = NOM[look[1:]]
        elif look.startswith('#'):
            hn, kind = look[1:].split('|')
            for x in els:
                t = x.get('tags', {})
                if t.get('building') == kind and t.get('addr:housenumber') == hn: ll = cen(x['geometry']); break
        else:
            for x in els:
                if x.get('tags', {}).get('name', '').startswith(look): ll = cen(x['geometry']); break
        assert ll, (key, name)
        pts.append((cat, name, addr, P(*ll)))
    out = []
    out.append(f'<rect width="{W}" height="{H:.0f}" fill="#F1ECFF"/>')
    def path(g):
        return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in (P(p['lat'], p['lon']) for p in g))
    for x in els:
        t = x.get('tags', {})
        if t.get('leisure') or t.get('natural'):
            out.append(f'<path d="{path(x["geometry"])}Z" fill="#CFF3E6"/>')
    for x in els:
        if 'building' in x.get('tags', {}):
            out.append(f'<path d="{path(x["geometry"])}Z" fill="#DCD3F2"/>')
    roads = [x for x in els if x.get('tags', {}).get('highway') in ROADW]
    roads.sort(key=lambda x: ROADW[x['tags']['highway']])
    for x in roads:
        w = ROADW[x['tags']['highway']]
        out.append(f'<path d="{path(x["geometry"])}" fill="none" stroke="#FFFFFF" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    # подписи главных улиц: по одной на название, на самом длинном отрезке
    # подписи улиц: для каждого названия — на середине самой длинной цепочки, по возможности внутри карты
    best = {}
    for x in roads:
        nm = x['tags'].get('name')
        if not nm or x['tags']['highway'] in ('service', 'pedestrian'): continue
        g = [P(p['lat'], p['lon']) for p in x['geometry']]
        g = [q for q in g if 30 < q[0] < W - 30 and 30 < q[1] < H - 30]
        if len(g) < 2: continue
        L = sum(math.hypot(b2[0] - a2[0], b2[1] - a2[1]) for a2, b2 in zip(g, g[1:]))
        if L > best.get(nm, (0,))[0]: best[nm] = (L, g)
    short = lambda n: n.replace('улица ', 'ул. ').replace(' улица', '').replace('проспект ', 'пр. ').replace('переулок', 'пер.')
    for nm, (L, g) in best.items():
        if L < 70: continue
        half, acc = L / 2, 0
        for (x1, y1), (x2, y2) in zip(g, g[1:]):
            seg = math.hypot(x2 - x1, y2 - y1)
            if acc + seg >= half: break
            acc += seg
        t = (half - acc) / seg if seg else 0
        cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        a = math.degrees(math.atan2(y2 - y1, x2 - x1))
        if a > 90: a -= 180
        if a < -90: a += 180
        out.append(f'<text x="{cx:.0f}" y="{cy:.0f}" transform="rotate({a:.0f} {cx:.0f} {cy:.0f})" text-anchor="middle" dy="5" class="cm-st">{html.escape(short(nm))}</text>')
    pins = []
    for i, (cat, name, addr, (x, y)) in enumerate(pts, 1):
        _, c, tc = CAT[cat]
        pins.append(f'<g class="cm-pin" data-n="{i}" data-cat="{cat}" transform="translate({x:.0f} {y:.0f})"><circle r="15" fill="{c}" stroke="#FFFFFF" stroke-width="3"/><text text-anchor="middle" dy="5" fill="{tc}">{i}</text></g>')
    svg = (f'<svg class="cm-svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Карта: {A["title"]}. Номера на карте совпадают с номерами в списке.">'
           + ''.join(out) + ''.join(pins) + '</svg>')
    items = ''.join(f'<li data-n="{i}" data-cat="{cat}"><button type="button" class="cm-it"><b style="background:{CAT[cat][1]};color:{CAT[cat][2]}">{i}</b><span><span class="cm-nm">{html.escape(name)}</span><span class="cm-ad">{html.escape(addr)}</span></span></button></li>'
                    for i, (cat, name, addr, _) in enumerate(pts, 1))
    return svg, items, len(pts)


def main():
    parts = {k: build(k) for k in AREAS}
    tabs = ''.join(f'<button type="button" class="cm-tab" data-area="{k}" aria-pressed="{"true" if k == "vtuz" else "false"}">{AREAS[k]["title"]} <small>{parts[k][2]}</small></button>' for k in AREAS)
    cats = '<button type="button" class="cm-cat" data-cat="all" aria-pressed="true">Все</button>' + ''.join(f'<button type="button" class="cm-cat" data-cat="{k}" aria-pressed="false"><i style="background:{c}"></i>{n}</button>' for k, (n, c, _) in CAT.items())
    areas = ''.join(f'<div class="cm-area" data-area="{k}"{"" if k == "vtuz" else " hidden"}><div class="cm-map">{parts[k][0]}</div><ol class="cm-list">{parts[k][1]}</ol></div>' for k in AREAS)
    block = f'''<!-- map -->
<section class="cm" aria-labelledby="cm-h">
<h2 id="cm-h" style="margin-top:64px">Карта кампусов</h2>
<p class="muted" style="margin-top:10px;max-width:70ch">Учебные корпуса, общежития, спорт, столовые и медицина. Нажмите на место в списке — оно подсветится на карте.</p>
<div class="cm-bar"><div class="cm-tabs" role="group" aria-label="Кампус">{tabs}</div><div class="cm-cats" role="group" aria-label="Что показать">{cats}</div></div>
{areas}
<p class="muted" style="font-size:13px;margin-top:10px">Карта нарисована по данным OpenStreetMap (© участники OpenStreetMap, лицензия ODbL).</p>
</section>
<!-- /map -->
'''
    f = os.path.join(SITE, 'Dorms.dc.html')
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- map -->.*?<!-- /map -->\n', '', s, flags=re.S)
    anchor = '<h2 style="margin-top:64px">Общежития в цифрах</h2>'
    assert anchor in s
    s = s.replace(anchor, block + anchor, 1)
    if 'campus-map.js' not in s:
        s = s.replace('<script src="site.js"></script>', '<script src="site.js"></script>\n<script src="campus-map.js"></script>', 1)
    open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok', {k: (len(v[0]) // 1024, v[2]) for k, v in parts.items()})


main()
