"""Страница «Наука» (Science.dc.html): проекты «Приоритет-2030» с поиском и фильтрами,
ведущие научные школы, что делать студенту, наука для бизнеса, журналы.
Данные — со страниц urfu.ru/ru/science/ (копии в веб-архиве 2025 г.).
Шапка и подвал берутся из NotFound.dc.html. Запуск: python make_science.py (можно повторно)."""
import os, json, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WA = 'https://web.archive.org/web/'
SRC_P = WA + '20250622194640/https://urfu.ru/ru/science/proekty-razvitija-v-ramkakh-programmy-prioritet-2030/'
SRC_S = WA + '20251116114406/https://urfu.ru/ru/science/vedushchie-nauchnye-shkoly/'
SRC_J = WA + '20250725162429/https://urfu.ru/ru/science/scientific-journals/'
SRC_G = WA + '20250727202056/https://urfu.ru/ru/science/grants/'

# тип проекта: (код, название)
TYPES = [('all', 'Все проекты'), ('young', 'Молодёжные лаборатории'), ('ind', 'Для промышленности'), ('star', 'С ведущими учёными'), ('lab', 'Проекты лабораторий'), ('center', 'Центры компетенций')]
TYPE_SHORT = {'young': 'Молодёжная лаборатория', 'ind': 'Для промышленности', 'star': 'Ведущий учёный', 'lab': 'Лаборатория', 'center': 'Центр компетенций'}

# Список проектов «Приоритет-2030» — дословно со страницы urfu.ru
P2030 = [
    ("lab", "Новая тест-система для диагностики и лечения заболеваний различного генеза"),
    ("lab", "Метеориты как источник прототипов новых функциональных материалов и природоподобных технологий"),
    ("lab", "Моделирование фазовых состояний и термодинамических свойств сильнокоррелированных магнитов"),
    ("lab", "Перспективные магнитные материалы для энергетики и сенсорики"),
    ("lab", "Применение методов управления и теории дифференциальных игр в атомной энергетике и экономике"),
    ("lab", "Противовирусные механизмы новых азолоазиновых и азолопиримидиновых молекул in silico и in vitro"),
    ("lab", "Противовирусные нуклеозиды в ряду пиримидинов и их азолоаннелированных аналогов"),
    ("lab", "Процессы распада метастабильных фаз в сплавах цветных металлов"),
    ("lab", "Стеклогерметики для твердооксидных электрохимических устройств"),
    ("lab", "Структура и физико-химические свойства композиционно сложных неорганических материалов"),
    ("lab", "Экстремальные проблемы конструктивной теории функций"),
    ("star", "ИИ для анализа граф-структурированных данных в диагностике функциональных сетей мозга"),
    ("star", "Новые многоуровневые лазерные явления и передовые лазерные технологии в фотонике и биомедицине"),
    ("star", "Разработка основ получения синтез-газа из биомассы"),
    ("star", "Разработка функциональных метаматериалов для плазмоники, спинтроники и нанофотоники"),
    ("star", "Стохастический транспорт наночастиц в живом организме и снижение их вреда для здоровья"),
    ("star", "Трансформация глобальных цепочек создания стоимости"),
    ("young", "Глобальный энергетический переход: вызовы и перспективы для российской экономики"),
    ("young", "Иерархические функциональные ансамбли на основе полиоксометаллатных нанокластеров"),
    ("young", "Историко-культурное наследие: социальная роль и презентация через цифровые технологии"),
    ("young", "Молодежная лаборатория фотовольтаических материалов"),
    ("young", "Наноматериалы, методы диагностики и изготовление наноустройств для электроники"),
    ("young", "Принципы создания коррозионностойких материалов для энергетики и химической промышленности"),
    ("ind", "Интеллектуальная система создания цифровых двойников электроэнергетических систем"),
    ("ind", "Моделирование многофазных физико-биологических сред для биотехнологической промышленности"),
    ("ind", "Новые гидрометаллургические процессы переработки полиметаллического упорного сырья цветных металлов"),
    ("ind", "Оптимальные технологии в машиностроении"),
    ("ind", "Получение и обработка материалов на основе титана с использованием цифровых технологий"),
    ("ind", "Разработка модификаций коррозионно-стойкого сплава ХН62М для использования в технике и технологии"),
    ("ind", "Разработка технологии переработки отходов электросталеплавильных цехов и шламов"),
    ("ind", "УМЗ материалы и цифровые технологии производства медицинских имплантатов"),
    ("center", "Диаспоральные сообщества в условиях трансформации глобальной политической системы"),
    ("center", "Инженерно-экономические исследования в энергетике и высокотехнологичных отраслях"),
    ("center", "Кристаллографические закономерности фазовых и структурных превращений в металлах и сплавах"),
    ("center", "Лаборатория естественнонаучных методов в гуманитарных исследованиях"),
    ("center", "Направленный органический синтез полезных продуктов на основе окса- и азагетероциклов"),
    ("center", "Научный центр компетенций Биологически активных веществ и пищевых добавок"),
    ("center", "Научный центр экологически толерантной, эффективной и безопасной энергетики"),
    ("center", "Нелинейная стохастическая динамика"),
    ("center", "Органическое материаловедение и молекулярная электроника"),
    ("center", "Разработка и исследование функциональных наноматериалов для применений в электронике и биомедицине"),
    ("center", "Региональная лингвистика"),
    ("center", "Религиоведение и историческая демография"),
    ("center", "Ресурсосберегающие клинкерные материалы специального назначения"),
    ("center", "Сорбционно-спектроскопическое определение ионов металлов"),
    ("center", "Социальная политика территорий: исследования, разработки, прогнозы"),
    ("center", "Субъектно-ориентированные модели развития университетов и их взаимосвязь с экономикой региона"),
    ("center", "Терагерцовые оптические материалы"),
    ("center", "Центр компьютерного моделирования механически мягких магнитных материалов"),
    ("center", "Центр наноинженерии"),
    ("center", "Центр нейро-квантовых методов моделирования"),
    ("center", "Центр обработки сигналов и изображений методами искусственного интеллекта"),
    ("center", "Цифровые технологии и моделирование в биомедицине"),
    ("center", "Энергоэффективные электродвигатели и генераторы"),
]

