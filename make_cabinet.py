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
return {
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
@media (max-width:900px){.cab{grid-template-columns:1fr}}
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
