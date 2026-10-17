"""Страница «Поступление»: календарь приёма, способы подачи, списки, особые права, стоимость.
Даты — из календаря приёма УрФУ 2026 (urfu.ru/ru/applicant/docs-abiturient/kalendar-priema/).
Цены программ берутся из каталога (Catalog.dc.html), чтобы цифры совпадали.
Запуск: python make_admission.py (можно повторно; блок между <!-- adm --> и <!-- /adm -->)."""
import os, re, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CAL = 'https://web.archive.org/web/20260831155039/https://urfu.ru/ru/applicant/docs-abiturient/kalendar-priema/'

BUDGET = [
    ('20 июня', 'Старт приёма документов', 'Через Госуслуги, личный кабинет абитуриента или лично.'),
    ('1–23 июля', 'Экзамены УрФУ', 'Тесты для тех, кому можно сдавать их вместо ЕГЭ (например, после колледжа), и творческие экзамены.'),
    ('15 июля', 'Конец подачи с экзаменами УрФУ', 'И для творческих направлений: журналистика, дизайн, архитектура, спорт и другие.'),
    ('25 июля', 'Конец подачи по ЕГЭ', 'До 17:00 по Екатеринбургу.'),
    ('1 августа', 'Согласие: квоты и без экзаменов', 'Приоритетный этап — особая, отдельная и целевая квоты, олимпиадники. Приказ 3 августа.'),
    ('5 августа', 'Согласие: основной этап', 'До 14:00. Приказ о зачислении — 7 августа.'),
    ('9 августа', 'Согласие: дополнительный этап', 'На оставшиеся места. Приказ — 11 августа.'),
]
PAID = [
    ('20 июня – 20 августа', 'Приём документов по ЕГЭ', 'С экзаменами УрФУ и на творческие направления — до 15 августа.'),
    ('21 августа', 'Последний день договора', 'Договор об обучении нужно заключить до 17:00.'),
    ('25 августа', 'Приказ о зачислении', 'На места с оплатой обучения.'),
    ('1 сентября – 22 октября', 'Осенний набор', 'Дополнительный приём на платное: договор до 28 октября, приказ 30 октября.'),
]


def tl(items):
    return ''.join(f'<li><span class="tl-d">{d}</span><b>{t}</b><span class="tl-n">{n}</span></li>' for d, t, n in items)


def progs():
    c = open('Catalog.dc.html', encoding='utf-8').read()
    c = c[c.index('const ALL_PROGS'):]
    c = c[:c.index('];')]
    out = []
    for line in c.split('\n'):
        n = re.search(r"name:'([^']+)'", line); i = re.search(r"inst:'([^']+)'", line)
        p = re.search(r"price:'(\d[\d ]*) ₽'", line)
        if line.startswith('{name') and n and p:
            out.append((n.group(1), i.group(1) if i else '', int(p.group(1).replace(' ', ''))))
    out.sort(key=lambda x: x[0])
    return out