# область — по ключевым словам названия (проект может попасть в несколько областей)
AREAS = [
    ('ai', 'ИИ и математика', ['искусствен', 'ИИ ', 'модел', 'теори', 'функций', 'стохастич', 'динамик', 'цифров', 'сигнал', 'кванто', 'игр']),
    ('mat', 'Материалы', ['материал', 'сплав', 'металл', 'нано', 'стекло', 'кристалл', 'магнит', 'титан', 'клинкер', 'метаматериал', 'кластер', 'покрыт', 'УМЗ']),
    ('energy', 'Энергетика', ['энерг', 'электродвиг', 'генератор', 'атомн', 'синтез-газ', 'фотовольт', 'электрохим', 'электроэнерг']),
    ('bio', 'Медицина и химия', ['вирус', 'нуклеоз', 'органическ', 'медицин', 'биомед', 'диагност', 'биолог', 'пищев', 'имплант', 'мозг', 'организм', 'гетероцикл', 'ионов', 'тест-систем']),
    ('soc', 'Общество и экономика', ['экономик', 'истор', 'лингвист', 'социаль', 'диаспор', 'религ', 'культур', 'университет', 'цепоч', 'наслед', 'гуманитар']),
]

SCHOOLS = [
    ('Естественно-научные', ['Современные методы функционализации гетероциклов', 'Физика магнитных материалов', 'Физико-химическая механика гетерогенных и многофазных сред', 'Школа В. М. Жуковского «Химия твердого тела»', 'Школа органического синтеза имени В. С. Мокрушина', 'Школа теории алгебраических систем и ее приложений в компьютерных науках', 'Электрохимическое материаловедение']),
    ('Инженерно-технические', ['Научная школа прикладной электродинамики', 'Проблемы безопасности и эффективности атомных электрических станций', 'Радиационная физика функциональных материалов', 'Технология редких и радиоактивных элементов', 'Уральская школа люминесценции', 'Уральская школа металловедов-термистов', 'Уральская школа турбоустановок', 'Уральская школа электроэнергетики', 'Физика и механика обработки металлов давлением', 'Школа теплоэнергетики', 'Школа тяжелых цветных металлов', 'Энергосберегающие электромеханические и электротехнологические установки и системы', 'Энергоэффективные технологии и информационно-моделирующие системы в металлургии']),
    ('Гуманитарные', ['Гуманитаризация обществознания', 'Научная школа лингвокультурологии и стилистики', 'Уральская семантическая школа', 'Социологическая школа исследований социальных общностей', 'Социология культуры и личности', 'Уральская школа ономастики, этимологии и этнолингвистики', 'Уральская школа прикладного источниковедения и археографии', 'Интеллектуальные бизнес-процессы в промышленности']),
]


def areas_of(title):
    t = title + ' '
    got = [k for k, _, kw in AREAS if any(w.lower() in t.lower() for w in kw)]
    return got or ['soc']


def projects():
    return [[k, t, areas_of(t)] for k, t in P2030]


