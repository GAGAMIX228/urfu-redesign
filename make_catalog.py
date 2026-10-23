"""Каталог программ из официальных данных: programs.edu.urfu.ru, набор 2026, бакалавриат и специалитет, очная форма.

  python make_catalog.py --fetch   — скачать список и страницы программ → data/programs-2026.json
  python make_catalog.py           — собрать ALL_PROGS в Catalog.dc.html и Search.dc.html и блоки под каталогом

Сайт УрФУ отдаёт страницы целиком только в сжатом виде (иначе соединение замирает на 16 КБ), поэтому просим gzip.
Проходных баллов на сайте программ нет — их берём из прежнего каталога (там они с источником и годом).
После сборки: make_program, make_home, make_quiz, make_admission, make_heroph, make_og (последним)."""
import gzip, html, json, os, re, sys, time, urllib.request

os.chdir(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://programs.edu.urfu.ru'
# отметку «набор 2026» на сайте проставили не всем программам, поэтому берём списки 2026 и 2025
# и оставляем те, у которых на странице есть сведения о приёме 2026 года
LISTS = [BASE + '/ru/?year=%d&lvl=bac&lvl=spc&frm=ft&inst=' % y for y in (2026, 2025)]
DATA = 'data/programs-2026.json'


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                b = r.read()
                return (gzip.decompress(b) if r.headers.get('Content-Encoding') == 'gzip' else b).decode('utf-8', 'ignore')
        except Exception as e:
            print('  повтор', url, e); time.sleep(2 + attempt * 3)
    raise SystemExit('не скачалось: ' + url)


def lines(s):
    t = html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S))
    t = re.sub(r'<[^>]+>', '\n', t)
    return [x.strip() for x in t.split('\n') if x.strip()]


def after(L, key, n=1):
    for i, x in enumerate(L):
        if x == key: return L[i + 1:i + 1 + n]
    return []


def parse(pid, s):
    L = lines(s)
    title = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    name = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', title.group(1)))).strip() if title else ''
    code = after(L, 'Направление подготовки:', 2)
    p = dict(id=pid, name=name, code=code[0] if code else '', dir=code[1] if len(code) > 1 else '',
             inst_full=(after(L, 'Институт:') or [''])[0], lvl=(after(L, 'Уровень образования:') or [''])[0])
    # форма и срок: строки после «Форма и срок обучения:» до «Язык обучения:» / «Открытая…»
    i = L.index('Форма и срок обучения:') if 'Форма и срок обучения:' in L else -1
    forms = []
    if i >= 0:
        for x in L[i + 1:i + 6]:
            if x.startswith(('Язык', 'Открытая', 'Закрытая')): break
            forms.append(x)
    p['forms'] = forms
    # описание: первые абзацы после «Язык обучения:» и его значения
    j = L.index('Язык обучения:') + 2 if 'Язык обучения:' in L else -1
    desc = []
    if j > 0:
        for x in L[j:j + 40]:
            if re.match(r'(Участие партнеров|Контакты|Индивидуальные образовательные|Актуально)', x): break
            desc.append(x)
    p['desc'] = re.sub(r'\s+', ' ', ' '.join(desc)).strip()
    # минимальные баллы 2026: пары «предмет, балл»; «По выбору:» открывает группу выбора
    k = next((i for i, x in enumerate(L) if x.startswith('Минимальные баллы')), -1)
    req, choice = [], []; cur = req
    if k >= 0:
        q = k + 1
        while q < len(L) - 1 and L[q] != 'Вступительные испытания':
            if L[q] == 'По выбору:': cur = choice; q += 1; continue
            if re.fullmatch(r'\d{1,3}', L[q + 1]): cur.append([L[q], int(L[q + 1])]); q += 2
            else: q += 1
    p['req'], p['choice'] = req, choice
    num = lambda key: int(re.sub(r'\D', '', after(L, key)[0])) if after(L, key) and re.search(r'\d', after(L, key)[0]) else None
    p['price'], p['disc'], p['budget'], p['paid'] = num('Полная'), num('Со скидкой'), num('Бюджетных'), num('Внебюджетных')
    c = next((i for i, x in enumerate(L) if x == 'Руководитель образовательной программы'), -1)
    p['head'] = L[c - 1] if c > 0 else ''
    p['years'] = (after(L, 'Год(ы) набора:') or [''])[0]
    my = next((x for x in L if x.startswith('Минимальные баллы')), '')
    p['mins_year'] = (re.search(r'\d{4}', my) or [''])[0] if my else ''
    return p


