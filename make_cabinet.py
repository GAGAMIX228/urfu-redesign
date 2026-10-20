"""Демо-кабинет студента (Cabinet.dc.html).
Источники настоящих данных:
- плата за общежитие — приказы УрФУ № 655/03 от 01.07.2025 и № 628/03 от 20.06.2025 (вдвоём в комнате);
- стипендии, пропуск, первые недели, отсрочка — «Навигатор первокурсника УрФУ» (privet.urfu.ru, разделы
  «За деньги — да», «Это база», «Айти-сервисы», «Поселение», «Воинская обязанность»);
- шкала баллов — методические рекомендации ИЕНиМ УрФУ по БРС (insma.urfu.ru, 2018): 80–100 «отлично»,
  60–79 «хорошо», 40–59 «удовлетворительно», меньше 40 — «неудовлетворительно».
Пары, дедлайны, баллы, заявки — пример (так и подписано на странице).
Шапка и подвал берутся из NotFound.dc.html. Запуск: python make_cabinet.py (можно повторно),
после него — make_heroph.py и make_og.py."""
import os, json, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# общежитие: (название, зимой, летом) — рублей в месяц на человека, вдвоём в комнате
DORMS = [
    ('№ 1 · Большакова, 79', 1470, 1109), ('№ 2 · Большакова, 77', 1476, 1110), ('№ 4 · Большакова, 71', 1591, 1253),
    ('№ 5 · Малышева, 144', 2000, 1749), ('№ 6 · Чапаева, 16а', 2033, 1426), ('№ 7 · С. Набойченко, 3', 1595, 1251),
    ('№ 8 · Комсомольская, 70/10', 2040, 1715), ('№ 9 · Фонвизина, 8', 2108, 1749), ('№ 10 · Ленина, 66', 1490, 1086),
    ('№ 11 · Коминтерна, 5', 1340, 1089), ('№ 12 · Фонвизина, 4', 1340, 1085), ('№ 13 · Комсомольская, 66а', 1629, 1263),
    ('№ 14 · С. Набойченко, 1а', 1562, 1237), ('№ 15 · Коминтерна, 11', 1938, 1424), ('Новокольцовский, № 1, 2, 4, 5', 2378, 1654),
]
REQ = [('study', 'Справка об обучении'), ('army', 'Справка в военкомат'), ('stip', 'Справка о стипендии'), ('dorm', 'Справка для общежития')]
# государственная академическая стипендия, рублей в месяц, без уральского коэффициента («Навигатор первокурсника», 2026)
STIP = [
    ('first', '1 курс, до первой сессии', 2314.2, 'Получают все студенты-бюджетники очной формы — без условий.'),
    ('good', 'Сессия на «хорошо» и «отлично»', 3008.2, 'Для 2–6 курса и для первокурсников после первой сессии.'),
    ('best', 'Сессия только на «отлично»', 4398.0, 'Стипендия отличникам учёбы.'),
    ('mag', 'Магистратура', 4398.0, 'С 1 сентября 2026 года — для магистрантов и специалитета высшего уровня.'),
    ('magbest', 'Магистратура, отличник', 6480.6, 'С 1 сентября 2026 года.'),
]
# баллы БРС — пример
BRS = [('Алгоритмы и структуры данных', 91), ('Программирование', 84), ('Математический анализ', 72),
       ('Английский язык', 63), ('Физика', 54), ('История России', 38)]
# первые недели — по «Навигатору первокурсника»
FIRST = [
    ('Активировать учётную запись на id.urfu.ru', 'По телефону или почте, которые указали при поступлении.'),
    ('Подписать согласие и загрузить фото', 'В личном кабинете студента. Фото пойдёт и на QR-код, и на пластиковый пропуск.'),
    ('Получить QR-код, потом пластиковый пропуск', 'QR появится в кабинете после проверки фото — до 5 рабочих дней. Пластиковый выдаёт дирекция института.'),
    ('Выбрать секцию физкультуры и уровень английского', 'Только в браузере, на istudent.urfu.ru — в приложении этого нет.'),
    ('Поставить приложение «УрФУ.Учеба»', 'Расписание в телефоне и синхронизация с календарём.'),
    ('Живёте в общежитии — пройти медкомиссию', 'Медсанчасть УрФУ, ул. Комсомольская, 59, пн–пт 8:00–18:00. Осмотр — 210 ₽.'),
    ('Оформить регистрацию и заселение за 7 рабочих дней', 'Паспортный стол студгородка, затем — к заведующему общежитием. Иначе договор могут аннулировать.'),
    ('Найти наставника и профбюро института', 'Наставники — старшекурсники: помогают привыкнуть к университету.'),
]

GRP_NAV = [('cg-study', 'Учёба'), ('cg-money', 'Деньги'), ('cg-docs', 'Документы и пропуск'), ('cg-first', 'Первые недели'), ('cg-camp', 'Кампус и работа')]