RIA = 'https://ria.ru/organization_Uralskijj_federalnyjj_universitet/'
# научные новости 2026 (РИА Новости): дата, область, заголовок, пояснение
FINDS = [
    ('8 октября', 'mat', 'Титановые сплавы для авиадвигателей', 'Выдерживают экстремальные условия работы двигателя.'),
    ('8 октября', 'mat', 'Материал для долгой жизни двигателей и турбин', 'Продлевает срок службы деталей, которые работают в жаре и под нагрузкой.'),
    ('7 сентября', 'ai', 'Астероиды, опасные для Земли', 'Учёные изучили объекты, которые могут сблизиться с планетой.'),
    ('31 августа', 'energy', '«Газовые батарейки» в восемь раз мощнее', 'Нашли способ заметно поднять мощность источника тока.'),
    ('18 августа', 'bio', 'Причина необъяснимого мужского бесплодия', 'Вместе с УрО РАН выяснили, чем опасен перегрев.'),
    ('14 июля', 'bio', 'Биодобавки из отходов виноделия', 'Отходы производства превратили в полезный продукт.'),
    ('2 июля', 'bio', 'Рентген ускоряет созревание йогуртов', 'Новый способ ускорить производство кисломолочных продуктов.'),
]


JOURNALS = [('Quaestio Rossica', 'Web of Science'), ('Античная древность и средние века', 'Scopus · ERIH PLUS · РИНЦ'), ('Известия УрФУ. Серия 2. Гуманитарные науки', 'Web of Science (ESCI) · ERIH PLUS · ВАК'),
    ('Известия УрФУ. Серия 1. Проблемы образования, науки и культуры', 'РИНЦ · «Белый список»'), ('Уральское востоковедение', 'РИНЦ'), ('Вопросы ономастики', ''), ('Changing Societies & Personalities', ''),
    ('Экономика региона', ''), ('Chimica Techno Acta', ''), ('Ural Mathematical Journal', ''), ('Аналитика и контроль', ''), ('Journal of Tax Reform', ''), ('Университетское управление: практика и анализ', ''),
    ('R-Economy', ''), ('Journal of Applied Economic Research', ''), ('Ural Radio Engineering Journal', ''), ('Tempus et Memoria', ''),
    ('Russian Journal of Construction Science and Technology', ''), ('Актуальные вопросы спортивной психологии и педагогики', ''), ('Electrochemical Materials and Technologies', '')]
CKP = [('Комплексных исследований и экспертной оценки органических материалов', 'О. С. Ельцов, канд. хим. наук'), ('Структурных методов анализа и свойств материалов и наноматериалов', 'С. В. Беликов, канд. техн. наук'), ('Электромагнитной совместимости', 'Н. С. Князев, канд. техн. наук')]


