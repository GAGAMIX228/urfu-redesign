/* ЭКСПЕРИМЕНТ «Цвета быстрых ссылок»: ?v=mono — все карточки фирменного синего;
   ?v=role — у каждой роли свой самоцвет (Абитуриент — малахит, Студент — аметист, Сотрудник — сапфир, International — яшма) */
(function () {
  var v = new URLSearchParams(location.search).get('v') || 'role';
  var ROLE = { 'Абитуриент': '--a1', 'Студент': '--a2', 'Сотрудник': '--a3', 'International': '--a4' };
  var root = document.documentElement;
  function apply() {
    var q = document.querySelector('.qgrid'); if (!q) return;
    var c = '--a3';
    if (v === 'role') { var b = document.querySelector('.seg [aria-pressed="true"]'); c = (b && ROLE[b.textContent.trim()]) || '--a3'; }
    root.style.setProperty('--qc', 'var(' + c + ')');
    q.classList.add('qc');
  }
  var st = document.createElement('style');
  st.textContent = '.qgrid.qc>.q{--c:var(--qc)} .qgrid.qc{transition:none} .seg button[aria-pressed="true"]{box-shadow:inset 0 -3px 0 var(--qc),0 1px 2px rgba(14,27,43,.12)}';
  document.head.appendChild(st);
  function start() { apply(); var r = document.getElementById('dc-root'); if (r) new MutationObserver(apply).observe(r, { childList: true }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