def block():
    ps = progs()
    lopts = ''.join(f'<option value="{html.escape(n)}">{html.escape(n)}</option>' for n, i, v in ps)
    opts = ''.join(f'<option value="{html.escape(n)}" data-price="{v}">{html.escape(n)} — {html.escape(i)}</option>' for n, i, v in ps)
    return f'''<!-- adm -->
<section id="calendar" class="adm-sec" aria-labelledby="cal-h">
<h2 id="cal-h">Календарь приёма</h2>
<p class="muted adm-lead">Даты приёма-2026 в бакалавриат и специалитет. Правила следующего года УрФУ публикует зимой: на приём-2026 — до 20 января. Сроки от года к году меняются мало.</p>
<div class="tl-cols">
<div class="tl-col tl-b"><h3>На бюджет</h3><ol class="tl">{tl(BUDGET)}</ol></div>
<div class="tl-col tl-p"><h3>На платное</h3><ol class="tl">{tl(PAID)}</ol></div>
</div>
<p class="muted adm-src">Источник: <a href="{CAL}" target="_blank" rel="noopener">календарь приёма УрФУ 2026<span class="sr"> (откроется в новой вкладке)</span></a>. Время — екатеринбургское.</p>
</section>

<section id="apply" class="adm-sec" aria-labelledby="apply-h">
<h2 id="apply-h">Как подать документы</h2>
<div class="g3 adm-ways">
<div class="card way"><span class="way-i" aria-hidden="true">1</span><h3>Через Госуслуги</h3><p class="muted">Сервис «Поступление в вуз онлайн»: заявление, документы и согласие — без поездки в Екатеринбург.</p></div>
<div class="card way"><span class="way-i" aria-hidden="true">2</span><h3>В личном кабинете абитуриента</h3><p class="muted">На сайте приёмной комиссии УрФУ. Там же видно своё место в конкурсных списках.</p></div>
<div class="card way"><span class="way-i" aria-hidden="true">3</span><h3>Лично</h3><p class="muted">Приёмная комиссия: Екатеринбург, ул. Мира, 19, аудитория ГУК-100. <a href="tel:+73433754474">+7 (343) 375-44-74</a>, <a href="mailto:priem@urfu.ru">priem@urfu.ru</a></p></div>
</div>
</section>

<section id="lists" class="adm-sec" aria-labelledby="lists-h">
<h2 id="lists-h">Списки и согласие — как это работает</h2>
<div class="g2 adm-two">
<div class="card"><h3>Конкурсные списки</h3><p class="muted">После подачи вы попадаете в список каждой выбранной программы. Списки обновляются каждый день, своё место видно в личном кабинете. Можно выбрать до 5 направлений и расставить программы по приоритету.</p>
<p style="margin-top:14px"><a href="Catalog.dc.html">Сравнить свою сумму с проходными баллами прошлых лет →</a></p></div>
<div class="card"><h3>Согласие на зачисление</h3><p class="muted">Согласие подтверждает, на какую программу вы идёте. Подайте его до 14:00 в день этапа: 1 августа — квоты и олимпиадники, 5 августа — основной этап, 9 августа — дополнительный. Без согласия на бюджет не зачисляют.</p>
<p style="margin-top:14px"><a href="#calendar">Смотреть даты этапов →</a></p></div>
</div>
<div class="card lf" role="search" aria-labelledby="lf-h">
<div class="lf-in"><h3 id="lf-h">Найди себя в списках</h3>
<p class="muted">В списках вместо фамилии — СНИЛС или уникальный код из личного кабинета абитуриента.</p>
<form class="lf-form" novalidate>
<label for="lf-c">СНИЛС или код</label><input id="lf-c" class="input" inputmode="numeric" autocomplete="off" placeholder="Например, 1234567" aria-describedby="lf-err">
<label for="lf-p">Программа</label><select id="lf-p" class="cost-sel">{lopts}</select>
<button class="btn" type="submit">Найти</button>
<p id="lf-err" class="lf-err" role="alert"></p>
</form></div>
<div class="lf-out" aria-live="polite"><p class="lf-empty">Здесь появится ваше место в списке, баллы и подано ли согласие.</p></div>
</div>
<p class="muted adm-src">Это демо: ответ — пример того, как будет выглядеть поиск. Настоящие списки появятся с 20 июня, когда начнётся приём.</p>
</section>

<section id="benefits" class="adm-sec" aria-labelledby="ben-h">
<h2 id="ben-h">Особые права</h2>
<p class="muted adm-lead">Кому положены отдельные места или зачисление без экзаменов — по закону об образовании.</p>
<div class="g4 adm-ben">
<div class="card ben"><b>Без экзаменов</b><p class="muted">Победители и призёры заключительного этапа Всероссийской олимпиады школьников. Победителям и призёрам олимпиад из перечня — по решению вуза и по профилю программы.</p></div>
<div class="card ben"><b>Особая квота</b><p class="muted">Для детей-инвалидов, инвалидов I и II групп и с детства, детей-сирот. Не меньше 10% бюджетных мест.</p></div>
<div class="card ben"><b>Отдельная квота</b><p class="muted">Для участников специальной военной операции и их детей. Тоже не меньше 10% бюджетных мест.</p></div>
<div class="card ben"><b>Целевое обучение</b><p class="muted">Учёба бесплатно по договору с компанией или ведомством — и работа у него после выпуска. Конкурс отдельный.</p></div>
</div>
</section>

<section id="cost" class="adm-sec" aria-labelledby="cost-h">
<h2 id="cost-h">Сколько стоит платное</h2>
<div class="cost card">
<div class="cost-in"><label for="cost-p">Программа</label>
<select id="cost-p" class="cost-sel">{opts}</select>
<p class="muted" style="font-size:14px;margin-top:10px">Цены — из каталога программ, {len(ps)} программ с известной ценой.</p></div>
<dl class="cost-out" aria-live="polite">
<div><dt>За год</dt><dd id="cost-y">—</dd></div>
<div><dt>За семестр</dt><dd id="cost-s">—</dd></div>
<div><dt>За 4 года</dt><dd id="cost-t">—</dd></div>
</dl>
</div>
<p class="muted adm-src">Цена может расти каждый год вместе с инфляцией. УрФУ даёт скидки отдельным категориям студентов — условия в приказе о скидках. Ещё есть образовательный кредит с господдержкой: 3% годовых, платить начинают после выпуска.</p>
</section>

<section id="year" class="adm-sec" aria-labelledby="year-h">
<h2 id="year-h">Приём-2026 в цифрах</h2>
<div class="g4 yr">
<div class="yr-c"><b>49 832</b><span>заявления на бюджет</span></div>
<div class="yr-c"><b>+7,5 тыс.</b><span>заявлений больше, чем в 2025 году</span></div>
<div class="yr-c"><b>1 065</b><span>заявлений по целевой квоте — на 40% больше, чем мест</span></div>
<div class="yr-c"><b>IT</b><span>и инженерные программы — самый высокий спрос</span></div>
</div>
<p class="muted adm-src">По данным ОТВ, 27 июля 2026. <a href="Article.dc.html">Подробнее об итогах приёма →</a></p>
</section>

<section id="school" class="adm-sec" aria-labelledby="school-h">
<h2 id="school-h">Ещё в школе? Начни сейчас</h2>
<p class="muted adm-lead">Олимпиады, кружки и турниры УрФУ. Победители и призёры олимпиад, которые УрФУ проводит сам, получают +4 балла при поступлении в УрФУ.</p>
<div class="sch">
<div class="sch-main card"><span class="sch-k">Олимпиада УрФУ</span><h3>«Изумруд»</h3><p>Отборочный этап — с 1 сентября 2026 по 19 января 2027 года. Регистрация открыта.</p><a class="btn" href="https://dovuz.urfu.ru/olymps/izumrud" target="_blank" rel="noopener">Зарегистрироваться<span class="sr"> (откроется в новой вкладке)</span></a></div>
<ul class="sch-list">
<li><b class="sch-d">окт–май</b><div><b>Школа юного биолога и Школа юного химика</b><span>Занятия весь учебный год · набор шёл до 4 октября</span></div></li>
<li><b class="sch-d">17 окт</b><div><b>Метрологический хакатон</b><span>Регистрация открыта</span></div></li>
<li><b class="sch-d">ноя–дек</b><div><b>Уральский турнир юных биологов</b><span>bioturnir.ru</span></div></li>
<li><b class="sch-d">27 фев</b><div><b>Фестиваль естествознания</b><span>Подробности позже</span></div></li>
<li><b class="sch-d">апр</b><div><b>День открытых дверей, «Химический бой», конференция школьников</b><span>Институт естественных наук и математики</span></div></li>
</ul>
</div>
<div class="sch-more"><span>Ещё кружки:</span><span class="chip">Школа юных математиков</span><span class="chip">Школа олимпиадного программирования</span><span class="chip">Мастер-классы по биотехнологии</span><span class="chip">Химический диктант</span></div>
<p class="muted adm-src">Источник: <a href="https://insma.urfu.ru/shkolniku/" target="_blank" rel="noopener">раздел «Школьнику» ИЕНиМ УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>, сезон 2026/27.</p>
</section>
<!-- /adm -->'''