def main_html(n_proj, n_school):
    n_young = sum(1 for k, _ in P2030 if k == 'young')
    n_ind = sum(1 for k, _ in P2030 if k == 'ind')
    an = {k: n for k, n, _ in AREAS}
    cnt = {k: 0 for k, _, _ in AREAS}
    for _, t, a in projects():
        for x in a: cnt[x] += 1
    mx = max(cnt.values())
    bars = ''.join(f'<li><span class="sb-n">{an[k]}</span><span class="sb-bar"><i style="width:{round(v / mx * 100)}%"></i></span><b>{v}</b></li>' for k, v in sorted(cnt.items(), key=lambda x: -x[1]))
    finds = ''.join(f'<li class="sf sf-{a}"><span class="sf-d">{d} 2026 · {an[a]}</span><b>{t}</b><span class="muted">{x}</span></li>' for d, a, t, x in FINDS)
    jl = ''.join(f'<li><b>{n}</b>' + (f'<span>{i}</span>' if i else '') + '</li>' for n, i in JOURNALS)
    ckp = ''.join(f'<li><b>Лаборатория {n[0].lower() + n[1:]}</b><span>Заведующий — {h}</span></li>' for n, h in CKP)
    schools = ''.join(f'<div class="sc-col"><h3>{g} <span>{len(xs)}</span></h3><ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul></div>' for g, xs in SCHOOLS)
    return f'''<main id="main" tabindex="-1" style="outline:none"><section class="phead dark sci-head"><div class="wrap">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / Наука</div>
<h1 class="big" style="font-size:52px;color:#FFFFFF">Наука в УрФУ</h1>
<p style="color:var(--on-dark-muted);margin-top:12px;font-size:19px;max-width:740px">Чем занимаются лаборатории университета, как студенту попасть в науку и как компании заказать исследование.</p>
<div class="sci-stats">
<div><b>{n_proj}</b><span>научных проектов по программе «Приоритет-2030»</span></div>
<div><b>{n_school}</b><span>ведущих научных школ</span></div>
<div><b>23</b><span>научных журнала, 12 — в международных базах</span></div>
<div><b>{n_young}</b><span>молодёжных лаборатории — для студентов и аспирантов</span></div>
</div>
</div></section>
<div class="wrap" style="padding-bottom:72px">

<section class="sci-sec" aria-labelledby="proj-h">
<h2 id="proj-h">Над чем работают учёные</h2>
<p class="muted sci-lead">Все проекты программы «Приоритет-2030» — со страницы urfu.ru. Найдите тему по слову или выберите область.</p>
<div class="sci-tools">
<div class="sci-q"><label for="sci-q" class="sr">Поиск по проектам</label><input id="sci-q" type="search" placeholder="Например: магнит, мозг, металл, энергия" value="{{{{q}}}}" onChange="{{{{setQ}}}}" autocomplete="off"></div>
<div class="sci-chips" role="group" aria-label="Область"><sc-for list="{{{{areas}}}}" as="a" hint-placeholder-count="6"><button type="button" class="chip" aria-pressed="{{{{a.on}}}}" onClick="{{{{a.pick}}}}">{{{{a.n}}}}</button></sc-for></div>
<div class="sci-chips" role="group" aria-label="Тип проекта"><sc-for list="{{{{types}}}}" as="t" hint-placeholder-count="6"><button type="button" class="chip sci-type" aria-pressed="{{{{t.on}}}}" onClick="{{{{t.pick}}}}">{{{{t.n}}}}</button></sc-for></div>
</div>
<p class="muted sci-count" aria-live="polite">{{{{countText}}}}</p>
<ul class="sci-grid">
<sc-for list="{{{{list}}}}" as="p" hint-placeholder-count="9"><li class="sci-card sci-{{{{p.k}}}}"><span class="sci-kind">{{{{p.kn}}}}</span><b>{{{{p.t}}}}</b><span class="sci-area">{{{{p.an}}}}</span></li></sc-for>
</ul>
<sc-if value="{{{{none}}}}" hint-placeholder-val="{{{{false}}}}"><div class="card" style="margin-top:12px"><b>Таких проектов нет.</b> <button type="button" class="hp-link" onClick="{{{{reset}}}}">Показать все проекты</button></div></sc-if>
<sc-if value="{{{{more}}}}" hint-placeholder-val="{{{{false}}}}"><button type="button" class="btn2 sci-more" onClick="{{{{showAll}}}}">Показать все {{{{total}}}}</button></sc-if>
<p class="muted sci-src">Источник: <a href="{SRC_P}" target="_blank" rel="noopener">проекты развития в рамках программы «Приоритет-2030», urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>. Области мы проставили сами по названию проекта.</p>
</section>

<section class="sci-sec" aria-labelledby="dir-h">
<h2 id="dir-h">Где больше всего проектов</h2>
<p class="muted sci-lead">Сколько из {n_proj} проектов «Приоритет-2030» относится к каждой области. Один проект может быть сразу в двух.</p>
<ul class="sci-bars">{bars}</ul>
</section>

<section class="sci-sec" aria-labelledby="find-h">
<h2 id="find-h">Открытия 2026 года</h2>
<p class="muted sci-lead">О чём писали в новостях про учёных УрФУ.</p>
<ol class="sci-finds">{finds}</ol>
<p class="muted sci-src">По данным <a href="{RIA}" target="_blank" rel="noopener">РИА Новости<span class="sr"> (откроется в новой вкладке)</span></a>. <a href="News.dc.html?tag=Наука">Все новости науки →</a></p>
</section>

<section class="sci-sec" aria-labelledby="stud-h">
<h2 id="stud-h">Студенту: как попасть в науку</h2>
<div class="g4 sci-steps">
<div class="card"><span class="way-i" aria-hidden="true">1</span><h3>Выберите тему</h3><p class="muted">Посмотрите проекты выше. {n_young} молодёжных лабораторий — коллективы молодых учёных: хороший старт для студента.</p><button type="button" class="hp-link" onClick="{{{{pickYoung}}}}">Показать молодёжные лаборатории</button></div>
<div class="card"><span class="way-i" aria-hidden="true">2</span><h3>Найдите руководителя</h3><p class="muted">Подойдите к преподавателю, который ведёт близкую тему, или напишите в лабораторию — так начинается почти любая студенческая научная работа.</p></div>
<div class="card"><span class="way-i" aria-hidden="true">3</span><h3>Портал молодёжной науки</h3><p class="muted">Конкурсы, школы и конференции для студентов и аспирантов УрФУ.</p><a href="https://youthscience.urfu.ru/" target="_blank" rel="noopener">youthscience.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a></div>
<div class="card"><span class="way-i" aria-hidden="true">4</span><h3>Гранты и конкурсы</h3><p class="muted">Открытые конкурсы фондов и университета — для студентов, аспирантов и молодых учёных.</p><a href="{SRC_G}" target="_blank" rel="noopener">Гранты на urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a></div>
</div>
</section>

<section class="sci-sec" aria-labelledby="path-h">
<h2 id="path-h">Путь в науке</h2>
<p class="muted sci-lead">От первой курсовой до защиты — все ступени есть в самом университете.</p>
<ol class="sci-path">
<li><b>Бакалавриат</b><span>Проектный практикум, студенческие лаборатории, первые доклады на конференциях.</span></li>
<li><b>Магистратура</b><span>Своя тема исследования и публикации вместе с руководителем.</span></li>
<li><b>Аспирантура</b><span>Подготовка диссертации — по направлениям аспирантуры УрФУ.</span></li>
<li><b>Защита</b><span>В диссертационных советах университета.</span></li>
<li><b>Молодой учёный</b><span>Гранты, премии, международные лаборатории и научные школы.</span></li>
</ol>
</section>

<section class="sci-sec" aria-labelledby="rate-h">
<h2 id="rate-h">Научный рейтинг студента</h2>
<div class="sci-rate">
<div><p class="sci-lead" style="margin-top:0">Достижения за учебный год — два семестра — студент загружает в научное портфолио. Модератор их проверяет, и из них складывается рейтинг. По нему назначают <b>повышенную стипендию</b> за научную деятельность.</p>
<p class="muted" style="margin-top:12px;font-size:15px">У части достижений есть предельный балл. Подробности — в сервисе «Учёт научных достижений».</p></div>
<div class="sci-formula" role="group" aria-label="Из чего складывается рейтинг">
<p class="sci-fx" aria-hidden="true">РС<sub>н</sub> = Б<sub>п</sub> + Б<sub>м</sub> + Б<sub>ис</sub> + Б<sub>г</sub> + Б<sub>ид</sub> + Б<sub>с</sub> + Б<sub>ст</sub></p>
<ul class="sci-fl"><li><b>Публикации</b></li><li><b>Научные мероприятия</b></li><li><b>Патенты и права на разработки</b></li><li><b>Гранты</b></li><li><b>Инновационная деятельность</b></li><li><b>Стипендии</b></li><li><b>Стажировки</b></li></ul>
</div>
</div>
<p class="muted sci-src">По разделу «Про рейтинги» <a href="https://privet.urfu.ru/ratings" target="_blank" rel="noopener">«Навигатора первокурсника» УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>

<section class="sci-sec" aria-labelledby="gr-h">
<h2 id="gr-h">Премии и гранты для молодых учёных</h2>
<p class="muted sci-lead">Конкурсы, которые университет собирает в один список. Сроки — по циклу 2025 года: они повторяются каждый год, точные даты 2026 уточняйте у отдела.</p>
<ul class="sci-gr">
<li><em>до 1 августа</em><b>Премия имени Татищева и де Геннина</b><span>Екатеринбург</span></li>
<li><em>до 1 сентября</em><b>Премия губернатора Свердловской области в сфере информационных технологий</b><span>Свердловская область</span></li>
<li><em>до 22 сентября</em><b>Премия РАО «Молодым учёным за успехи в науке»</b><span>Российская академия образования</span></li>
<li><em>до 15 октября</em><b>Премия Президента РФ в области науки и инноваций для молодых учёных</b><span>Россия</span></li>
</ul>
<div class="sci-funds"><span>Российский научный фонд</span><span>Фонд президентских грантов</span><span>Гранты Президента РФ</span><span>Премии Правительства РФ</span><span>Гранты на международное сотрудничество</span></div>
<div class="card sci-grc"><b>Контакты по конкурсам и грантам</b><span>ул. Мира, 19, ауд. Э-302 · <a href="tel:+73433745975">+7 (343) 374-59-75</a></span><span>пр. Ленина, 51, ауд. 243 · <a href="tel:+73433899326">+7 (343) 389-93-26</a></span><span class="muted">Там же — порядок оформления документов и электронная подпись заявок для РНФ.</span></div>
<p class="muted sci-src">Источник: <a href="https://web.archive.org/web/20250727202056/https://urfu.ru/ru/science/grants/" target="_blank" rel="noopener">«Конкурсы и гранты», urfu.ru (копия в веб-архиве, 2025)<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>

<section class="sci-sec" aria-labelledby="sch-h">
<h2 id="sch-h">Ведущие научные школы</h2>
<p class="muted sci-lead">Научные коллективы, которым учёный совет присвоил статус ведущей школы.</p>
<div class="sc-cols">{schools}</div>
<p class="muted sci-src">Источник: <a href="{SRC_S}" target="_blank" rel="noopener">ведущие научные школы, urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>

<section class="sci-sec sci-biz" aria-labelledby="biz-h">
<div class="sci-biz-in">
<div><h2 id="biz-h">Компаниям: заказать исследование</h2>
<p>{n_ind} проектов «Приоритет-2030» университет ведёт в интересах предприятий: цифровые двойники энергосистем, переработка шламов и отходов, титановые сплавы, медицинские импланты. Ещё в УрФУ есть центры коллективного пользования с научным оборудованием.</p>
<div class="sci-biz-btns"><button type="button" class="btn" onClick="{{{{pickInd}}}}">Проекты для промышленности</button><a class="btn2 sci-line" href="tel:88001005044">Контакт-центр: 8-800-100-50-44</a></div></div>
</div>
</section>

<section class="sci-sec" aria-labelledby="ckp-h">
<h2 id="ckp-h">Центр коллективного пользования</h2>
<p class="muted sci-lead">Научное оборудование университета, на котором можно заказать исследования и анализы. В центре три лаборатории:</p>
<ul class="sci-ckp">{ckp}</ul>
<p class="muted sci-src">Список оборудования, услуги и цены — на <a href="https://ckp.urfu.ru/" target="_blank" rel="noopener">ckp.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>

<section class="sci-sec" aria-labelledby="inf-h">
<h2 id="inf-h">Где делают науку</h2>
<p class="muted sci-lead">Научные подразделения и сервисы, которые перечислены в разделе «Наука» сайта УрФУ.</p>
<div class="sci-inf">
<div><b>Уральский математический центр</b><span>Региональный научно-образовательный математический центр.</span></div>
<div><b>«Урал-Карбон»</b><span>Карбоновый полигон Свердловской области: как экосистемы поглощают углерод.</span></div>
<div><b>Международные лаборатории</b><span>Совместные коллективы с учёными из других стран.</span></div>
<div><b>Научно-исследовательская часть</b><span>Договоры, гранты и сопровождение проектов.</span></div>
<div><b>Зональная научная библиотека</b><span>Фонды университета и доступ к научным базам.</span></div>
<div><b>Электронный научный архив</b><span>Статьи, диссертации и ВКР в открытом доступе — <a href="https://elar.urfu.ru/" target="_blank" rel="noopener">elar.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>.</span></div>
<div><b>Портал молодёжной науки</b><span>Конкурсы, школы и конференции — <a href="https://youthscience.urfu.ru/" target="_blank" rel="noopener">youthscience.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>.</span></div>
<div><b>Диссертационные советы</b><span>Защиты кандидатских и докторских диссертаций.</span></div>
</div>
</section>

<section class="sci-sec" aria-labelledby="jr-h">
<h2 id="jr-h">Журналы и издательство</h2>
<div class="g2 sci-two">
<div class="card"><b class="sci-big">23</b><h3>научных журнала</h3><p class="muted">Двенадцать из них входят в международные базы цитирования. Все журналы — на одном портале.</p><a href="https://journals.urfu.ru/" target="_blank" rel="noopener">journals.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a></div>
<div class="card"><h3>Издательство Уральского университета</h3><p class="muted">По данным УрФУ — крупнейшее университетское издательство в Уральском регионе: учебники, монографии, научная литература.</p><a href="https://print.urfu.ru/" target="_blank" rel="noopener">print.urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a></div>
</div>
<h3 class="sci-jh">Журналы на портале journals.urfu.ru</h3>
<ul class="sci-jl">{jl}</ul>
<p class="muted sci-src">Здесь — 20 журналов, которые сейчас есть на портале; число 23 — по разделу «Наука» сайта urfu.ru. Индексы — как указаны на портале; у журналов без подписи сведений на портале нет.</p>
<p class="muted sci-src">Источник: <a href="{SRC_J}" target="_blank" rel="noopener">научное издательство, urfu.ru<span class="sr"> (откроется в новой вкладке)</span></a>. <a href="News.dc.html?tag=Наука">Новости науки →</a></p>
</section>
</div>
</main>'''


