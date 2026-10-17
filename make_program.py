"""Собирает Program.dc.html — одну страницу для всех программ каталога.
Какую программу показать, берётся из адреса: Program.dc.html?p=<название>. Без параметра — «Программная инженерия».
Список программ (институт, экзамены, баллы, места, цена) копируется из Catalog.dc.html, чтобы данные были одни и те же.
Запуск: python make_program.py — после правок каталога."""
import os, json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('Program.dc.html', encoding='utf-8').read()
cat = open('Catalog.dc.html', encoding='utf-8').read()
i = cat.index('const ALL_PROGS = [')
progs = cat[i:cat.index('];', i) + 2]

head = s[:s.index('<main')]
foot = s[s.index('</main>'):s.index('<script type="text/x-dc" id="dc-logic">')]
tail = s[s.index('<script src="dc-lite.js"></script>'):]

MAIN = """<main id="main" tabindex="-1" style="outline:none"><section class="phead">
<div class="wrap" style="padding-bottom:56px">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / <a href="Catalog.dc.html">Каталог программ</a> / {{name}}</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px"><span class="tag" style="background:#FFFFFF">Бакалавриат</span><sc-if value="{{hasCode}}" hint-placeholder-val="{{true}}"><span class="tag" style="background:#FFFFFF">{{code}}</span></sc-if><a class="tag" href="{{instHref}}" style="background:#FFFFFF;text-decoration:none" title="{{instFull}}">{{instL}}</a></div>
<h1 class="big" style="font-size:52px;margin-top:20px;max-width:900px">{{name}}</h1>
<p style="font-size:19px;margin-top:16px;max-width:760px;color:#2B3946">{{lead}}</p>
<div class="g4" style="margin-top:36px;background:#FFFFFF;border-radius:8px;padding:28px">
<sc-if value="{{hasScoreV}}" hint-placeholder-val="{{true}}"><div><div class="muted" style="font-size:14px">Проходной балл {{sy}}</div><div style="font-family:var(--narrow);font-weight:700;font-size:28px">{{score}}</div></div></sc-if>
<sc-if value="{{hasBudget}}" hint-placeholder-val="{{true}}"><div><div class="muted" style="font-size:14px">Бюджетных мест</div><div style="font-family:var(--narrow);font-weight:700;font-size:28px">{{budget}}</div></div></sc-if>
<sc-if value="{{hasPrice}}" hint-placeholder-val="{{true}}"><div><div class="muted" style="font-size:14px">Стоимость в год</div><div style="font-family:var(--narrow);font-weight:700;font-size:28px">{{price}}</div></div></sc-if>
<div><div class="muted" style="font-size:14px">Форма обучения</div><div style="font-family:var(--narrow);font-weight:700;font-size:28px">{{form}}</div></div>
</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px"><a class="btn" href="Admission.dc.html" style="min-height:52px;padding:0 28px">Подать документы</a><a class="btn2" href="{{cmpHref}}" style="min-height:52px">Сравнить с другими</a><button type="button" class="btn2 share-btn" style="min-height:52px" data-share="">Поделиться</button></div>
</div>
</section>
<div class="wrap">
<div class="row" style="margin-top:64px;align-items:flex-start">
<div class="main">
<h2>Вступительные испытания</h2>
<div class="g3" style="margin-top:20px">
<sc-for list="{{exams}}" as="e" hint-placeholder-count="3"><div class="card exm"><div class="muted" style="font-size:14px">{{e.kind}}</div><div style="font-weight:600;font-size:18px;margin-top:4px">{{e.t}}</div><sc-if value="{{e.hasMin}}" hint-placeholder-val="{{false}}"><div class="muted" style="font-size:14px;margin-top:8px">Минимум: {{e.min}}</div></sc-if></div></sc-for>
</div>

<sc-if value="{{known}}" hint-placeholder-val="{{true}}"><h2 style="margin-top:56px">Проходной балл на бюджет</h2>
<sc-if value="{{hasHist}}" hint-placeholder-val="{{true}}"><div class="card" style="margin-top:20px;display:flex;gap:40px;align-items:flex-end;flex-wrap:wrap">
<div style="display:flex;gap:28px;align-items:flex-end;height:180px" role="img" aria-label="{{histLabel}}">
<sc-for list="{{hist}}" as="h" hint-placeholder-count="3"><div style="display:flex;flex-direction:column;align-items:center;gap:6px" aria-hidden="true"><b class="num">{{h.v}}</b><div style="width:64px;height:{{h.px}}px;background:{{h.c}};border-radius:8px 8px 0 0"></div><span class="muted" style="font-size:14px">{{h.y}}</span></div></sc-for>
</div>
<div style="flex:1 1 260px"><p style="font-size:17px">Баллы меняются от года к году — ориентируйтесь на диапазон, а не на одно число.</p><p class="muted" style="font-size:14px;margin-top:8px">Плюс до 6 баллов за аттестат с отличием, 2 — за волонтёрство, 1 — за золотой значок ГТО.</p></div>
</div></sc-if>
<sc-if value="{{oneScore}}" hint-placeholder-val="{{false}}"><div class="card" style="margin-top:20px"><p style="font-size:17px">В {{sy}} году проходной балл на бюджет — <b>{{score}}</b>.</p><p class="muted" style="font-size:14px;margin-top:8px">Плюс до 10 баллов за достижения: аттестат с отличием, волонтёрство, значок ГТО.</p></div></sc-if></sc-if>

<sc-if value="{{hasSkills}}" hint-placeholder-val="{{true}}"><h2 style="margin-top:56px">Чему вы научитесь</h2>
<div class="g2" style="margin-top:20px"><sc-for list="{{skills}}" as="k" hint-placeholder-count="4"><div class="card"><div style="font-weight:600;font-size:18px">{{k.t}}</div><p class="muted" style="margin-top:8px">{{k.d}}</p></div></sc-for></div>
<sc-if value="{{noDeep}}" hint-placeholder-val="{{false}}"><h2 style="margin-top:56px">Кем работают выпускники</h2>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:20px"><sc-for list="{{jobs}}" as="j" hint-placeholder-count="6"><span class="chip">{{j}}</span></sc-for></div></sc-if></sc-if>

<sc-if value="{{deep}}" hint-placeholder-val="{{true}}">
<h2 style="margin-top:56px" id="study-h">Что будешь изучать</h2>
<p class="muted" style="margin-top:8px;max-width:720px">Модули учебного плана по темам. С 2 курса часть предметов выбираете сами — это индивидуальная траектория.</p>
<div class="pg-blks" style="margin-top:20px"><div class="pg-blk" style="--c:#E0337A"><div class="pg-blk-h"><b>Математика</b><span>6 модулей</span></div><ul><li>Элементарные основы математики и физики</li><li>Математические методы для разработчиков 1 и 2</li><li>Дискретная математика и математическая логика</li><li>Теория вероятностей и математическая статистика</li><li>Векторный анализ</li><li>Дополнительные главы математики</li></ul></div><div class="pg-blk" style="--c:#6B2BE0"><div class="pg-blk-h"><b>Программирование</b><span>6 модулей</span></div><ul><li>Программирование</li><li>Современные языки программирования</li><li>Технологии программирования</li><li>Прикладное программирование</li><li>Алгоритмы и анализ сложности</li><li>Web-технологии</li></ul></div><div class="pg-blk" style="--c:#0E8A6A"><div class="pg-blk-h"><b>Системы и данные</b><span>7 модулей</span></div><ul><li>Архитектура ЭВМ</li><li>Операционные системы</li><li>Компьютерные сети</li><li>Базы данных</li><li>Виртуализация и облачные технологии</li><li>Информационная безопасность</li><li>Анализ данных и искусственный интеллект</li></ul></div><div class="pg-blk" style="--c:#B86E00"><div class="pg-blk-h"><b>Инженерия и управление</b><span>7 модулей</span></div><ul><li>Теория и практика программной инженерии</li><li>Базовая архитектура ПО</li><li>Проектирование информационных систем</li><li>Системная аналитика</li><li>Управление проектами</li><li>Экономика инженерии</li><li>Правовые основы IT</li></ul></div><div class="pg-blk" style="--c:#1F5FD1"><div class="pg-blk-h"><b>Проекты и практика</b><span>4 модуля</span></div><ul><li>Основы проектной деятельности</li><li>Проектная деятельность</li><li>Учебная практика: ознакомительная и проектно-технологическая</li><li>Производственная практика: технологическая, проектная, преддипломная</li></ul></div><div class="pg-blk" style="--c:#C2185B"><div class="pg-blk-h"><b>По выбору</b><span>2 модуля</span></div><ul><li>Профессиональные спецкурсы 1–6</li><li>Майнор — курс другого направления</li></ul></div></div>
<p style="margin-top:14px;font-size:15px"><a href="https://programs.edu.urfu.ru/ru/9797/documents/" target="_blank" rel="noopener">Учебный план и рабочие программы модулей<span class="sr"> (откроется в новой вкладке)</span></a></p>

<h2 style="margin-top:56px">Проекты — с первого года</h2>
<p class="muted" style="margin-top:8px;max-width:720px">Проектная деятельность идёт каждый семестр. Задачи часто приносят компании-партнёры. Вот проекты студентов программы:</p>
<div class="g3 pg-projs" style="margin-top:20px"><div class="card pg-proj"><span class="tag">Заказ партнёра</span><div class="pg-proj-t">Meetups — платформа для мероприятий</div><div class="muted" style="font-size:14px;margin-top:auto">Заказчик: ГК «Иннотех»</div></div><div class="card pg-proj"><span class="tag">Заказ партнёра</span><div class="pg-proj-t">Сервис онлайн-опросов и голосований с аналитикой</div><div class="muted" style="font-size:14px;margin-top:auto">Заказчик: ГК «Иннотех»</div></div><div class="card pg-proj"><span class="tag">Заказ партнёра</span><div class="pg-proj-t">Мобильный путеводитель по городам России</div><div class="muted" style="font-size:14px;margin-top:auto">Заказчик: УБРиР</div></div><div class="card pg-proj"><span class="tag">Реализован</span><div class="pg-proj-t">Образовательная игра «Coding Learn» на Unity: учит программировать на C#</div></div><div class="card pg-proj"><span class="tag">Реализован</span><div class="pg-proj-t">Система бронирования мест в коворкинге</div><div class="muted" style="font-size:14px;margin-top:auto">Заказчик: ГК «Хост»</div></div></div>

<h2 style="margin-top:56px">Кем будешь работать</h2>
<ul class="pg-profs" style="margin-top:20px"><li><b>Программист — разработчик ПО</b><span>Пишет программы и приложения.</span></li><li><b>Web-разработчик</b><span>Сайты, веб-сервисы, мобильные и настольные приложения.</span></li><li><b>Разработчик мобильных приложений</b><span>Приложения для телефонов и планшетов.</span></li><li><b>Тестировщик</b><span>Проверяет, что программа работает правильно.</span></li><li><b>DevOps-инженер</b><span>Ускоряет выпуск обновлений: сборка, выкладка, мониторинг.</span></li><li><b>Архитектор ПО</b><span>Решает, из каких частей состоит система и как они связаны.</span></li><li><b>Разработчик компьютерных игр</b><span>От концепции и прототипа до готовой игры.</span></li><li><b>Менеджер IT-проектов</b><span>Сроки, качество и команда проекта.</span></li><li><b>Руководитель разработки ПО</b><span>Организует процесс разработки и ресурсы.</span></li></ul>

<h2 style="margin-top:56px">С кем работает программа</h2>
<p class="muted" style="margin-top:8px;max-width:720px">Партнёры помогают составлять программу, ведут проекты, берут на практику и на работу.</p>
<div class="pg-logos" style="margin-top:20px"><span class="pg-logo">Сбер</span><span class="pg-logo">СКБ Контур</span><span class="pg-logo">VK</span><span class="pg-logo">Naumen</span><span class="pg-logo">Альфа-Банк</span><span class="pg-logo">МТС Банк</span><span class="pg-logo">УЦСБ</span><span class="pg-logo">66 Бит</span><span class="pg-logo">Targem Games</span><span class="pg-logo">Artsofte</span><span class="pg-logo">НПО автоматики</span><span class="pg-logo">НПЦ «РИЦ»</span><span class="pg-logo">Акоммерс</span><span class="pg-logo">ФТ-Софт</span></div>

<h2 style="margin-top:56px">Кто будет учить</h2>
<div class="g2" style="margin-top:20px"><div class="card pg-t"><span class="pg-ava" aria-hidden="true">НМ</span><div><b>Новиков Максим Юрьевич</b><div class="muted" style="font-size:14px">канд. пед. наук, руководитель программы</div><p style="font-size:15px;margin-top:8px">Технологии программирования · Облачные вычисления · Fullstack на Next.js</p></div></div><div class="card pg-t"><span class="pg-ava" aria-hidden="true">ОИ</span><div><b>Обабков Илья Николаевич</b><div class="muted" style="font-size:14px">канд. техн. наук, ректор УрФУ</div><p style="font-size:15px;margin-top:8px">Инженерия программного обеспечения · Анализ и управление требованиями</p></div></div><div class="card pg-t"><span class="pg-ava" aria-hidden="true">БВ</span><div><b>Белоусова Вероника Игоревна</b><div class="muted" style="font-size:14px">канд. физ.-мат. наук, доцент</div><p style="font-size:15px;margin-top:8px">Математический анализ · Дискретная математика · Теория вероятностей</p></div></div><div class="card pg-t"><span class="pg-ava" aria-hidden="true">ДА</span><div><b>Долганов Антон Юрьевич</b><div class="muted" style="font-size:14px">канд. техн. наук, доцент</div><p style="font-size:15px;margin-top:8px">Машинное обучение · Обработка естественного языка</p></div></div><div class="card pg-t"><span class="pg-ava" aria-hidden="true">ЗО</span><div><b>Зверева Ольга Михайловна</b><div class="muted" style="font-size:14px">канд. техн. наук, доцент</div><p style="font-size:15px;margin-top:8px">Операционные системы · Современные интернет-технологии</p></div></div><div class="card pg-t"><span class="pg-ava" aria-hidden="true">РМ</span><div><b>Ронкин Михаил Владимирович</b><div class="muted" style="font-size:14px">канд. техн. наук, старший научный сотрудник</div><p style="font-size:15px;margin-top:8px">Нейронные сети · Компьютерное зрение · Анализ временных рядов</p></div></div></div>
<p style="margin-top:14px;font-size:15px"><a href="https://programs.edu.urfu.ru/ru/9797/teachers/" target="_blank" rel="noopener">Все преподаватели программы<span class="sr"> (откроется в новой вкладке)</span></a></p>

<h2 style="margin-top:56px">Что говорят студенты</h2>
<div class="card pg-rev" style="margin-top:20px">
<p class="pg-rev-q">Любимый предмет — проектный практикум: каждый семестр делаешь проект, часто для настоящего заказчика, и сам выбираешь роль в команде.</p>
<p style="margin-top:12px">Ещё нравится, что предметы можно выбирать: если не хочется только программировать, можно уйти в дизайн или аналитику. Поначалу было трудно с программированием — помогало спрашивать преподавателей.</p>
<div class="muted" style="font-size:14px;margin-top:14px">Пересказ интервью студентки 3 курса Ксении Поповой · <a href="https://programs.edu.urfu.ru/ru/9797/pages/feedback/" target="_blank" rel="noopener">полный текст<span class="sr"> (откроется в новой вкладке)</span></a></div>
</div>

<h2 style="margin-top:56px">Частые вопросы о программе</h2>
<div class="faq" style="margin-top:12px"><details><summary>Можно ли самому выбирать предметы?</summary><p>Да. Со 2 курса вместе с обязательными курсами выбираете курсы по выбору — так складывается своя траектория. Если выбор не подошёл, на старших курсах его можно поправить. Плюс майнор — курс другого направления.</p></details><details><summary>Сколько мест в 2026 году?</summary><p>Очная форма: 130 бюджетных и 70 платных мест.</p></details><details><summary>Сколько стоит платное обучение?</summary><p>390 000 ₽ в год, со скидкой — 331 500 ₽ (для граждан России). Условия скидок — в разделе «Стоимость и скидки» на сайте программы.</p></details><details><summary>Какие минимальные баллы ЕГЭ?</summary><p>В 2026 году: математика — 40, русский язык — 40, по выбору информатика — 46 или физика — 41.</p></details><details><summary>Будет ли практика в компаниях?</summary><p>Да: две учебные и три производственные практики. Места дают компании-партнёры, они же приносят задачи для проектов.</p></details><details><summary>Что такое ТОП-трек?</summary><p>С 2025 года на базе учебно-научного центра «Информационные технологии» ИРИТ-РтФ есть обучение по программам топ-уровня вместе с индустриальными партнёрами — в рамках нацпроекта «Экономика данных».</p></details><details><summary>Где проходят занятия?</summary><p>В ИРИТ-РтФ: Екатеринбург, ул. Мира, 32.</p></details></div>

<h2 style="margin-top:56px">Контакты программы</h2>
<div class="g3" style="margin-top:20px">
<div class="card"><div class="muted" style="font-size:14px">Руководитель программы</div><b style="display:block;margin-top:4px">Новиков Максим Юрьевич</b><p class="muted" style="font-size:14px;margin-top:6px">Р-327, ул. Мира, 32</p><a href="mailto:novikov.maksim@urfu.ru">novikov.maksim@urfu.ru</a></div>
<div class="card"><div class="muted" style="font-size:14px">Тьютор</div><b style="display:block;margin-top:4px">Ирина Колмогорцева</b><p class="muted" style="font-size:14px;margin-top:6px">Р-138а, ул. Мира, 32</p><a href="mailto:i.s.kolmogortseva@urfu.ru">i.s.kolmogortseva@urfu.ru</a></div>
<div class="card"><div class="muted" style="font-size:14px">Тьютор</div><b style="display:block;margin-top:4px">Алёна Садова</b><p class="muted" style="font-size:14px;margin-top:6px">Р-138а, ул. Мира, 32</p><a href="mailto:a.a.sadova@urfu.ru">a.a.sadova@urfu.ru</a></div>
</div>
<p class="muted" style="font-size:14px;margin-top:16px">Данные — с официального <a href="https://programs.edu.urfu.ru/ru/9797/" target="_blank" rel="noopener">сайта образовательных программ УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>, октябрь 2026.</p>
</sc-if>
__DEEP_MORE__


<sc-if value="{{linkBox}}" hint-placeholder-val="{{false}}"><h2 style="margin-top:56px">Подробнее о программе</h2>
<div class="card" style="margin-top:20px"><p>Учебный план, преподаватели и документы программы — на официальном сайте образовательных программ УрФУ.</p><a href="{{link}}" target="_blank" rel="noopener" style="display:inline-block;margin-top:10px;font-weight:600">Открыть страницу программы на programs.edu.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a></div></sc-if>

<h2 style="margin-top:56px">Похожие программы</h2>
<div class="g3" style="margin-top:20px"><sc-for list="{{similar}}" as="o" hint-placeholder-count="3"><a class="card" href="{{o.href}}"><span class="tag" title="{{o.instFull}}">{{o.instL}}</span><div style="font-weight:600;font-size:18px;margin-top:12px">{{o.name}}</div><div class="muted" style="font-size:14px;margin-top:8px">{{o.info}}</div></a></sc-for></div>
</div>
<aside class="side" style="display:flex;flex-direction:column;gap:16px">
<sc-if value="{{known}}" hint-placeholder-val="{{true}}"><div class="card" style="background:var(--ink);color:#FFFFFF;border-color:var(--ink)"><div style="font-family:var(--narrow);font-weight:700;font-size:20px">Хватит ли баллов?</div><p style="color:var(--on-dark-muted);margin-top:8px">{{calcLead}}</p><div class="field" style="margin-top:16px"><label for="my" style="color:#FFFFFF">Моя сумма баллов</label><input autocomplete="off" id="my" name="my" class="input" inputmode="numeric" placeholder="Например, 245…" value="{{my}}" onChange="{{onMy}}"></div><div aria-live="polite"><sc-if value="{{has}}" hint-placeholder-val="{{false}}"><div class="{{resCls}}"><b>{{resT}}</b><span>{{resD}}</span></div></sc-if></div><a class="btn" href="Catalog.dc.html" style="margin-top:12px;width:100%;background:#FFFFFF;color:var(--ink)">Подобрать похожие программы</a></div></sc-if>
<div class="card"><div style="font-weight:600">Приёмная комиссия</div><p style="margin-top:6px"><a href="tel:+73433754474">+7 (343) 375-44-74</a></p><p class="muted">Екатеринбург, ул. Мира, 19, каб. ГУК-100</p><a href="Contacts.dc.html" style="display:inline-block;margin-top:8px">Все контакты</a></div>
<div class="card"><div style="font-weight:600">Дни открытых дверей</div><p class="muted" style="margin-top:6px">{{instFull}} · даты — в календаре событий</p><a href="Events.dc.html" style="display:inline-block;margin-top:8px">Календарь событий</a></div>
</aside>
</div>
</div>
"""


