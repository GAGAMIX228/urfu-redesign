/* Главная: калькулятор «Хватит ли баллов?» и бегущая строка.
   Работает отдельно от движка страниц: ползунок двигается плавно, а после перерисовки страницы
   выбранные балл и область восстанавливаются. Данные — из каталога (атрибут data-progs). */
(function () {
  var EN = document.documentElement.lang === 'en';
  var st = { v: 240, area: 'all' };
  function plural(n, a, b, c) { var m = n % 10, h = n % 100; return m === 1 && h !== 11 ? a : (m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c); }
  function nf(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }
  function draw(box) {
    var data = JSON.parse(box.getAttribute('data-progs') || '[]');
    var r = box.querySelector('#calc-r'), v = st.v;
    if (r && String(r.value) !== String(v)) r.value = v;
    if (r) { var p = (v - r.min) / (r.max - r.min) * 100; r.style.setProperty('--p', p + '%'); }
    var out = box.querySelector('#calc-v'); if (out) out.textContent = v;
    var ok = data.filter(function (x) { return (st.area === 'all' || x[0] === st.area) && x[1] <= v; });
    var n = ok.length, seats = ok.reduce(function (s, x) { return s + x[2]; }, 0);
    var nEl = box.querySelector('#calc-n'), dEl = box.querySelector('#calc-d');
    if (nEl) nEl.textContent = EN ? n + (n === 1 ? ' programme' : ' programmes') : n + ' ' + plural(n, 'программа', 'программы', 'программ');
    if (dEl) dEl.textContent = n ? (EN ? 'pass mark at or below your score · ' + nf(seats) + ' state-funded places' : 'с проходным не выше вашей суммы · ' + nf(seats) + ' ' + plural(seats, 'бюджетное место', 'бюджетных места', 'бюджетных мест'))
                                 : (EN ? 'none yet — try another field or open the catalogue' : 'пока нет — попробуйте другую область или откройте каталог');
    [].forEach.call(box.querySelectorAll('.yu-chip'), function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-area') === st.area ? 'true' : 'false'); });
    var go = box.querySelector('#calc-go');
    if (go) go.href = box.getAttribute('data-cat') + '?my=' + v + (st.area !== 'all' ? '&area=' + st.area : '');
  }
  function all() { [].forEach.call(document.querySelectorAll('.yu-calc'), draw); }
  document.addEventListener('input', function (e) { if (e.target && e.target.id === 'calc-r') { st.v = parseInt(e.target.value, 10) || 240; all(); } });
  document.addEventListener('click', function (e) {
    var c = e.target.closest && e.target.closest('.yu-chip'); if (!c) return;
    st.area = c.getAttribute('data-area') || 'all'; all();
  });
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(function () { all(); }).observe(root, { childList: true });
  all();
})();
