/* Смена фото на первом экране главной: 4 снимка кампуса, плавная смена раз в 7 секунд,
   точки для выбора, кнопка паузы (правило доступности: движение дольше 5 секунд должно останавливаться).
   Движок перерисовывает страницу при наборе в поиске — слайды восстанавливаются на том же снимке. */
(function () {
  var EN = document.documentElement.lang === 'en';
  var SLIDES = EN ? [
    { img: 'photos/glavnyj-korpus-leto.webp', t: 'Main academic building', d: '19 Mira St' },
    { img: 'photos/kampus-sverhu.webp', t: 'Campus from above', d: 'Vtuzgorodok' },
    { img: 'photos/irit-zdanie.webp', t: 'Institute of Radioelectronics and IT', d: '32 Mira St' },
    { img: 'photos/kampus-leto.webp', t: 'Campus in summer', d: 'square in front of the main building' }
  ] : [
    { img: 'photos/glavnyj-korpus-leto.webp', t: 'Главный учебный корпус', d: 'ул. Мира, 19' },
    { img: 'photos/kampus-sverhu.webp', t: 'Кампус с высоты', d: 'Втузгородок' },
    { img: 'photos/irit-zdanie.webp', t: 'Институт радиоэлектроники и IT', d: 'ул. Мира, 32' },
    { img: 'photos/kampus-leto.webp', t: 'Кампус летом', d: 'площадь перед главным корпусом' }
  ];
  var L = EN ? { group: 'Hero photos', photo: 'Photo ', play: 'Resume photo slideshow', stop: 'Pause photo slideshow' }
             : { group: 'Фото первого экрана', photo: 'Фото ', play: 'Продолжить смену фото', stop: 'Остановить смену фото' };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cur = 0, paused = reduce, timer = null;
  document.documentElement.classList.add('hs-on');
  SLIDES.forEach(function (s) { var i = new Image(); i.src = s.img; }); /* заранее загрузить */

  var PAUSE = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"></rect><rect x="14" y="4" width="4" height="16" rx="1"></rect></svg>';
  var PLAY = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4l13 8-13 8z"></path></svg>';

  function build() {
    var hero = document.querySelector('.hero.photo');
    if (!hero || hero.querySelector('.hs')) return;
    var box = document.createElement('div');
    box.className = 'hs'; box.setAttribute('aria-hidden', 'true');
    SLIDES.forEach(function (s, i) {
      var d = document.createElement('div');
      d.className = 'hs-s' + (i === cur ? ' on' : '');
      d.style.backgroundImage = "url('" + s.img + "')";
      box.appendChild(d);
    });
    hero.insertBefore(box, hero.firstChild);
    var stats = hero.querySelector('.stats');
    var ctl = document.createElement('div');
    ctl.className = 'hs-ctl';
    ctl.innerHTML = '<div class="hs-cap" aria-live="polite"></div><div class="hs-dots" role="group" aria-label="' + L.group + '"></div><button type="button" class="hs-pause"></button>';
    var dots = ctl.querySelector('.hs-dots');
    SLIDES.forEach(function (s, i) {
      var b = document.createElement('button'); b.type = 'button';
      b.setAttribute('aria-label', L.photo + (i + 1) + ': ' + s.t);
      b.addEventListener('click', function () { show(i, true); });
      dots.appendChild(b);
    });
    ctl.querySelector('.hs-pause').addEventListener('click', function () { paused = !paused; paint(); schedule(); });
    if (stats) stats.parentNode.insertBefore(ctl, stats); else hero.appendChild(ctl);
    paint();
  }
  function paint() {
    var hero = document.querySelector('.hero.photo'); if (!hero) return;
    hero.querySelectorAll('.hs-s').forEach(function (s, i) { s.classList.toggle('on', i === cur); s.classList.toggle('zoom', i === cur && !paused); });
    hero.querySelectorAll('.hs-dots button').forEach(function (b, i) { b.setAttribute('aria-current', String(i === cur)); });
    var cap = hero.querySelector('.hs-cap');
    if (cap) cap.innerHTML = '<b>' + SLIDES[cur].t + '</b>' + SLIDES[cur].d;
    var p = hero.querySelector('.hs-pause');
    if (p) { p.innerHTML = paused ? PLAY : PAUSE; p.setAttribute('aria-label', paused ? L.play : L.stop); }
  }
  function show(i, byUser) { cur = (i + SLIDES.length) % SLIDES.length; paint(); if (byUser) schedule(); }
  function schedule() { clearInterval(timer); if (!paused) timer = setInterval(function () { show(cur + 1); }, 7000); }

  function start() {
    build(); schedule();
    var r = document.getElementById('dc-root');
    if (r) new MutationObserver(function () { build(); }).observe(r, { childList: true });
    /* скрытая вкладка — не листаем зря */
    document.addEventListener('visibilitychange', function () { if (document.hidden) clearInterval(timer); else schedule(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
