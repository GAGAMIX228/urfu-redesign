"""Собирает страницу «Подбор программы за 3 вопроса» (Quiz.dc.html) из шапки, подвала и данных каталога."""
import os
import re

os.chdir(r'C:\Users\Admin\urfu-redesign')
s = open('Catalog.dc.html', encoding='utf-8').read()
head = s[:s.index('<main')]
foot = s[s.index('</main>'):s.index('<script type="text/x-dc" id="dc-logic">')]
logic = s[s.index('<script type="text/x-dc" id="dc-logic">'):]
i = logic.index('const ALL_PROGS = [')
progs = logic[i:logic.index('];', i) + 2]
subj = re.search(r"const SUBJ = .*?;\n", logic).group(0)
tail = logic[logic.index('</script>') + len('</script>'):]
head = re.sub(r'<title>[^<]*</title>', '<title>[Эксперимент] Подбор программы — УрФУ</title>', head)
head = head.replace(' aria-current="page"', '')

CSS = """<style>
.qz > *{max-width:880px}
.qz-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:28px}
.qz-steps span{height:6px;border-radius:999px;background:var(--line)}
.qz-steps span.on{background:var(--c)}
.qz-steps span:nth-child(1){--c:var(--a1)}.qz-steps span:nth-child(2){--c:var(--a2)}.qz-steps span:nth-child(3){--c:var(--a3)}
.qz-q{margin-top:28px}
.qz-q h2{font-size:30px}
.qz-q h2:focus{outline:none}
.qz-hint{color:var(--muted);margin-top:8px}
.qz-opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:20px}
.qz-opt{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:4px;min-height:84px;padding:16px 18px;border:2px solid var(--line);border-radius:var(--r-lg);background:#FFFFFF;font:inherit;text-align:left;cursor:pointer;color:var(--text);transition:border-color .15s ease,background .15s ease}
.qz-opt b{font-size:17px}.qz-opt small{color:var(--muted);font-size:14px}
.qz-opt:hover{border-color:var(--blue)}
.qz-opt[aria-pressed="true"]{border-color:var(--blue);background:var(--blue-soft)}
.qz-opt[aria-pressed="true"] b::before{content:"✓ ";color:var(--blue)}
.qz-nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}
.qz-res{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:20px}
.qz-card{display:flex;flex-direction:column;gap:8px;padding:20px;border:1px solid var(--line);border-radius:var(--r-lg);background:#FFFFFF;text-decoration:none;color:var(--text);box-shadow:inset 0 4px 0 var(--c,var(--line))}
.qz-card:hover{border-color:var(--blue);color:var(--text)}
.qz-card b{font-size:18px;line-height:1.3}
.qz-card .v{font-size:14px;font-weight:600}
.v-ok{--c:var(--a1)}.v-ok .v{color:var(--a1)}
.v-short{--c:var(--a4)}.v-short .v{color:var(--a4)}
.v-none{--c:var(--a3)}.v-none .v{color:var(--muted)}
</style>
"""
head = head.replace('</head>', CSS + '</head>', 1)