LOGIC = '''<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
const P = __P__, TYPES = __TYPES__, AREAS = __AREAS__, TS = __TS__;
const st = this.state || {};
const q0 = st.q || '', a = st.a || 'all', t = st.t || 'all';
const AN = {}; AREAS.forEach(x => AN[x[0]] = x[1]);
const words = q0.toLowerCase().split(/\\s+/).filter(w => w.length > 1).map(w => w.slice(0, Math.max(4, w.length - 2)));
const all = P.filter(p => (t === 'all' || p[0] === t) && (a === 'all' || p[2].indexOf(a) !== -1) && words.every(w => p[1].toLowerCase().indexOf(w) !== -1));
const filtered = !!q0 || a !== 'all' || t !== 'all';
const LIM = 30, open = st.all || filtered;
const list = (open ? all : all.slice(0, LIM)).map(p => ({ k: p[0], kn: TS[p[0]], t: p[1], an: p[2].map(x => AN[x]).join(' · ') }));
const n = all.length;
const form = n % 10 === 1 && n % 100 !== 11 ? 'проект' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'проекта' : 'проектов';
const go = id => setTimeout(() => { const el = document.getElementById(id); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 0);
return {
  q: q0, setQ: e => this.setState({ q: e.target.value }),
  areas: [['all', 'Все области']].concat(AREAS).map(x => ({ n: x[1], on: String(x[0] === a), pick: () => this.setState({ a: x[0] }) })),
  types: TYPES.map(x => ({ n: x[1], on: String(x[0] === t), pick: () => this.setState({ t: x[0] }) })),
  list, none: n === 0, more: !open && n > LIM, total: n,
  countText: filtered ? (n ? 'Нашлось ' + n + ' ' + form : 'Ничего не нашлось') : 'Показаны ' + Math.min(LIM, n) + ' из ' + n + ' проектов',
  showAll: () => this.setState({ all: true }),
  reset: () => this.setState({ q: '', a: 'all', t: 'all' }),
  pickYoung: () => { this.setState({ t: 'young', a: 'all', q: '' }); go('proj-h'); },
  pickInd: () => { this.setState({ t: 'ind', a: 'all', q: '' }); go('proj-h'); }
};
}
}
</script>'''

