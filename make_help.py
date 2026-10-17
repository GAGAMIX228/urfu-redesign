"""Центр помощи (Help.dc.html): поиск по частым вопросам, темы, справочник служб, горячие линии.
Все ответы и контакты — из открытых страниц urfu.ru (копии в веб-архиве 2025–2026) и приказов УрФУ.
Шапка и подвал берутся из NotFound.dc.html. Запуск: python make_help.py (можно повторно)."""
import os, json, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WA = 'https://web.archive.org/web/'
SRC = {
    'cal': WA + '20260831155039/https://urfu.ru/ru/applicant/docs-abiturient/kalendar-priema/',
    'hot': WA + '20251114010920/https://urfu.ru/ru/feedback/priem/obshchie-voprosy-po-priemu/',
    'pos': WA + '20251114102246/https://urfu.ru/ru/students/social/campus/',
    'cont': WA + '20251114044926/https://urfu.ru/ru/contacts/',
    'line': WA + '20251114063908/https://urfu.ru/ru/students/social/gorjachaja-linija-dlja-studentov/',
}

TOPICS = [('all', 'Все'), ('adm', 'Поступление'), ('dorm', 'Общежитие'), ('study', 'Учёба'), ('health', 'Здоровье'), ('money', 'Деньги'), ('it', 'Wi-Fi и почта')]

