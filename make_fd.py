"""Эксперимент «Уральский камень»: собирает Main.fd.dc.html из шапки, подвала и логики Main.dc.html."""
import os
import re

os.chdir(r'C:\Users\Admin\urfu-redesign')
s = open('Main.dc.html', encoding='utf-8').read()
head = s[:s.index('<main')]
foot = s[s.index('</main>'):]

head = re.sub(r'<title>[^<]*</title>', '<title>[Эксперимент: Уральский камень] УрФУ — Уральский федеральный университет</title>', head)
head = head.replace('<link rel="stylesheet" href="slides.css">\n', '')
head = head.replace('<link rel="preload" href="fonts/IBMPlexSans-SemiBold.woff2" as="font" type="font/woff2" crossorigin>',
                    '<link rel="preload" href="fonts/IBMPlexSans-SemiBold.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="fonts/PTSansNarrow-Bold-cyr.woff2" as="font" type="font/woff2" crossorigin>')
head = head.replace('<link rel="stylesheet" href="logo-live.css">', '<link rel="stylesheet" href="logo-live.css">\n<link rel="stylesheet" href="fd.css">')
head = head.replace('<template id="dc-tpl">\n<div>', '<template id="dc-tpl">\n<div class="fd">', 1)
assert 'class="fd"' in head
foot = foot.replace('<script src="slides.js"></script>\n', '')

MAIN = """<main id="main" tabindex="-1" style="outline:none">
<section class="fd-hero"><div class="wrap fd-hero-in">
<div>
<h1>Что вам нужно в УрФУ?</h1>
<p class="fd-lead">Программы, расписание, общежития, люди и события — найдём за пару секунд.</p>
<div class="search fd-search">
<div class="search-box">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>
<label for="q" class="sr">Поиск по сайту</label>
<input id="q" autocomplete="off" placeholder="Например: общежитие или ИИ" value="{{q}}" onChange="{{onQ}}">
<a class="btn" href="{{qHref}}">Найти</a>
</div>
<sc-if value="{{open}}">
<div class="sug" role="listbox" aria-label="Подсказки">
<sc-for list="{{sug}}" as="g">
<a href="{{g.href}}" role="option"><span style="font-weight:500">{{g.t}}</span><span class="muted" style="font-size:13px;white-space:nowrap">{{g.kind}}</span></a>
</sc-for>
<sc-if value="{{none}}"><div class="muted" style="padding:14px 18px">Ничего не нашлось. Попробуйте <a href="Quiz.dc.html">подбор программы</a>, <a href="Schedule.dc.html">расписание</a> или <a href="Dorms.dc.html">общежития</a>.</div></sc-if>
<a href="{{qHref}}" style="background:var(--bg-soft-2);font-weight:600;color:var(--blue)">Все результаты поиска</a>
</div>
</sc-if>
</div>
<p class="fd-often">Часто ищут: <a href="Schedule.dc.html">расписание</a><a href="Catalog.dc.html">проходные баллы</a><a href="Dorms.dc.html">общежития</a><a href="Contacts.dc.html">карту кампуса</a></p>
</div>
<div class="fd-gems">
<sc-for list="{{gems}}" as="g" hint-placeholder-count="4">
<section class="fd-gem" data-role="{{g.key}}" lang="{{g.lang}}" aria-labelledby="{{g.hid}}">
<h2 id="{{g.hid}}">{{g.me}}</h2>
<ul><sc-for list="{{g.links}}" as="l" hint-placeholder-count="3"><li><a href="{{l.href}}">{{l.t}}<span>{{l.d}}</span></a></li></sc-for></ul>
<button type="button" class="fd-toggle" id="{{g.bid}}" aria-expanded="{{g.exp}}" onClick="{{g.toggle}}">{{g.more}}</button>
</section>
</sc-for>
</div>
</div></section>

<div class="fd-photo" role="img" aria-label="Главный учебный корпус УрФУ на улице Мира, 19"></div>

<section class="fd-sec soft" aria-labelledby="adm-h"><div class="wrap fd-adm">
<div>
<h2 id="adm-h" class="sr">Поступление</h2>
<div class="fd-days">{{days}}</div>
<p class="fd-days-l">{{daysWord}} до начала приёма документов</p>
<p class="fd-note">Считаем до 20 июня — так по правилам приёма 2026 года. Даты на 2027 год объявят весной.</p>
</div>
<div>
<ol class="fd-steps">
<li><b>20 июня</b><span>Приём документов открыт</span></li>
<li><b>25 июля</b><span>Последний день для бюджета по ЕГЭ</span></li>
<li><b>20 августа</b><span>Последний день для платного</span></li>
<li><b>1 сентября</b><span>Первая пара</span></li>
</ol>
<div class="fd-adm-cta"><a class="btn" href="Quiz.dc.html">Подобрать программу за 3 вопроса</a><a class="btn2" href="Admission.dc.html" style="background:#FFFFFF">Как поступить</a></div>
</div>
</div></section>

<section class="fd-sec"><div class="wrap fd-two">
<div>
<div class="fd-head"><h2 class="fd-col-h">Новости</h2><a class="fd-more" href="News.dc.html">Все новости</a></div>
<ul class="fd-list fd-news">
<li><a href="Article.dc.html"><small>Июль 2026</small><span class="fd-t">Почти 50 тысяч заявлений на бюджет: итоги приёма-2026</span></a></li>
<li><a href="Article.dc.html"><small>2026</small><span class="fd-t">УрФУ вошёл в пилотный проект новой системы высшего образования</span></a></li>
<li><a href="Article.dc.html"><small>2026</small><span class="fd-t">Около 500 преподавателей освоили нейросети для создания учебных курсов</span></a></li>
<li><a href="Article.dc.html"><small>2026</small><span class="fd-t">Учёные УрФУ и УрО РАН объяснили одну из загадочных причин мужского бесплодия</span></a></li>
</ul>
</div>
<div>
<div class="fd-head"><h2 class="fd-col-h">События</h2><a class="fd-more" href="Events.dc.html">Календарь</a></div>
<ul class="fd-list fd-ev">
<li><a href="Events.dc.html"><b>13–22<small>октября</small></b><div><div class="fd-ev-t">Статистический диктант</div><div class="fd-ev-d">Онлайн, можно успеть</div></div></a></li>
<li><a href="Events.dc.html"><b>24<small>октября</small></b><div><div class="fd-ev-t">Школа экскурсоводов</div><div class="fd-ev-d">Набор на программу допобразования</div></div></a></li>
<li><a href="Events.dc.html"><b>29<small>октября</small></b><div><div class="fd-ev-t">Кейс-чемпионат «Лига твоего имени»</div><div class="fd-ev-d">Приём заявок</div></div></a></li>
<li><a href="Events.dc.html"><b>3–12<small>ноября</small></b><div><div class="fd-ev-t">Большой этнографический диктант</div><div class="fd-ev-d">Онлайн на сайте акции</div></div></a></li>
</ul>
</div>
</div></section>

<section class="fd-sec soft"><div class="wrap">
<div class="fd-head"><div><h2 class="fd-h2">Институты</h2><p class="fd-lead">Восемь институтов — от радиотехники до гуманитарных наук.</p></div><a class="fd-more" href="Institute.dc.html">Все подразделения</a></div>
<div class="fd-inst">
<a href="Institute.dc.html"><b>ИРИТ-РтФ</b><span>Радиоэлектроника и IT</span></a>
<a href="Institute.dc.html"><b>ИЕНиМ</b><span>Естественные науки и математика</span></a>
<a href="Institute.dc.html"><b>ИНМиТ</b><span>Новые материалы и технологии</span></a>
<a href="Institute.dc.html"><b>УралЭНИН</b><span>Энергетика</span></a>
<a href="Institute.dc.html"><b>ИСА</b><span>Строительство и архитектура</span></a>
<a href="Institute.dc.html"><b>УГИ</b><span>Гуманитарные науки</span></a>
<a href="Institute.dc.html"><b>ИнЭУ</b><span>Экономика и управление</span></a>
<a href="Institute.dc.html"><b>ФТИ</b><span>Физика и технологии</span></a>
</div>
</div></section>

<section class="fd-sec"><div class="wrap">
<div class="fd-head"><h2 class="fd-h2">Жизнь в УрФУ</h2><a class="fd-more" href="Life.dc.html">Клубы, спорт и события</a></div>
<div class="fd-life">
<a href="Life.dc.html"><div class="ph" style="background-image:url('photos/kampus-leto.webp')"></div><b>Кампус</b><span>Втузгородок и улица Мира</span></a>
<a href="Life.dc.html"><div class="ph" style="background-image:url('photos/bassejn.webp')"></div><b>Спорт</b><span>Бассейн, залы, секции</span></a>
<a href="Life.dc.html"><div class="ph" style="background-image:url('photos/tochka-kipeniya.webp')"></div><b>Студклубы</b><span>Наука, IT, творчество</span></a>
<a href="Life.dc.html"><div class="ph" style="background-image:url('photos/volontery-2026.webp')"></div><b>Волонтёрство</b><span>Проекты и события</span></a>
</div>
</div></section>
</main>"""