def main_html():
    nav = ''.join(f'<a href="#{i}">{n}</a>' for i, n in GRP_NAV)
    return '''<main id="main" tabindex="-1" style="outline:none"><section class="phead cab-head"><div class="wrap">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / <a href="Login.dc.html">Личный кабинет</a> / Студент</div>
<p class="cab-demo" role="note"><b>Демо-кабинет.</b> Так будет выглядеть кабинет студента. Пары, баллы и заявки — пример, они хранятся только в этом браузере. Суммы, адреса и правила — настоящие, со ссылками на источники.</p>
<h1 class="big" style="font-size:48px">Здравствуйте!</h1>
<p class="muted" style="margin-top:10px;font-size:19px">{{hello}}</p>
<ul class="cab-sum" aria-label="Коротко на сегодня">
<li><b>{{sumPairs}}</b><span>{{sumPairsL}}</span></li>
<li><b>{{sumDl}}</b><span>{{sumDlL}}</span></li>
<li><b>{{sumStip}}</b><span>стипендия в месяц</span></li>
<li><b>{{sumFirst}}</b><span>шагов первых недель</span></li>
</ul>
</div></section>
<nav class="wrap cab-nav" aria-label="Разделы кабинета">''' + nav + '''</nav>

<div class="wrap cab">
<section class="card cab-nt cab-wide" aria-labelledby="cnt-h">
<div class="cab-h"><h2 id="cnt-h" class="cab-h2s">Уведомления <span class="cab-badge">{{ntN}}</span></h2></div>
<ul class="cab-nts"><sc-for list="{{nts}}" as="x" hint-placeholder-count="3"><li class="{{x.cls}}"><b>{{x.t}}</b><span>{{x.d}}</span><sc-if value="{{x.href}}" hint-placeholder-val="{{false}}"><a href="{{x.href}}">{{x.lt}}</a></sc-if></li></sc-for></ul>
</section>

<section class="cab-grp" aria-labelledby="cg-study">
<h2 class="cab-gh" id="cg-study">Учёба</h2>
<div class="cab-cols"><div class="cab-col">
<section class="card cab-today" aria-labelledby="ct-h">
<div class="cab-h"><h3 id="ct-h">{{dayTitle}}</h3><a href="Schedule.dc.html">Вся неделя →</a></div>
<ul class="cab-pairs"><sc-for list="{{pairs}}" as="p" hint-placeholder-count="3"><li><span>{{p.from}}–{{p.to}}</span><b>{{p.t}}</b><small>{{p.kind}}</small></li></sc-for></ul>
<p class="muted cab-note">Пары — пример, как в разделе «Расписание». Между 3-й и 4-й парой — «большак»: 45 минут на Мира, 19 и 40 минут на Ленина, 51.</p>
</section>

<section class="card cab-brs" aria-labelledby="cb-h">
<div class="cab-h"><h3 id="cb-h">Мои баллы</h3><span class="muted" style="font-size:14px">семестр · пример</span></div>
<p class="muted cab-lead">В УрФУ по каждому предмету копятся баллы из 100 — за контрольные, лабораторные и экзамен. Из них получается оценка.</p>
<ul class="cab-bl"><sc-for list="{{brs}}" as="b" hint-placeholder-count="6"><li class="{{b.cls}}">
<div class="cab-blt"><b>{{b.t}}</b><em>{{b.p}} <small>из 100</small></em></div>
<div class="cab-bar" aria-hidden="true"><i style="width:{{b.p}}%"></i></div>
<div class="cab-blg"><span class="cab-gr">{{b.g}}</span><small>{{b.next}}</small></div>
</li></sc-for></ul>
<ul class="cab-scale" aria-label="Шкала оценок">
<li class="s5"><b>80–100</b>отлично</li><li class="s4"><b>60–79</b>хорошо</li><li class="s3"><b>40–59</b>удовл.</li><li class="s2"><b>0–39</b>неудовл.</li>
</ul>
<p class="muted cab-note">Баллы — пример. Шкала — по <a href="https://insma.urfu.ru/fileadmin/user_upload/site_32133/IENiM/Dokumenty/Studentam/Metodicheskie_rekomendacii_po_kriterijam_i_shkalam_ocenivanija_v_ramkakh_ballno-reitingovoi_sistemy.pdf" target="_blank" rel="noopener">методическим рекомендациям УрФУ по БРС<span class="sr"> (PDF, откроется в новой вкладке)</span></a>. Зачёт ставят от 40 баллов.</p>
</section>
</div><div class="cab-col">
<section class="card cab-dl" aria-labelledby="cdl-h">
<div class="cab-h"><h3 id="cdl-h">Дедлайны</h3><span class="muted" style="font-size:14px">{{dlLeft}}</span></div>
<ul class="cab-dls"><sc-for list="{{dls}}" as="x" hint-placeholder-count="4"><li class="{{x.cls}}"><button type="button" class="cab-chk" aria-pressed="{{x.done}}" onClick="{{x.tog}}"><span class="sr">Отметить выполненным: {{x.t}}</span></button><span class="cab-dlt"><b>{{x.t}}</b><small>{{x.s}}</small></span><em>{{x.when}}</em></li></sc-for></ul>
<p class="muted cab-note">Задания — пример. Отметки сохраняются в этом браузере.</p>
</section>

<section class="card cab-ses" aria-labelledby="cse-h">
<div class="cab-h"><h3 id="cse-h">Зимняя сессия</h3><span class="muted" style="font-size:14px">январь · пример</span></div>
<table class="cab-tb"><caption class="sr">Экзамены и зачёты зимней сессии — пример</caption><thead><tr><th scope="col">Предмет</th><th scope="col">Форма</th></tr></thead><tbody>
<tr><td>Математический анализ</td><td><span class="cab-ex">экзамен</span></td></tr>
<tr><td>Программирование</td><td><span class="cab-ex">экзамен</span></td></tr>
<tr><td>Физика</td><td><span class="cab-ex">экзамен</span></td></tr>
<tr><td>Алгебра и геометрия</td><td>зачёт</td></tr>
<tr><td>История России</td><td>зачёт</td></tr>
<tr><td>Английский язык</td><td>зачёт</td></tr>
<tr><td>Физическая культура</td><td>зачёт</td></tr>
</tbody></table>
<h4 class="cab-sub">Если не сдали</h4>
<p class="muted" style="font-size:15px;margin-top:6px">Перед пересдачей возьмите в дирекции института экзаменационный лист — его студенты зовут «хвостовкой». Заказать его можно и в личном кабинете студента, вместе со справками.</p>
</section>
</div></div>
</section>

<section class="cab-grp" aria-labelledby="cg-money">
<h2 class="cab-gh" id="cg-money">Деньги</h2>
<div class="cab-cols"><div class="cab-col">
<section class="card cab-stip" aria-labelledby="cs-h">
<div class="cab-h"><h3 id="cs-h">Сколько я буду получать?</h3><a href="Help.dc.html?q=стипенд">Вопросы →</a></div>
<p class="lg-lbl" id="stip-l">Государственная академическая стипендия — выберите свой случай</p>
<div class="cab-sopt" role="group" aria-labelledby="stip-l"><sc-for list="{{stips}}" as="x" hint-placeholder-count="5"><button type="button" aria-pressed="{{x.on}}" onClick="{{x.pick}}">{{x.n}}</button></sc-for></div>
<div class="cab-sres" aria-live="polite">
<p class="cab-sbig">{{stipSum}}<small> в месяц</small></p>
<p class="cab-scf">{{stipK}}</p>
<p class="muted" style="font-size:15px;margin-top:6px">{{stipNote}}</p>
</div>
<h4 class="cab-sub">Когда назначают</h4>
<ul class="cab-st">
<li><b>С 1 февраля по 30 июня</b><span>по итогам зимней сессии</span></li>
<li><b>С 1 июля по 31 января</b><span>по итогам летней сессии</span></li>
</ul>
<h4 class="cab-sub">Что ещё бывает</h4>
<ul class="cab-st">
<li><b>Повышенная академическая</b><span>За достижения в учёбе, науке, спорте, творчестве или общественной работе. Достижения за год загружают в портфолио, их проверяет модератор.</span></li>
<li><b>Социальная</b><span>Тем, у кого есть право на соцподдержку: сироты, инвалиды, получатели госсоциальной помощи и другие.</span></li>
<li><b>Материальная помощь</b><span>Разовая выплата в трудной ситуации — по заявлению.</span></li>
</ul>
<p class="muted cab-note">Суммы — по <a href="https://privet.urfu.ru/money" target="_blank" rel="noopener">«Навигатору первокурсника» УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>, без уральского коэффициента. Задерживают выплату — горячая линия Минобрнауки <a href="tel:88002225571">8-800-222-55-71</a>, доб. 1.</p>
</section>
</div><div class="cab-col">
<section class="card cab-dorm" aria-labelledby="cd-h">
<div class="cab-h"><h3 id="cd-h">Плата за общежитие</h3><a href="Dorms.dc.html#price-h">Все цены →</a></div>
<p class="lg-lbl" id="dorm-l">Моё общежитие</p>
<div class="cab-dorms" role="group" aria-labelledby="dorm-l"><sc-for list="{{dorms}}" as="d" hint-placeholder-count="15"><button type="button" class="chip" aria-pressed="{{d.on}}" onClick="{{d.pick}}">{{d.n}}</button></sc-for></div>
<dl class="cab-pay" aria-live="polite"><div><dt>Зимой</dt><dd>{{winter}}</dd></div><div><dt>Летом</dt><dd>{{summer}}</dd></div></dl>
<p class="muted cab-note">В месяц на человека, вдвоём в комнате — по приказам УрФУ 2025 года.</p>
<h4 class="cab-sub">Как оплатить</h4>
<ul class="cab-st">
<li><b>Онлайн</b><span>на pay.urfu.ru, в приложении «Сбербанк Онлайн»</span></li>
<li><b>В банке</b><span>Синара — ГУК, правое крыло (пн–пт 9:00–19:00, сб 10:00–16:00); Сбербанк — ГУК, 1 этаж</span></li>
<li><b>Код оплаты</b><span>внизу ордера; код обеспечительного платежа — в п. 1 дополнительного соглашения</span></li>
</ul>
</section>
<section class="card cab-mny" aria-labelledby="cm-h">
<div class="cab-h"><h3 id="cm-h">Бюджет на месяц</h3><span class="muted" style="font-size:14px">подсказка</span></div>
<p class="muted cab-lead">Сравните стипендию с платой за выбранное общежитие.</p>
<div class="cab-cmp" aria-live="polite">
<div><span>Стипендия</span><b>{{stipShort}}</b></div>
<div><span>Общежитие зимой</span><b>− {{winter}}</b></div>
<div class="is-res"><span>Остаётся</span><b>{{leftover}}</b></div>
</div>
<p class="muted cab-note">Считаем по выбранным выше вариантам, без уральского коэффициента.</p>
</section>
</div></div>
</section>

<section class="cab-grp" aria-labelledby="cg-docs">
<h2 class="cab-gh" id="cg-docs">Документы и пропуск</h2>
<div class="cab-cols"><div class="cab-col">
<section class="card cab-req" aria-labelledby="cr-h">
<div class="cab-h"><h3 id="cr-h">Справки и заявления</h3></div>
<p class="lg-lbl" id="req-l">Какая справка нужна?</p>
<div class="seg cab-seg" role="group" aria-labelledby="req-l"><sc-for list="{{reqTypes}}" as="r" hint-placeholder-count="4"><button type="button" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.n}}</button></sc-for></div>
<div class="cab-row"><label for="req-n">Сколько экземпляров</label><input id="req-n" type="number" min="1" max="5" value="{{reqN}}" onChange="{{setN}}" class="input cab-num"><button type="button" class="btn" onClick="{{order}}">Заказать</button></div>
<sc-if value="{{hasReq}}" hint-placeholder-val="{{false}}"><h4 class="cab-sub">Мои заявки</h4><ul class="cab-list" aria-live="polite"><sc-for list="{{reqs}}" as="q" hint-placeholder-count="2"><li><b>{{q.n}}</b><span>{{q.c}} экз. · {{q.d}}</span><em>{{q.st}}</em></li></sc-for></ul><button type="button" class="linkbtn" onClick="{{clearReq}}">Очистить пример</button></sc-if>
<sc-if value="{{noReq}}" hint-placeholder-val="{{true}}"><p class="muted cab-note">Заявок пока нет. Закажите справку — она появится здесь со статусом.</p></sc-if>
</section>
<section class="card cab-army" aria-labelledby="ca-h">
<div class="cab-h"><h3 id="ca-h">Армия и учёба</h3></div>
<ul class="cab-st">
<li><b>Отсрочка</b><span>Студентам очной формы — на весь нормативный срок обучения. Для военкомата закажите справку выше.</span></li>
<li><b>Военный учебный центр</b><span>Студент УрФУ может поступить: заявление на имя ректора, направление из военкомата, медосвидетельствование, документы и нормативы по физподготовке.</span></li>
</ul>
<p class="muted cab-note">По разделу «Воинская обязанность» <a href="https://privet.urfu.ru/military" target="_blank" rel="noopener">«Навигатора первокурсника»<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>
<section class="card cab-wrong" aria-labelledby="cw-h">
<div class="cab-h"><h3 id="cw-h">Если что-то пошло не так</h3><a href="Help.dc.html">Центр помощи →</a></div>
<ul class="cab-st">
<li><b>Не сдал экзамен</b><span>Возьмите экзаменационный лист в дирекции института или закажите его в личном кабинете — и договоритесь о пересдаче.</span></li>
<li><b>Не пришла стипендия</b><span>Сначала — в дирекцию института. Не помогли — горячая линия Минобрнауки 8-800-222-55-71, доб. 1.</span></li>
<li><b>Не работает пропуск</b><span>Бюро пропусков, ауд. И-104 — с пропуском и студенческим билетом.</span></li>
<li><b>Хочу перевестись или восстановиться</b><span>В УрФУ это можно сделать в любое время года — заявление подают через сайт университета.</span></li>
<li><b>Тяжело и тревожно</b><span>Психологическая помощь студентам — 8-800-222-55-71, доб. 2, бесплатно.</span></li>
</ul>
</section>
</div><div class="cab-col">
<section class="card cab-pass" aria-labelledby="cp-h">
<div class="cab-h"><h3 id="cp-h">Мой пропуск</h3><span class="muted" style="font-size:14px">статус · пример</span></div>
<ol class="cab-steps">
<li class="is-done"><b>Учётная запись</b><span>активирована на id.urfu.ru</span></li>
<li class="is-done"><b>Фото и согласие</b><span>загружены в личном кабинете</span></li>
<li class="is-done"><b>Проверка фото</b><span>«Принята» — проверяют до 5 рабочих дней</span></li>
<li class="is-now"><b>QR-код</b><span>работает с 10:00 следующего дня после проверки, но только до 26 октября</span></li>
<li><b>Пластиковый пропуск</b><span>выдаёт дирекция института — о начале выдачи скажет староста</span></li>
</ol>
<div class="cab-warn"><b>Забыли пропуск?</b> Без него в корпус не пустят — придётся вернуться. Пропуск не работает — бюро пропусков, ауд. И-104: возьмите пропуск и студенческий билет.</div>
<p class="muted cab-note">Порядок — по разделам «Это база» и «Безопасность» <a href="https://privet.urfu.ru/baza" target="_blank" rel="noopener">«Навигатора первокурсника»<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>
</div></div>
</section>

<section class="cab-grp" aria-labelledby="cg-first">
<h2 class="cab-gh" id="cg-first">Первые недели</h2>
<section class="card cab-first" aria-labelledby="cf-h">
<div class="cab-h"><h3 id="cf-h">Чек-лист первокурсника</h3><span class="muted" style="font-size:14px">{{firstLeft}}</span></div>
<div class="cab-prog" aria-hidden="true"><i style="width:{{firstPct}}%"></i></div>
<ul class="cab-fl"><sc-for list="{{first}}" as="x" hint-placeholder-count="8"><li class="{{x.cls}}"><button type="button" class="cab-chk" aria-pressed="{{x.done}}" onClick="{{x.tog}}"><span class="sr">Отметить выполненным: {{x.t}}</span></button><span class="cab-dlt"><b>{{x.t}}</b><small>{{x.s}}</small></span></li></sc-for></ul>
<p class="muted cab-note">Шаги — по <a href="https://privet.urfu.ru/" target="_blank" rel="noopener">«Навигатору первокурсника» УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>. Отметки сохраняются в этом браузере. Контакт-центр: <a href="tel:88001005044">8-800-100-50-44</a>.</p>
</section>
</section>

<section class="cab-grp" aria-labelledby="cg-camp">
<h2 class="cab-gh" id="cg-camp">Кампус и работа</h2>
<div class="cab-cols"><div class="cab-col">
<section class="card cab-camp" aria-labelledby="ccm-h">
<div class="cab-h"><h3 id="ccm-h">Мой корпус</h3><a href="Help.dc.html#bld-h">Все корпуса →</a></div>
<p class="cab-big">Радиофак <span>ул. Мира, 32 · ИРИТ-РтФ</span></p>
<ul class="cab-cm">
<li><b>Коворкинг</b><span>1 этаж, Р-044 и левое крыло</span></li>
<li><b>Столовая</b><span>1 этаж</span></li>
<li><b>Библиотека</b><span>в ГУК: Б-202 техническая, Б-203 гуманитарная</span></li>
<li><b>Тьюторы</b><span>Р-138а</span></li>
</ul>
<h4 class="cab-sub">Как читать номер аудитории</h4>
<p class="cab-room" aria-hidden="true"><span class="r1">Р</span><span class="r2">1</span><span class="r3">38а</span></p>
<ul class="cab-rl"><li><i class="r1"></i>Буквы — корпус: Р — Радиофак, ГУК — главный учебный корпус</li><li><i class="r2"></i>Первая цифра — этаж</li><li><i class="r3"></i>Дальше — номер по порядку от входа в коридор</li></ul>
<p class="muted cab-note">Пример для группы РИ. По данным <a href="https://privet.urfu.ru/navigation" target="_blank" rel="noopener">«Навигатора первокурсника»<span class="sr"> (откроется в новой вкладке)</span></a> и сайта программ УрФУ.</p>
</section>
<section class="card cab-svc" aria-labelledby="csv-h">
<div class="cab-h"><h3 id="csv-h">Сервисы УрФУ</h3></div>
<ul>
<li><a href="https://istudent.urfu.ru/" target="_blank" rel="noopener"><b>Личный кабинет студента</b><span>istudent.urfu.ru — зачётка, справки, физкультура</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://id.urfu.ru/" target="_blank" rel="noopener"><b>Учётная запись</b><span>id.urfu.ru — вход во все сервисы и Wi-Fi</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://pay.urfu.ru/" target="_blank" rel="noopener"><b>Оплата</b><span>pay.urfu.ru — общежитие, медосмотр</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://programs.edu.urfu.ru/" target="_blank" rel="noopener"><b>Моя программа</b><span>Учебный план и преподаватели</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://youthscience.urfu.ru/" target="_blank" rel="noopener"><b>Молодёжная наука</b><span>Конкурсы и конференции</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://elar.urfu.ru/" target="_blank" rel="noopener"><b>Электронный архив</b><span>Статьи, ВКР, газета университета</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
</ul>
</section>
</div><div class="cab-col">
<section class="card cab-job" aria-labelledby="cj-h">
<div class="cab-h"><h3 id="cj-h">Практика и работа</h3></div>
<p class="muted" style="margin-top:8px">У ИРИТ-РтФ больше 50 компаний-партнёров. Они берут на практику и стажировки, ведут спецкурсы и проекты.</p>
<div class="cab-co"><span>УЦСБ</span><span>Naumen</span><span>СКБ Контур</span><span>Сбер</span><span>Прософт-Системы</span><span>JetStyle</span><span>Targem Games</span><span>Artsofte</span><span>Yandex Cloud</span><span>НПО автоматики</span></div>
<ul class="cab-ev"><li><b>Ярмарка вакансий</b><span>Компании ищут стажёров и выпускников</span></li><li><b>Выставка проектов</b><span>Студенческие проекты для партнёров</span></li></ul>
<p class="muted cab-note">На примере ИРИТ-РтФ — по данным <a href="https://programs.edu.urfu.ru/ru/9797/pages/employers/" target="_blank" rel="noopener">сайта образовательных программ УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>
<section class="card cab-evs nw-afisha" aria-labelledby="cev-h">
<div class="cab-h"><h3 id="cev-h">Конкурсы и олимпиады</h3><a href="Events.dc.html">Все события →</a></div>
<ul data-prune><li data-end="2026-10-25"><b class="nw-d">25<span>окт</span></b><div><b>Твой ход</b><span class="muted">Всероссийский студенческий проект</span></div></li><li data-end="2026-10-29"><b class="nw-d">29<span>окт</span></b><div><b>Кейс-чемпионат «Лига твоего имени»</b><span class="muted">Успей подать заявку</span></div></li><li data-end="2026-11-01"><b class="nw-d">1<span>ноя</span></b><div><b>Премия губернатора для молодых учёных</b><span class="muted">Приём заявок</span></div></li><li data-end="2026-11-10"><b class="nw-d">10<span>ноя</span></b><div><b>Я — профессионал</b><span class="muted">Олимпиада для студентов</span></div></li><li data-end="2027-01-19"><b class="nw-d">19<span>янв</span></b><div><b>Изумруд.Студент</b><span class="muted">Олимпиада УрФУ</span></div></li></ul><p class="muted cab-note" data-prune-empty hidden>Новые конкурсы — в <a href="Events.dc.html">календаре событий</a>.</p>
</section>
<section class="card cab-links" aria-labelledby="cl-h">
<div class="cab-h"><h3 id="cl-h">Быстро</h3></div>
<ul>
<li><a href="Help.dc.html"><b>Центр помощи</b><span>Медосмотр, Wi-Fi, справки</span></a></li>
<li><a href="Science.dc.html#stud-h"><b>Попасть в науку</b><span>Молодёжные лаборатории</span></a></li>
<li><a href="Dorms.dc.html#settle-h"><b>Как заселиться</b><span>Медкомиссия, регистрация, ордер</span></a></li>
<li><a href="tel:88002225571"><b>Горячая линия для студентов</b><span>8-800-222-55-71 · доб. 1 — права, доб. 2 — психолог</span></a></li>
</ul>
</section>
</div></div>
</section>
</div>
</main>'''


