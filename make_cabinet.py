"""Демо-кабинет студента (Cabinet.dc.html): пары на сегодня, заказ справки, плата за общежитие.
Плата — по приказам УрФУ № 655/03 от 01.07.2025 и № 628/03 от 20.06.2025 (вдвоём в комнате).
Шапка и подвал берутся из NotFound.dc.html. Запуск: python make_cabinet.py (можно повторно)."""
import os, json, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# общежитие: (название, зимой, летом) — рублей в месяц на человека, вдвоём в комнате
DORMS = [
    ('№ 1 · Большакова, 79', 1470, 1109), ('№ 2 · Большакова, 77', 1476, 1110), ('№ 4 · Большакова, 71', 1591, 1253),
    ('№ 5 · Малышева, 144', 2000, 1749), ('№ 6 · Чапаева, 16а', 2033, 1426), ('№ 7 · С. Набойченко, 3', 1595, 1251),
    ('№ 8 · Комсомольская, 70/10', 2040, 1715), ('№ 9 · Фонвизина, 8', 2108, 1749), ('№ 10 · Ленина, 66', 1490, 1086),
    ('№ 11 · Коминтерна, 5/2', 1340, 1089), ('№ 12 · Фонвизина, 4', 1340, 1085), ('№ 13 · Комсомольская, 66а', 1629, 1263),
    ('№ 14 · С. Набойченко, 1а', 1562, 1237), ('№ 15 · Коминтерна, 11', 1938, 1424), ('Новокольцовский, № 1, 2, 4, 5', 2378, 1654),
]
REQ = [('study', 'Справка об обучении'), ('army', 'Справка в военкомат'), ('stip', 'Справка о стипендии'), ('dorm', 'Справка для общежития')]


