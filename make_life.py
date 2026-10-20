"""Страница «Жизнь в УрФУ» (Life.dc.html): студенческие организации, традиции и большие проекты, спорт, события.
Данные — «Навигатор первокурсника УрФУ» (privet.urfu.ru, разделы «Студенческие организации» и «Крупные проекты»,
октябрь 2026; описания части организаций — по копии раздела в веб-архиве, май 2026). Описания сокращены.
Где описания нет — показываем только название. Запуск: python make_life.py, затем make_heroph.py и make_og.py."""
import os, re, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CATS = [('all', 'Все'), ('self', 'Самоуправление и забота'), ('job', 'Работа и карьера'), ('art', 'Творчество и игры'),
        ('sport', 'Спорт и туризм'), ('intl', 'Международное и языки'), ('vol', 'Волонтёрство')]
# (название, направление, коротко, ссылка)
ORGS = [
    ('Союз студентов УрФУ', 'self', 'Самая большая студенческая организация: защищает интересы более 19 000 студентов, ведёт образовательные проекты, помогает с трудоустройством.', 'vk.com/posnews'),
    ('Ассоциация студентов-наставников', 'self', 'Старшекурсники помогают первокурсникам освоиться в университете. Стать наставником можно со второго курса.', 'vk.com/asn_urfu'),
    ('Объединённый совет студенческого городка', 'self', 'Работает со всеми общежитиями: помогает с бытовыми вопросами и организует досуг жителей.', 'vk.com/ossg.urfu'),
    ('Студенческий психологический клуб УГИ', 'self', 'Психология для всех, кому интересно, и бесплатная краткосрочная поддержка — три встречи.', 'vk.com/studentpsychologicalclub'),
    ('Отряд охраны правопорядка «Феникс»', 'self', 'С 1994 года охраняет общественный порядок в университете и Екатеринбурге.', 'vk.com/coonp_urfu'),
    ('Штаб студенческих отрядов', 'job', '30 отрядов: строительные, педагогические, проводники, археологический. Летняя работа за плату и практика.', 'vk.com/so_urfu'),
    ('Команда продвижения УрФУ', 'job', 'Студенты бесплатно ездят в свои города рассказать школьникам об университете. Выезды — осенью и весной.', 'vk.com/kpurfu'),
    ('AIESEC', 'job', 'Лидерские программы по России и международные стажировки.', 'vk.com/aiesec_ekaterinburg'),
    ('Союз молодых инноваторов', 'job', 'Поддерживает инновационные идеи и развивает предпринимательские навыки.', 'vk.com/sminnovators'),
    ('Клуб переговорных технологий «Юниверс»', 'job', 'Учат договариваться и выходить из конфликтов: курс, мастер-классы, деловые игры.', 'vk.com/universe_urfu'),
    ('Центр творчества УрФУ', 'art', '20 творческих коллективов — от школы ведущих до рок-клуба. Номера и сценарии для событий университета.', 'vk.com/creation_urfu'),
    ('Совет студенческих СМИ', 'art', 'Объединяет студенческие редакции. Каждый год — Медиашкола для новичков.', 'vk.com/urfu_smi'),
    ('Ролевой проект', 'art', 'Квесты, ролевые и настольные игры, D&D — всё про гик-культуру.', 'vk.com/roleplayfti'),
    ('Клуб настольных игр «Играриум»', 'art', 'Каждый месяц — вечера настольных игр. Новичкам всё объяснят ведущие.', 'vk.com/igrariuminfo'),
    ('Спорт УрФУ', 'sport', 'Сборные и соревнования — для спортсменов и тех, кто просто любит активный отдых.', 'vk.com/sporturfu'),
    ('Киберспорт УрФУ', 'sport', '', ''),
    ('Турклуб «Романтик»', 'sport', 'Готовит к категорийным походам: пеший, горный, лыжный и велотуризм.', 'vk.com/turclub_romantic'),
    ('Турклуб «Рифей»', 'sport', '', ''),
    ('Велком центр УрФУ', 'sport', 'Студенческий туристический кластер, работает по проекту «Твой маршрут — Россия».', 'vk.com/uralwelcome'),
    ('Совет по культурно-историческому наследию Урала', 'sport', 'Свои туристические проекты: экскурсии, маршруты, сопровождение гостей.', 'vk.com/sapkinu'),
    ('Студенческая организация объединённых наций', 'intl', 'Помогает иностранным студентам освоиться. В организации — 17 землячеств.', 'vk.com/international_students_urfu'),
    ('ISU Ural Federal', 'intl', 'Одно из двух российских подразделений International Student Union: помощь иностранным студентам.', 'vk.com/isu.uralfederal'),
    ('Бадди УрФУ', 'intl', 'Студенты-«бадди» помогают иностранным первокурсникам: адаптация и документы.', 'vk.com/buddysysturfu'),
    ('Клуб иностранных языков', 'intl', 'Занятия ведут студенты и носители языка: игры, кинопоказы, дебаты.', 'vk.com/club_urfu'),
    ('Екатеринбургская международная модель ООН', 'intl', 'Моделирование заседаний ООН и молодёжная дипломатия.', 'vk.com/eimun'),
    ('Юношеское лингвистическое сообщество', 'intl', '', ''),
    ('МОСТ УрФУ', 'intl', '', ''),
    ('Волонтёрский центр «Волонтёры Урала»', 'vol', 'Помогают на событиях университета, города и страны — от Олимпиады в Сочи до чемпионата мира по футболу 2018 года.', 'vk.com/volural'),
    ('Патриотический клуб «Я горжусь»', 'vol', 'Студенческий клуб в рамках федерального проекта «Патриотическое воспитание».', 'vk.com/ya_gorzhus_urfu'),
]
# (название, когда, коротко)
PROJ = [
    ('Неделя первокурсника', 'начало учёбы', 'Квизы и квесты по корпусам и организациям, фестиваль у главного корпуса.'),
    ('Хоровод УрФУ', '19 октября', 'День рождения университета: сотни студентов водят хоровод на площади у ГУК, потом — торт.'),
    ('Дебют первокурсников', 'первый курс', 'Каждая группа готовит творческий номер. Победители института выходят на университетский этап.'),
    ('«Студент года УрФУ»', 'премия', '12 номинаций и три этапа: заявка, очные тренинги, защита проекта в финале.'),
    ('«Время карьеры»', 'карьера', 'Знакомство с работодателями, стажировки, подготовка к собеседованиям. Больше 100 000 участников со всей страны.'),
    ('«Пик IT»', 'день IT', 'День открытых дверей IT-отрасли для школьников и студентов. Генеральный партнёр — СКБ Контур.'),
    ('Фестиваль «Дружба народов»', 'фестиваль', 'Землячества показывают свою культуру: спорт, мастер-классы и концерт.'),
    ('Универсиада УрФУ', 'весь год', 'Соревнования институтских команд по 17 видам спорта — и для профи, и для любителей.'),
    ('Бенефис', 'театр', 'Институты ставят спектакли по 30–35 минут — на сцене сразу 40–60 человек.'),
    ('«НаукаФест»', 'наука', 'Достижения молодёжных лабораторий, научно-популярные лекции и экспресс-хакатон.'),
    ('Парад 9 мая', '9 мая', 'Парад у главного корпуса со студентами военного учебного центра и легкоатлетическая эстафета.'),
    ('Выпускной УрФУ', 'лето', '100 лучших выпускников получают дипломы из рук ректора на площади у ГУК.'),
]
NUMS = [('29', 'студенческих организаций'), ('19 000+', 'студентов в Союзе студентов'), ('20', 'творческих коллективов'),
        ('30', 'студенческих отрядов'), ('17', 'видов спорта в Универсиаде'), ('17', 'землячеств иностранных студентов')]


