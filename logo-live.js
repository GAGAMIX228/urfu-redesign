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
  function swirl(svg, ms) {
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
  function loop(svg) {
    var g = svg.querySelector('linearGradient'); if (!g || g.dataset.loop) return;
    g.dataset.loop = '1';
    var t0 = null;
    function step(t) {
      if (!g.isConnected) return;
      if (t0 === null) t0 = t;
      /* медленное покачивание: ±50° за 8 секунд */
      setAngle(g, 90 + 50 * Math.sin((t - t0) / 8000 * 2 * Math.PI));
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function hook() {
    document.querySelectorAll('.phead svg[viewBox="0 0 35 62"]:not(.mark), .hero svg[viewBox="0 0 35 62"]:not(.mark)').forEach(loop);
  }
  function start() {
    var head = document.querySelector('.hd .brand svg');
    if (head) setTimeout(function () { swirl(head, 1800); }, 500);
    hook();
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
