/* Поступление: калькулятор стоимости платного обучения. Вне движка страницы — переживает перерисовку. */
(function () {
  var KEY = 'urfu-cost';
  var cur = '';
  try { cur = localStorage.getItem(KEY) || ''; } catch (e) {}
  function rub(n) { return Math.round(n).toLocaleString('ru-RU').replace(/ /g, ' ') + ' ₽'; }
  function show() {
    var sel = document.getElementById('cost-p');
    if (!sel) return;
    if (cur && sel.value !== cur) { for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === cur) sel.selectedIndex = i; }
    var o = sel.options[sel.selectedIndex], y = o ? Number(o.getAttribute('data-price')) || 0 : 0;
    var set = function (id, v) { var el = document.getElementById(id); if (el && el.textContent !== v) el.textContent = v; };
    set('cost-y', rub(y));
    set('cost-s', rub(y / 2));
    set('cost-t', rub(y * 4));
  }
  document.addEventListener('change', function (e) {
    if (e.target.id !== 'cost-p') return;
    cur = e.target.value;
    try { localStorage.setItem(KEY, cur); } catch (err) {}
    show();
  });
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(function () { if (document.getElementById('cost-y') && document.getElementById('cost-y').textContent === '—') show(); }).observe(root, { childList: true });
  document.addEventListener('DOMContentLoaded', show);
  show();
})();

/* «Найди себя в списках» — демо: ответ строится из введённого кода, чтобы показать, как будет выглядеть поиск. */
(function () {
  function num(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }
  document.addEventListener('submit', function (e) {
    var f = e.target.closest && e.target.closest('.lf-form'); if (!f) return;
    e.preventDefault();
    var inp = f.querySelector('#lf-c'), err = f.querySelector('.lf-err'), out = document.querySelector('.lf-out');
    var code = (inp.value || '').replace(/\D/g, '');
    if (code.length < 6) { err.textContent = 'Нужно не меньше 6 цифр: СНИЛС (11 цифр) или код из личного кабинета'; inp.setAttribute('aria-invalid', 'true'); inp.focus(); return; }
    err.textContent = ''; inp.removeAttribute('aria-invalid');
    var prog = f.querySelector('#lf-p').value, h = 0;
    for (var i = 0; i < code.length; i++) h = (h * 31 + code.charCodeAt(i)) % 1000003;
    var total = 600 + h % 900, places = 100 + h % 60, pos = 1 + (h >> 3) % total, score = 200 + h % 91, agree = h % 2 === 0;
    var ok = pos <= places;
    out.innerHTML = '';
    var add = function (tag, cls, txt) { var el = document.createElement(tag); if (cls) el.className = cls; if (txt) el.textContent = txt; out.appendChild(el); return el; };
    add('div', 'lf-demo', 'Пример ответа · ' + prog);
    var p = add('div', 'lf-pos', num(pos)); var sm = document.createElement('small'); sm.textContent = ' из ' + num(total); p.appendChild(sm);
    var row = add('div', 'lf-row');
    [num(score) + ' баллов', 'бюджетных мест: ' + places, agree ? 'согласие подано' : 'согласия нет'].forEach(function (t) { var s = document.createElement('span'); s.textContent = t; row.appendChild(s); });
    add('p', 'lf-v', ok ? (agree ? 'Сейчас вы в зоне бюджетных мест.' : 'Вы в зоне бюджетных мест — не забудьте подать согласие.') : 'Пока ниже бюджетной границы. Следите за списком: места освобождаются после каждого этапа.');
  });
})();