CSS = '''
/* Наука */
.sci-head .wrap{padding-bottom:48px}
.sci-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:36px}
.sci-stats div{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:18px 20px}
.sci-stats b{display:block;font-family:var(--narrow);font-size:44px;line-height:1;color:var(--gold)}
.sci-stats span{display:block;margin-top:8px;color:#E7E1FA;font-size:15px;line-height:1.4}
.sci-sec{margin-top:72px}
.sci-lead{margin-top:8px;max-width:760px;font-size:17px}
.sci-src{margin-top:16px;font-size:14px}
.sci-tools{margin-top:20px;display:flex;flex-direction:column;gap:12px}
.sci-q input{width:100%;max-width:620px;min-height:52px;padding:0 18px;border-radius:14px;border:2px solid var(--limestone);font:inherit;font-size:17px;background:#FFFFFF;color:var(--ink)}
.sci-q input:focus-visible{outline:3px solid var(--amethyst);outline-offset:2px;border-color:var(--amethyst)}
.sci-chips{display:flex;flex-wrap:wrap;gap:8px}
.sci-chips .chip{cursor:pointer;font:inherit}
.sci-chips .chip[aria-pressed="true"]{background:var(--ink);color:#FFFFFF;border-color:var(--ink)}
.sci-chips .sci-type[aria-pressed="true"]{background:var(--amethyst);border-color:var(--amethyst)}
.sci-count{margin-top:16px}
.sci-grid{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.sci-card{background:#FFFFFF;border:1px solid var(--limestone);border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:8px;box-shadow:inset 4px 0 0 var(--c,var(--amethyst))}
.sci-card b{line-height:1.4;font-weight:600}
.sci-kind{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.sci-area{font-size:14px;color:var(--muted);margin-top:auto}
.sci-young{--c:var(--rhodonite)}.sci-ind{--c:var(--gold)}.sci-star{--c:var(--malachite)}.sci-center{--c:#C9B2FF}
.sci-more{margin-top:16px}
.sci-steps{margin-top:24px}
.sci-steps h3{margin-top:14px;font-size:19px}.sci-steps p{margin-top:8px;font-size:15px}
.sci-steps .card{display:flex;flex-direction:column;gap:4px;align-items:flex-start}
.sci-steps .card>a,.sci-steps .card>button{margin-top:auto;padding-top:10px}
.sc-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:24px}
.sc-col{background:#FFFFFF;border:1px solid var(--limestone);border-radius:18px;padding:22px 24px}
.sc-col h3{font-size:19px;display:flex;justify-content:space-between;align-items:baseline}
.sc-col h3 span{font-family:var(--narrow);font-size:28px;color:var(--amethyst)}
.sc-col ul{margin:12px 0 0;padding-left:18px;color:var(--text);font-size:15px;line-height:1.5}
.sc-col li+li{margin-top:6px}
.sci-biz{background:var(--ink);color:#FFFFFF;border-radius:24px;padding:40px}
.sci-biz h2{color:#FFFFFF}
.sci-biz p{color:#E7E1FA;margin-top:12px;max-width:780px;font-size:17px;line-height:1.6}
.sci-biz-btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
.sci-biz-btns .btn,.sci-biz-btns .btn2{white-space:normal;text-align:center;max-width:100%}
.sci-line{background:transparent;color:#FFFFFF;border:2px solid rgba(255,255,255,.6)}
.sci-line:hover{background:rgba(255,255,255,.1);color:#FFFFFF}
.sci-line:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.sci-two{margin-top:24px}
.sci-two h3{font-size:19px;margin-top:6px}.sci-two p{margin-top:8px}.sci-two a{display:inline-block;margin-top:12px}
.sci-big{font-family:var(--narrow);font-size:44px;line-height:1;color:var(--rhodonite)}
@media (max-width:1000px){.sci-grid,.sc-cols{grid-template-columns:repeat(2,minmax(0,1fr))}.sci-stats{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.sci-grid,.sc-cols{grid-template-columns:1fr}.sci-biz{padding:24px}.sci-stats b{font-size:36px}}
'''


