/* ЭКСПЕРИМЕНТ «Живой знак»: цвета самоцветов в знаке «У» перетекают по кругу —
   один раз при загрузке, снова при наведении на логотип; большой знак на «Концепции» переливается постоянно.
   Работает через поворот цветового перехода внутри знака, сама форма не меняется. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;
  var running = new WeakMap();

  function setAngle(g, a) {
    /* поворачиваем линию перехода вокруг центра знака */
    var r = a * Math.PI / 180, dx = Math.cos(r) / 2, dy = Math.sin(r) / 2;
    g.setAttribute('x1', (0.5 - dx).toFixed(4)); g.setAttribute('y1', (0.5 - dy).toFixed(4));
    g.setAttribute('x2', (0.5 + dx).toFixed(4)); g.setAttribute('y2', (0.5 + dy).toFixed(4));
  }
  /* блик: светлая полоса пробегает по знаку по диагонали, как свет по грани камня */
  var NS = 'http://www.w3.org/2000/svg', uid = 0;
  function shine(svg, ms) {
    var path = svg.querySelector('path'); if (!path || svg.dataset.shining) return;
    svg.dataset.shining = '1';
    var id = 'llshine' + (++uid);
    var defs = svg.querySelector('defs') || svg.insertBefore(document.createElementNS(NS, 'defs'), svg.firstChild);
    var g = document.createElementNS(NS, 'linearGradient');
    g.setAttribute('id', id); g.setAttribute('x1', '0'); g.setAttribute('y1', '0'); g.setAttribute('x2', '1'); g.setAttribute('y2', '1');
    [['0', 0], ['0.42', 0], ['0.5', 0.85], ['0.58', 0], ['1', 0]].forEach(function (st) {
      var e = document.createElementNS(NS, 'stop'); e.setAttribute('offset', st[0]); e.setAttribute('stop-color', '#FFFFFF'); e.setAttribute('stop-opacity', String(st[1])); g.appendChild(e);
    });
    defs.appendChild(g);
    /* блик по всем частям ленты */
    var overs = [].map.call(svg.querySelectorAll('path:not(.ll-shine)'), function (p) { var o = p.cloneNode(false); o.setAttribute('fill', 'url(#' + id + ')'); o.setAttribute('class', 'll-shine'); svg.appendChild(o); return o; });
    var over = { remove: function () { overs.forEach(function (o) { o.remove(); }); } };
    var t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 2);
      g.setAttribute('gradientTransform', 'translate(' + (-1 + 2 * e) + ' ' + (-1 + 2 * e) + ')');
      if (k < 1 && svg.isConnected) requestAnimationFrame(step); else { over.remove(); g.remove(); delete svg.dataset.shining; }
    }
    requestAnimationFrame(step);
  }
  function swirl(svg, ms) {
    shine(svg, Math.max(1200, ms * 0.85));
    var g = svg.querySelector('linearGradient'); if (!g || running.get(g)) return;
    running.set(g, true);
    var t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / ms), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
      setAngle(g, 90 + 360 * e);
      if (k < 1 && g.isConnected) requestAnimationFrame(step); else { setAngle(g, 90); running.delete(g); }
    }
    requestAnimationFrame(step);
  }
  /* вариант знака в шапке выбирается в адресе: ?m=a — постоянный перелив, ?m=b — «искра» раз в 12 с, ?m=c (или ничего) — при загрузке и наведении */
  var MODE = (new URLSearchParams(location.search).get('m') || 'c').toLowerCase();
  function loop(svg, amp, period) {
    var g = svg.querySelector('linearGradient'); if (!g || g.dataset.loop) return;
    g.dataset.loop = '1';
    var t0 = null;
    function step(t) {
      if (!g.isConnected) return;
      if (t0 === null) t0 = t;
      /* пока идёт перелив по кругу — ждём, потом продолжаем покачивание с того же положения, без скачка */
      if (running.get(g)) t0 = t; else setAngle(g, 90 + (amp || 50) * Math.sin((t - t0) / (period || 8000) * 2 * Math.PI));
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function hook() {
    document.querySelectorAll('.phead svg[viewBox="10 6 82 94"]:not(.mark), .hero svg[viewBox="10 6 82 94"]:not(.mark)').forEach(function (s) { loop(s); });
    /* вариант А: знак в шапке переливается постоянно, чуть сильнее, чем большой — он маленький */
    if (MODE === 'a') { var h = document.querySelector('.hd .brand svg'); if (h) loop(h, 75, 6000); }
  }
  function start() {
    var head = document.querySelector('.hd .brand svg');
    if (head) setTimeout(function () { swirl(head, 1800); }, 500);
    hook();
    /* вариант Б: короткая «искра» раз в 12 секунд */
    if (MODE === 'b') setInterval(function () { if (document.hidden) return; var h = document.querySelector('.hd .brand svg'); if (h) swirl(h, 1300); }, 12000);
    document.addEventListener('mouseover', function (e) {
      var b = e.target.closest && e.target.closest('.brand'); if (!b) return;
      var s = b.querySelector('svg'); if (s) swirl(s, 1400);
    });
    document.addEventListener('focusin', function (e) {
      var b = e.target.closest && e.target.closest('.brand'); if (b && b.querySelector('svg')) swirl(b.querySelector('svg'), 1400);
    });
    var r = document.getElementById('dc-root');
    if (r) new MutationObserver(hook).observe(r, { childList: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