def main_html():
    return '''<main id="main" tabindex="-1" style="outline:none"><section class="phead cab-head"><div class="wrap">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / <a href="Login.dc.html">Личный кабинет</a> / Студент</div>
<p class="cab-demo" role="note"><b>Демо-кабинет.</b> Так будет выглядеть кабинет студента. Данные здесь — пример, они хранятся только в этом браузере.</p>
<h1 class="big" style="font-size:48px">Здравствуйте!</h1>
<p class="muted" style="margin-top:10px;font-size:19px">{{hello}}</p>
</div></section>
<div class="wrap cab">
<section class="card cab-today" aria-labelledby="ct-h">
<div class="cab-h"><h2 id="ct-h">{{dayTitle}}</h2><a href="Schedule.dc.html">Вся неделя →</a></div>
<ul class="cab-pairs"><sc-for list="{{pairs}}" as="p" hint-placeholder-count="3"><li><span>{{p.from}}–{{p.to}}</span><b>{{p.t}}</b><small>{{p.kind}}</small></li></sc-for></ul>
<p class="muted cab-note">Пары — пример, как в разделе «Расписание».</p>
</section>

<section class="card cab-dl" aria-labelledby="cdl-h">
<div class="cab-h"><h2 id="cdl-h">Дедлайны</h2><span class="muted" style="font-size:14px">{{dlLeft}}</span></div>
<ul class="cab-dls"><sc-for list="{{dls}}" as="x" hint-placeholder-count="4"><li class="{{x.cls}}"><button type="button" class="cab-chk" aria-pressed="{{x.done}}" onClick="{{x.tog}}"><span class="sr">Отметить выполненным: {{x.t}}</span></button><span class="cab-dlt"><b>{{x.t}}</b><small>{{x.s}}</small></span><em>{{x.when}}</em></li></sc-for></ul>
<p class="muted cab-note">Задания — пример. Отметки сохраняются в этом браузере.</p>
</section>

<section class="card cab-nt" aria-labelledby="cnt-h">
<div class="cab-h"><h2 id="cnt-h">Уведомления <span class="cab-badge">{{ntN}}</span></h2></div>
<ul class="cab-nts"><sc-for list="{{nts}}" as="x" hint-placeholder-count="3"><li class="{{x.cls}}"><b>{{x.t}}</b><span>{{x.d}}</span><sc-if value="{{x.href}}" hint-placeholder-val="{{false}}"><a href="{{x.href}}">{{x.lt}}</a></sc-if></li></sc-for></ul>
</section>

<section class="card cab-req" aria-labelledby="cr-h">
<div class="cab-h"><h2 id="cr-h">Справки и заявления</h2></div>
<p class="lg-lbl" id="req-l">Какая справка нужна?</p>
<div class="seg cab-seg" role="group" aria-labelledby="req-l"><sc-for list="{{reqTypes}}" as="r" hint-placeholder-count="4"><button type="button" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.n}}</button></sc-for></div>
<div class="cab-row"><label for="req-n">Сколько экземпляров</label><input id="req-n" type="number" min="1" max="5" value="{{reqN}}" onChange="{{setN}}" class="input cab-num"><button type="button" class="btn" onClick="{{order}}">Заказать</button></div>
<sc-if value="{{hasReq}}" hint-placeholder-val="{{false}}"><h3 class="cab-sub">Мои заявки</h3><ul class="cab-list" aria-live="polite"><sc-for list="{{reqs}}" as="q" hint-placeholder-count="2"><li><b>{{q.n}}</b><span>{{q.c}} экз. · {{q.d}}</span><em>{{q.st}}</em></li></sc-for></ul><button type="button" class="linkbtn" onClick="{{clearReq}}">Очистить пример</button></sc-if>
</section>

<section class="card cab-dorm" aria-labelledby="cd-h">
<div class="cab-h"><h2 id="cd-h">Плата за общежитие</h2><a href="Dorms.dc.html#price-h">Все цены →</a></div>
<p class="lg-lbl" id="dorm-l">Моё общежитие</p>
<div class="cab-dorms" role="group" aria-labelledby="dorm-l"><sc-for list="{{dorms}}" as="d" hint-placeholder-count="15"><button type="button" class="chip" aria-pressed="{{d.on}}" onClick="{{d.pick}}">{{d.n}}</button></sc-for></div>
<dl class="cab-pay" aria-live="polite"><div><dt>Зимой</dt><dd>{{winter}}</dd></div><div><dt>Летом</dt><dd>{{summer}}</dd></div></dl>
<p class="muted cab-note">В месяц на человека, вдвоём в комнате — по приказам УрФУ 2025 года. Оплата — на pay.urfu.ru или по QR-коду.</p>
</section>

<section class="card cab-stip" aria-labelledby="cs-h">
<div class="cab-h"><h2 id="cs-h">Стипендии и выплаты</h2><a href="Help.dc.html?q=стипенд">Вопросы →</a></div>
<ul class="cab-st">
<li><b>Академическая</b><span>Студентам бюджета, которые сдали сессию без троек и долгов.</span></li>
<li><b>Повышенная академическая</b><span>За достижения в учёбе, науке, спорте, творчестве или общественной работе.</span></li>
<li><b>Социальная</b><span>Тем, у кого есть право на соцподдержку: сироты, инвалиды, получатели госсоциальной помощи и другие.</span></li>
<li><b>Материальная помощь</b><span>Разовая выплата в трудной ситуации — по заявлению.</span></li>
</ul>
<p class="muted cab-note">Начисления ведёт институт. Если выплату задерживают — горячая линия Минобрнауки <a href="tel:88002225571">8-800-222-55-71</a>, доб. 1. Суммы зависят от решения университета, поэтому здесь их не приводим.</p>
</section>

<section class="card cab-job" aria-labelledby="cj-h">
<div class="cab-h"><h2 id="cj-h">Практика и работа</h2></div>
<p class="muted" style="margin-top:8px">У ИРИТ-РтФ больше 50 компаний-партнёров. Они берут на практику и стажировки, ведут спецкурсы и проекты.</p>
<div class="cab-co"><span>УЦСБ</span><span>Naumen</span><span>СКБ Контур</span><span>Сбер</span><span>Прософт-Системы</span><span>JetStyle</span><span>Targem Games</span><span>Artsofte</span><span>Yandex Cloud</span><span>НПО автоматики</span></div>
<ul class="cab-ev"><li><b>Ярмарка вакансий</b><span>Компании ищут стажёров и выпускников</span></li><li><b>Выставка проектов</b><span>Студенческие проекты для партнёров</span></li></ul>
<p class="muted cab-note">На примере ИРИТ-РтФ — по данным <a href="https://programs.edu.urfu.ru/ru/9797/pages/employers/" target="_blank" rel="noopener">сайта образовательных программ УрФУ<span class="sr"> (откроется в новой вкладке)</span></a>. <a href="Events.dc.html">Ближайшие события →</a></p>
</section>

<section class="card cab-ses" aria-labelledby="cse-h">
<div class="cab-h"><h2 id="cse-h">Зимняя сессия</h2><span class="muted" style="font-size:14px">январь · пример</span></div>
<table class="cab-tb"><caption class="sr">Экзамены и зачёты зимней сессии — пример</caption><thead><tr><th scope="col">Предмет</th><th scope="col">Форма</th></tr></thead><tbody>
<tr><td>Математический анализ</td><td><span class="cab-ex">экзамен</span></td></tr>
<tr><td>Программирование</td><td><span class="cab-ex">экзамен</span></td></tr>
<tr><td>Физика</td><td><span class="cab-ex">экзамен</span></td></tr>
<tr><td>Алгебра и геометрия</td><td>зачёт</td></tr>
<tr><td>История России</td><td>зачёт</td></tr>
<tr><td>Английский язык</td><td>зачёт</td></tr>
<tr><td>Физическая культура</td><td>зачёт</td></tr>
</tbody></table>
<p class="muted cab-note">Чтобы получать академическую стипендию, сдайте сессию без троек и долгов. Предметы — как в примере расписания.</p>
</section>

<section class="card cab-camp" aria-labelledby="ccm-h">
<div class="cab-h"><h2 id="ccm-h">Мой корпус</h2><a href="Help.dc.html#bld-h">Все корпуса →</a></div>
<p class="cab-big">Радиофак <span>ул. Мира, 32 · ИРИТ-РтФ</span></p>
<ul class="cab-cm">
<li><b>Коворкинг</b><span>1 этаж, Р-044 и левое крыло</span></li>
<li><b>Столовая</b><span>1 этаж</span></li>
<li><b>Библиотека</b><span>в ГУК: Б-202 техническая, Б-203 гуманитарная</span></li>
<li><b>Тьюторы</b><span>Р-138а</span></li>
</ul>
<p class="muted cab-note">Пример для группы РИ. По данным «Навигатора первокурсника» и сайта программ УрФУ.</p>
</section>

<section class="card cab-evs nw-afisha" aria-labelledby="cev-h">
<div class="cab-h"><h2 id="cev-h">Конкурсы и олимпиады</h2><a href="Events.dc.html">Все события →</a></div>
<ul><li><b class="nw-d">25<span>окт</span></b><div><b>Твой ход</b><span class="muted">Всероссийский студенческий проект</span></div></li><li><b class="nw-d">29<span>окт</span></b><div><b>Кейс-чемпионат «Лига твоего имени»</b><span class="muted">Успей подать заявку</span></div></li><li><b class="nw-d">1<span>ноя</span></b><div><b>Премия губернатора для молодых учёных</b><span class="muted">Приём заявок</span></div></li><li><b class="nw-d">10<span>ноя</span></b><div><b>Я — профессионал</b><span class="muted">Олимпиада для студентов</span></div></li><li><b class="nw-d">19<span>янв</span></b><div><b>Изумруд.Студент</b><span class="muted">Олимпиада УрФУ</span></div></li></ul>
</section>

<section class="card cab-svc" aria-labelledby="csv-h">
<div class="cab-h"><h2 id="csv-h">Сервисы УрФУ</h2></div>
<ul>
<li><a href="https://pay.urfu.ru/" target="_blank" rel="noopener"><b>Оплата</b><span>pay.urfu.ru — общежитие, медосмотр</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://programs.edu.urfu.ru/" target="_blank" rel="noopener"><b>Моя программа</b><span>Учебный план и преподаватели</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://youthscience.urfu.ru/" target="_blank" rel="noopener"><b>Молодёжная наука</b><span>Конкурсы и конференции</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
<li><a href="https://elar.urfu.ru/" target="_blank" rel="noopener"><b>Электронный архив</b><span>Статьи, ВКР, газета университета</span><i class="sr"> (откроется в новой вкладке)</i></a></li>
</ul>
</section>

<section class="card cab-links" aria-labelledby="cl-h">
<div class="cab-h"><h2 id="cl-h">Быстро</h2></div>
<ul>
<li><a href="Help.dc.html"><b>Центр помощи</b><span>Медосмотр, Wi-Fi, справки</span></a></li>
<li><a href="Science.dc.html#stud-h"><b>Попасть в науку</b><span>Молодёжные лаборатории</span></a></li>
<li><a href="Events.dc.html"><b>События</b><span>Лекции, конкурсы, ярмарки</span></a></li>
<li><a href="tel:88002225571"><b>Горячая линия для студентов</b><span>8-800-222-55-71 · доб. 1 — права, доб. 2 — психолог</span></a></li>
</ul>
</section>
</div>
</main>'''