# логика: берём из главной поиск и наборы ссылок, добавляем «самоцветы» и отсчёт
logic_start = foot.index('<script type="text/x-dc" id="dc-logic">')
logic = foot[logic_start:]
ret = "const qHref = 'Search.dc.html'"
assert ret in logic
GEMS = """const ME = {abit:'Я поступаю', student:'Я учусь', staff:'Я работаю в УрФУ', intl:'International students'};
const openG = (this.state && this.state.openG) || {};
const gems = list.map(([k]) => {
  const all = sets[k], ex = !!openG[k];
  return { key: k, me: ME[k], lang: k === 'intl' ? 'en' : 'ru', hid: 'gem-' + k, bid: 'gem-b-' + k,
    links: ex ? all : all.slice(0, 3), exp: String(ex),
    more: ex ? (k === 'intl' ? 'Show less' : 'Свернуть') : (k === 'intl' ? 'Show 3 more' : 'Ещё ' + (all.length - 3)),
    toggle: () => this.setState({ openG: { ...openG, [k]: !ex } }) };
});
const NOW = new Date(); const Y0 = NOW.getFullYear();
let target = new Date(Y0, 5, 20); if (NOW > new Date(Y0, 7, 20)) target = new Date(Y0 + 1, 5, 20);
const days = Math.max(0, Math.ceil((target - new Date(Y0, NOW.getMonth(), NOW.getDate())) / 864e5));
const dw = (days % 10 === 1 && days % 100 !== 11) ? 'день остался' : (days % 10 >= 2 && days % 10 <= 4 && (days % 100 < 12 || days % 100 > 14)) ? 'дня осталось' : 'дней осталось';
"""
logic = logic.replace(ret, GEMS + ret, 1)
logic = logic.replace("return { qHref,", "return { qHref, gems, days, daysWord: dw.charAt(0).toUpperCase() + dw.slice(1),", 1)
foot = foot[:logic_start] + logic

open('Main.fd.dc.html', 'w', encoding='utf-8', newline='\n').write(head + MAIN + foot)
print('ok')
