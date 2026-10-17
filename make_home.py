"""Собирает главные страницы в стиле «Уральский камень»: Main.dc.html (RU) и MainEn.dc.html (EN).
Шапка, подвал и логика (поиск, наборы ссылок для ролей) берутся из самих страниц, меняется только содержимое <main>.
Запуск: python make_home.py — можно запускать повторно."""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

T = {
 'ru': dict(
  file='Main.dc.html',
  tag='дней до начала приёма документов',
  tick=['УрФУ — с 1920 года', '8 институтов', '18 общежитий в двух кампусах', 'Екатеринбург, ул. Мира, 19', 'Приём документов — с 20 июня', 'Версия для слабовидящих на каждой странице'],
  col=[('kampus-leto', 'Главный учебный корпус'), ('studenty', 'Студенты УрФУ'), ('it-konferenciya-2026-slushateli', 'IT-конференция, 2026')],
  badge1=('1920', 'год основания'), badge2=('8', 'институтов'),
  roles_h='С чего начнём?', roles_lead='Выберите, кто вы, — покажем главное именно для вас.',
  calc_h='Хватит ли баллов?', calc_lead='Сдвиньте ползунок на свою сумму трёх ЕГЭ — покажем, на сколько программ вы прошли бы по проходным баллам прошлого года.',
  calc_sum='Моя сумма баллов', calc_area='Область', calc_go='Показать в каталоге', calc_src='Проходные баллы 2024–2025 годов из каталога. Программы без опубликованного балла не учитываются.',
  areas=[('all', 'Все'), ('it', 'IT'), ('eng', 'Инженерия'), ('nat', 'Естественные'), ('hum', 'Гуманитарные'), ('eco', 'Экономика')],
  cat='Catalog.dc.html',
  ask_h='Не нашли ответ?', ask_lead='Спросите нас — ответим по телефону или почте.',
  ask=[('8-800-100-50-44', 'tel:88001005044', 'Контакт-центр, звонок по России бесплатный'), ('+7 (343) 375-44-74', 'tel:+73433754474', 'Приёмная комиссия'), ('contact@urfu.ru', 'mailto:contact@urfu.ru', 'Почта университета')],
  ask_all=('Help.dc.html', 'Центр помощи: ответы и службы'),
  who=[('abit', 'поступаю'), ('student', 'учусь'), ('staff', 'работаю'), ('intl', 'International')],
  who_h={'abit': ('Поступление в УрФУ — на одном экране', 'Проходные баллы прошлых лет, сроки, стоимость и общежития. Без лишних вкладок.'),
         'student': ('Что у вас сегодня?', 'Пары вашей группы, общежитие, помощь и события — главное для студента.'),
         'staff': ('УрФУ для сотрудников', 'Наука, справочник служб, новости и мероприятия университета.'),
         'intl': ('Study at UrFU', 'Programmes in English, how to apply and where to live.')},
  panel={'abit': ('Главное для поступающих', [('Каталог программ', 'Фильтр по ЕГЭ и баллам', 'Catalog.dc.html'), ('Календарь приёма', 'Сроки подачи и согласия', 'Admission.dc.html#calendar'), ('Подбор за 3 вопроса', 'Куда вы проходите', 'Quiz.dc.html'), ('Стоимость обучения', 'Калькулятор по программам', 'Admission.dc.html#cost'), ('Общежития и цены', 'Таблица по приказам УрФУ', 'Dorms.dc.html#price-h'), ('Центр помощи', 'Ответы на частые вопросы', 'Help.dc.html')]),
         'student': ('Главное для студента', [('Расписание', 'Ваша группа, недели, календарь', 'Schedule.dc.html'), ('Центр помощи', 'Справки, медосмотр, Wi-Fi', 'Help.dc.html'), ('Общежитие', 'Цены и заселение', 'Dorms.dc.html'), ('Молодёжные лаборатории', 'Как попасть в науку', 'Science.dc.html#stud-h'), ('Клубы и спорт', 'Секции и студклубы', 'Life.dc.html'), ('Карта кампуса', 'Корпуса и медсанчасть', 'Contacts.dc.html')]),
         'staff': ('Главное для сотрудников', [('Наука', 'Проекты «Приоритет-2030»', 'Science.dc.html'), ('Справочник служб', 'Телефоны и почта', 'Help.dc.html#dir-h'), ('Новости', 'Что происходит в УрФУ', 'News.dc.html'), ('Мероприятия', 'Календарь университета', 'Events.dc.html'), ('Институты', 'Структура и подразделения', 'Institute.dc.html'), ('Личный кабинет', 'Сервисы сотрудника', 'Login.dc.html?role=staff')]),
         'intl': ('For international students', [('Programme catalogue', 'In English: exams and pass marks', 'CatalogEn.dc.html'), ('How to apply', 'Steps, documents, deadlines', 'AdmissionEn.dc.html'), ('Housing', 'Dormitories and prices', 'Dorms.dc.html'), ('Campus map', 'Buildings and contacts', 'Contacts.dc.html'), ('English home page', 'The whole site in brief', 'MainEn.dc.html'), ('Help centre', 'Contacts of university services', 'Help.dc.html')])},
  h1='Что вам нужно в УрФУ?',
  lead='Программы, расписание, общежития и события — найдём за пару секунд.',
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
  tag='days until applications open',
  tick=['UrFU — since 1920', '8 institutes', '18 dormitories on two campuses', 'Yekaterinburg, 19 Mira St.', 'Applications open on 20 June', 'Accessibility mode on every page'],
  col=[('kampus-leto', 'Main academic building'), ('studenty', 'UrFU students'), ('it-konferenciya-2026-slushateli', 'IT conference, 2026')],
  badge1=('1920', 'founded'), badge2=('8', 'institutes'),
  roles_h='Where shall we start?', roles_lead='Choose who you are — we will show what matters to you.',
  calc_h='Is my score enough?', calc_lead='Move the slider to your total for three EGE exams — we will show how many programmes you would have passed with last year’s pass marks.',
  calc_sum='My total score', calc_area='Field', calc_go='Show in the catalogue', calc_src='Pass marks for 2024–2025 from the catalogue. Programmes without a published pass mark are not counted.',
  areas=[('all', 'All'), ('it', 'IT'), ('eng', 'Engineering'), ('nat', 'Sciences'), ('hum', 'Humanities'), ('eco', 'Economics')],
  cat='CatalogEn.dc.html',
  ask_h='Didn’t find an answer?', ask_lead='Ask us by phone or email.',
  ask=[('8-800-100-50-44', 'tel:88001005044', 'Contact centre, free within Russia'), ('+7 (343) 375-44-74', 'tel:+73433754474', 'Admissions Office'), ('contact@urfu.ru', 'mailto:contact@urfu.ru', 'University email')],
  ask_all=('Contacts.dc.html', 'All contacts and map'),
  h1='What do you need at UrFU?',
  lead='Programmes, timetable, housing and events — found in seconds.',
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


def progs_json():
    """Короткие данные программ для калькулятора — из каталога, чтобы цифры совпадали: [область, балл, бюджетные места]."""
    import json
    c = open('Catalog.dc.html', encoding='utf-8').read()
    c = c[c.index('const ALL_PROGS'):]
    c = c[:c.index('];')]
    out = []
    for line in c.split('\n'):
        k = re.search(r"k:'(\w+)'", line); sc = re.search(r"score:'(\d+)'", line); bu = re.search(r"budget:'(\d+)'", line)
        if line.startswith('{name') and k and sc:
            out.append([k.group(1), int(sc.group(1)), int(bu.group(1)) if bu else 0])
    return json.dumps(out, separators=(',', ':'))


def who_html(t):
    """Переключатель «Я —» и заголовки для каждой роли (показывает home-role.js)."""
    if not t.get('who'):
        return '', f"<h1>{t['h1']}</h1>\n<p class=\"fd-lead\">{t['lead']}</p>"
    btns = ''.join(f'<button type="button" class="yu-who-b" data-urole="{k}" aria-pressed="false"{" lang=\"en\"" if k == "intl" else ""}>{n}</button>' for k, n in t['who'])
    sw = f'<div class="yu-who" role="group" aria-label="Кто вы"><span>Я —</span>{btns}</div>'
    h = f'<h1><span class="r-any">{t["h1"]}</span>' + ''.join(f'<span class="r-{k}"{" lang=\"en\"" if k == "intl" else ""}>{a}</span>' for k, (a, b) in t['who_h'].items()) + '</h1>'
    lead = f'<p class="fd-lead"><span class="r-any">{t["lead"]}</span>' + ''.join(f'<span class="r-{k}"{" lang=\"en\"" if k == "intl" else ""}>{b}</span>' for k, (a, b) in t['who_h'].items()) + '</p>'
    return sw, h + '\n' + lead


def panels_html(t):
    """Панель «Главное для вас» под выбранную роль."""
    if not t.get('panel'):
        return ''
    out = []
    for k, (title, links) in t['panel'].items():
        en = ' lang="en"' if k == 'intl' else ''
        ls = ''.join(f'<li><a href="{h}"><b>{a}</b><span>{d}</span></a></li>' for a, d, h in links)
        if k == 'abit':
            live = '<div class="me-live"><b class="me-big" data-me="days">—</b><span data-me="daysw">дней до приёма документов</span><a class="btn yu-btn-gold" href="#calc-h">Хватит ли моих баллов?</a></div>'
        elif k == 'student':
            live = '<div class="me-live"><span class="me-k" data-me="dayk">Сегодня</span><b data-me="grp">Пример расписания</b><ul class="me-pairs" data-me="pairs"></ul><a class="btn yu-btn-gold" href="Schedule.dc.html" data-me="grpbtn">Укажите свою группу</a><span class="me-note">Пары — пример, как в разделе «Расписание».</span></div>'
        elif k == 'staff':
            live = '<div class="me-live"><b class="me-big">54</b><span>научных проекта «Приоритет-2030» — с поиском и фильтрами</span><a class="btn yu-btn-gold" href="Science.dc.html">Открыть «Науку»</a></div>'
        else:
            live = '<div class="me-live"><b class="me-big">32</b><span>bachelor programmes with entrance exams and pass marks in English</span><a class="btn yu-btn-gold" href="CatalogEn.dc.html">Open catalogue</a></div>'
        out.append(f'<div class="me-panel me-{k}"{en}><div class="me-top"><h3>{title}</h3><button type="button" class="me-reset" data-urole="">{"Change role" if k == "intl" else "Сменить роль"}</button></div><div class="me-grid"><ul class="me-links">{ls}</ul>{live}</div></div>')
    return '<div class="me-panels">' + ''.join(out) + '</div>'


def main_html(t):
    steps = ''.join(f'<li><b>{d}</b><span>{w}</span></li>' for d, w in t['steps'][:3])
    news = ''.join(f'<li><a href="{"Article.dc.html" if i == 0 else "News.dc.html"}"><small>{d}</small><span class="fd-t">{x}</span></a></li>' for i, (d, x) in enumerate(t['news']))
    ev = ''.join(f'<li><a href="Events.dc.html"><b>{d}<small>{m}</small></b><div><div class="fd-ev-t">{x}</div><div class="fd-ev-d">{n}</div></div></a></li>' for d, m, x, n in t['ev'])
    RU = ['ИРИТ-РтФ', 'ИЕНиМ', 'ИНМиТ', 'УралЭНИН', 'ИСА', 'УГИ', 'ИнЭУ', 'ФТИ']
    inst = ''.join(f'<a class="yu-i yu-i{k % 4}" href="Institute.dc.html?i={RU[k]}"><b>{a}</b><span>{n}</span></a>' for k, (a, n) in enumerate(t['inst']))
    life = ''.join(f'<a class="yu-l yu-l{k}" href="Life.dc.html"><div class="ph" style="background-image:url(\'photos/{p}.webp\')"></div><b>{x}</b><span>{n}</span></a>' for k, (p, x, n) in enumerate(t['life']))
    tick = ''.join(f'<li>{x}</li>' for x in t['tick'])
    col = ''.join(f'<div class="yu-ph yu-ph{k}" role="img" aria-label="{c}" style="background-image:url(\'photos/{p}.webp\')"></div>' for k, (p, c) in enumerate(t['col']))
    areas = ''.join(f'<button type="button" class="yu-chip" data-area="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in t['areas'])
    ask = ''.join(f'<a href="{h}"><b>{n}</b><span>{d}</span></a>' for n, h, d in t['ask'])
    who, heads = who_html(t)
    pick = '<button type="button" class="fd-pick" data-urole="{{g.key}}">{{g.pickT}}</button>' if t.get('who') else ''
    return f"""<main id="main" tabindex="-1" style="outline:none">
<section class="yu-hero"><div class="wrap yu-hero-in">
<div class="yu-hero-txt">
{who}<p class="yu-tag"><b>{{{{days}}}}</b> {t['tag']}</p>
{heads}
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
<div class="yu-collage">{col}
<div class="yu-badge yu-b1"><b data-count="{t['badge1'][0]}">{t['badge1'][0]}</b><span>{t['badge1'][1]}</span></div>
<div class="yu-badge yu-b2"><b data-count="{t['badge2'][0]}">{t['badge2'][0]}</b><span>{t['badge2'][1]}</span></div>
</div>
</div></section>

<div class="yu-tick"><ul>{tick}</ul><ul aria-hidden="true">{tick}</ul></div>

<section class="yu-roles" aria-labelledby="roles-h"><div class="wrap">
<div class="yu-head"><h2 id="roles-h">{t['roles_h']}</h2><p>{t['roles_lead']}</p></div>
<div class="fd-gems">
<sc-for list="{{{{gems}}}}" as="g" hint-placeholder-count="4">
<section class="fd-gem" data-role="{{{{g.key}}}}" lang="{{{{g.lang}}}}" aria-labelledby="{{{{g.hid}}}}">
<h3 id="{{{{g.hid}}}}">{{{{g.me}}}}</h3>
<ul><sc-for list="{{{{g.links}}}}" as="l" hint-placeholder-count="3"><li><a href="{{{{l.href}}}}">{{{{l.t}}}}<span>{{{{l.d}}}}</span></a></li></sc-for></ul>
<button type="button" class="fd-toggle" id="{{{{g.bid}}}}" aria-expanded="{{{{g.exp}}}}" onClick="{{{{g.toggle}}}}">{{{{g.more}}}}</button>{pick}
</section>
</sc-for>
</div>
{panels_html(t)}
</div></section>

<section class="yu-calc-sec" aria-labelledby="calc-h"><div class="wrap yu-calc-in">
<div class="yu-calc-txt">
<h2 id="calc-h">{t['calc_h']}</h2>
<p>{t['calc_lead']}</p>
<ol class="yu-dates">{steps}</ol>
<p class="yu-note">{t['note']}</p>
<div class="fd-adm-cta"><a class="btn yu-btn-gold" href="{t['cta1'][0]}">{t['cta1'][1]}</a><a class="btn2 yu-btn-line" href="{t['cta2'][0]}">{t['cta2'][1]}</a></div>
</div>
<div class="yu-calc" data-progs='{progs_json()}' data-cat="{t['cat']}">
<label for="calc-r" class="yu-calc-l">{t['calc_sum']}</label>
<output class="yu-calc-v" for="calc-r" id="calc-v">240</output>
<input type="range" id="calc-r" min="150" max="310" step="1" value="240">
<div class="yu-calc-l" id="calc-al">{t['calc_area']}</div>
<div class="yu-chips" role="group" aria-labelledby="calc-al">{areas}</div>
<div class="yu-res" aria-live="polite"><b id="calc-n">—</b><span id="calc-d"></span></div>
<a class="btn yu-btn-pink" id="calc-go" href="{t['cat']}">{t['calc_go']}</a>
<p class="yu-src">{t['calc_src']}</p>
</div>
</div></section>

<section class="fd-sec yu-news-sec"><div class="wrap fd-two">
<div>
<div class="fd-head"><h2 class="fd-col-h">{t['news_h']}</h2><a class="fd-more" href="News.dc.html">{t['news_all']}</a></div>
<ul class="fd-list fd-news">{news}</ul>
</div>
<div class="yu-evbox">
<div class="fd-head"><h2 class="fd-col-h">{t['ev_h']}</h2><a class="fd-more" href="Events.dc.html">{t['ev_all']}</a></div>
<ul class="fd-list fd-ev">{ev}</ul>
</div>
</div></section>

<section class="fd-sec yu-inst-sec"><div class="wrap">
<div class="fd-head"><div><h2 class="fd-h2">{t['inst_h']}</h2><p class="fd-lead">{t['inst_lead']}</p></div><a class="fd-more" href="Institute.dc.html">{t['inst_all']}</a></div>
<div class="yu-inst">{inst}</div>
</div></section>

<section class="fd-sec yu-life-sec"><div class="wrap">
<div class="fd-head"><h2 class="fd-h2">{t['life_h']}</h2><a class="fd-more" href="Life.dc.html">{t['life_all']}</a></div>
<div class="yu-life">{life}</div>
</div></section>

<section class="yu-ask" aria-labelledby="ask-h"><div class="wrap yu-ask-in">
<div><h2 id="ask-h">{t['ask_h']}</h2><p>{t['ask_lead']}</p><a class="btn2 yu-btn-line" href="{t['ask_all'][0]}">{t['ask_all'][1]}</a></div>
<div class="yu-ask-list">{ask}</div>
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
    if t.get('who') and 'home-role.js' not in foot:
        foot = foot.replace('<script src="home-calc.js"></script>', '<script src="home-calc.js"></script>\n<script src="home-role.js"></script>', 1)
    if 'home-calc.js' not in foot:
        foot = foot.replace('<script src="site.js"></script>', '<script src="site.js"></script>\n<script src="home-calc.js"></script>', 1)
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