CSS = '''
/* Поступление: календарь, способы подачи, особые права, стоимость */
.adm-sec{margin-top:72px}
.adm-lead{margin-top:8px;max-width:760px;font-size:17px}
.adm-src{margin-top:14px;font-size:14px;max-width:820px}
.tl-cols{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:20px;margin-top:24px}
.tl-col{border-radius:20px;padding:24px 26px;background:#FFFFFF;border:1px solid var(--limestone)}
.tl-col h3{font-size:20px;display:flex;align-items:center;gap:10px}
.tl-col h3::before{content:"";width:12px;height:12px;border-radius:4px;background:var(--c)}
.tl-b{--c:var(--malachite)}.tl-p{--c:var(--gold)}
.tl{list-style:none;margin:18px 0 0;padding:0 0 0 22px;position:relative}
.tl::before{content:"";position:absolute;left:5px;top:8px;bottom:8px;width:2px;background:var(--limestone)}
.tl li{position:relative;padding:0 0 18px;display:flex;flex-direction:column;gap:2px}
.tl li:last-child{padding-bottom:0}
.tl li::before{content:"";position:absolute;left:-22px;top:5px;width:12px;height:12px;border-radius:50%;background:#FFFFFF;border:3px solid var(--c)}
.tl-d{font-family:var(--narrow);font-weight:700;font-size:19px;color:var(--ink)}
.tl-n{color:var(--muted);font-size:15px;line-height:1.5}
.adm-ways,.adm-ben,.adm-two{margin-top:24px}
.way h3{margin-top:14px;font-size:19px}.way p{margin-top:8px}
.way-i{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:12px;background:var(--amethyst);color:#FFFFFF;font-weight:700;font-family:var(--narrow);font-size:20px}
.adm-two h3{font-size:20px}.adm-two p.muted{margin-top:10px}
.ben{box-shadow:inset 0 4px 0 var(--rhodonite)}
.ben b{font-family:var(--narrow);font-size:20px}.ben p{margin-top:8px;font-size:15px}
.cost{margin-top:24px;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:28px;align-items:center;padding:28px}
.cost label{display:block;font-weight:600;margin-bottom:8px}
.cost-sel{width:100%;min-height:48px;border-radius:12px;border:2px solid var(--limestone);padding:0 12px;font:inherit;font-size:16px;background:#FFFFFF;color:var(--ink)}
.cost-sel:focus-visible{outline:3px solid var(--amethyst);outline-offset:2px}
.cost-out{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0}
.cost-out div{background:var(--gold-soft);border-radius:14px;padding:14px 16px}
.cost-out dt{font-size:14px;color:var(--muted)}
.cost-out dd{margin:4px 0 0;font-family:var(--narrow);font-weight:700;font-size:22px;color:var(--ink);white-space:nowrap}
.lf{margin-top:20px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px;padding:28px}
.lf h3{font-size:22px;font-family:var(--narrow)}
.lf-in>p{margin-top:6px}
.lf-form{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.lf-form label{font-weight:600}
.lf-form .input{width:100%}
.lf-form .btn{align-self:flex-start;margin-top:6px}
.lf-err{color:var(--a4,#A63A3A);font-weight:600;font-size:15px}
.lf-err:empty{display:none}
.lf-out{border-radius:18px;background:var(--ink);color:#FFFFFF;padding:24px;display:flex;flex-direction:column;justify-content:center;min-height:220px}
.lf-empty{color:var(--on-dark-muted)}
.lf-pos{font-family:var(--narrow);font-size:56px;font-weight:700;line-height:1}
.lf-pos small{font-size:20px;color:var(--on-dark-muted);font-weight:500}
.lf-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.lf-row span{background:rgba(255,255,255,.12);border-radius:999px;padding:4px 12px;font-size:14px}
.lf-v{margin-top:14px;font-weight:600}
.lf-demo{margin-top:10px;font-size:13px;color:var(--on-dark-muted)}
.yr{margin-top:24px}
.yr-c{border-top:4px solid var(--amethyst);padding-top:14px;display:flex;flex-direction:column;gap:4px}
.yr-c b{font-family:var(--narrow);font-size:40px;line-height:1.05;color:var(--ink)}
.yr-c span{color:var(--muted);font-size:15px}
.sch{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:20px;margin-top:24px;align-items:start}
.sch-main{background:linear-gradient(135deg,#0B7A63,#14523F);color:#FFFFFF;border:0;display:flex;flex-direction:column;gap:10px;padding:28px}
.sch-main h3{font-family:var(--narrow);font-size:40px;color:#FFFFFF}
.sch-main .btn{align-self:flex-start;background:#FFFFFF;color:var(--ink);margin-top:8px}
.sch-k{font-size:14px;font-weight:600;color:#CFF5EA}
.sch-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.sch-list li{display:flex;gap:16px;align-items:center;background:#FFFFFF;border:1px solid var(--line);border-radius:16px;padding:14px 18px}
.sch-list li div{display:flex;flex-direction:column}
.sch-list li div span{font-size:14px;color:var(--muted)}
.sch-d{flex:0 0 84px;font-family:var(--narrow);font-size:18px;color:var(--amethyst)}
.sch-more{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:16px}
.sch-more>span:first-child{font-weight:600;margin-right:4px}
.sch-more .chip{cursor:default}
@media (max-width:900px){.lf,.sch{grid-template-columns:1fr}}
@media (max-width:900px){.tl-cols,.cost{grid-template-columns:1fr}}
@media (max-width:520px){.cost-out{grid-template-columns:1fr}.cost{padding:20px}}
'''