CSS2 = '''
/* Наука v3 */
.sci-path{list-style:none;margin:22px 0 0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0;counter-reset:pt}
.sci-path li{position:relative;counter-increment:pt;display:flex;flex-direction:column;gap:6px;padding:52px 16px 0 0}
.sci-path li::before{content:counter(pt);position:absolute;left:0;top:0;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--ink);color:var(--gold);font-family:var(--narrow);font-size:22px;font-weight:700;z-index:1}
.sci-path li::after{content:"";position:absolute;left:40px;right:0;top:19px;height:3px;background:linear-gradient(90deg,var(--amethyst),var(--rhodonite))}
.sci-path li:last-child::after{display:none}
.sci-path b{font-family:var(--narrow);font-size:22px}
.sci-path span{font-size:15px;color:var(--muted)}
.sci-rate{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;margin-top:18px;align-items:start}
.sci-formula{padding:22px;border-radius:18px;background:var(--ink);color:#FFFFFF}
.sci-fx{font-family:var(--narrow);font-size:26px;font-weight:700;color:var(--gold);overflow-wrap:anywhere}
.sci-fx sub{font-size:.6em}
.sci-fl{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.sci-fl li{padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.12);font-size:14px}
.sci-gr{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.sci-gr li{display:flex;flex-direction:column;gap:6px;padding:18px;border-radius:16px;background:#FFFFFF;border:1px solid var(--line);border-top:5px solid var(--gold)}
.sci-gr em{font-style:normal;font-family:var(--narrow);font-size:22px;font-weight:700;color:var(--rhodonite-d,#C81A62)}
.sci-gr b{font-size:16px}
.sci-gr span{font-size:14px;color:var(--muted)}
.sci-funds{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.sci-funds span{padding:8px 14px;border-radius:12px;background:var(--limestone);font-weight:600;font-size:14px}
.sci-grc{display:flex;flex-direction:column;gap:4px;margin-top:16px;max-width:620px}
.sci-inf{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}
.sci-inf div{display:flex;flex-direction:column;gap:6px;padding:18px;border-radius:16px;background:#FFFFFF;border:1px solid var(--line);border-left:5px solid var(--malachite)}
.sci-inf b{font-family:var(--narrow);font-size:20px}
.sci-inf span{font-size:14px;color:var(--muted)}
@media (max-width:1000px){.sci-path{grid-template-columns:minmax(0,1fr);gap:14px}.sci-path li{padding:0 0 0 56px;min-height:44px}.sci-path li::after{left:19px;right:auto;top:40px;bottom:-14px;width:3px;height:auto}.sci-gr,.sci-inf{grid-template-columns:repeat(2,minmax(0,1fr))}.sci-rate{grid-template-columns:minmax(0,1fr)}}
@media (max-width:560px){.sci-gr,.sci-inf{grid-template-columns:minmax(0,1fr)}.sci-fx{font-size:22px}}
/* /Наука v3 */
'''