# (тема, вопрос, ответ, ссылка, текст ссылки, источник)
FAQ = [
    ('adm', 'Когда начинается приём документов?', 'С 20 июня. На бюджет по результатам ЕГЭ документы принимают до 25 июля, с экзаменами УрФУ — до 15 июля. Это даты приёма-2026; правила следующего года УрФУ публикует зимой.', 'Admission.dc.html#calendar', 'Весь календарь приёма', 'cal'),
    ('adm', 'Как подать документы, не приезжая в Екатеринбург?', 'Через Госуслуги (сервис «Поступление в вуз онлайн») или в личном кабинете абитуриента на сайте приёмной комиссии. Лично — ул. Мира, 19, аудитория ГУК-100.', 'Admission.dc.html#apply', 'Способы подачи', 'cont'),
    ('adm', 'Хватит ли моих баллов на бюджет?', 'Сравните сумму с проходными баллами прошлых лет: на главной есть ползунок баллов, а в каталоге — фильтр по сумме и ЕГЭ. У каждой программы — баллы за несколько лет.', 'Catalog.dc.html', 'Каталог программ', ''),
    ('adm', 'Дают ли дополнительные баллы за службу в армии?', 'Да, 10 баллов за индивидуальное достижение — всем, кто прошёл службу в Вооружённых силах России. Подтверждается копией двух первых разворотов военного билета.', '', '', 'hot'),
    ('adm', 'Когда день открытых дверей?', 'Обычно в январе. Перед приёмом-2026 приёмная комиссия называла ориентировочно 17–18 января — точную дату объявляют на сайте.', 'Events.dc.html', 'Календарь событий', 'hot'),
    ('adm', 'Когда подавать согласие на зачисление?', 'До 14:00 в день этапа: 1 августа — квоты и олимпиадники, 5 августа — основной этап, 9 августа — дополнительный. Без согласия на бюджет не зачисляют.', 'Admission.dc.html#lists', 'Как работают списки', 'cal'),
    ('adm', 'Сколько стоит платное обучение?', 'Зависит от программы: в нашем каталоге — от 246 000 до 390 000 ₽ в год. Есть скидки отдельным категориям и образовательный кредит с господдержкой под 3% годовых.', 'Admission.dc.html#cost', 'Посчитать стоимость', ''),
    ('dorm', 'Как получить место в общежитии?', 'Отметьте потребность в общежитии при подаче документов. Первокурсников в 2025 году заселяли в три этапа: 25–29 августа, в сентябре и в октябре — на освободившиеся места. Графики и списки готовят жилищные комиссии институтов.', 'Dorms.dc.html', 'Кампус и общежития', 'pos'),
    ('dorm', 'Сколько стоит общежитие?', 'В студгородке — от 1 340 до 2 110 ₽ в месяц вдвоём в комнате, вместе с коммунальными. В кампусе Новокольцовский — около 2 380 ₽. Летом без отопления дешевле.', 'Dorms.dc.html#price-h', 'Таблица цен', ''),
    ('dorm', 'Какой медосмотр нужен для заселения?', 'В медсанчасти УрФУ на Комсомольской, 59 или в медцентре кампуса Новокольцовский. С собой: паспорт, СНИЛС, полис ОМС, прививочный сертификат и флюорография не старше 11 месяцев. Осмотр в 2025 году стоил 210 ₽, флюорография — 234 ₽.', '', '', 'pos'),
    ('dorm', 'Что делать, если места в общежитии не хватило?', 'Университет помогает со съёмным жильём — проект «Платное жильё». Вопросы о местах решает жилищная комиссия вашего института.', 'Dorms.dc.html', 'Кампус и общежития', 'pos'),
    ('study', 'Где посмотреть расписание своей группы?', 'На странице «Расписание»: выберите буквы группы и введите 6 цифр. Сайт запомнит группу, и в следующий раз пары откроются сразу.', 'Schedule.dc.html', 'Открыть расписание', ''),
    ('study', 'Куда жаловаться, если нарушают права студента?', 'Горячая линия Минобрнауки по правовой и социальной защите студентов: 8-800-222-55-71, добавочный 1. Учёба и аттестация, перевод, стипендии, общежитие, документы об образовании.', '', '', 'line'),
    ('health', 'Где медпункт и поликлиника?', 'Медсанчасть УрФУ — ул. Комсомольская, 59, пн–пт 8:00–18:00. В кампусе Новокольцовский — медцентр на ул. 100-летия Университета, стр. 10, пн–пт 8:30–17:00.', 'Contacts.dc.html', 'На карте', 'pos'),
    ('health', 'Мне тяжело, нужна психологическая помощь', 'Горячая линия психологической помощи студентам: 8-800-222-55-71, добавочный 2. Тревога, напряжение в учёбе, трудности в отношениях. Звонок бесплатный.', '', '', 'line'),
    ('money', 'Кто поможет со стипендией и выплатами?', 'Начисления ведёт ваш институт. Если выплату задерживают или отказывают без причины — горячая линия Минобрнауки 8-800-222-55-71, добавочный 1.', '', '', 'line'),
    ('money', 'Как оплатить общежитие или медосмотр?', 'Через сервис электронных платежей УрФУ pay.urfu.ru, Систему быстрых платежей по QR-коду или в кассе медсанчасти.', '', '', 'pos'),
    ('it', 'Не работает Wi-Fi, почта или доступ к сервисам', 'Техподдержка УрФУ: +7 (343) 227-20-70, support@urfu.ru.', '', '', 'cont'),
]

# (название, что решает, телефон, tel, почта, часы/адрес, ключевые слова)
DIR = [
    ('Контакт-центр', 'Любые вопросы об университете', '8-800-100-50-44', '88001005044', 'contact@urfu.ru', 'Бесплатно по России. Пн–пт 8:30–19:00, сб 10:00–16:00', 'общий вопрос справка'),
    ('Приёмная комиссия', 'Поступление, документы, списки', '+7 (343) 375-44-74', '+73433754474', 'priem@urfu.ru', 'ул. Мира, 19, ГУК-100', 'поступление абитуриент'),
    ('Техподдержка', 'Wi-Fi, почта, личный кабинет', '+7 (343) 227-20-70', '+73432272070', 'support@urfu.ru', '', 'it интернет пароль'),
    ('Медсанчасть УрФУ', 'Медосмотр, справки, лечение', '', '', '', 'ул. Комсомольская, 59. Пн–пт 8:00–18:00', 'врач здоровье медосмотр'),
    ('Пресс-служба', 'Для журналистов', '+7 (343) 375-97-33', '+73433759733', 'news@urfu.ru', '', 'сми журналист'),
    ('Реклама и партнёрство', 'Реклама в университете', '+7 (343) 375-93-53', '+73433759353', 'partner@urfu.ru', '', 'партнёр бизнес'),
]

