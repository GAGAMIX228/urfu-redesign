"""Собирает главные страницы в стиле «Уральский камень»: Main.dc.html (RU) и MainEn.dc.html (EN).
Шапка, подвал и логика (поиск, наборы ссылок для ролей) берутся из самих страниц, меняется только содержимое <main>.
Запуск: python make_home.py — можно запускать повторно."""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

T = {
 'ru': dict(
  file='Main.dc.html',
  h1='Что вам нужно в УрФУ?',
  lead='Программы, расписание, общежития, люди и события — найдём за пару секунд.',
  search_l='Поиск по сайту', ph='Например: общежитие или ИИ…', find='Найти', sug_l='Подсказки',
  none='Ничего не нашлось. Попробуйте <a href="Quiz.dc.html">подбор программы</a>, <a href="Schedule.dc.html">расписание</a> или <a href="Dorms.dc.html">общежития</a>.',
  all_res='Все результаты поиска',
  often='Часто ищут: <a href="Schedule.dc.html">расписание</a><a href="Catalog.dc.html">проходные баллы</a><a href="Dorms.dc.html">общежития</a><a href="Contacts.dc.html">карту кампуса</a>',
  photo='Главный учебный корпус', adm_h='Поступление',
  note='Считаем до 20 июня — так по правилам приёма 2026 года. Даты на 2027 год объявят весной.',
  steps=[('20 июня', 'Приём документов открыт'), ('25 июля', 'Последний день для бюджета по ЕГЭ'), ('20 августа', 'Последний день для платного'), ('1 сентября', 'Первая пара')],
  cta1=('Quiz.dc.html', 'Подобрать программу за 3 вопроса'), cta2=('Admission.dc.html', 'Как поступить'),
  news_h='Новости', news_all='Все новости', ev_h='События', ev_all='Календарь',
  news=[('Июль 2026', 'Почти 50 тысяч заявлений на бюджет: итоги приёма-2026'), ('2026', 'УрФУ вошёл в пилотный проект новой системы высшего образования'),
        ('2026', 'Около 500 преподавателей освоили нейросети для создания учебных курсов'), ('2026', 'Учёные УрФУ и УрО РАН объяснили одну из загадочных причин мужского бесплодия')],
  ev=[('13–22', 'октября', 'Статистический диктант', 'Онлайн, можно успеть'), ('24', 'октября', 'Школа экскурсоводов', 'Набор на программу допобразования'),
      ('29', 'октября', 'Кейс-чемпионат «Лига твоего имени»', 'Приём заявок'), ('3–12', 'ноября', 'Большой этнографический диктант', 'Онлайн на сайте акции')],
  inst_h='Институты', inst_lead='Восемь институтов — от радиотехники до гуманитарных наук.', inst_all='Все подразделения',
  inst=[('ИРИТ-РтФ', 'Радиоэлектроника и IT'), ('ИЕНиМ', 'Естественные науки и математика'), ('ИНМиТ', 'Новые материалы и технологии'), ('УралЭНИН', 'Энергетика'),
        ('ИСА', 'Строительство и архитектура'), ('УГИ', 'Гуманитарные науки'), ('ИнЭУ', 'Экономика и управление'), ('ФТИ', 'Физика и технологии')],
  life_h='Жизнь в УрФУ', life_all='Клубы, спорт и события',
  life=[('kampus-leto', 'Кампус', 'Втузгородок и улица Мира'), ('bassejn', 'Спорт', 'Бассейн, залы, секции'), ('tochka-kipeniya', 'Студклубы', 'Наука, IT, творчество'), ('volontery-2026', 'Волонтёрство', 'Проекты и события')],
  me="{abit:'Я поступаю', student:'Я учусь', staff:'Я работаю в УрФУ', intl:'International students'}",
  more="ex ? (k === 'intl' ? 'Show less' : 'Свернуть') : (k === 'intl' ? 'Show 3 more' : 'Ещё ' + (all.length - 3))",
  glang="k === 'intl' ? 'en' : 'ru'",
  days_word="(days % 10 === 1 && days % 100 !== 11) ? 'День остался' : (days % 10 >= 2 && days % 10 <= 4 && (days % 100 < 12 || days % 100 > 14)) ? 'Дня осталось' : 'Дней осталось'",
  days_tail=' до начала приёма документов',
 ),
 'en': dict(
  file='MainEn.dc.html',
  h1='What do you need at UrFU?',
  lead='Programmes, timetable, housing, people and events — found in seconds.',
  search_l='Search the site', ph='For example: housing or AI…', find='Search', sug_l='Suggestions',
  none='Nothing found. Try the <a href="CatalogEn.dc.html">programme catalogue</a>, <a href="Schedule.dc.html">timetable</a> or <a href="Dorms.dc.html">housing</a>.',
  all_res='All search results',
  often='Popular: <a href="Schedule.dc.html">timetable</a><a href="CatalogEn.dc.html">pass marks</a><a href="Dorms.dc.html">housing</a><a href="Contacts.dc.html">campus map</a>',
  photo='Main academic building', adm_h='Admissions',
  note='Counting to 20 June, as in the 2026 admission rules. Dates for 2027 will be announced in spring.',
  steps=[('20 June', 'Applications open'), ('25 July', 'Last day for state-funded places by EGE'), ('20 August', 'Last day for paid places'), ('1 September', 'First class')],
  cta1=('CatalogEn.dc.html', 'Find a programme'), cta2=('AdmissionEn.dc.html', 'How to apply'),
  news_h='News', news_all='All news', ev_h='Events', ev_all='Calendar',
  news=[('July 2026', 'Almost 50,000 applications for state-funded places in 2026'), ('2026', 'UrFU joins the pilot of the new higher education system'),
        ('2026', 'About 500 teachers learned to build courses with neural networks'), ('2026', 'UrFU scientists explain a puzzling cause of male infertility')],
  ev=[('13–22', 'October', 'Statistics Dictation', 'Open to everyone online'), ('24', 'October', 'Tour Guide School', 'Enrolment for a continuing-education course'),
      ('29', 'October', '“League of Your Name” case championship', 'Applications open'), ('3–12', 'November', 'Big Ethnographic Dictation', 'Online on the campaign website')],
  inst_h='Institutes', inst_lead='Eight institutes, from radio engineering to the humanities.', inst_all='All units',
  inst=[('IRIT-RTF', 'Radio electronics and IT'), ('INSM', 'Natural sciences and mathematics'), ('INMT', 'New materials and technologies'), ('UralENIN', 'Power engineering'),
        ('ICEA', 'Civil engineering and architecture'), ('UIH', 'Humanities'), ('GSEM', 'Economics and management'), ('IPT', 'Physics and technology')],
  life_h='Campus life', life_all='Clubs, sports and events',
  life=[('kampus-leto', 'Campus', 'Vtuzgorodok and Mira Street'), ('bassejn', 'Sports', 'Pool, gyms, sections'), ('tochka-kipeniya', 'Student clubs', 'Science, IT, creativity'), ('volontery-2026', 'Volunteering', 'Projects and events')],
  me="{abit:'I’m applying', student:'I’m a student', staff:'I work at UrFU', intl:'International students'}",
  more="ex ? 'Show less' : 'Show 3 more'",
  glang="'en'",
  days_word="days === 1 ? 'Day left' : 'Days left'",
  days_tail=' until applications open',
 ),
}


