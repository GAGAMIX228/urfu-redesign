/* ЭКСПЕРИМЕНТ «Движение»: появление при прокрутке, счётчики, полоса прочтения, смена ролей.
   Движок перерисовывает страницу целиком при каждом действии, поэтому всё, что уже показано,
   после перерисовки сразу ставится на место, без повторной анимации. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  root.classList.add('mo');
  var start = Date.now();

  /* что появляется при прокрутке; дети групп — лесенкой */
  var SINGLE = '.sec-head, main h2, .adm, .story, .ev, .qgrid, .phead + .wrap > .g4, .cmap, .cleg';
  var GROUPS = '.inst, .news, .bento, main .g2, main .g3, main .g4, .week, .evl, .mgrid, .pc-list';
  var io = null, seen = 0;

  function mark(el, i) {
    if (el.classList.contains('mo-r') || el.closest('.hero,.phead,.ft,[role=dialog],.phone')) return;
    el.classList.add('mo-r');
    el.style.setProperty('--i', Math.min(i || 0, 8));
    var r = el.getBoundingClientRect();
    /* то, что уже было показано до перерисовки или лежит выше экрана, — сразу на месте */
    if (r.top + window.scrollY < seen || r.bottom < 0) { el.classList.add('in'); return; }
    if (io) io.observe(el); else el.classList.add('in');
  }
  function scan() {
    document.querySelectorAll(SINGLE).forEach(function (el) { mark(el, 0); });
    document.querySelectorAll(GROUPS).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) { mark(c, i); });
    });
    var ft = document.querySelector('.ft');
    if (ft && !ft.classList.contains('mo-seen')) { ft.classList.add('mo-seen'); if (io) io.observe(ft); else ft.classList.add('in'); }
    else if (ft && ft.getBoundingClientRect().top + window.scrollY < seen) ft.classList.add('in');
  }
  if (!reduce && 'IntersectionObserver' in window) {
    io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in'); io.unobserve(e.target);
        seen = Math.max(seen, e.target.getBoundingClientRect().bottom + window.scrollY);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  }
  function updateSeen() { seen = Math.max(seen, window.scrollY + window.innerHeight * 0.92); }

  /* счётчики на первом экране: 400+, 164, 100+ набегают от нуля; год основания не трогаем */
  function counters() {
    if (reduce) return;
    document.querySelectorAll('.stat b.num').forEach(function (b) {
      var m = b.textContent.trim().match(/^(\d+)(\D*)$/);
      if (!m || +m[1] >= 1800) return;
      var to = +m[1], suf = m[2], t0 = null;
      b.textContent = '0' + suf;
      function step(t) {
        if (!b.isConnected) return;
        if (t0 === null) t0 = t;
        var k = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - k, 3);
        b.textContent = Math.round(to * e) + suf;
        if (k < 1) requestAnimationFrame(step);
      }
      setTimeout(function () { requestAnimationFrame(step); }, 350);
    });
  }

  /* полоса прочтения */
  var bar = document.createElement('div');
  bar.className = 'mo-progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  function progress() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ')';
  }
  window.addEventListener('scroll', function () { progress(); updateSeen(); }, { passive: true });
  window.addEventListener('resize', progress);

  /* смена роли на главной */
  var role = null;
  function roleNow() { var b = document.querySelector('.seg [aria-pressed="true"]'); return b ? b.textContent.trim() : null; }

  function afterRender() {
    root.style.setProperty('--kb-delay', -((Date.now() - start) / 1000) + 's');
    scan();
    var r = roleNow();
    if (role !== null && r !== role) {
      var q = document.querySelector('.qgrid');
      if (q && !reduce) { q.classList.add('mo-swap'); Array.prototype.forEach.call(q.children, function (c, i) { c.style.setProperty('--i', i); c.classList.add('in'); }); }
    }
    role = r;
    progress();
  }

  function init() {
    if (!document.querySelector('#dc-root > *')) { requestAnimationFrame(init); return; }
    afterRender();
    counters();
    new MutationObserver(function () { afterRender(); }).observe(document.getElementById('dc-root'), { childList: true });
  }
  init();
})();