LINES = [
    ('Правовая защита студентов', '8-800-222-55-71', 'доб. 1', 'Учёба, перевод, стипендии, общежитие'),
    ('Психологическая помощь', '8-800-222-55-71', 'доб. 2', 'Тревога, стресс, трудности в отношениях'),
]


def main_html():
    lines = ''.join(f'<div class="hl-line"><b>{t}</b><a href="tel:88002225571" class="hl-tel">{p} <span>{a}</span></a><span class="muted">{d}</span></div>' for t, p, a, d in LINES)
    return f'''<main id="main" tabindex="-1" style="outline:none"><section class="phead hp-head"><div class="wrap">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / Центр помощи</div>
<h1 class="big" style="font-size:52px">Чем помочь?</h1>
<p class="muted" style="margin-top:12px;font-size:19px;max-width:720px">Ответы на частые вопросы и контакты служб — в одном месте. Ответы — по открытым страницам urfu.ru и приказам университета, со ссылками на источники.</p>
<div class="hp-search" role="search"><label for="help-q" class="sr">Поиск по вопросам и службам</label>
<input id="help-q" type="search" placeholder="Например: общага, медосмотр, стипендия" value="{{{{q}}}}" onChange="{{{{setQ}}}}" autocomplete="off">
<sc-if value="{{{{hasQ}}}}" hint-placeholder-val="{{{{false}}}}"><button type="button" class="hp-clear" onClick="{{{{clear}}}}">Очистить</button></sc-if></div>
<div class="hp-topics" role="group" aria-label="Темы">
<sc-for list="{{{{topics}}}}" as="t" hint-placeholder-count="7"><button type="button" class="chip hp-chip" aria-pressed="{{{{t.on}}}}" onClick="{{{{t.pick}}}}">{{{{t.n}}}}</button></sc-for>
</div>
</div></section>
<div class="wrap hp-body">
<div class="hp-main">
<h2 id="faq-h">Частые вопросы</h2>
<p class="muted hp-count" aria-live="polite">{{{{countText}}}}</p>
<div class="hp-faq">
<sc-for list="{{{{faq}}}}" as="f" hint-placeholder-count="6"><details class="hp-q"><summary><span class="tag">{{{{f.tn}}}}</span>{{{{f.q}}}}</summary><div class="hp-a"><p>{{{{f.a}}}}</p>
<div class="hp-links"><sc-if value="{{{{f.href}}}}" hint-placeholder-val="{{{{true}}}}"><a href="{{{{f.href}}}}">{{{{f.lt}}}} →</a></sc-if><sc-if value="{{{{f.src}}}}" hint-placeholder-val="{{{{true}}}}"><a class="hp-src" href="{{{{f.src}}}}" target="_blank" rel="noopener">Источник: urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a></sc-if></div></div></details></sc-for>
<sc-if value="{{{{none}}}}" hint-placeholder-val="{{{{false}}}}"><div class="card hp-none"><b>Такого вопроса пока нет.</b><p class="muted">Позвоните в контакт-центр — <a href="tel:88001005044">8-800-100-50-44</a>, бесплатно по России. Или задайте вопрос на горячей линии приёмной комиссии: там отвечают за 2–3 рабочих дня.</p></div></sc-if>
</div>
<h2 id="dir-h" style="margin-top:56px">Справочник служб</h2>
<div class="hp-dir">
<sc-for list="{{{{dir}}}}" as="d" hint-placeholder-count="6"><div class="card hp-svc"><b>{{{{d.n}}}}</b><span class="muted">{{{{d.w}}}}</span>
<sc-if value="{{{{d.tel}}}}" hint-placeholder-val="{{{{true}}}}"><a class="hp-tel" href="tel:{{{{d.tel}}}}">{{{{d.p}}}}</a></sc-if>
<sc-if value="{{{{d.m}}}}" hint-placeholder-val="{{{{true}}}}"><a href="mailto:{{{{d.m}}}}">{{{{d.m}}}}</a></sc-if>
<sc-if value="{{{{d.h}}}}" hint-placeholder-val="{{{{true}}}}"><span class="hp-h">{{{{d.h}}}}</span></sc-if></div></sc-for>
<sc-if value="{{{{dirNone}}}}" hint-placeholder-val="{{{{false}}}}"><p class="muted">По этому запросу служб не нашлось — <button type="button" class="hp-link" onClick="{{{{clear}}}}">показать все</button>.</p></sc-if>
</div>
<p class="muted" style="margin-top:14px;font-size:14px">Контакты — со страницы <a href="{SRC['cont']}" target="_blank" rel="noopener">«Контакты» urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</div>
<aside class="hp-side" aria-labelledby="hl-h">
<div class="hp-lines"><h2 id="hl-h">Если трудно</h2><p>Бесплатные горячие линии Минобрнауки для студентов — звонок по России бесплатный.</p>{lines}</div>
<div class="card hp-ask"><h3>Не нашли ответ?</h3><p class="muted">Контакт-центр отвечает на любые вопросы об УрФУ.</p><a class="btn" href="tel:88001005044">8-800-100-50-44</a><a class="btn2" href="mailto:contact@urfu.ru">Написать на contact@urfu.ru</a></div>
</aside>
</div>
</main>'''