LOGIC = '''<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
const DL0 = [['Лабораторная работа №3', 'Программирование', 2], ['Домашнее задание', 'Математический анализ', 4], ['Эссе', 'Основы российской государственности', 8], ['Контрольная работа', 'Физика', 12], ['Проект: защита прототипа', 'Проектная деятельность', 19]];
const DORMS = __DORMS__, REQ = __REQ__, STIP = __STIP__, BRS = __BRS__, FIRST = __FIRST__;
const load = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v === null || v === undefined ? d : v; } catch (e) { return d; } };
const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
if (!this.state) this.state = { rt: 'study', n: 1, reqs: load('urfu-cab-reqs', []), dorm: load('urfu-cab-dorm', 8), dlDone: load('urfu-dl', []), fwDone: load('urfu-fw', [0, 1]), stip: load('urfu-cab-stip', 'first') };
const s = this.state;
const dlDone = s.dlDone;
const tday = new Date(); tday.setHours(0, 0, 0, 0);
const MNs = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
const plural = (k, a, b, c) => (k % 10 === 1 && k % 100 !== 11) ? a : (k % 10 >= 2 && k % 10 <= 4 && (k % 100 < 12 || k % 100 > 14)) ? b : c;
const dls = DL0.map(([t, s2, k], i) => { const dd = new Date(tday.getTime() + k * 864e5); const done = dlDone.indexOf(i) !== -1;
  return { t, s: s2, done: String(done), cls: 'cab-dli' + (done ? ' is-done' : (k <= 3 ? ' is-soon' : '')), when: done ? 'готово' : (k === 1 ? 'завтра' : 'через ' + k + ' ' + plural(k, 'день', 'дня', 'дней')) + ' · ' + dd.getDate() + ' ' + MNs[dd.getMonth()],
    tog: () => { const nx = done ? dlDone.filter(x => x !== i) : dlDone.concat(i); save('urfu-dl', nx); this.setState({ dlDone: nx }); } }; });
const left = DL0.length - dlDone.length;
const fw = s.fwDone;
const first = FIRST.map(([t, d], i) => { const done = fw.indexOf(i) !== -1;
  return { t, s: d, done: String(done), cls: 'cab-dli' + (done ? ' is-done' : ''), tog: () => { const nx = done ? fw.filter(x => x !== i) : fw.concat(i); save('urfu-fw', nx); this.setState({ fwDone: nx }); } }; });
const fwN = fw.filter(i => i < FIRST.length).length;
let g = ''; try { g = localStorage.getItem('urfu-group') || ''; } catch (e) {}
// пример расписания — как на странице «Расписание»
const T = [['08:30','10:00'],['10:15','11:45'],['12:00','13:30'],['14:15','15:45'],['16:00','17:30']];
const PLAN = [
[[0,'Математический анализ','Лекция'],[1,'Программирование','Практика'],[2,'Английский язык','Практика']],
[[1,'Физика','Лекция'],[2,'Алгоритмы и структуры данных','Лабораторная'],[3,'Физическая культура','Практика']],
[[0,'Основы российской государственности','Семинар'],[1,'Математический анализ','Практика']],
[[0,'Программирование','Лекция'],[1,'Программирование','Лабораторная'],[2,'Физика','Практика'],[3,'История России','Лекция']],
[[1,'Алгебра и геометрия','Лекция'],[2,'Алгебра и геометрия','Практика']], [], []];
const DN = ['понедельник','вторник','среду','четверг','пятницу','субботу','воскресенье'];
const wd = (new Date().getDay() + 6) % 7; let day = wd, k = 0;
while (!PLAN[day].length && k < 7) { day = (day + 1) % 7; k++; }
const rub = n => Math.round(n).toLocaleString('ru-RU') + ' ₽';
const rub1 = n => n.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' ₽';
const D = DORMS[s.dorm] || DORMS[0];
const ST = STIP.find(x => x[0] === s.stip) || STIP[0];
const RN = {}; REQ.forEach(r => RN[r[0]] = r[1]);
const order = () => {
  const n = Math.min(5, Math.max(1, parseInt(s.n, 10) || 1));
  const d = new Date(); const dd = String(d.getDate()).padStart(2, '0') + '.' + String(d.getMonth() + 1).padStart(2, '0');
  const reqs = [{ t: s.rt, c: n, d: dd }].concat(s.reqs).slice(0, 5); save('urfu-cab-reqs', reqs); this.setState({ reqs });
};
// баллы: оценка по шкале УрФУ и сколько до следующей
const grade = p => p >= 80 ? ['отлично', 's5', '', 0] : p >= 60 ? ['хорошо', 's4', 'до «отлично»', 80 - p] : p >= 40 ? ['удовлетворительно', 's3', 'до «хорошо»', 60 - p] : ['пока не набрано', 's2', 'до зачёта', 40 - p];
const brs = BRS.map(([t, p]) => { const [gname, cls, to, n] = grade(p); return { t, p, g: gname, cls: 'cab-bli ' + cls, next: n ? to + ' — ' + n + ' ' + plural(n, 'балл', 'балла', 'баллов') : 'высшая оценка' }; });
const pairsN = PLAN[day].length;
const ntPass = tday.getMonth() === 9 && tday.getDate() <= 26;
const ntReady = s.reqs.length > 1;
const nts = [
  ntPass ? { t: 'QR-код работает только до 26 октября', d: 'Успейте получить пластиковый пропуск в дирекции института.', href: '#cp-h', lt: 'Мой пропуск', cls: 'cab-nti is-new' } : null,
  ntReady ? { t: 'Справка готова', d: 'Заберите в дирекции института или скачайте в кабинете.', href: '#cr-h', lt: 'К справкам', cls: 'cab-nti is-new' } : null,
  { t: 'Снова очные занятия', d: 'С 15 октября занятия идут в аудиториях — гибридный формат закончился.', href: 'News.dc.html', lt: 'Новости', cls: 'cab-nti is-new' },
  { t: 'Расписание на следующую неделю', d: 'Пример: в четверг пара по физике перенесена на 12:00.', href: 'Schedule.dc.html', lt: 'Расписание', cls: 'cab-nti' },
  { t: 'Горячая линия для студентов', d: 'Права студента и психологическая помощь — бесплатно по России.', href: 'Help.dc.html#hl-h', lt: 'Подробнее', cls: 'cab-nti' }
].filter(Boolean);
const lo = ST[2] - D[1];
return {
  dls, dlLeft: left ? 'Осталось: ' + left : 'Всё сделано!', nts, ntN: String(nts.filter(x => x.cls.indexOf('is-new') !== -1).length),
  hello: g ? 'Группа ' + g + ' · это ваш кабинет: расписание, баллы, стипендия, справки и общежитие в одном месте.' : 'Это ваш кабинет: расписание, баллы, стипендия, справки и общежитие в одном месте.',
  sumPairs: String(pairsN), sumPairsL: plural(pairsN, 'пара', 'пары', 'пар') + (day === wd ? ' сегодня' : ' в ' + DN[day]),
  sumDl: String(left), sumDlL: plural(left, 'дедлайн', 'дедлайна', 'дедлайнов') + ' впереди',
  sumStip: rub(ST[2]), sumFirst: fwN + ' из ' + FIRST.length,
  dayTitle: day === wd ? 'Сегодня' : 'Сегодня пар нет · в ' + DN[day],
  pairs: PLAN[day].map(([i, t, kind]) => ({ from: T[i][0], to: T[i][1], t, kind })),
  brs,
  stips: STIP.map(([key, n]) => ({ n, on: String(key === ST[0]), pick: () => { save('urfu-cab-stip', key); this.setState({ stip: key }); } })),
  stipSum: rub1(ST[2]), stipK: 'С уральским коэффициентом 1,15 — около ' + rub(ST[2] * 1.15), stipNote: ST[3], stipShort: rub(ST[2]),
  leftover: (lo < 0 ? '− ' : '') + rub(Math.abs(lo)),
  first, firstLeft: 'Готово: ' + fwN + ' из ' + FIRST.length, firstPct: Math.round(fwN / FIRST.length * 100),
  reqTypes: REQ.map(([key, n]) => ({ n, on: String(key === s.rt), pick: () => this.setState({ rt: key }) })),
  reqN: s.n, setN: e => this.setState({ n: e.target.value }), order,
  hasReq: s.reqs.length > 0, noReq: s.reqs.length === 0,
  reqs: s.reqs.map((q, i) => ({ n: RN[q.t], c: q.c, d: 'заказана ' + q.d, st: i === 0 ? 'Принята' : 'Готова' })),
  clearReq: () => { save('urfu-cab-reqs', []); this.setState({ reqs: [] }); },
  dorms: DORMS.map((x, i) => ({ n: x[0], on: String(i === s.dorm), pick: () => { save('urfu-cab-dorm', i); this.setState({ dorm: i }); } })),
  winter: rub(D[1]), summer: rub(D[2])
};
}
}
</script>'''

