"""Собирает Program.dc.html — одну страницу для всех программ каталога.
Какую программу показать, берётся из адреса: Program.dc.html?p=<название>. Без параметра — «Программная инженерия».
Список программ (институт, экзамены, баллы, места, цена) копируется из Catalog.dc.html, чтобы данные были одни и те же.
Запуск: python make_program.py — после правок каталога."""
import os

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

LOGIC = """<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
""" + progs + """
// коды направлений (по общероссийскому перечню) и страницы программ на официальном сайте УрФУ
const CODE = {'Фундаментальная информатика и информационные технологии':'02.03.02','Прикладные математика и физика':'03.03.01','Программная инженерия':'09.03.04','Алгоритмы искусственного интеллекта':'09.03.01','Прикладной искусственный интеллект':'09.03.03','Интеллектуальные системы в гуманитарной сфере':'45.03.04','Информационная безопасность':'10.03.01','Информатика и вычислительная техника':'09.03.01','Прикладная информатика':'09.03.03','Инфокоммуникационные технологии и системы связи':'11.03.02','Радиотехника':'11.03.01','Прикладная математика':'01.03.04','Математика':'01.03.01','Физика':'03.03.02','Химия':'04.03.01','Биология':'06.03.01','Металлургия':'22.03.02','Материаловедение и технологии материалов':'22.03.01','Электроэнергетика и электротехника':'13.03.02','Теплоэнергетика и теплотехника':'13.03.01','Строительство':'08.03.01','Архитектура':'07.03.01','Ядерная энергетика и теплофизика':'14.03.01','История':'46.03.01','Журналистика':'42.03.02','Филология':'45.03.01','Лингвистика':'45.03.02','Психология':'37.03.01','Международные отношения':'41.03.05','Экономика':'38.03.01','Менеджмент':'38.03.02','Бизнес-информатика':'38.03.05'};
const PAGE = {'Программная инженерия':9797,'Алгоритмы искусственного интеллекта':10591,'Прикладной искусственный интеллект':10680,'Интеллектуальные системы в гуманитарной сфере':9875,'Информационная безопасность':10216,'Информатика и вычислительная техника':9795,'Прикладная информатика':9796,'Инфокоммуникационные технологии и системы связи':9813,'Радиотехника':9812,'Прикладная математика':9987,'Математика':9985,'Физика':9897,'Металлургия':10117,'Электроэнергетика и электротехника':9980,'Теплоэнергетика и теплотехника':9979,'Строительство':9826,'Архитектура':9843,'История':10151,'Журналистика':9869,'Филология':10145,'Лингвистика':10149,'Международные отношения':10331};
const INST = {'ИРИТ-РтФ':'Института радиоэлектроники и информационных технологий','ИЕНиМ':'Института естественных наук и математики','ИНМиТ':'Института новых материалов и технологий','УралЭНИН':'Уральского энергетического института','ИСА':'Института строительства и архитектуры','ФТИ':'Физико-технологического института','УГИ':'Уральского гуманитарного института','ИнЭУ':'Института экономики и управления'};
// подробности есть только у программы-примера
const EXTRA = {'Программная инженерия': {
  lead: 'Проектирование, разработка и сопровождение программных систем: от требований заказчика до работающего продукта.',
  form: '4 года, очно', deep: true, mins: {'математика': 40, 'информатика или физика': '46 / 41', 'русский': 40},
  hist: [[2023, 253], [2024, 244], [2025, 259]],
  skills: [['Писать код', 'Алгоритмы, структуры данных, несколько языков программирования.'], ['Проектировать системы', 'Архитектура, базы данных, требования к продукту.'], ['Работать в команде', 'Командные проекты по методологиям разработки.'], ['Проверять качество', 'Тестирование, ревью кода, сопровождение.']],
  jobs: ['Backend-разработчик', 'Frontend-разработчик', 'Инженер по тестированию', 'Системный аналитик', 'DevOps-инженер', 'Руководитель проектов'] }};
let want = 'Программная инженерия';
try { const q = new URLSearchParams(location.search).get('p'); if (q && ALL_PROGS.some(x => x.name === q)) want = q; } catch (e) {}
const P = { score: '—', budget: '—', price: '—', sy: '2025', ...ALL_PROGS.find(x => x.name === want) };
const X = EXTRA[P.name] || {};
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
  deep: !!X.deep, noDeep: !X.deep, linkBox: !!PAGE[P.name] && !X.deep,
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
open('Program.dc.html', 'w', encoding='utf-8', newline='\n').write(head + MAIN + foot + LOGIC + tail)
# синхронизация списка программ на странице института
inst = open('Institute.dc.html', encoding='utf-8').read()
a = inst.index('const ALL_PROGS = ['); b = inst.index('];', a) + 2
open('Institute.dc.html', 'w', encoding='utf-8', newline='').write(inst[:a] + progs + inst[b:])
print('ok')