def main_html(t):
    steps = ''.join(f'<li><b>{d}</b><span>{w}</span></li>' for d, w in t['steps'])
    news = ''.join(f'<li><a href="Article.dc.html"><small>{d}</small><span class="fd-t">{x}</span></a></li>' for d, x in t['news'])
    ev = ''.join(f'<li><a href="Events.dc.html"><b>{d}<small>{m}</small></b><div><div class="fd-ev-t">{x}</div><div class="fd-ev-d">{n}</div></div></a></li>' for d, m, x, n in t['ev'])
    RU = ['ИРИТ-РтФ', 'ИЕНиМ', 'ИНМиТ', 'УралЭНИН', 'ИСА', 'УГИ', 'ИнЭУ', 'ФТИ']
    inst = ''.join(f'<a href="Institute.dc.html?i={RU[k]}"><b>{a}</b><span>{n}</span></a>' for k, (a, n) in enumerate(t['inst']))
    life = ''.join(f'<a href="Life.dc.html"><div class="ph" style="background-image:url(\'photos/{p}.webp\')"></div><b>{x}</b><span>{n}</span></a>' for p, x, n in t['life'])
    return f"""<main id="main" tabindex="-1" style="outline:none">
<section class="fd-hero"><div class="wrap fd-hero-in">
<div>
<h1>{t['h1']}</h1>
<p class="fd-lead">{t['lead']}</p>
<div class="search fd-search">
<div class="search-box">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>
<label for="q" class="sr">{t['search_l']}</label>
<input type="search" id="q" name="q" autocomplete="off" placeholder="{t['ph']}" value="{{{{q}}}}" onChange="{{{{onQ}}}}">
<a class="btn" href="{{{{qHref}}}}">{t['find']}</a>
</div>
<sc-if value="{{{{open}}}}">
<div class="sug" role="listbox" aria-label="{t['sug_l']}">
<sc-for list="{{{{sug}}}}" as="g">
<a href="{{{{g.href}}}}" role="option"><span style="font-weight:500">{{{{g.t}}}}</span><span class="muted" style="font-size:13px;white-space:nowrap">{{{{g.kind}}}}</span></a>
</sc-for>
<sc-if value="{{{{none}}}}"><div class="muted" style="padding:14px 18px">{t['none']}</div></sc-if>
<a href="{{{{qHref}}}}" style="background:var(--bg-soft-2);font-weight:600;color:var(--blue)">{t['all_res']}</a>
</div>
</sc-if>
</div>
<p class="fd-often">{t['often']}</p>
</div>
<div class="fd-gems">
<sc-for list="{{{{gems}}}}" as="g" hint-placeholder-count="4">
<section class="fd-gem" data-role="{{{{g.key}}}}" lang="{{{{g.lang}}}}" aria-labelledby="{{{{g.hid}}}}">
<h2 id="{{{{g.hid}}}}">{{{{g.me}}}}</h2>
<ul><sc-for list="{{{{g.links}}}}" as="l" hint-placeholder-count="3"><li><a href="{{{{l.href}}}}">{{{{l.t}}}}<span>{{{{l.d}}}}</span></a></li></sc-for></ul>
<button type="button" class="fd-toggle" id="{{{{g.bid}}}}" aria-expanded="{{{{g.exp}}}}" onClick="{{{{g.toggle}}}}">{{{{g.more}}}}</button>
</section>
</sc-for>
</div>
</div></section>

<figure class="fd-photo"><figcaption class="fd-photo-cap">{t['photo']}</figcaption></figure>

<section class="fd-sec soft" aria-labelledby="adm-h"><div class="wrap fd-adm">
<div>
<h2 id="adm-h" class="sr">{t['adm_h']}</h2>
<div class="fd-days">{{{{days}}}}</div>
<p class="fd-days-l">{{{{daysWord}}}}{t['days_tail']}</p>
<p class="fd-note">{t['note']}</p>
</div>
<div>
<ol class="fd-steps">{steps}</ol>
<div class="fd-adm-cta"><a class="btn" href="{t['cta1'][0]}">{t['cta1'][1]}</a><a class="btn2" href="{t['cta2'][0]}" style="background:#FFFFFF">{t['cta2'][1]}</a></div>
</div>
</div></section>

<section class="fd-sec"><div class="wrap fd-two">
<div>
<div class="fd-head"><h2 class="fd-col-h">{t['news_h']}</h2><a class="fd-more" href="News.dc.html">{t['news_all']}</a></div>
<ul class="fd-list fd-news">{news}</ul>
</div>
<div>
<div class="fd-head"><h2 class="fd-col-h">{t['ev_h']}</h2><a class="fd-more" href="Events.dc.html">{t['ev_all']}</a></div>
<ul class="fd-list fd-ev">{ev}</ul>
</div>
</div></section>

<section class="fd-sec soft"><div class="wrap">
<div class="fd-head"><div><h2 class="fd-h2">{t['inst_h']}</h2><p class="fd-lead">{t['inst_lead']}</p></div><a class="fd-more" href="Institute.dc.html">{t['inst_all']}</a></div>
<div class="fd-inst">{inst}</div>
</div></section>

<section class="fd-sec"><div class="wrap">
<div class="fd-head"><h2 class="fd-h2">{t['life_h']}</h2><a class="fd-more" href="Life.dc.html">{t['life_all']}</a></div>
<div class="fd-life">{life}</div>
</div></section>
</main>"""