LOGIC = '''<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
const FAQ = __FAQ__, DIR = __DIR__, TOP = __TOP__, SRC = __SRC__;
const st = this.state || {};
let q0 = st.q; if (q0 === undefined) { q0 = new URLSearchParams(location.search).get('q') || ''; }
const t = st.t || 'all';
// живые слова → слова из ответов
const SYN = { 'общаг': 'общежит', 'стипух': 'стипенд', 'вайфай': 'wi-fi', 'вай-фай': 'wi-fi', 'инет': 'wi-fi', 'врач': 'мед', 'больниц': 'мед', 'деньг': 'оплат', 'армия': 'армии' };
let q = q0.toLowerCase().trim(); Object.keys(SYN).forEach(k => { q = q.split(k).join(SYN[k]); });
const words = q.split(/\\s+/).filter(w => w.length > 1).map(w => w.slice(0, Math.max(4, w.length - 2)));
const hit = s => words.every(w => s.toLowerCase().indexOf(w) !== -1);
const TN = {}; TOP.forEach(([k, n]) => TN[k] = n);
const faq = FAQ.filter(f => (t === 'all' || f[0] === t) && hit(f[1] + ' ' + f[2] + ' ' + TN[f[0]]))
  .map(f => ({ tn: TN[f[0]], q: f[1], a: f[2], href: f[3], lt: f[4], src: f[5] ? SRC[f[5]] : '' }));
const dir = DIR.filter(d => hit(d.join(' '))).map(d => ({ n: d[0], w: d[1], p: d[2], tel: d[3], m: d[4], h: d[5] }));
const n = faq.length;
const form = n % 10 === 1 && n % 100 !== 11 ? 'ответ' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'ответа' : 'ответов';
return {
  q: q0, hasQ: !!q0,
  setQ: e => this.setState({ q: e.target.value }),
  clear: () => this.setState({ q: '', t: 'all' }),
  topics: TOP.map(([k, nm]) => ({ n: nm, on: String(k === t), pick: () => this.setState({ t: k }) })),
  faq, none: n === 0, dir, dirNone: dir.length === 0,
  countText: (q0 || t !== 'all') ? (n ? 'Нашлось ' + n + ' ' + form : 'Ничего не нашлось') : n + ' ' + form + ' на частые вопросы'
};
}
}
</script>'''

