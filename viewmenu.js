/* ЭКСПЕРИМЕНТ «Кнопка Вид»: «глаз» и луна объединены в одну кнопку с меню —
   «Версия для слабовидящих» и «Тёмная тема». ?nav=center — разделы меню по центру шапки. */
(function () {
  var root = document.documentElement;
  if (new URLSearchParams(location.search).get('nav') === 'center') root.classList.add('nav-center');
  root.classList.add('vm-on');
  var ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor" stroke="none"></path></svg>';

  function sw(on) { return '<span class="vm-sw' + (on ? ' on' : '') + '" aria-hidden="true"><i></i></span>'; }
  function isDark() { return root.getAttribute('data-theme') === 'dark'; }
  function isA11y() { var c = document.getElementById('a11y'); return !!(c && c.checked); }

  function paint(d) {
    var a = d.querySelector('.vm-a11y'), t = d.querySelector('.vm-theme');
    if (a) { a.setAttribute('aria-checked', String(isA11y())); a.querySelector('.vm-sw').classList.toggle('on', isA11y()); }
    if (t) { t.setAttribute('aria-checked', String(isDark())); t.querySelector('.vm-sw').classList.toggle('on', isDark()); }
  }
  function build() {
    var tools = document.querySelector('.hd .tools');
    if (!tools || tools.querySelector('.vm')) return;
    var d = document.createElement('details');
    d.className = 'vm';
    d.innerHTML = '<summary class="ico" aria-label="Настройки вида" title="Настройки вида">' + ICON + '</summary>' +
      '<div class="vm-panel" role="group" aria-label="Настройки вида">' +
      '<button type="button" class="vm-row vm-a11y" role="switch"><span>Версия для слабовидящих<small>крупнее текст, чётче контраст</small></span>' + sw(false) + '</button>' +
      '<button type="button" class="vm-row vm-theme" role="switch"><span>Тёмная тема<small>удобно вечером</small></span>' + sw(false) + '</button>' +
      '</div>';
    d.querySelector('.vm-a11y').addEventListener('click', function () { var c = document.getElementById('a11y'); if (c) { c.checked = !c.checked; c.dispatchEvent(new Event('change', { bubbles: true })); } paint(d); });
    d.querySelector('.vm-theme').addEventListener('click', function () { var b = document.querySelector('.theme-btn'); if (b) b.click(); paint(d); });
    d.addEventListener('toggle', function () { paint(d); });
    tools.insertBefore(d, tools.firstChild);
    paint(d);
  }
  /* закрыть по Esc и по щелчку мимо */
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; var d = document.querySelector('.vm[open]'); if (d) { d.open = false; d.querySelector('summary').focus(); } });
  document.addEventListener('click', function (e) { if (!e.isTrusted) return; /* программные нажатия (переключение темы) меню не закрывают */ var d = document.querySelector('.vm[open]'); if (d && !d.contains(e.target)) d.open = false; });

  function start() {
    build();
    var r = document.getElementById('dc-root');
    if (r) new MutationObserver(function () { build(); }).observe(r, { childList: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