def deep_block(flag, d):
    """Подробный блок программы по данным programs.edu.urfu.ru (показывается через sc-if flag)."""
    src = 'https://programs.edu.urfu.ru/ru/' + d['id'] + '/'
    nm = lambda n: 'модуль' if n == 1 else 'модуля' if n < 5 else 'модулей'
    study = ''.join(f'<div class="pg-blk" style="--c:{c}"><div class="pg-blk-h"><b>{t}</b><span>{len(it)} {nm(len(it))}</span></div><ul>' + ''.join(f'<li>{i}</li>' for i in it) + '</ul></div>' for t, c, it in d['blocks'])
    out = [f'<sc-if value="{{{{{flag}}}}}" hint-placeholder-val="{{{{false}}}}">']
    if d.get('about'):
        out.append('<h2 style="margin-top:56px">' + d['about'][0] + '</h2><div class="pg-about">' + ''.join(f'<p>{x}</p>' for x in d['about'][1]) + '</div>')
    if d.get('skills'):
        out.append('<h2 style="margin-top:56px">' + d['skills'][0] + '</h2><ul class="pg-skills">' + ''.join(f'<li>{x}</li>' for x in d['skills'][1]) + '</ul>')
    out.append(f'<h2 style="margin-top:56px">Что будешь изучать</h2><p class="muted" style="margin-top:8px;max-width:720px">{d["study_lead"]}</p><div class="pg-blks" style="margin-top:20px">{study}</div>'
               f'<p style="margin-top:14px;font-size:15px"><a href="{src}documents/" target="_blank" rel="noopener">Учебный план и рабочие программы модулей<span class="sr"> (откроется в новой вкладке)</span></a></p>')
    if d.get('tracks'):
        out.append('<h2 style="margin-top:56px">' + d['tracks'][0] + '</h2><div class="g3" style="margin-top:20px">' + ''.join(f'<div class="card pg-tr"><b>{t}</b><ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul></div>' for t, xs in d['tracks'][1]) + '</div>')
    if d.get('projects'):
        out.append('<h2 style="margin-top:56px">Проекты студентов</h2><div class="g3 pg-projs" style="margin-top:20px">' + ''.join(f'<div class="card pg-proj"><span class="tag">{st}</span><div class="pg-proj-t">{t}</div>' + (f'<div class="muted" style="font-size:14px;margin-top:auto">{c}</div>' if c else '') + '</div>' for t, c, st in d['projects']) + '</div>')
    if d.get('profs'):
        out.append('<h2 style="margin-top:56px">Кем будешь работать</h2><ul class="pg-profs" style="margin-top:20px">' + ''.join((f'<li><b>{a}</b><span>{b}</span></li>' if b else f'<li><b>{a}</b></li>') for a, b in d['profs']) + '</ul>')
    if d.get('partners'):
        out.append('<h2 style="margin-top:56px">С кем работает программа</h2><p class="muted" style="margin-top:8px;max-width:720px">' + d['partners'][0] + '</p><div class="pg-logos" style="margin-top:20px">' + ''.join(f'<span class="pg-logo">{x}</span>' for x in d['partners'][1]) + '</div>')
    if d.get('teachers'):
        ini = lambda n: n.split()[0][0] + n.split()[1][0]
        out.append('<h2 style="margin-top:56px">Кто будет учить</h2><div class="g2" style="margin-top:20px">' + ''.join(f'<div class="card pg-t"><span class="pg-ava" aria-hidden="true">{ini(n)}</span><div><b>{n}</b><div class="muted" style="font-size:14px">{r}</div>' + (f'<p style="font-size:15px;margin-top:8px">{c}</p>' if c else '') + '</div></div>' for n, r, c in d['teachers']) + f'</div><p style="margin-top:14px;font-size:15px"><a href="{src}teachers/" target="_blank" rel="noopener">Все преподаватели программы<span class="sr"> (откроется в новой вкладке)</span></a></p>')
    out.append('<h2 style="margin-top:56px">Частые вопросы о программе</h2><div class="faq" style="margin-top:12px">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in d['faq']) + '</div>')
    if d['contacts']: out.append('<h2 style="margin-top:56px">Контакты программы</h2><div class="g3" style="margin-top:20px">' + ''.join(f'<div class="card"><div class="muted" style="font-size:14px">{r}</div><b style="display:block;margin-top:4px">{n}</b><p class="muted" style="font-size:14px;margin-top:6px">{a}</p><a href="mailto:{m}">{m}</a></div>' for r, n, a, m in d['contacts']) + '</div>')
    out.append(f'<p class="muted" style="font-size:14px;margin-top:16px">Данные — с официального <a href="{src}" target="_blank" rel="noopener">сайта образовательных программ УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>, октябрь 2026.</p>')
    out.append('</sc-if>')
    return '\n'.join(out)


IB = dict(id='10216',
    about=('Универсальный безопасник', ['Программа учит защищать информацию со всех сторон: сети, операционные системы, программы и документы. Выпускник — «универсальный безопасник» с хорошей математикой и навыками программирования.',
        'Официальный партнёр программы — системный интегратор УЦСБ. Часть преподавателей работает в компаниях и учит на реальных задачах. Есть сообщество кибербезопасности UCS и лаборатория кибербезопасности NEO от УЦСБ.']),
    skills=('Что будешь уметь', ['Строить и защищать компьютерные сети', 'Применять математику в криптографии', 'Администрировать ОС и находить уязвимости', 'Проводить криминалистический анализ в ОС',
        'Писать программы на C#, Python и C++', 'Расследовать компьютерные инциденты', 'Знать правовые основы защиты информации', 'Применять технические средства защиты']),
    study_lead='Модули учебного плана по темам. Проектный практикум идёт с 1 по 4 курс, на 3 курсе выбираете траекторию.',
    blocks=[('Защита информации', '#C2185B', ['Основы информационной безопасности', 'Методы и средства защиты информации', 'Криптографическая защита информации', 'Программно-аппаратные средства защиты', 'Защита от утечки по техническим каналам', 'Противодействие вредоносным программам', 'Элементы компьютерной криминалистики']),
            ('Системы и программирование', '#6B2BE0', ['Программирование', 'Технологии программирования', 'Безопасность компьютерных систем', 'Электроника и схемотехника', 'Корпоративные информационные системы', 'Анализ данных и искусственный интеллект']),
            ('Математика и теория', '#1D4E9E', ['Элементарные основы математики и физики', 'Высшая математика для профессиональной деятельности', 'Теория информации', 'Методы обработки информации']),
            ('Право и управление', '#B86E00', ['Организационное и правовое обеспечение ИБ', 'Основы управления информационной безопасностью', 'Комплексная защита объекта информатизации', 'Защита интеллектуальной собственности', 'Документоведение', 'Экономика и организация производства']),
            ('Проекты и практика', '#0E8A6A', ['Основы проектной деятельности', 'Проектная деятельность', 'Учебная практика, ознакомительная', 'Производственная практика: проектно-технологическая и преддипломная']),
            ('По выбору', '#E0337A', ['Спецкурсы 1–3', 'Майнор — курс другого направления', 'Модуль дополнительной квалификации'])],
    tracks=('Три траектории на 3 курсе', [('Аналитики', ['Управление доступом', 'Облачные технологии и безопасность', 'Критическая информационная инфраструктура', 'Персональные данные']),
        ('Security Operation Center', ['Реагирование на инциденты', 'Цифровые следы в ОС', 'Цифровые следы в сети', 'Киберразведка']),
        ('Безопасная разработка', ['Основы разработки безопасного ПО', 'DevSecOps: контейнеры, облака, CI/CD', 'Сканеры, анализ сработок, WAF'])]),
    projects=[('Мобильное приложение «НВК Life» для адаптации в новом кампусе', 'Заказчик: УрФУ', 'Лучший проект')],
    partners=('Партнёры помогают составлять программу, ведут проекты, берут на практику и на работу.', ['УЦСБ', 'Интом', 'НПП «Гамма»', 'ИТ-Элемент29']),
    teachers=[('Куц Дмитрий Владимирович', 'старший преподаватель, специалист по ИБ', 'Программно-аппаратная защита · Безопасность сетей и ОС · Кибербезопасность'),
              ('Ермаков Дмитрий Германович', 'канд. физ.-мат. наук, доцент', 'Базы данных · Управление данными · Информационная безопасность')],
    faq=[('Сколько мест в 2026 году?', 'Очная форма: 135 бюджетных и 55 платных мест.'),
         ('Сколько стоит платное обучение?', '390 000 ₽ в год, со скидкой — 331 500 ₽ (для граждан России).'),
         ('Какие минимальные баллы ЕГЭ?', 'В 2026 году: математика — 40, русский язык — 40, по выбору информатика — 46 или физика — 41.'),
         ('Когда выбирать траекторию?', 'На 3 курсе: аналитика, Security Operation Center или безопасная разработка.'),
         ('Будут ли реальные проекты?', 'Да, проектный практикум идёт все четыре года — проекты от настоящих компаний, можно попробовать разные роли.'),
         ('Где проходят занятия?', 'В ИРИТ-РтФ: Екатеринбург, ул. Мира, 32.')],
    contacts=[('Руководитель программы', 'Астафьева Анна Викторовна', 'Р-443, ул. Мира, 32', 'anna.astafyeva@urfu.ru')])

AI = dict(id='10680',
    about=('ИИ — на практике', ['Программа учит применять машинное и глубокое обучение и внедрять искусственный интеллект в экономике, науке и технике. Ещё — технологии анализа больших данных.',
        'Учёба идёт в проектном формате: компании-партнёры выступают заказчиками и экспертами. Проект с потенциалом стать бизнесом можно защитить как выпускную работу — в формате «Стартап как диплом».']),
    study_lead='Модули учебного плана по темам. Программа новая — набор с 2024 года.',
    blocks=[('Данные и ИИ', '#6B2BE0', ['Анализ данных и искусственный интеллект', 'Алгоритмы и анализ сложности', 'Системная аналитика']),
            ('Программирование и системы', '#1D4E9E', ['Современные языки программирования', 'Технологии программирования', 'Виртуализация и облачные технологии', 'Компьютерные сети', 'Информационная безопасность']),
            ('Проекты и практика', '#0E8A6A', ['Основы проектной деятельности', 'Проектная деятельность', 'Учебная практика: ознакомительная и проектно-технологическая', 'Производственная практика: технологическая, проектная, преддипломная']),
            ('Инженерия и экономика', '#B86E00', ['Введение в инженерную деятельность', 'Экономика инженерии', 'Информационные технологии и сервисы']),
            ('По выбору', '#E0337A', ['Майнор — курс другого направления'])],
    projects=[('ИИ-помощник для настольных игр', 'Заказчик: «66 Бит»', 'Лучший проект'), ('Предсказание трендов по данным из соцсетей', '', 'Будущий проект'), ('Рекомендательная система для интернет-магазина', '', 'Будущий проект')],
    profs=[('Инженер искусственного интеллекта', 'Проектирует, разрабатывает и внедряет системы на основе ИИ.'), ('Разработчик рекомендательных систем', 'Алгоритмы, которые подсказывают пользователю нужное.'),
           ('Специалист по Data Mining', 'Находит скрытые закономерности в больших данных.'), ('Специалист по Big Data', 'Обрабатывает данные, с которыми не справляются обычные методы.')],
    teachers=[('Созыкин Андрей Владимирович', 'канд. техн. наук, руководитель программы', 'Программная инженерия · Управление программными проектами'),
              ('Долганов Антон Юрьевич', 'канд. техн. наук, доцент', 'Машинное обучение · Обработка естественного языка'),
              ('Ронкин Михаил Владимирович', 'канд. техн. наук, старший научный сотрудник', 'Нейронные сети · Компьютерное зрение · Временные ряды'),
              ('Корелин Иван Андреевич', 'канд. техн. наук, доцент', 'Обработка больших данных · Инженерия данных'),
              ('Борисов Василий Ильич', 'канд. техн. наук, доцент', 'Методы анализа данных и статистики · Проектный практикум'),
              ('Кислицын Евгений Витальевич', 'канд. экон. наук, заведующий кафедрой', 'Управление продуктом · Базы данных и SQL · Системная аналитика')],
    faq=[('Сколько мест в 2026 году?', 'Очная форма: 105 бюджетных и 25 платных мест.'),
         ('Сколько стоит платное обучение?', '300 000 ₽ в год, со скидкой — 255 000 ₽ (для граждан России).'),
         ('Какие минимальные баллы ЕГЭ?', 'В 2026 году: математика — 40, русский язык — 40, по выбору информатика — 46 или физика — 41.'),
         ('Что такое «Стартап как диплом»?', 'Студенческий проект в области ИИ, который может стать бизнесом, можно защитить как выпускную квалификационную работу.'),
         ('Чем отличается от «Программной инженерии»?', 'Здесь упор на машинное обучение, нейросети и большие данные; в «Программной инженерии» — на разработку и сопровождение программ.'),
         ('Где проходят занятия?', 'В ИРИТ-РтФ: Екатеринбург, ул. Мира, 32.')],
    contacts=[('Руководитель программы', 'Созыкин Андрей Владимирович', 'ИРИТ-РтФ, ул. Мира, 32', 'Andrey.Sozykin@urfu.ru'), ('Тьютор', 'Артём Хрушков', 'Р-138а, ул. Мира, 32', 'ae.khrushkov@urfu.ru')])


OPS = ['Основы проектной деятельности', 'Проектная деятельность', 'Учебная практика: ознакомительная и проектно-технологическая', 'Производственная практика: технологическая, проектная, преддипломная']

IVT = dict(id='9795',
    about=('Компьютер — от «железа» до сетей', ['Программа объединяет программирование, сетевые технологии, вычислительные системы и микропроцессорную технику. Студенты изучают устройство компьютеров и операционных систем, учатся анализировать потоки информации, создавать поисковые системы, сети хранения и передачи данных.',
        'Учёба идёт по индивидуальным траекториям: можно выбирать курсы, формат, команду, преподавателя и уровень сложности — и поправить выбор на старших курсах.']),
    study_lead='Модули учебного плана по темам. Профессиональные спецкурсы выбираете сами.',
    blocks=[('Математика', '#E0337A', ['Элементарные основы математики и физики', 'Математические методы для разработчиков 1–3', 'Дискретная математика и логика', 'Теория вероятностей и статистика', 'Векторный анализ']),
            ('Компьютеры и сети', '#1D4E9E', ['Архитектура ЭВМ', 'Операционные системы', 'Компьютерные сети', 'Виртуализация и облачные технологии', 'Информационная безопасность']),
            ('Программирование', '#6B2BE0', ['Программирование', 'Современные языки программирования', 'Технологии программирования', 'Прикладное программирование', 'Алгоритмы и анализ сложности', 'Web-технологии']),
            ('Системы и данные', '#0E8A6A', ['Базы данных', 'Проектирование информационных систем', 'Системная аналитика', 'Анализ данных и искусственный интеллект', 'Моделирование сложных процессов и систем']),
            ('Проекты и практика', '#B86E00', OPS),
            ('По выбору', '#C2185B', ['Профессиональные спецкурсы 1–6', 'Майнор — курс другого направления'])],
    projects=[('Сервис плана городских территорий', 'Заказчик: УрФУ · экспертиза УЦСБ', 'Социальный проект'), ('UX/UI платформы для соревнований по машинному обучению', 'Заказчик: УрФУ', 'Лучший проект'), ('Система «Доступный туризм»', 'Заказчик: ГАУ СО «РЦФКС»', 'Социальный проект'), ('Мобильный путеводитель по городам России', 'Заказчик: УБРиР', 'Лучший проект')],
    profs=[('DevOps-инженер', 'Ускоряет разработку и выпуск обновлений.'), ('Администратор баз данных', 'Проектирует и поддерживает базы данных.'), ('Инженер-программист', 'Создаёт программы для операционных систем.'), ('Системный инженер', 'Настраивает сети и офисную технику.'),
           ('Корпоративный архитектор', 'Проектирует программные системы компании.'), ('Интегратор', 'Внедряет IT в компаниях.'), ('Инженер-электронщик', 'Отвечает за электронное оборудование.'), ('Инженер связи', 'Мобильная, спутниковая и другая связь.')],
    partners=('Партнёры участвуют в составлении программы, проектах, практике и трудоустройстве.', ['НПЦ «РИЦ»', 'Ламарт', 'Сайберлимфа', '66 Бит', 'ТД УЭТ', 'НАУ-Сервис', 'НПО автоматики']),
    teachers=[('Спиричева Наталия Рахматулловна', 'старший преподаватель, руководитель программы', 'Структуры данных · ООП · Теория информации'),
              ('Аксенов Константин Александрович', 'канд. техн. наук, доцент', 'Системы поддержки принятия решений · Интеллектуальные системы'),
              ('Добряк Павел Вадимович', 'канд. техн. наук', 'Объектно-ориентированное программирование · Управление данными'),
              ('Доросинский Леонид Григорьевич', 'доктор техн. наук', 'Теория электрических цепей · Теория принятия решений'),
              ('Денисов Дмитрий Вадимович', 'канд. техн. наук', 'Цифровые двойники · Анализ данных'),
              ('Зверева Ольга Михайловна', 'канд. техн. наук, доцент', 'Операционные системы · Интернет-технологии')],
    faq=[('Сколько мест в 2026 году?', 'Очная форма: 140 бюджетных и 20 платных мест.'), ('Сколько стоит платное обучение?', '300 000 ₽ в год, со скидкой — 255 000 ₽ (для граждан России).'),
         ('Какие минимальные баллы ЕГЭ?', 'В 2026 году: математика — 40, русский язык — 40, по выбору информатика — 46 или физика — 41.'),
         ('Чем отличается от «Программной инженерии»?', 'Здесь больше про устройство компьютеров, сети и вычислительные системы; в «Программной инженерии» — про разработку и сопровождение программ.'),
         ('Где проходят занятия?', 'В ИРИТ-РтФ: Екатеринбург, ул. Мира, 32.')],
    contacts=[('Руководитель программы', 'Спиричева Наталия Рахматулловна', 'Р-246, ул. Мира, 32', 'nr.spiricheva@urfu.ru'), ('Тьютор', 'Георгий Базаров', 'Р-138а, ул. Мира, 32', 'gdbazarov@urfu.ru')])

PRI = dict(id='9796',
    about=('IT для любой сферы', ['Прикладная информатика — на стыке дисциплин: как применять информационные технологии в экономике, дизайне, гуманитарных науках и везде в жизни.',
        'Учиться можно очно (4 года), очно-заочно и заочно (4,6 года). Траектория индивидуальная: курсы, формат, команду и преподавателя выбираете сами.']),
    study_lead='Модули учебного плана по темам — общая база с другими IT-программами ИРИТ-РтФ плюс спецкурсы по выбору.',
    blocks=[('Программирование', '#6B2BE0', ['Программирование', 'Современные языки программирования', 'Технологии программирования', 'Web-технологии', 'Алгоритмы и анализ сложности']),
            ('Данные и системы', '#0E8A6A', ['Базы данных', 'Анализ данных и искусственный интеллект', 'Проектирование информационных систем', 'Системная аналитика']),
            ('Управление и экономика', '#B86E00', ['Управление проектами', 'Экономика инженерии', 'Экономические и гуманитарные аспекты IT', 'Правовые основы IT']),
            ('Проекты и практика', '#1D4E9E', OPS),
            ('По выбору', '#C2185B', ['Профессиональные спецкурсы 1–6', 'Майнор — курс другого направления'])],
    projects=[('Система картирования городских деревьев волонтёрами', '', 'Реализован'), ('Приложение для личной программы участника конференции', '', 'Реализован'), ('Мобильный путеводитель по городам России', 'Заказчик: УБРиР', 'Лучший проект')],
    profs=[('Системный аналитик', 'Формулирует требования к системам.'), ('Продукт-менеджер', 'Отвечает за создание продукта.'), ('Продуктовый аналитик', 'Работает с данными о продукте.'), ('UX/UI-дизайнер', 'Проектирует интерфейсы.'),
           ('Data Scientist', 'Анализирует большие массивы данных.'), ('IT-менеджер', 'Планирует и продвигает продукт.'), ('SMM-менеджер', 'Продвигает бренд в интернете.'), ('Технический писатель', 'Пишет документацию.')],
    partners=('Партнёры участвуют в составлении программы, проектах, практике и трудоустройстве.', ['СКБ Контур', 'Сбер', 'VK', '66 Бит', 'Targem Games', 'Artsofte', 'НПЦ «РИЦ»', 'Ламарт', 'Сайберлимфа', 'Селфи Айди', 'НАУ-Сервис', 'ФТ-Софт', 'ГК «Статус»']),
    teachers=[('Алферьева Татьяна Игоревна', 'канд. пед. наук, руководитель программы', 'Информатика · IT и сервисы · Эконометрика'),
              ('Чернильцев Андрей Германович', 'канд. техн. наук', 'Языки и технологии программирования · Разработка приложений'),
              ('Кислицын Евгений Витальевич', 'канд. экон. наук, заведующий кафедрой', 'Управление продуктом · Имитационное моделирование'),
              ('Третьяков Андрей Игоревич', 'канд. физ.-мат. наук, доцент', 'Программирование'),
              ('Чуксина Наталия Владимировна', 'канд. физ.-мат. наук', 'Алгебра и геометрия · Векторный анализ'),
              ('Папуловская Наталья Владимировна', 'канд. пед. наук, доцент', 'Интернет вещей · Постановка задач управления')],
    faq=[('Сколько мест в 2026 году?', 'Очно: 130 бюджетных и 80 платных. Ещё 50 платных мест очно-заочно и 55 — заочно.'),
         ('Сколько стоит платное обучение?', 'Очно — 300 000 ₽ в год (со скидкой 255 000 ₽), очно-заочно — 197 000 ₽, заочно — 165 000 ₽. Цены для граждан России.'),
         ('Какие минимальные баллы ЕГЭ?', 'В 2026 году: математика — 40, русский язык — 40, по выбору информатика — 46 или физика — 41.'),
         ('Можно ли учиться и работать?', 'Да, есть очно-заочная и заочная формы — 4,6 года.'),
         ('Где проходят занятия?', 'В ИРИТ-РтФ: Екатеринбург, ул. Мира, 32.')],
    contacts=[('Руководитель программы', 'Алферьева Татьяна Игоревна', 'Р-331б, ул. Мира, 32', 't.i.alfereva@urfu.ru'), ('Тьютор', 'Артём Хрушков', 'Р-138а, ул. Мира, 32', 'ae.khrushkov@urfu.ru')])

AAI = dict(id='10591',
    about=('Алгоритмы, на которых работает ИИ', ['С первого курса студенты изучают алгоритмы машинного обучения, компьютерного зрения и обработки естественного языка. Особый упор — на зрение, язык и большие данные.',
        'ИИ — сквозная технология: промышленность, экономика, медицина, транспорт, образование. Свой проект можно защитить в формате стартапа и привлечь инвестиции.']),
    study_lead='Модули учебного плана по темам. Программа новая — набор с 2023 года.',
    blocks=[('ИИ и данные', '#6B2BE0', ['Анализ данных и искусственный интеллект', 'Алгоритмы и анализ сложности', 'Системная аналитика']),
            ('Программирование и системы', '#1D4E9E', ['Современные языки программирования', 'Виртуализация и облачные технологии', 'Компьютерные сети']),
            ('Проекты и практика', '#0E8A6A', OPS),
            ('По выбору', '#C2185B', ['Майнор — курс другого направления'])],
    projects=[('AI-агент для подбора помещений для отделений банка', 'Заказчик: Сбер, Уральский банк', 'Лучший проект'), ('Мобильное приложение для распознавания ArUco-маркеров', 'Быстрая проверка ответов учеников камерой', 'Реализован'),
              ('Распознавание лиц для контроля доступа', '', 'Будущий проект'), ('Распознавание автомобильного трафика', '', 'Будущий проект')],
    profs=[('Разработчик систем ИИ', 'Создаёт и внедряет системы на основе ИИ.'), ('Специалист по компьютерному зрению', 'Распознавание объектов на фото и видео.'), ('NLP-программист', 'Обработка естественного языка.'),
           ('Data Scientist', 'Учит компьютер на больших данных.'), ('Специалист по данным для машинного обучения', 'Готовит данные и оценивает модели.'), ('Дизайнер взаимодействия с ИИ', 'Интерфейсы для систем ИИ.')],
    teachers=[('Белоусова Вероника Игоревна', 'канд. физ.-мат. наук, руководитель программы', 'Математический анализ · Теория вероятностей · Дискретная математика'),
              ('Долганов Антон Юрьевич', 'канд. техн. наук, доцент', 'Машинное обучение · Обработка естественного языка'),
              ('Браславский Павел Исаакович', 'канд. техн. наук, старший научный сотрудник', ''),
              ('Корелин Иван Андреевич', 'канд. техн. наук, доцент', 'Обработка больших данных · Инженерия данных'),
              ('Кошелев Антон Александрович', 'канд. физ.-мат. наук, доцент', 'Математический анализ · Математическое моделирование'),
              ('Борисов Василий Ильич', 'канд. техн. наук, доцент', 'Методы анализа данных · Проектный практикум')],
    faq=[('Сколько мест в 2026 году?', 'Очная форма: 105 бюджетных и 60 платных мест.'), ('Сколько стоит платное обучение?', '300 000 ₽ в год, со скидкой — 255 000 ₽ (для граждан России).'),
         ('Какие минимальные баллы ЕГЭ?', 'В 2026 году: математика — 40, русский язык — 40, по выбору информатика — 46 или физика — 41.'),
         ('Чем отличается от «Прикладного ИИ»?', 'Здесь упор на сами алгоритмы: компьютерное зрение, обработку языка, большие данные. В «Прикладном ИИ» — на внедрение ИИ в отрасли.'),
         ('Где проходят занятия?', 'В ИРИТ-РтФ: Екатеринбург, ул. Мира, 32.')],
    contacts=[('Руководитель программы', 'Белоусова Вероника Игоревна', 'ИРИТ-РтФ, ул. Мира, 32', 'v.i.belousova@urfu.ru'), ('Тьютор', 'Георгий Базаров', 'Р-138а, ул. Мира, 32', 'gdbazarov@urfu.ru')])

STR = dict(id='9826',
    about=('Программу делают вместе со стройкой', ['Программа готовит инженеров для архитектуры, проектирования, геодезии и строительства. Выпускник решает проектные, технологические, управленческие и изыскательские задачи.',
        'Партнёры — крупные девелоперы и строительные компании. Они дают реальные задачи с первого курса, берут на практику, водят на стройки жилых комплексов и участвуют в защите дипломов. Есть целевое обучение, а часть модулей можно сдать в формате демонстрационного экзамена «Ворлдскиллс».']),
    study_lead='Модули учебного плана по темам. Профили — от конструкций и технологий до водоснабжения, вентиляции и городского хозяйства.',
    blocks=[('Конструкции и архитектура', '#6B2BE0', ['Основы архитектуры и строительных конструкций', 'Проектирование строительных конструкций', 'Архитектура промышленных и гражданских зданий', 'Строительные материалы', 'Механика']),
            ('Технологии и управление', '#B86E00', ['Технология возведения зданий и сооружений', 'Организация, управление и планирование в строительстве', 'Управление качеством в строительстве', 'Техническая экспертиза и реконструкция', 'Правовое регулирование строительства']),
            ('Инженерные системы', '#1D4E9E', ['Водоснабжение', 'Отопление', 'Вентиляция и кондиционирование', 'Теплогазоснабжение', 'Подземные сети']),
            ('Город', '#0E8A6A', ['Планировка, застройка и реконструкция', 'Городские улицы и дороги', 'Городской транспорт и организация движения', 'Благоустройство территорий', 'Экология городской среды']),
            ('Цифровые инструменты', '#E0337A', ['Информационное моделирование BIM', 'Умное проектирование в nanoCAD', 'Программирование на Python', 'Инженерная графика', 'Excel для профессии'])],
    projects=[('Информационная модель школы на 120 мест с детским садом', 'Заказчик: Renga Software', 'Лучший проект'), ('Благоустройство территорий в Дегтярске', 'Заказчик: администрация Дегтярска', 'Лучший проект'),
              ('Глэмпинг в Екатеринбурге: концепция и экономика', 'Заказчик: «АрдисСтройКомплект»', 'Социальный проект'), ('Туристический маршрут «Исеть — Сысерть»', 'Заказчик: Бобровская администрация', 'Социальный проект'),
              ('Победа в конкурсе «Проект будущего — 2048»', 'Форум 100+ TechnoBuild', 'Реализован')],
    profs=[('Градостроитель', 'Проекты и управление в градостроительстве.'), ('Инженер-проектировщик сетей водоснабжения и канализации', 'Наружные сети воды и стоков.'), ('Проектировщик газооборудования', 'Котельные и теплоэлектроцентрали.'),
           ('Специалист по экспертизе проектов', 'Оценка качества и норм.'), ('Специалист по планово-экономической работе', 'Ресурсы и бюджет стройки.')],
    partners=('Крупные федеральные и региональные девелоперы и строительные компании.', ['Брусника', 'ЛСР', 'Самолёт', 'TEN', 'Атомстройкомплекс', 'ГК «Кортрос»', 'Форум-групп', 'НПП «Стройтэк»', 'НИЦ «Геотехструктура»', 'Renga Software', 'Газпром газораспределение Екатеринбург', 'Уралгипротранс', 'Водоканал', 'Уралэлектромедь']),
    teachers=[('Беляева Зоя Владимировна', 'канд. техн. наук', 'Металлические конструкции · Конструкции из дерева и пластмасс'), ('Кудрявцев Сергей Владимирович', 'канд. техн. наук', 'Металлические и каменные конструкции'),
              ('Мигалатий Евгений Васильевич', 'доктор техн. наук', 'Очистка воды · Системы водоснабжения и водоотведения'), ('Морозов Антон Юрьевич', 'канд. техн. наук', 'Вентиляция · Кондиционирование воздуха'),
              ('Булавина Людмила Вениаминовна', 'канд. техн. наук', 'Городской транспорт · Экология городской среды'), ('Ананьин Михаил Юрьевич', 'канд. техн. наук', 'Архитектура гражданских и промышленных зданий')],
    faq=[('Сколько мест в 2026 году?', 'Очная форма: 239 бюджетных и 55 платных мест.'), ('Сколько стоит платное обучение?', '283 000 ₽ в год (очно).'),
         ('Какие минимальные баллы ЕГЭ в 2026 году?', 'Русский язык — 40, профильная математика — 40, по выбору информатика — 46 или физика — 41.'),
         ('Есть ли целевое обучение?', 'Да, для абитуриентов доступно целевое обучение от компаний-партнёров.'),
         ('Будут ли экскурсии на стройку?', 'Да, партнёры водят студентов на объекты — например, ЖК «Северное сияние», «NOVA Park», «Основинские кварталы», «Русь».'),
         ('Где проходят занятия?', 'В Институте строительства и архитектуры: Екатеринбург, ул. Мира, 17.')],
    contacts=[])

JRN = dict(id='9869',
    about=('Журфак с восьмидесятилетней историей', ['Программа готовит журналистов для печати, телевидения, радио и сетевых изданий. Учёба практико-ориентированная: жанры, редактирование, фото- и видеосъёмка, мультимедиа.',
        'Среди выпускников — писатель Альберт Лиханов, первый замглавреда «Российской газеты» Юрий Лепский, тележурналист Евгений Енин, неоднократный лауреат ТЭФИ.']),
    study_lead='Модули учебного плана по темам. Можно взять модуль дополнительной квалификации и майноры.',
    blocks=[('Основы профессии', '#C2185B', ['Основы журналистской деятельности', 'Жанры журналистики', 'Отечественная и зарубежная журналистика', 'Экономика и право в журналистике']),
            ('Язык и текст', '#6B2BE0', ['Современный русский язык', 'Практическая стилистика', 'Речевые технологии в СМИ', 'Риторика и дискурс-анализ', 'История литературы']),
            ('Медиа', '#1D4E9E', ['Журналистика в интернете', 'Сетевые СМИ', 'Журналист в конвергентной редакции', 'Подготовка контента для печатных СМИ', 'Материалы для электронных СМИ', 'Продюсирование на региональном ТВ']),
            ('Практика и проекты', '#0E8A6A', ['Выпуск учебных СМИ', 'Медиапроектирование', 'Проектная деятельность', 'Практика']),
            ('Общество', '#B86E00', ['Социальная проблематика в СМИ', 'Социально-политические проблемы в журналистике', 'Научно-исследовательская деятельность журналиста'])],
    projects=[('Выпуск журнала УГИ «Ундервуд»', 'Заказчик: «Областная газета»', 'Лучший проект'), ('Фэшн-журналистика', 'Заказчик: УрФУ', 'Лучший проект')],
    profs=[('Корреспондент', ''), ('Редактор', ''), ('Продюсер', ''), ('Пресс-секретарь', ''), ('Медиаменеджер', ''), ('Копирайтер', ''), ('SMM-менеджер', ''), ('PR-менеджер', ''), ('Ведущий', '')],
    partners=('Редакции и телеканалы Екатеринбурга и России.', ['ТАСС', '«Коммерсантъ» в Екатеринбурге', '«Областная газета»', 'Областное телевидение', '4 канал', '66.ру', 'Сибирско-Уральская медиакомпания', '«Коляда-Театр»', 'ФК «Урал»']),
    teachers=[('Николай Яблонский', 'практик, «Коммерсантъ»', 'Практические занятия'), ('Кристина Свет-Яковлева', 'практик, ВГТРК «Урал»', 'Практические занятия'),
              ('Евгений Зашихин', 'Издательство Уральского университета', 'Практические занятия'), ('Роберт Карапетян', 'лауреат премии «ТЭФИ»', 'Практические занятия')],
    faq=[('Какие вступительные испытания?', 'Творческое испытание, литература и русский язык. Минимум в 2026 году — по 40 баллов за каждое.'),
         ('Сколько мест в 2026 году?', 'Очная форма: 4 бюджетных и 68 платных мест. Есть заочная форма — 5 лет.'),
         ('Сколько стоит платное обучение?', '300 000 ₽ в год (очно).'),
         ('Кто ведёт практику?', 'В основном опытные журналисты: из «Коммерсанта», ВГТРК «Урал», лауреаты «ТЭФИ».'),
         ('Где проходят занятия?', 'В Уральском гуманитарном институте: Екатеринбург, пр. Ленина, 51.')],
    contacts=[('Руководитель программы', 'Третьякова Любовь Анатольевна', '403А, пр. Ленина, 51', 'l.a.tretiakova@urfu.ru')])

DEEPS = [('dIB', 'Информационная безопасность', IB), ('dAI', 'Прикладной искусственный интеллект', AI), ('dIVT', 'Информатика и вычислительная техника', IVT),
         ('dPRI', 'Прикладная информатика', PRI), ('dAAI', 'Алгоритмы искусственного интеллекта', AAI), ('dSTR', 'Строительство', STR), ('dJRN', 'Журналистика', JRN)]
DEEP_MORE = '\n'.join(deep_block(f, d) for f, n, d in DEEPS)

LOGIC = """<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
""" + progs + """
// коды направлений (по общероссийскому перечню) и страницы программ на официальном сайте УрФУ
const CODE = {'Фундаментальная информатика и информационные технологии':'02.03.02','Прикладные математика и физика':'03.03.01','Программная инженерия':'09.03.04','Алгоритмы искусственного интеллекта':'09.03.01','Прикладной искусственный интеллект':'09.03.03','Интеллектуальные системы в гуманитарной сфере':'45.03.04','Информационная безопасность':'10.03.01','Информатика и вычислительная техника':'09.03.01','Прикладная информатика':'09.03.03','Инфокоммуникационные технологии и системы связи':'11.03.02','Радиотехника':'11.03.01','Прикладная математика':'01.03.04','Математика':'01.03.01','Физика':'03.03.02','Химия':'04.03.01','Биология':'06.03.01','Металлургия':'22.03.02','Материаловедение и технологии материалов':'22.03.01','Электроэнергетика и электротехника':'13.03.02','Теплоэнергетика и теплотехника':'13.03.01','Строительство':'08.03.01','Архитектура':'07.03.01','Ядерная энергетика и теплофизика':'14.03.01','История':'46.03.01','Журналистика':'42.03.02','Филология':'45.03.01','Лингвистика':'45.03.02','Психология':'37.03.01','Международные отношения':'41.03.05','Экономика':'38.03.01','Менеджмент':'38.03.02','Бизнес-информатика':'38.03.05'};
const PAGE = {'Программная инженерия':9797,'Алгоритмы искусственного интеллекта':10591,'Прикладной искусственный интеллект':10680,'Интеллектуальные системы в гуманитарной сфере':9875,'Информационная безопасность':10216,'Информатика и вычислительная техника':9795,'Прикладная информатика':9796,'Инфокоммуникационные технологии и системы связи':9813,'Радиотехника':9812,'Прикладная математика':9987,'Математика':9985,'Физика':9897,'Металлургия':10117,'Электроэнергетика и электротехника':9980,'Теплоэнергетика и теплотехника':9979,'Строительство':9826,'Архитектура':9843,'История':10151,'Журналистика':9869,'Филология':10145,'Лингвистика':10149,'Международные отношения':10331};
const INST = {'ИРИТ-РтФ':'Института радиоэлектроники и информационных технологий','ИЕНиМ':'Института естественных наук и математики','ИНМиТ':'Института новых материалов и технологий','УралЭНИН':'Уральского энергетического института','ИСА':'Института строительства и архитектуры','ФТИ':'Физико-технологического института','УГИ':'Уральского гуманитарного института','ИнЭУ':'Института экономики и управления'};
// подробности есть только у программы-примера
const EXTRA = {
'Информационная безопасность': { lead: 'Защита информации со всех сторон: сети, операционные системы, программы, документы. Официальный партнёр — УЦСБ.', form: '4 года, очно', deep: true, mins: {'математика': 40, 'информатика или физика': '46 / 41', 'русский': 40}, skills: [['Защищать сети', 'Архитектура и безопасность сетей.'], ['Работать с криптографией', 'Математика для защиты данных.'], ['Искать уязвимости', 'Администрирование ОС и анализ инцидентов.'], ['Писать код', 'C#, Python, C++.']], jobs: [] },
'Прикладной искусственный интеллект': { lead: 'Машинное и глубокое обучение, большие данные и внедрение ИИ в реальные отрасли. Проект можно защитить как «Стартап как диплом».', form: '4 года, очно', deep: true, mins: {'математика': 40, 'информатика': 46, 'русский': 40}, skills: [['Обучать модели', 'Машинное обучение и нейросети.'], ['Работать с данными', 'Анализ больших данных.'], ['Внедрять ИИ', 'Проекты для компаний-партнёров.'], ['Запускать стартапы', 'Проект с потенциалом бизнеса — как диплом.']], jobs: [] },
'Информатика и вычислительная техника': { lead: 'Программирование, сети, вычислительные системы и микропроцессорная техника — как устроен компьютер и как им управлять.', form: '4 года, очно', deep: true, mins: {'математика': 40, 'информатика или физика': '46 / 41', 'русский': 40}, skills: [['Понимать «железо»', 'Архитектура ЭВМ и операционные системы.'], ['Строить сети', 'Сети хранения, обработки и передачи данных.'], ['Программировать', 'Несколько языков и технологий.'], ['Анализировать данные', 'Потоки информации и поисковые системы.']], jobs: [] },
'Прикладная информатика': { lead: 'Информационные технологии для экономики, дизайна, гуманитарных наук и любой другой сферы. Можно учиться очно, очно-заочно или заочно.', form: '4 года очно; 4,6 — очно-заочно и заочно', deep: true, mins: {'математика': 40, 'информатика': 46, 'русский': 40}, skills: [['Анализировать', 'Требования к системам и данные о продукте.'], ['Программировать', 'Веб и прикладные системы.'], ['Управлять проектами', 'Продукт, сроки, команда.'], ['Проектировать интерфейсы', 'UX/UI и пользовательский опыт.']], jobs: [] },
'Алгоритмы искусственного интеллекта': { lead: 'Алгоритмы машинного обучения, компьютерное зрение, обработка естественного языка и большие данные — с первого курса.', form: '4 года, очно', deep: true, mins: {'математика': 40, 'информатика или физика': '46 / 41', 'русский': 40}, skills: [['Обучать модели', 'Машинное обучение с первого курса.'], ['Видеть как компьютер', 'Компьютерное зрение.'], ['Понимать язык', 'Обработка естественного языка.'], ['Запускать стартапы', 'Защита проекта в формате стартапа.']], jobs: [] },
'Строительство': { lead: 'Инженеры для архитектуры, проектирования, геодезии и строительства. Программу составляют вместе с крупнейшими девелоперами.', form: '4 года очно; 4,7 — очно-заочно', deep: true, skills: [['Проектировать', 'Конструкции, сети, благоустройство.'], ['Строить', 'Технологии и организация стройки.'], ['Моделировать', 'BIM, nanoCAD, Python.'], ['Управлять', 'Качество, экспертиза, экономика.']], jobs: [] },
'Журналистика': { lead: 'Журналисты для печати, ТВ, радио и сетевых изданий. Практику ведут действующие журналисты.', form: '4 года очно; 5 лет заочно', deep: true, skills: [['Писать', 'Жанры, стилистика, редактирование.'], ['Снимать', 'Фото, видео, мультимедиа.'], ['Делать медиа', 'Учебные СМИ и медиапроекты.'], ['Понимать общество', 'Социальная и политическая повестка.']], jobs: [] },
'Программная инженерия': {
  lead: 'Проектирование, разработка и сопровождение программных систем: от требований заказчика до работающего продукта.',
  form: '4 года, очно', deep: true, mins: {'математика': 40, 'информатика или физика': '46 / 41', 'русский': 40},
  hist: [[2023, 253], [2024, 244], [2025, 259]],
  skills: [['Писать код', 'Алгоритмы, структуры данных, несколько языков программирования.'], ['Проектировать системы', 'Архитектура, базы данных, требования к продукту.'], ['Работать в команде', 'Командные проекты по методологиям разработки.'], ['Проверять качество', 'Тестирование, ревью кода, сопровождение.']],
  jobs: ['Backend-разработчик', 'Frontend-разработчик', 'Инженер по тестированию', 'Системный аналитик', 'DevOps-инженер', 'Руководитель проектов'] }};
let want = 'Программная инженерия';
try { const q = new URLSearchParams(location.search).get('p'); if (q && ALL_PROGS.some(x => x.name === q)) want = q; } catch (e) {}
const P = { score: '—', budget: '—', price: '—', sy: '2025', ...ALL_PROGS.find(x => x.name === want) };
const X = EXTRA[P.name] || {};
const DF = {}; __DFLAGS__.forEach(([f, n]) => { DF[f] = P.name === n; });
const href = n => 'Program.dc.html?p=' + encodeURIComponent(n);
try { document.title = P.name + ' — бакалавриат УрФУ'; } catch (e) {}
const cap = t => t.charAt(0).toUpperCase() + t.slice(1);
const parts = P.exams.split(', ');
const exams = parts.map((t, i) => {
  const kind = t === 'русский' ? 'Обязательный' : (t.includes(' или ') ? 'На выбор' : (i === 0 ? 'Профильный' : 'Обязательный'));
  const min = X.mins ? X.mins[t] : undefined;
  return { t: cap(t === 'русский' ? 'русский язык' : t), kind, hasMin: min !== undefined, min };
});
const sc = parseInt(P.score, 10), known = !isNaN(sc);
const hist = (X.hist || []).map(([y, v], i, a) => ({ y, v, px: Math.round(60 + (v - 200) * 1.2), c: i === a.length - 1 ? 'var(--blue)' : '#A9BFE2' }));
const lo = hist.length ? Math.min(...hist.map(h => h.v)) : sc;
const my = (this.state && this.state.my) || '';
const v = parseInt(my, 10);
let has = false, resT = '', resD = '', resCls = 'calc';
if (my.trim() !== '') {
  has = true;
  if (isNaN(v) || v < 0 || v > 310) { resT = 'Введите сумму от 0 до 310'; resD = 'Три ЕГЭ — до 300 баллов, плюс до 10 за достижения.'; resCls = 'calc calc-warn'; }
  else if (!known) { resT = 'Проходной балл пока не добавлен'; resD = 'Сравните с минимальными баллами ЕГЭ или посмотрите похожие программы.'; resCls = 'calc calc-mid'; }
  else if (v >= sc) { resT = 'Хватает'; resD = 'Ваша сумма не ниже проходного балла ' + P.sy + ' года (' + sc + ').'; resCls = 'calc calc-ok'; }
  else if (v >= lo) { resT = 'На границе'; resD = 'За последние годы проходной был от ' + lo + ' до ' + Math.max(...hist.map(h => h.v)) + '. До балла ' + P.sy + ' не хватает ' + (sc - v) + '.'; resCls = 'calc calc-mid'; }
  else { resT = 'Пока не хватает ' + (sc - v) + ' баллов'; resD = 'Посмотрите похожие программы с проходным ниже.'; resCls = 'calc calc-warn'; }
}
const IL = {'ИРИТ-РтФ':['Радиоэлектроника и IT','Институт радиоэлектроники и информационных технологий — РтФ'],'ИЕНиМ':['Естественные науки и математика','Институт естественных наук и математики'],'ИНМиТ':['Новые материалы и технологии','Институт новых материалов и технологий'],'УралЭНИН':['Энергетика','Уральский энергетический институт'],'ИСА':['Строительство и архитектура','Институт строительства и архитектуры'],'УГИ':['Гуманитарные науки','Уральский гуманитарный институт'],'ИнЭУ':['Экономика и управление','Институт экономики и управления'],'ФТИ':['Физика и технологии','Физико-технологический институт']};
const similar = ALL_PROGS.filter(x => x.k === P.k && x.name !== P.name)
  .map(x => ({ score: '—', sy: '2025', budget: '—', ...x }))
  .sort((a, b) => (isNaN(parseInt(a.score, 10)) ? 1 : 0) - (isNaN(parseInt(b.score, 10)) ? 1 : 0)).slice(0, 3)
  .map(x => ({ name: x.name, inst: x.inst, instL: (IL[x.inst] || [x.inst])[0], instFull: (IL[x.inst] || [x.inst, x.inst])[1], href: href(x.name), info: !isNaN(parseInt(x.score, 10)) ? 'Проходной балл ' + x.sy + ': ' + x.score : (x.budget && x.budget !== '—' ? 'Бюджетных мест: ' + x.budget + (x.price ? ' · ' + x.price : '') : '') }));
return {
  name: P.name, inst: P.inst, instL: (IL[P.inst] || [P.inst])[0], instFull: (IL[P.inst] || [P.inst, P.inst])[1], instHref: 'Institute.dc.html?i=' + encodeURIComponent(P.inst), area: P.area, code: CODE[P.name] || '', hasCode: !!CODE[P.name],
  lead: X.lead || ('Программа бакалавриата ' + (INST[P.inst] || P.inst) + '. Вступительные испытания: ' + P.exams + '.'),
  score: P.score, budget: P.budget, price: P.price, sy: P.sy, form: X.form || 'Очная',
  exams, hasHist: hist.length > 0, hist, histLabel: 'Проходной балл: ' + hist.map(h => h.y + ' — ' + h.v).join(', '),
  oneScore: !hist.length && known, known, hasScoreV: known, hasBudget: P.budget !== '—' && !!P.budget, hasPrice: P.price !== '—' && !!P.price,
  deep: P.name === 'Программная инженерия', ...DF, noDeep: !X.deep, linkBox: !!PAGE[P.name] && !X.deep,
  hasSkills: !!X.skills, skills: (X.skills || []).map(([t, d]) => ({ t, d })), jobs: X.jobs || [],
  hasLink: !!PAGE[P.name], link: PAGE[P.name] ? 'https://programs.edu.urfu.ru/ru/' + PAGE[P.name] + '/' : '',
  similar, cmpHref: 'Catalog.dc.html?cmp=' + encodeURIComponent(P.name) + '',
  calcLead: known ? 'Сравните свою сумму с проходным баллом ' + P.sy + ' года.' : 'Введите сумму баллов ЕГЭ — подскажем, что делать дальше.',
  my, has, resT, resD, resCls, onMy: (e) => this.setState({ my: e.target.value })
};
}
}
</script>
"""
open('Program.dc.html', 'w', encoding='utf-8', newline='\n').write(head + MAIN.replace('__DEEP_MORE__', DEEP_MORE) + foot + LOGIC.replace('__DFLAGS__', json.dumps([[f, n] for f, n, _ in DEEPS], ensure_ascii=False)) + tail)
# синхронизация списка программ на странице института
inst = open('Institute.dc.html', encoding='utf-8').read()
a = inst.index('const ALL_PROGS = ['); b = inst.index('];', a) + 2
open('Institute.dc.html', 'w', encoding='utf-8', newline='').write(inst[:a] + progs + inst[b:])
print('ok')