CSS = '''
/* Центр помощи */
.hp-head{padding-bottom:8px}
.hp-search{margin-top:28px;display:flex;gap:8px;max-width:680px}
.hp-search input{flex:1;min-width:0;min-height:56px;padding:0 20px;border-radius:16px;border:2px solid var(--limestone);font:inherit;font-size:18px;background:#FFFFFF;color:var(--ink)}
.hp-search input:focus-visible{outline:3px solid var(--amethyst);outline-offset:2px;border-color:var(--amethyst)}
.hp-clear{min-height:56px;padding:0 18px;border-radius:16px;border:0;background:var(--ink);color:#FFFFFF;font:inherit;font-weight:600;cursor:pointer}
.hp-topics{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.hp-chip{cursor:pointer;font:inherit}
.hp-chip[aria-pressed="true"]{background:var(--ink);color:#FFFFFF;border-color:var(--ink)}
.hp-body{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:40px;align-items:start;padding-top:48px;padding-bottom:72px}
.hp-count{margin-top:6px}
.hp-faq{margin-top:16px;display:flex;flex-direction:column;gap:10px}
.hp-q{background:#FFFFFF;border:1px solid var(--limestone);border-radius:16px;padding:0}
.hp-q summary{padding:18px 20px;font-weight:600;cursor:pointer;display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;line-height:1.4}
.hp-q summary .tag{font-size:12px;font-weight:600}
.hp-q[open] summary{border-bottom:1px solid var(--limestone)}
.hp-a{padding:16px 20px 20px;line-height:1.6}
.hp-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:12px;font-size:15px}
.hp-src{color:var(--muted)}
.hp-none p{margin-top:8px}
.hp-dir{margin-top:20px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.hp-svc{display:flex;flex-direction:column;gap:4px;padding:20px}
.hp-svc b{font-family:var(--narrow);font-size:20px}
.hp-tel{font-weight:700;font-size:18px;margin-top:6px}
.hp-h{font-size:14px;color:var(--muted)}
.hp-link{border:0;background:none;padding:0;font:inherit;color:var(--amethyst);text-decoration:underline;cursor:pointer}
.hp-side{position:sticky;top:96px;display:flex;flex-direction:column;gap:16px}
.hp-lines{background:var(--ink);color:#FFFFFF;border-radius:20px;padding:24px}
.hp-lines h2{color:#FFFFFF;font-size:26px}
.hp-lines>p{color:#D9D2F0;margin-top:8px;font-size:15px}
.hl-line{margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.15);display:flex;flex-direction:column;gap:2px}
.hl-line b{color:#FFFFFF}
.hl-line .muted{color:#D9D2F0;font-size:14px}
.hl-tel{color:var(--gold);font-weight:700;font-size:22px;text-decoration:none;font-family:var(--narrow)}
.hl-tel span{font-size:16px}
.hl-tel:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.hp-ask{display:flex;flex-direction:column;gap:10px}
.hp-ask .btn,.hp-ask .btn2{text-align:center;justify-content:center}
@media (max-width:980px){.hp-body{grid-template-columns:1fr}.hp-side{position:static}}
@media (max-width:620px){.hp-dir{grid-template-columns:1fr}.hp-search input{font-size:16px}}
'''


def main():
    base = open('NotFound.dc.html', encoding='utf-8').read()
    head, rest = base.split('<main', 1)
    foot = rest[rest.index('</main>') + len('</main>'):]
    foot = foot[:foot.index('<script type="text/x-dc"')]
    tail = base[base.index('<script src="dc-lite.js">'):]
    title = 'Центр помощи — УрФУ'
    desc = 'Ответы на частые вопросы студентов и абитуриентов УрФУ, справочник служб и горячие линии — с поиском.'
    head = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + desc + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + title + '"', head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + desc + '"', head)
    head = head.replace('NotFound.dc.html"', 'Help.dc.html"')
    logic = (LOGIC.replace('__FAQ__', json.dumps(FAQ, ensure_ascii=False))
             .replace('__DIR__', json.dumps(DIR, ensure_ascii=False))
             .replace('__TOP__', json.dumps(TOPICS, ensure_ascii=False))
             .replace('__SRC__', json.dumps(SRC, ensure_ascii=False)))
    out = head + main_html() + foot + logic + '\n' + tail
    open('Help.dc.html', 'w', encoding='utf-8', newline='').write(out)
    css = open('site.css', encoding='utf-8').read()
    if '/* Центр помощи */' not in css:
        open('site.css', 'a', encoding='utf-8', newline='').write(CSS)
    print('Help.dc.html: вопросов', len(FAQ), 'служб', len(DIR))


if __name__ == '__main__':
    main()