def main():
    p = 'Admission.dc.html'
    s = open(p, encoding='utf-8').read()
    b = block()
    if '<!-- adm -->' in s:
        s = re.sub(r'<!-- adm -->.*?<!-- /adm -->', lambda m: b, s, flags=re.S)
    else:
        # старый блок «Ключевые даты» заменяем календарём, остальные разделы — после колонок
        s = re.sub(r'<h2>Ключевые даты</h2>.*?</div>\n</div>\n<h2 style="margin-top:56px">Частые вопросы</h2>',
                   '<h2>Частые вопросы</h2>', s, count=1, flags=re.S)
        anchor = '</aside>\n</div>\n'
        assert anchor in s
        s = s.replace(anchor, anchor + b + '\n', 1)
        s = s.replace('<script src="site.js"></script>', '<script src="site.js"></script>\n<script src="admission-cost.js"></script>', 1)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    css = open('site.css', encoding='utf-8').read()
    if '/* Поступление: календарь' in css:
        a = css.index('\n/* Поступление: календарь')
        b = css.index('@media (max-width:520px){.cost-out', a)
        b = css.index('\n', b) + 1
        css = css[:a] + css[b:]
    open('site.css', 'w', encoding='utf-8', newline='').write(css.rstrip('\n') + '\n' + CSS)
    print('Admission: программ с ценой', len(progs()))


if __name__ == '__main__':
    main()