def main_html():
    nums = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in NUMS)
    proj = ''.join(f'<li><span class="lf-when">{w}</span><b>{t}</b><p>{d}</p></li>' for t, w, d in PROJ)
    return '''<main id="main" tabindex="-1" style="outline:none"><section class="phead">
<div class="wrap" style="padding-bottom:56px">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / Жизнь в УрФУ</div>
<div class="row" style="align-items:center;margin-top:8px">
<div class="main"><h1 class="big" style="font-size:52px">Жизнь в УрФУ — это не только пары</h1>
<p style="font-size:19px;margin-top:16px;max-width:620px;color:#2B3946">29 студенческих организаций, 20 творческих коллективов, Универсиада по 17 видам спорта. Найдите своих.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn" href="#orgs">Найти свою команду</a><a class="btn2" href="Events.dc.html">Календарь событий</a></div></div>
<div class="side"><div class="ph art t1 photo" style="--img:url('photos/studenty.webp');height:300px;position:relative;overflow:hidden"></div></div>
</div>
</div>
</section>
<div class="wrap">
<ul class="lf-nums" aria-label="Студенческая жизнь в цифрах">''' + nums + '''</ul>

<section id="orgs" class="sec" aria-labelledby="orgs-h">
<h2 id="orgs-h">Студенческие организации</h2>
<p class="muted" style="margin-top:8px;max-width:760px">Все организации из «Навигатора первокурсника» УрФУ. Выберите, что вам ближе.</p>
<div class="lf-cats" role="group" aria-label="Направление"><sc-for list="{{cats}}" as="c" hint-placeholder-count="7"><button type="button" class="chip" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}} <small>{{c.n}}</small></button></sc-for></div>
<p class="lf-count" aria-live="polite">{{count}}</p>
<ul class="lf-orgs"><sc-for list="{{orgs}}" as="o" hint-placeholder-count="8"><li class="card">
<span class="tag" style="align-self:flex-start">{{o.cat}}</span>
<b>{{o.t}}</b>
<sc-if value="{{o.hasD}}" hint-placeholder-val="{{true}}"><p class="muted">{{o.d}}</p></sc-if>
<sc-if value="{{o.hasL}}" hint-placeholder-val="{{true}}"><a href="{{o.href}}" target="_blank" rel="noopener">{{o.l}}<span class="sr"> (откроется в новой вкладке)</span></a></sc-if>
</li></sc-for></ul>
<p class="muted" style="font-size:14px;margin-top:12px">По разделу «Студенческие организации» <a href="https://privet.urfu.ru/orgs" target="_blank" rel="noopener">«Навигатора первокурсника» УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>; описания сокращены.</p>
</section>

<section class="sec" aria-labelledby="proj-h">
<h2 id="proj-h">Традиции и большие проекты</h2>
<p class="muted" style="margin-top:8px;max-width:760px">Их ждут каждый год. Можно прийти зрителем — или помочь в организации.</p>
<ol class="lf-proj">''' + proj + '''</ol>
<p class="muted" style="font-size:14px;margin-top:12px">По разделу «Крупные проекты» <a href="https://privet.urfu.ru/projects" target="_blank" rel="noopener">«Навигатора первокурсника»<span class="sr"> (откроется в новой вкладке)</span></a>.</p>
</section>

<section class="sec">
<div class="g2" style="align-items:stretch">
<div class="ph art t2 photo" role="img" aria-label="Дворец водных видов спорта в новом кампусе в Новокольцовском" style="--img:url('photos/dvorec-vodnyh-vidov-sporta.webp');min-height:320px;position:relative;overflow:hidden"></div>
<div class="card" style="padding:40px;display:flex;flex-direction:column;justify-content:center;gap:16px;background:var(--ink);color:#FFFFFF;border-color:var(--ink)">
<span class="tag" style="align-self:flex-start;background:var(--ink-2);color:#FFFFFF">Спорт</span>
<h2 style="color:#FFFFFF">Физкультура по интересам</h2>
<p style="color:var(--on-dark-muted)">Секцию физкультуры первокурсник выбирает сам — в личном кабинете студента на istudent.urfu.ru. А за институт можно выступить на Универсиаде: обратитесь к спорторгу института или в Союз студентов.</p>
<a class="btn" href="Cabinet.dc.html#cg-first" style="align-self:flex-start;background:#FFFFFF;color:var(--ink)">Чек-лист первокурсника</a>
</div>
</div>
</section>

<section class="sec" aria-labelledby="ev-h">
<h2 id="ev-h">Ближайшие события</h2>
<div class="g3" style="margin-top:24px" data-prune>
<a class="card lf-ev" data-end="2026-10-25" href="Events.dc.html"><div class="lf-evd"><b>25</b><span>окт</span></div><div style="font-weight:600">Твой ход — всероссийский студенческий проект</div></a>
<a class="card lf-ev" data-end="2026-10-31" href="Events.dc.html"><div class="lf-evd"><b>31</b><span>окт</span></div><div style="font-weight:600">Во имя героев</div></a>
<a class="card lf-ev" data-end="2026-11-12" href="Events.dc.html"><div class="lf-evd"><b>3–12</b><span>ноя</span></div><div style="font-weight:600">Большой этнографический диктант</div></a>
<a class="card lf-ev" data-end="2026-11-14" href="Events.dc.html"><div class="lf-evd"><b>12–14</b><span>ноя</span></div><div style="font-weight:600">Российские регионы в фокусе перемен</div></a>
<a class="card lf-ev" data-end="2027-01-19" href="Events.dc.html"><div class="lf-evd"><b>19</b><span>янв</span></div><div style="font-weight:600">Изумруд.Студент — олимпиада УрФУ</div></a>
</div>
<p class="muted" data-prune-empty hidden style="margin-top:12px">Новые события — в <a href="Events.dc.html">календаре</a>.</p>
</section>

<section class="sec">
<div class="lf-join">
<div><h2>Хочу в актив</h2><p style="margin-top:8px">Приходите в Союз студентов УрФУ — ГУК-309: подскажут, с чего начать, и помогут с любым вопросом. В каждом институте есть своё профбюро.</p></div>
<div class="lf-join-b"><a class="btn" href="https://vk.com/posnews" target="_blank" rel="noopener">Союз студентов ВКонтакте<span class="sr"> (откроется в новой вкладке)</span></a><a class="btn2" href="Institute.dc.html#il-s-h">Профбюро институтов</a></div>
</div>
</section>
</div>
</main>'''