MAIN = """<main id="main" tabindex="-1" style="outline:none"><section class="phead"><div class="wrap">
<div class="crumbs"><a href="Main.dc.html">Главная</a> / <a href="Admission.dc.html">Поступить</a> / Подбор программы</div>
<h1 class="big" style="font-size:48px">Подбор программы за 3 вопроса</h1>
<p class="muted" style="margin-top:12px;font-size:19px;max-width:720px">Ответьте на три вопроса — покажем программы, куда можно поступить с вашими ЕГЭ.</p>
</div></section>
<div class="wrap qz">
<div class="qz-steps" aria-hidden="true"><span class="{{s1}}"></span><span class="{{s2}}"></span><span class="{{s3}}"></span></div>
<p class="muted" style="margin-top:8px;font-size:14px" aria-live="polite">{{stepLabel}}</p>

<sc-if value="{{isStep1}}" hint-placeholder-val="{{true}}"><div class="qz-q">
<h2>Что вам интересно?</h2><p class="qz-hint">Можно выбрать несколько.</p>
<div class="qz-opts" role="group" aria-label="Направления">
<sc-for list="{{areaOpts}}" as="o" hint-placeholder-count="6"><button type="button" class="qz-opt" aria-pressed="{{o.on}}" onClick="{{o.toggle}}"><b>{{o.label}}</b><small>{{o.d}}</small></button></sc-for>
</div>
<div class="qz-nav"><button type="button" class="btn" onClick="{{next}}">Дальше <span class="arrow">→</span></button></div>
</div></sc-if>

<sc-if value="{{isStep2}}" hint-placeholder-val="{{false}}"><div class="qz-q">
<h2>Какие ЕГЭ вы сдаёте или сдали?</h2><p class="qz-hint">Отметьте все предметы, включая русский язык.</p>
<div class="qz-opts" role="group" aria-label="Предметы ЕГЭ">
<sc-for list="{{subjOpts}}" as="o" hint-placeholder-count="8"><button type="button" class="qz-opt" style="min-height:56px" aria-pressed="{{o.on}}" onClick="{{o.toggle}}"><b>{{o.label}}</b></button></sc-for>
</div>
<div class="qz-nav"><button type="button" class="btn2" onClick="{{back}}">← Назад</button><button type="button" class="btn" onClick="{{next}}">Дальше <span class="arrow">→</span></button></div>
</div></sc-if>

<sc-if value="{{isStep3}}" hint-placeholder-val="{{false}}"><div class="qz-q">
<h2>Сколько у вас баллов?</h2><p class="qz-hint">Сумма трёх ЕГЭ. Если пока не знаете — оставьте пустым, покажем все подходящие программы.</p>
<div class="field" style="max-width:320px;margin-top:20px"><label for="qzs">Сумма баллов</label><input id="qzs" class="input" inputmode="numeric" placeholder="Например, 240" value="{{my}}" onChange="{{onMy}}"></div>
<div class="qz-nav"><button type="button" class="btn2" onClick="{{back}}">← Назад</button><button type="button" class="btn" onClick="{{next}}">Показать программы <span class="arrow">→</span></button></div>
</div></sc-if>

<sc-if value="{{isRes}}" hint-placeholder-val="{{false}}"><div class="qz-q">
<h2>{{resTitle}}</h2><p class="qz-hint">{{resHint}}</p>
<div class="qz-res">
<sc-for list="{{res}}" as="p" hint-placeholder-count="6"><a class="{{p.cls}}" href="Program.dc.html"><span class="tag" style="align-self:flex-start">{{p.area}}</span><b>{{p.name}}</b><span class="muted" style="font-size:14px">ЕГЭ: {{p.exams}}</span><span class="v">{{p.verdict}}</span></a></sc-for>
</div>
<sc-if value="{{hasNear}}" hint-placeholder-val="{{false}}"><h3 style="margin-top:36px">Почти подходят</h3><p class="qz-hint">Не хватает одного предмета ЕГЭ.</p>
<div class="qz-res"><sc-for list="{{near}}" as="p" hint-placeholder-count="2"><a class="qz-card v-none" href="Program.dc.html"><b>{{p.name}}</b><span class="v">Нужен ещё: {{p.need}}</span></a></sc-for></div></sc-if>
<div class="qz-nav"><button type="button" class="btn2" onClick="{{restart}}">Пройти заново</button><a class="btn" href="Catalog.dc.html">Весь каталог с фильтрами</a></div>
</div></sc-if>
</div>
"""