if '--fetch' in sys.argv:
    ids = []
    for url in LISTS:
        lst = get(url)
        found = re.search(r'Найдено (\d+)', lst)
        print(url, '→', found.group(1) if found else '?')
        ids += re.findall(r'href="/ru/(\d+)/"', lst)
    ids = list(dict.fromkeys(ids))
    print('всего разных программ', len(ids))
    out = []
    for n, pid in enumerate(ids, 1):
        x = parse(pid, get(BASE + '/ru/%s/' % pid))
        x['y2026'] = x['years'].endswith('2026') or x['mins_year'] == '2026'
        if x['y2026']:  # английское название — для английской версии каталога
            t = re.search(r'<h1[^>]*>(.*?)</h1>', get(BASE + '/en/%s/' % pid), re.S)
            x['name_en'] = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', t.group(1)))).strip() if t else ''
        out.append(x)
        print(n, pid, out[-1]['name'], '|', out[-1]['inst_full'][:40], '|', out[-1]['budget'], out[-1]['price'], flush=True)
        time.sleep(0.3)
    os.makedirs('data', exist_ok=True)
    json.dump({'source': LISTS, 'date': time.strftime('%Y-%m-%d'), 'programs': out}, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('сохранено', DATA)
    sys.exit()

# ── сборка каталога ──
D = json.load(open(DATA, encoding='utf-8'))
SHORT = {'Уральский гуманитарный институт': 'УГИ', 'Институт радиоэлектроники и информационных технологий - РтФ': 'ИРИТ-РтФ',
         'Институт естественных наук и математики': 'ИЕНиМ', 'Институт экономики и управления': 'ИнЭУ',
         'Институт новых материалов и технологий': 'ИНМиТ', 'Физико-технологический институт': 'ФТИ',
         'Уральский энергетический институт': 'УралЭНИН', 'Институт Строительства и Архитектуры': 'ИСА',
         'Институт физической культуры, спорта и молодежной политики': 'ИФКСиМП', 'Институт фундаментального образования': 'ИнФО',
         'Химико-технологический институт': 'ХТИ', 'Уральская передовая инженерная школа «Цифровое производство»': 'УПИШ'}
SUBJ = {'Русский язык': 'rus', 'Математика': 'math', 'Информатика': 'inf', 'Физика': 'phys', 'Химия': 'chem', 'Биология': 'bio',
        'Обществознание': 'soc', 'История': 'hist', 'Литература': 'lit', 'География': 'geo'}
WORD = {'rus': 'русский', 'math': 'математика', 'inf': 'информатика', 'phys': 'физика', 'chem': 'химия', 'bio': 'биология',
        'soc': 'обществознание', 'hist': 'история', 'lit': 'литература', 'geo': 'география', 'lang': 'иностранный язык'}
AREA = {'it': 'IT', 'eng': 'Инженерия', 'nat': 'Естественные науки', 'hum': 'Гуманитарные', 'eco': 'Экономика'}


def subj(t):
    if t.startswith('Иностранный язык'): return 'lang'
    if t.startswith('Испытание') or 'творческ' in t.lower(): return 'tvor'
    return SUBJ.get(t)


def area_by_code(code):
    g = int(code[:2])
    if g in (2, 9, 10, 11): return 'it'
    if g in (1, 3, 4, 5, 6): return 'nat'
    if g == 38: return 'eco'
    if 7 <= g <= 29: return 'eng'
    return 'hum'


cat = open('Catalog.dc.html', encoding='utf-8').read()
a = cat.index('const ALL_PROGS = ['); b = cat.index('];', a) + 2
OLD = {}
for m in re.finditer(r"\{name:'([^']+)'(.*?)\}(?=,\n|\n\])", cat[a:b]):
    g = lambda k: (re.search(k + r":'([^']*)'", m.group(2)) or [None, None])[1]
    OLD[m.group(1)] = dict(k=g('k'), score=g('score'), sy=g('sy'))

# прежние названия-направления → официальные названия программ (тот же номер страницы на programs.edu.urfu.ru)
RENAME = {'Информационная безопасность': 'Безопасность компьютерных систем',
          'Строительство': 'Строительство зданий, сооружений и развитие территорий',
          'Лингвистика': 'Лингвистика в сфере деловых и профессиональных коммуникаций и информационных технологий',
          'Международные отношения': 'Международные отношения и мировая политика'}
for o, n in RENAME.items():
    if o in OLD and n not in OLD: OLD[n] = OLD[o]
js = lambda v: json.dumps(v, ensure_ascii=False)
q = lambda v: "'" + str(v).replace(chr(92), chr(92) * 2).replace("'", chr(92) + "'") + "'"
out, skipped = [], []
for p in D['programs']:
    if not p.get('y2026'): continue
    inst = SHORT.get(p['inst_full'])
    if not inst: skipped.append((p['name'], p['inst_full'])); continue
    codes_req = [subj(t) for t, _ in p['req']]
    codes_ch = [subj(t) for t, _ in p['choice']]
    creative = 'tvor' in codes_req + codes_ch
    req = [c for c in codes_req if c and c != 'tvor']
    ch = [[c for c in codes_ch if c and c != 'tvor']] if [c for c in codes_ch if c and c != 'tvor'] else []
    words = [WORD[c] for c in req if c != 'rus']
    if ch: words.append(' или '.join(WORD[c] for c in ch[0]))
    if creative: words.insert(0, 'творческое испытание')
    if 'rus' in req: words.append('русский')
    exams = ', '.join(words) or 'свои вступительные испытания — на сайте программы'
    old = OLD.get(p['name'], {})
    k = old.get('k') or area_by_code(p['code'])
    mins = [[WORD.get(subj(t), t.lower()), n] for t, n in p['req'] + p['choice'] if subj(t) != 'tvor']
    dur = '; '.join(f.replace('Очная: ', '') for f in p['forms'] if f.startswith('Очная')) or ''
    desc = p['desc']
    lead = re.split(r'(?<=[.!?])\s+', desc)[0] if desc else ''
    if len(lead) > 230: lead = lead[:lead.rfind(' ', 0, 225)] + '…'
    fmt = lambda n: f'{n:,}'.replace(',', ' ') + ' ₽'
    e = [f"name:{q(p['name'])}", f"inst:{q(inst)}", f"area:{q(AREA[k])}", f"k:{q(k)}", f"exams:{q(exams)}",
         f"req:{js(req)}", f"ch:{js(ch)}"]
    if old.get('score'): e.append(f"score:{q(old['score'])}")
    if old.get('sy'): e.append(f"sy:{q(old['sy'])}")
    e.append(f"budget:{q(p['budget'] if p['budget'] else ('0' if p['paid'] else '—'))}")
    if p['price']: e.append(f"price:{q(fmt(p['price']))}")
    if p['disc']: e.append(f"disc:{q(fmt(p['disc']))}")
    if p['paid']: e.append(f"paid:{q(p['paid'])}")
    e += [f"lvl:{q('spec' if p['lvl'].startswith('Специал') else 'bach')}", f"dur:{q(dur)}", f"code:{q(p['code'])}", f"id:{q(p['id'])}",
          f"mins:{js(mins)}", f"lead:{q(lead)}", f"head:{q(p['head'])}"]
    out.append('{' + ', '.join(e) + '}')
print('в каталог:', len(out), '| пропущены (филиалы):', skipped)
lost = [n for n in OLD if n not in {p['name'] for p in D['programs']}]
print('из прежнего каталога нет в данных 2026:', lost)
PROGS = 'const ALL_PROGS = [\n' + ',\n'.join(out) + '\n];'
for f in ('Catalog.dc.html', 'Search.dc.html'):
    s = open(f, encoding='utf-8').read()
    i = s.index('const ALL_PROGS = ['); j = s.index('];', i) + 2
    open(f, 'w', encoding='utf-8', newline='').write(s[:i] + PROGS + s[j:])
print('ALL_PROGS записан в Catalog и Search')

# ── блоки под каталогом (только русская версия): по областям, «самые-самые», IT, ещё программы ──
from urllib.parse import quote
num = lambda x: int(re.sub(r'\D', '', x)) if x and re.search(r'\d', x) else None
progs = []
for m in re.finditer(r"\{name:'((?:[^'\\]|\\.)+)', inst:'([^']+)', area:'([^']+)', k:'(\w+)'(.*?)\}(?=,\n|\n\])", PROGS):
    rest = m.group(5)
    g = lambda k: (re.search(k + r":'((?:[^'\\]|\\.)*)'", rest) or [None, None])[1]
    progs.append(dict(name=m.group(1).replace("\\'", "'"), inst=m.group(2), k=m.group(4), score=g('score'), sy=g('sy') or '2025',
                      budget=g('budget'), price=g('price')))
href = lambda n: 'Program.dc.html?p=' + quote(n)
AREAS = [('it', 'IT'), ('eng', 'Инженерия'), ('nat', 'Естественные науки'), ('hum', 'Гуманитарные'), ('eco', 'Экономика')]
plural = lambda n: 'программа' if n % 10 == 1 and n % 100 != 11 else ('программы' if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else 'программ')
rows = ''
for k, n in AREAS:
    ps = [x for x in progs if x['k'] == k]
    sc = [num(x['score']) for x in ps if num(x['score'])]
    pr = [num(x['price']) for x in ps if num(x['price'])]
    bu = sum(num(x['budget']) or 0 for x in ps)
    lo, hi = (min(sc), max(sc)) if sc else (None, None)
    bar = (f'<div class="cg-bar" aria-hidden="true"><i style="left:{(lo - 150) / 1.5:.1f}%;width:{max(2, (hi - lo) / 1.5):.1f}%"></i></div>'
           if sc else '<div class="cg-bar is-empty" aria-hidden="true"></div>')
    rng = f'{lo}–{hi}' if sc and lo != hi else (str(lo) if sc else 'нет данных')
    price = (f'{min(pr):,}–{max(pr):,} ₽'.replace(',', ' ') if len(set(pr)) > 1 else f'{pr[0]:,} ₽'.replace(',', ' ')) if pr else '—'
    rows += (f'<li><a class="cg-a" href="Catalog.dc.html?area={k}">{n}</a><span class="cg-n">{len(ps)} прогр.</span>{bar}'
             f'<span class="cg-v"><small>балл</small>{rng}</span><span class="cg-v"><small>бюджет</small>{bu or "—"}</span>'
             f'<span class="cg-v"><small>цена в год</small>{price}</span></li>')
li = lambda x, v, sub: f'<li><a href="{href(x["name"])}">{x["name"]}</a><b>{v}</b><span>{sub}</span></li>'
top = ''.join(li(x, x['score'], x['inst'] + ' · ' + x['sy']) for x in sorted([x for x in progs if num(x['score'])], key=lambda x: -num(x['score']))[:5])
big = ''.join(li(x, x['budget'], x['inst']) for x in sorted([x for x in progs if num(x['budget'])], key=lambda x: -num(x['budget']))[:5])
cheap = ''.join(li(x, x['price'], x['inst']) for x in sorted([x for x in progs if num(x['price'])], key=lambda x: num(x['price']))[:5])
its = sorted([x for x in progs if x['k'] == 'it'], key=lambda x: (-(num(x['score']) or 0), -(num(x['budget']) or 0)))
it_rows = ''.join(f'<div class="cg-ir"><a href="{href(x["name"])}">{x["name"]}</a><span><small>Институт</small>{x["inst"]}</span>'
                  f'<span><small>Балл</small>{x["score"] or "—"}</span><span><small>Бюджет</small>{x["budget"] or "—"}</span>'
                  f'<span><small>Цена в год</small>{x["price"] or "—"}</span></div>' for x in its)
more = sorted([p for p in D['programs'] if not p.get('y2026') and SHORT.get(p['inst_full'])], key=lambda p: (SHORT[p['inst_full']], p['name']))
more_html = ''.join(f'<li><a href="{BASE}/ru/{p["id"]}/" target="_blank" rel="noopener">{p["name"]}<span class="sr"> (откроется в новой вкладке)</span></a>'
                    f'<span>{SHORT[p["inst_full"]]} · {p["code"]}</span></li>' for p in more)
n_sc = sum(1 for x in progs if num(x['score']))

cat = open('Catalog.dc.html', encoding='utf-8').read()
i = cat.index('<!-- ru-only -->'); j = cat.index('<!-- /ru-only -->') + len('<!-- /ru-only -->')
blk = cat[i:j]


def sub(pat, new):
    global blk
    m2 = re.search(pat, blk, re.S); assert m2, pat
    blk = blk[:m2.start()] + new + blk[m2.end():]


sub(r'<ul class="cg-areas">.*?</ul>', f'<ul class="cg-areas">{rows}</ul>')
sub(r'<p class="muted" style="font-size:14px;margin-top:10px">Считаем по данным каталога:.*?</p>',
    f'<p class="muted" style="font-size:14px;margin-top:10px">Считаем по данным каталога: места и цены 2026 года — с сайта образовательных '
    f'программ УрФУ, проходные баллы 2024–2025 годов — у {n_sc} программ, где они есть с источником. «—» — данных нет.</p>')
tops = re.findall(r'<ol class="cg-top">.*?</ol>', blk, re.S); assert len(tops) == 3
for old_, new_ in zip(tops, (top, big, cheap)): blk = blk.replace(old_, f'<ol class="cg-top">{new_}</ol>', 1)
sub(r'<p class="muted" style="margin-top:8px;max-width:760px">Самая востребованная область — .*?</p>',
    f'<p class="muted" style="margin-top:8px;max-width:760px">Самая востребованная область — {len(its)} {plural(len(its))}. '
    f'Сначала — с известным проходным баллом.</p>')
a2 = blk.index('<div class="cg-it">'); b2 = blk.index('</section>', a2)
head_row = re.match(r'<div class="cg-it"><div class="cg-ir cg-irh" aria-hidden="true">.*?</div>', blk[a2:], re.S).group(0)
blk = blk[:a2] + head_row + it_rows + '</div>\n' + blk[b2:]
blk = re.sub(r'\n?<section class="sec" aria-labelledby="cg-m-h">.*?</section>', '', blk, flags=re.S)
more_sec = (f'\n<section class="sec" aria-labelledby="cg-m-h">\n<h2 id="cg-m-h">Ещё {len(more)} {plural(len(more))}: набор 2025 года</h2>\n'
            f'<p class="muted" style="margin-top:8px;max-width:760px">На сайте образовательных программ у них пока нет сведений о приёме '
            f'2026 года — экзаменов, мест и цен. Поэтому их нет в фильтрах выше; ссылки ведут на официальные страницы.</p>\n'
            f'<details class="cg-more"><summary>Показать все {len(more)}</summary><ul>{more_html}</ul></details>\n</section>')
anchor = '\n<section class="sec" aria-labelledby="cg-s-h">'
assert anchor in blk
blk = blk.replace(anchor, more_sec + anchor, 1)
faq = re.search(r'<details><summary>Где магистратура и аспирантура\?</summary><p class="muted">.*?</p></details>', blk, re.S).group(0)
blk = blk.replace(faq, '<details><summary>Где магистратура и аспирантура?</summary><p class="muted">В прототипе каталог показывает бакалавриат '
                       'и специалитет — с них начинают после школы. Магистерские программы есть на сайте образовательных программ УрФУ.</p></details>')
cat = cat[:i] + blk + cat[j:]
if '.cg-more{' not in cat:
    css = ('.cg-more{margin-top:16px;border:1px solid var(--line);border-radius:16px;background:#FFFFFF;padding:14px 18px}'
           '.cg-more summary{cursor:pointer;font-weight:600;min-height:32px;display:flex;align-items:center}'
           '.cg-more ul{list-style:none;margin:12px 0 0;padding:0;columns:2 320px;column-gap:28px}'
           '.cg-more li{break-inside:avoid;display:flex;flex-direction:column;padding:6px 0;border-top:1px solid var(--line)}'
           '.cg-more li span:not(.sr){font-size:13px;color:var(--muted)}\n')
    cat = cat.replace('<style id="cg-css">\n', '<style id="cg-css">\n' + css, 1)
    assert '.cg-more{' in cat
open('Catalog.dc.html', 'w', encoding='utf-8', newline='').write(cat)
print('блоки под каталогом пересчитаны; ещё программ:', len(more), '; с проходным баллом:', n_sc)
