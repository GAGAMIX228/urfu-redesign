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