LOGIC = """<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
""" + progs + "\n" + subj + """const NAME = {}; SUBJ.forEach(([k, n]) => { NAME[k] = n; });
const s = this.state || {};
const step = s.step || 1;
const areas = s.areas || {};
const sel = s.sel || { rus: true };
const my = s.my || '';
const AREAS = [['it','IT и программирование','Код, данные, ИИ, безопасность'],['eng','Инженерия','Энергетика, радиотехника, архитектура'],['nat','Естественные науки','Математика, физика, химия, биология'],['hum','Гуманитарные','Языки, история, общество'],['eco','Экономика','Бизнес, управление, финансы'],['any','Пока не знаю','Покажем всё, что подходит по ЕГЭ']];
const LBL = {}; AREAS.forEach(([k, l]) => { LBL[k] = l; });
const missing = p => { const m = p.req.filter(r => !sel[r]); p.ch.forEach(g => { if (!g.some(x => sel[x])) m.push(g[0]); }); return m; };
const picked = Object.keys(areas).filter(k => areas[k] && k !== 'any');
const inArea = p => !picked.length || picked.includes(p.k);
const myN = parseInt(my, 10), hasMy = !isNaN(myN) && myN > 0;
const pool = ALL_PROGS.filter(inArea);
const fit = pool.filter(p => missing(p).length === 0).map(p => {
  const sc = parseInt(p.score, 10), known = !isNaN(sc);
  let verdict = 'Проходной балл уточняется', cls = 'qz-card v-none', rank = 1;
  if (known && hasMy && myN >= sc) { verdict = 'Баллов хватает: проходной ' + sc; cls = 'qz-card v-ok'; rank = 0; }
  else if (known && hasMy) { verdict = 'Не хватает ' + (sc - myN) + ': проходной ' + sc; cls = 'qz-card v-short'; rank = 2; }
  else if (known) { verdict = 'Проходной 2025: ' + sc; cls = 'qz-card v-ok'; rank = 1; }
  return { ...p, verdict, cls, rank, area: LBL[p.k] || p.area };
}).sort((a, b) => a.rank - b.rank);
const near = pool.filter(p => missing(p).length === 1).slice(0, 4).map(p => ({ name: p.name, need: NAME[missing(p)[0]] }));
const n = fit.length, w = (n % 10 === 1 && n % 100 !== 11) ? 'программа' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'программы' : 'программ';
const verb = (n % 10 === 1 && n % 100 !== 11) ? 'подходит' : 'подходят';
const go = k => () => { this.setState({ step: k }); setTimeout(() => { const h = document.querySelector('.qz-q h2'); if (h) { h.setAttribute('tabindex', '-1'); h.focus(); } }, 30); };
return {
  isStep1: step === 1, isStep2: step === 2, isStep3: step === 3, isRes: step === 4,
  s1: step >= 1 ? 'on' : '', s2: step >= 2 ? 'on' : '', s3: step >= 3 ? 'on' : '',
  stepLabel: step <= 3 ? 'Вопрос ' + step + ' из 3' : 'Готово',
  areaOpts: AREAS.map(([k, label, d]) => ({ label, d, on: String(!!areas[k]), toggle: () => this.setState({ areas: k === 'any' ? { any: !areas.any } : { ...areas, any: false, [k]: !areas[k] } }) })),
  subjOpts: SUBJ.map(([k, label]) => ({ label, on: String(!!sel[k]), toggle: () => this.setState({ sel: { ...sel, [k]: !sel[k] } }) })),
  my, onMy: e => this.setState({ my: e.target.value }),
  next: go(step + 1), back: go(step - 1), restart: go(1),
  res: fit, resTitle: n ? 'Вам ' + verb + ' ' + n + ' ' + w : 'Пока ничего не подходит',
  resHint: n ? (hasMy ? 'Сначала — где ваших баллов хватает. Нажмите на программу, чтобы узнать подробности.' : 'Укажите сумму баллов на шаге 3, чтобы увидеть, где их хватает.') : 'Попробуйте отметить другие предметы ЕГЭ или выбрать «Пока не знаю».',
  near, hasNear: near.length > 0
};
}
}
</script>""" + tail

open('Quiz.dc.html', 'w', encoding='utf-8').write(head + MAIN + foot + LOGIC)
print('ok', len(re.findall(r"^\{name:", progs, re.M)))