def main():
    base = open('NotFound.dc.html', encoding='utf-8').read()
    head, rest = base.split('<main', 1)
    foot = rest[rest.index('</main>') + len('</main>'):]
    foot = foot[:foot.index('<script type="text/x-dc"')]
    tail = base[base.index('<script src="dc-lite.js">'):]
    title = 'Наука — УрФУ'
    desc = 'Научные проекты УрФУ по программе «Приоритет-2030», ведущие научные школы, молодёжные лаборатории, журналы — и как студенту попасть в науку.'
    head = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*"', lambda m: m.group(1) + desc + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + title + '"', head)
    head = head.replace('NotFound.dc.html"', 'Science.dc.html"')
    # пункт меню «Наука» — текущая страница
    head = head.replace('<a href="Science.dc.html">Наука</a>', '<a href="Science.dc.html" aria-current="page">Наука</a>')
    ps = projects()
    n_school = sum(len(x) for _, x in SCHOOLS)
    logic = (LOGIC.replace('__P__', json.dumps(ps, ensure_ascii=False))
             .replace('__TYPES__', json.dumps(TYPES, ensure_ascii=False))
             .replace('__AREAS__', json.dumps([[k, n] for k, n, _ in AREAS], ensure_ascii=False))
             .replace('__TS__', json.dumps(TYPE_SHORT, ensure_ascii=False)))
    out = head + main_html(len(ps), n_school) + foot + logic + '\n' + tail
    open('Science.dc.html', 'w', encoding='utf-8', newline='').write(out)
    css = open('site.css', encoding='utf-8').read()
    if '/* Наука */' not in css:
        css += CSS
    if '/* Наука v3 */' in css:
        a = css.index('\n/* Наука v3 */'); b = css.index('/* /Наука v3 */', a) + len('/* /Наука v3 */\n')
        css = css[:a] + css[b:]
    open('site.css', 'w', encoding='utf-8', newline='').write(css.rstrip('\n') + '\n' + CSS2)
    from collections import Counter
    print('Science.dc.html: проектов', len(ps), 'школ', n_school, Counter(a for p in ps for a in p[2]))


if __name__ == '__main__':
    main()