CSS = '''
/* Кабинет v3 */
.cab-head .wrap{padding-bottom:8px}
.cab-sum{list-style:none;margin:22px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;max-width:860px}
.cab-sum li{display:flex;flex-direction:column;gap:2px;padding:12px 16px;border-radius:14px;background:#FFFFFF;border:2px solid var(--ink)}
.cab-sum b{font-family:var(--narrow);font-size:30px;line-height:1.05}
.cab-sum span{font-size:14px;color:var(--muted)}
.cab-nav{display:flex;flex-wrap:wrap;gap:8px;padding-top:26px}
.cab-nav a{display:inline-flex;align-items:center;min-height:40px;padding:6px 16px;border-radius:999px;border:2px solid var(--ink);color:var(--ink);font-weight:600;text-decoration:none;background:#FFFFFF}
.cab-nav a:hover{background:var(--ink);color:#FFFFFF}
.cab{display:block;padding-top:24px;padding-bottom:72px}
.cab-grp{margin-top:40px;scroll-margin-top:20px}
.cab-gh{font-family:var(--narrow);font-size:40px;line-height:1.05;margin:0 0 16px;display:flex;align-items:center;gap:14px}
.cab-gh::after{content:"";flex:1;height:3px;border-radius:3px;background:linear-gradient(90deg,var(--rhodonite) 0 25%,var(--gold) 25% 50%,var(--malachite) 50% 75%,var(--amethyst) 75%)}
.cab-cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;align-items:start}
.cab-col{display:flex;flex-direction:column;gap:20px;min-width:0}
.cab-h h2.cab-h2s,.cab-h h3{font-family:var(--narrow);font-size:26px;line-height:1.1;margin:0}
.cab-sub{margin:22px 0 0;font-size:17px}
.cab-lead{margin-top:8px;font-size:15px}
.cab-nts{display:grid !important;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.cab-bl{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-direction:column;gap:12px}
.cab-blt{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.cab-blt em{font-style:normal;font-family:var(--narrow);font-weight:700;font-size:24px;white-space:nowrap}
.cab-blt small{font-family:'IBM Plex Sans',sans-serif;font-size:13px;font-weight:500;color:var(--muted)}
.cab-bar{position:relative;height:10px;border-radius:6px;background:var(--limestone);margin-top:6px;overflow:hidden}
.cab-bar::before,.cab-bar::after{content:"";position:absolute;top:0;bottom:0;width:2px;background:#FFFFFF;z-index:1}
.cab-bar::before{left:60%}.cab-bar::after{left:80%}
.cab-bar i{display:block;height:100%;border-radius:6px;background:var(--bc,var(--amethyst))}
.cab-bli.s5{--bc:#00A37A}.cab-bli.s4{--bc:var(--amethyst)}.cab-bli.s3{--bc:#E89B00}.cab-bli.s2{--bc:var(--rhodonite)}
.cab-blg{display:flex;justify-content:space-between;gap:10px;margin-top:4px;font-size:14px;flex-wrap:wrap}
.cab-gr{font-weight:600}
.cab-bli.s2 .cab-gr{color:#B0124F}
.cab-blg small{color:var(--muted);font-size:14px}
.cab-scale{list-style:none;margin:16px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;font-size:13px}
.cab-scale li{display:flex;flex-direction:column;padding:8px 10px;border-radius:10px;background:var(--limestone);border-top:4px solid var(--bc)}
.cab-scale .s5{--bc:#00A37A}.cab-scale .s4{--bc:var(--amethyst)}.cab-scale .s3{--bc:#E89B00}.cab-scale .s2{--bc:var(--rhodonite)}
.cab-scale b{font-size:15px}
.cab-sopt{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.cab-sopt button{font:inherit;font-size:14px;font-weight:600;min-height:40px;padding:6px 14px;border-radius:999px;border:2px solid var(--line-strong);background:#FFFFFF;color:var(--ink);cursor:pointer}
.cab-sopt button[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#FFFFFF}
.cab-sopt button:focus-visible{outline:3px solid var(--amethyst);outline-offset:2px}
.cab-sres{margin-top:16px;padding:18px 20px;border-radius:16px;background:var(--ink);color:#FFFFFF}
.cab-sres .muted{color:var(--on-dark-muted)}
.cab-sbig{font-family:var(--narrow);font-size:48px;font-weight:700;line-height:1;color:var(--gold)}
.cab-sbig small{font-family:'IBM Plex Sans',sans-serif;font-size:16px;font-weight:500;color:#FFFFFF}
.cab-scf{margin-top:8px;font-weight:600}
.cab-cmp{display:flex;flex-direction:column;gap:6px;margin-top:14px}
.cab-cmp div{display:flex;justify-content:space-between;gap:10px;padding:10px 14px;border-radius:12px;background:var(--limestone)}
.cab-cmp b{font-family:var(--narrow);font-size:22px}
.cab-cmp .is-res{background:var(--gold-soft);border:2px solid var(--gold)}
.cab-steps{list-style:none;margin:14px 0 0;padding:0;counter-reset:st;display:flex;flex-direction:column}
.cab-steps li{position:relative;display:flex;flex-direction:column;padding:0 0 16px 44px;counter-increment:st}
.cab-steps li::before{content:counter(st);position:absolute;left:0;top:0;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:14px;background:#FFFFFF;border:2px solid var(--line-strong);color:var(--muted)}
.cab-steps li::after{content:"";position:absolute;left:15px;top:32px;bottom:2px;width:2px;background:var(--line)}
.cab-steps li:last-child::after{display:none}
.cab-steps li.is-done::before{content:"✓";background:#00A37A;border-color:#00A37A;color:#FFFFFF}
.cab-steps li.is-now::before{background:var(--gold);border-color:var(--ink);color:var(--ink)}
.cab-steps li.is-now b::after{content:" · сейчас";color:#8A5A00;font-weight:600;font-size:14px}
.cab-steps span{font-size:14px;color:var(--muted)}
.cab-warn{margin-top:4px;padding:12px 14px;border-radius:12px;background:#FFE9F1;border-left:4px solid var(--rhodonite);font-size:15px}
.cab-prog{height:12px;border-radius:8px;background:var(--limestone);margin-top:14px;overflow:hidden}
.cab-prog i{display:block;height:100%;background:linear-gradient(90deg,var(--amethyst),var(--rhodonite));border-radius:8px;transition:width .3s var(--ease)}
.cab-fl{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.cab-room{display:flex;gap:4px;margin-top:10px;font-family:var(--narrow);font-size:40px;font-weight:700;line-height:1}
.cab-room span{padding:6px 12px;border-radius:10px}
.cab-room .r1,.cab-rl .r1{background:#FFD9E7}.cab-room .r2,.cab-rl .r2{background:#FFF0C2}.cab-room .r3,.cab-rl .r3{background:#E3D6FF}
.cab-rl{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px;font-size:15px}
.cab-rl li{display:flex;gap:10px;align-items:center}
.cab-rl i{flex:0 0 18px;height:18px;border-radius:5px}
@media (max-width:900px){.cab-cols{grid-template-columns:minmax(0,1fr)}.cab-sum{grid-template-columns:repeat(2,minmax(0,1fr))}.cab-fl{grid-template-columns:minmax(0,1fr)}}
@media (max-width:520px){.cab-dorms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.cab-dorms .chip{white-space:normal;text-align:left;justify-content:flex-start;line-height:1.25;padding:6px 10px;font-size:13px}.cab .card{padding:20px 16px}.cab-gh{font-size:32px}.cab-scale{grid-template-columns:repeat(2,minmax(0,1fr))}.cab-sbig{font-size:40px}.cab-sum b{font-size:26px}}
/* /Кабинет v3 */
'''