LOGIC = '''<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
const DL0 = [['Лабораторная работа №3', 'Программирование', 2], ['Домашнее задание', 'Математический анализ', 4], ['Эссе', 'Основы российской государственности', 8], ['Контрольная работа', 'Физика', 12], ['Проект: защита прототипа', 'Проектная деятельность', 19]];
let dlDone = []; try { dlDone = JSON.parse(localStorage.getItem('urfu-dl') || '[]'); } catch (e) {}
if (this.state && this.state.dlDone) dlDone = this.state.dlDone;
const tday = new Date(); tday.setHours(0, 0, 0, 0);
const MNs = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
const dls = DL0.map(([t, s2, k], i) => { const dd = new Date(tday.getTime() + k * 864e5); const done = dlDone.indexOf(i) !== -1;
  return { t, s: s2, done: String(done), cls: 'cab-dli' + (done ? ' is-done' : (k <= 3 ? ' is-soon' : '')), when: done ? 'готово' : (k === 1 ? 'завтра' : 'через ' + k + ' ' + (k % 10 === 1 && k !== 11 ? 'день' : (k % 10 >= 2 && k % 10 <= 4 && (k < 12 || k > 14)) ? 'дня' : 'дней')) + ' · ' + dd.getDate() + ' ' + MNs[dd.getMonth()],
    tog: () => { const nx = done ? dlDone.filter(x => x !== i) : dlDone.concat(i); try { localStorage.setItem('urfu-dl', JSON.stringify(nx)); } catch (e) {} this.setState({ dlDone: nx }); } }; });
const left = DL0.length - dlDone.length;
const DORMS = __DORMS__, REQ = __REQ__;
const load = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } };
const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
if (!this.state) this.state = { rt: 'study', n: 1, reqs: load('urfu-cab-reqs', []), dorm: load('urfu-cab-dorm', 8) };
const s = this.state;
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
const rub = n => n.toLocaleString('ru-RU') + ' ₽';
const D = DORMS[s.dorm] || DORMS[0];
const RN = {}; REQ.forEach(r => RN[r[0]] = r[1]);
const order = () => {
  const n = Math.min(5, Math.max(1, parseInt(s.n, 10) || 1));
  const d = new Date(); const dd = String(d.getDate()).padStart(2, '0') + '.' + String(d.getMonth() + 1).padStart(2, '0');
  const reqs = [{ t: s.rt, c: n, d: dd }].concat(s.reqs).slice(0, 5); save('urfu-cab-reqs', reqs); this.setState({ reqs });
};
const ntReady = s.reqs.length > 1;
const nts = [
  ntReady ? { t: 'Справка готова', d: 'Заберите в дирекции института или скачайте в кабинете.', href: '#cr-h', lt: 'К справкам', cls: 'cab-nti is-new' } : null,
  { t: 'Снова очные занятия', d: 'С 15 октября занятия идут в аудиториях — гибридный формат закончился.', href: 'News.dc.html', lt: 'Новости', cls: 'cab-nti is-new' },
  { t: 'Расписание на следующую неделю', d: 'Пример: в четверг пара по физике перенесена на 12:00.', href: 'Schedule.dc.html', lt: 'Расписание', cls: 'cab-nti' },
  { t: 'Горячая линия для студентов', d: 'Права студента и психологическая помощь — бесплатно по России.', href: 'Help.dc.html#hl-h', lt: 'Подробнее', cls: 'cab-nti' }
].filter(Boolean);
return {
  dls, dlLeft: left ? 'Осталось: ' + left : 'Всё сделано!', nts, ntN: String(nts.filter(x => x.cls.indexOf('is-new') !== -1).length),
  hello: g ? 'Группа ' + g + ' · это ваш кабинет: расписание, справки и общежитие в одном месте.' : 'Это ваш кабинет: расписание, справки и общежитие в одном месте.',
  dayTitle: day === wd ? 'Сегодня' : 'Сегодня пар нет · в ' + DN[day],
  pairs: PLAN[day].map(([i, t, kind]) => ({ from: T[i][0], to: T[i][1], t, kind })),
  reqTypes: REQ.map(([key, n]) => ({ n, on: String(key === s.rt), pick: () => this.setState({ rt: key }) })),
  reqN: s.n, setN: e => this.setState({ n: e.target.value }), order,
  hasReq: s.reqs.length > 0,
  reqs: s.reqs.map((q, i) => ({ n: RN[q.t], c: q.c, d: 'заказана ' + q.d, st: i === 0 ? 'Принята' : 'Готова' })),
  clearReq: () => { save('urfu-cab-reqs', []); this.setState({ reqs: [] }); },
  dorms: DORMS.map((x, i) => ({ n: x[0], on: String(i === s.dorm), pick: () => { save('urfu-cab-dorm', i); this.setState({ dorm: i }); } })),
  winter: rub(D[1]), summer: rub(D[2])
};
}
}
</script>'''

