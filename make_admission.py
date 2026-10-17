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
    opts = ''.join(f'<option value="{html.escape(n)}" data-price="{v}">{html.escape(n)} — {html.escape(i)}</option>' for n, i, v in ps)
    return f'''<!-- adm -->
<section id="calendar" class="adm-sec" aria-labelledby="cal-h">
<h2 id="cal-h">Календарь приёма</h2>
<p class="muted adm-lead">Даты приёма-2026 в бакалавриат и специалитет. Правила приёма-2027 вуз публикует до 1 ноября — сроки обычно меняются мало.</p>
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
    if '/* Поступление: календарь' not in css:
        open('site.css', 'a', encoding='utf-8', newline='').write(CSS)
    print('Admission: программ с ценой', len(progs()))


if __name__ == '__main__':
    main()