LOGIC = '''<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
const CATS = __CATS__, ORGS = __ORGS__;
const c = (this.state && this.state.c) || 'all';
const CN = {}; CATS.forEach(([k, n]) => CN[k] = n);
const list = ORGS.filter(o => c === 'all' || o[1] === c);
const plural = n => n % 10 === 1 && n % 100 !== 11 ? 'организация' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? 'организации' : 'организаций');
return {
  cats: CATS.map(([k, n]) => ({ label: n, n: String(k === 'all' ? ORGS.length : ORGS.filter(o => o[1] === k).length), on: String(k === c), pick: () => this.setState({ c: k }) })),
  count: list.length + ' ' + plural(list.length),
  orgs: list.map(([t, k, d, l]) => ({ t, cat: CN[k], d: d || 'Описание и контакты — в «Навигаторе первокурсника».', hasD: true, l: l || 'privet.urfu.ru/orgs', hasL: true, href: 'https://' + (l || 'privet.urfu.ru/orgs') }))
};
}
}
</script>'''

CSS = '''<style id="lf-css">
.lf-nums{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));border-top:3px solid var(--ink);border-bottom:3px solid var(--ink)}
.lf-nums li{display:flex;flex-direction:column;gap:4px;padding:20px 16px}
.lf-nums li+li{border-left:1px solid var(--line-strong)}
.lf-nums b{font-family:var(--narrow);font-size:clamp(32px,3.2vw,46px);line-height:1}
.lf-nums span{font-size:14px;color:var(--muted)}
.lf-cats{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.lf-cats .chip{cursor:pointer}
.lf-cats .chip[aria-pressed="true"]{background:var(--ink);color:#FFFFFF;border-color:var(--ink)}
.lf-cats small{opacity:.7;font-weight:600}
.lf-count{margin-top:14px;font-weight:700}
.lf-orgs{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.lf-orgs li{display:flex;flex-direction:column;gap:8px}
.lf-orgs b{font-family:var(--narrow);font-size:21px;line-height:1.15}
.lf-orgs p{font-size:15px;flex:1}
.lf-orgs a{font-size:14px;font-weight:600;align-self:flex-start;padding:4px 0}
.lf-proj{list-style:none;margin:20px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.lf-proj li{display:flex;flex-direction:column;gap:6px;padding:18px;border-radius:16px;background:#FFFFFF;border:1px solid var(--line);border-top:5px solid var(--rhodonite)}
.lf-proj li:nth-child(4n+2){border-top-color:var(--gold)}.lf-proj li:nth-child(4n+3){border-top-color:var(--malachite)}.lf-proj li:nth-child(4n+4){border-top-color:var(--amethyst)}
.lf-when{align-self:flex-start;padding:2px 10px;border-radius:999px;background:var(--limestone);font-size:13px;font-weight:700}
.lf-proj b{font-family:var(--narrow);font-size:22px}
.lf-proj p{font-size:15px;color:var(--muted)}
.lf-ev{display:flex;gap:16px;align-items:center;text-decoration:none;color:var(--ink)}
.lf-evd{text-align:center;min-width:56px}
.lf-evd b{display:block;font-family:var(--narrow);font-size:28px;color:var(--rhodonite-d,#C81A62);white-space:nowrap}
.lf-evd span{font-size:13px;color:var(--muted)}
.lf-join{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;padding:36px;border-radius:20px;background:var(--gold-soft);border:2px solid var(--ink)}
.lf-join p{max-width:620px}
.lf-join-b{display:flex;gap:10px;flex-wrap:wrap}
@media (max-width:1000px){.lf-nums{grid-template-columns:repeat(3,minmax(0,1fr))}.lf-nums li:nth-child(4){border-left:0}.lf-nums li:nth-child(n+4){border-top:1px solid var(--line-strong)}.lf-orgs{grid-template-columns:repeat(2,minmax(0,1fr))}.lf-proj{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:620px){.lf-nums{grid-template-columns:repeat(2,minmax(0,1fr))}.lf-nums li{border-left:0 !important;border-top:1px solid var(--line-strong)}.lf-nums li:nth-child(2n){border-left:1px solid var(--line-strong) !important}.lf-nums li:nth-child(-n+2){border-top:0}.lf-orgs,.lf-proj{grid-template-columns:minmax(0,1fr)}.lf-join{padding:24px 18px}}
</style>'''


def main():
    s = open('Life.dc.html', encoding='utf-8').read()
    a = s.index('<main'); b = s.index('</main>') + len('</main>')
    s = s[:a] + main_html() + s[b:]
    s = re.sub(r'<script type="text/x-dc" id="dc-logic">.*?</script>', lambda m: LOGIC.replace('__CATS__', json.dumps(CATS, ensure_ascii=False)).replace('__ORGS__', json.dumps(ORGS, ensure_ascii=False)), s, count=1, flags=re.S)
    s = re.sub(r'<style id="lf-css">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    desc = 'Студенческая жизнь УрФУ: 29 организаций, традиции и большие проекты, спорт и события — по «Навигатору первокурсника».'
    for k in ('name="description"', 'property="og:description"'):
        s = re.sub(r'(<meta ' + k + r' content=")[^"]*"', lambda m: m.group(1) + desc + '"', s)
    open('Life.dc.html', 'w', encoding='utf-8', newline='').write(s)
    print('Life.dc.html: организаций', len(ORGS), 'проектов', len(PROJ))


if __name__ == '__main__':
    main()