CSS = '''
/* Демо-кабинет студента */
.cab-demo{display:inline-block;margin:6px 0 14px;padding:10px 16px;border-radius:12px;background:var(--gold-soft);border:2px solid var(--gold);font-size:15px;color:var(--ink)}
.cab{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;padding-top:40px;padding-bottom:72px;align-items:start}
.cab .card{padding:26px}
.cab-h{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.cab-h h2{font-size:26px}
.cab-pairs{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.cab-pairs li{display:grid;grid-template-columns:100px 1fr;gap:2px 12px;padding:12px 14px;border-radius:12px;background:var(--limestone)}
.cab-pairs span{grid-row:span 2;font-weight:700;color:var(--amethyst)}
.cab-pairs small{color:var(--muted)}
.cab-note{font-size:14px;margin-top:12px}
.cab-seg{flex-wrap:wrap}
.cab-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:16px}
.cab-num{width:84px}
.cab-sub{margin-top:22px;font-size:18px}
.cab-list{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.cab-list li{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:12px 14px;border-radius:12px;border:1px solid var(--limestone)}
.cab-list span{color:var(--muted);font-size:14px}
.cab-list em{margin-left:auto;font-style:normal;font-weight:600;color:#04735A}
.cab-dorms{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.cab-dorms .chip{cursor:pointer;font:inherit;font-size:14px}
.cab-dorms .chip[aria-pressed="true"]{background:var(--ink);color:#FFFFFF;border-color:var(--ink)}
.cab-pay{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:18px 0 0}
.cab-pay div{background:var(--gold-soft);border-radius:14px;padding:14px 16px}
.cab-pay dt{font-size:14px;color:var(--muted)}
.cab-pay dd{margin:4px 0 0;font-family:var(--narrow);font-weight:700;font-size:28px}
.cab-links ul{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:8px}
.cab-links a{display:flex;flex-direction:column;padding:14px 16px;border-radius:14px;border:2px solid var(--limestone);text-decoration:none;color:var(--ink)}
.cab-links a:hover{border-color:var(--amethyst)}
.cab-links span{font-size:14px;color:var(--muted)}
@media (max-width:900px){.cab{grid-template-columns:minmax(0,1fr)}}
'''


def main():
    base = open('NotFound.dc.html', encoding='utf-8').read()
    head, rest = base.split('<main', 1)
    foot = rest[rest.index('</main>') + len('</main>'):]
    foot = foot[:foot.index('<script type="text/x-dc"')]
    tail = base[base.index('<script src="dc-lite.js">'):]
    title = 'Кабинет студента (демо) — УрФУ'
    desc = 'Демо-кабинет студента УрФУ: пары на сегодня, заказ справок и плата за общежитие по приказам университета.'
    head = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*"', lambda m: m.group(1) + desc + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + title + '"', head)
    head = head.replace('NotFound.dc.html"', 'Cabinet.dc.html"')
    head = head.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
    logic = LOGIC.replace('__DORMS__', json.dumps(DORMS, ensure_ascii=False)).replace('__REQ__', json.dumps(REQ, ensure_ascii=False))
    open('Cabinet.dc.html', 'w', encoding='utf-8', newline='').write(head + main_html() + foot + logic + '\n' + tail)
    css = open('site.css', encoding='utf-8').read()
    if '/* Демо-кабинет студента */' not in css:
        open('site.css', 'a', encoding='utf-8', newline='').write(CSS)
    print('Cabinet.dc.html готов')


if __name__ == '__main__':
    main()