def main():
    base = open('NotFound.dc.html', encoding='utf-8').read()
    head, rest = base.split('<main', 1)
    foot = rest[rest.index('</main>') + len('</main>'):]
    foot = foot[:foot.index('<script type="text/x-dc"')]
    tail = base[base.index('<script src="dc-lite.js">'):]
    title = 'Кабинет студента (демо) — УрФУ'
    desc = 'Демо-кабинет студента УрФУ: пары и баллы, стипендия по суммам 2026 года, справки, пропуск, общежитие и чек-лист первокурсника.'
    head = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*"', lambda m: m.group(1) + desc + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + title + '"', head)
    head = head.replace('NotFound.dc.html"', 'Cabinet.dc.html"')
    head = head.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
    dump = lambda x: json.dumps(x, ensure_ascii=False)
    logic = (LOGIC.replace('__DORMS__', dump(DORMS)).replace('__REQ__', dump(REQ)).replace('__STIP__', dump(STIP))
             .replace('__BRS__', dump(BRS)).replace('__FIRST__', dump(FIRST)))
    open('Cabinet.dc.html', 'w', encoding='utf-8', newline='').write(head + main_html() + foot + logic + '\n' + tail)
    css = open('site.css', encoding='utf-8').read()
    if '/* Кабинет v3 */' in css:
        a = css.index('\n/* Кабинет v3 */')
        b = css.index('/* /Кабинет v3 */', a) + len('/* /Кабинет v3 */\n')
        css = css[:a] + css[b:]
    open('site.css', 'w', encoding='utf-8', newline='').write(css.rstrip('\n') + '\n' + CSS)
    print('Cabinet.dc.html готов')


if __name__ == '__main__':
    main()