def build(t):
    s = open(t['file'], encoding='utf-8').read()
    head, foot = s[:s.index('<main')], s[s.index('</main>') + len('</main>'):]
    if 'home.css' not in head:
        head = head.replace('<link rel="stylesheet" href="logo-live.css">', '<link rel="stylesheet" href="logo-live.css">\n<link rel="stylesheet" href="home.css">', 1)
    head = head.replace('<link rel="stylesheet" href="slides.css">\n', '')
    if 'PTSansNarrow-Bold-cyr.woff2" as="font"' not in head:
        head = head.replace('<link rel="stylesheet" href="site.css">', '<link rel="preload" href="fonts/PTSansNarrow-Bold-cyr.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="site.css">', 1)
    head = head.replace('<link rel="preload" href="photos/glavnyj-korpus-leto.webp" as="image">\n', '')
    head = head.replace('<template id="dc-tpl">\n<div>', '<template id="dc-tpl">\n<div class="fd">', 1)
    assert 'class="fd"' in head and 'home.css' in head
    foot = foot.replace('<script src="slides.js"></script>\n', '')
    if 'const gems =' not in foot:
        ret = "const qHref = 'Search.dc.html'"
        assert ret in foot
        gems = f"""const ME = {t['me']};
const openG = (this.state && this.state.openG) || {{}};
const gems = list.map(([k]) => {{
  const all = sets[k], ex = !!openG[k];
  return {{ key: k, me: ME[k], lang: {t['glang']}, hid: 'gem-' + k, bid: 'gem-b-' + k,
    links: ex ? all : all.slice(0, 3), exp: String(ex), more: {t['more']},
    toggle: () => this.setState({{ openG: {{ ...openG, [k]: !ex }} }}) }};
}});
const NOW = new Date(); const Y0 = NOW.getFullYear();
let target = new Date(Y0, 5, 20); if (NOW > new Date(Y0, 7, 20)) target = new Date(Y0 + 1, 5, 20);
const days = Math.max(0, Math.ceil((target - new Date(Y0, NOW.getMonth(), NOW.getDate())) / 864e5));
const daysWord = {t['days_word']};
"""
        foot = foot.replace(ret, gems + ret, 1)
        foot = foot.replace('return { qHref,', 'return { qHref, gems, days, daysWord,', 1)
    open(t['file'], 'w', encoding='utf-8', newline='\n').write(head + main_html(t) + foot)
    print('ok', t['file'])


for t in T.values():
    build(t)
