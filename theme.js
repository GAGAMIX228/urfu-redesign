/* ЭКСПЕРИМЕНТ «Тёмная тема»: кнопка с луной/солнцем в шапке. Выбор запоминается в этом браузере.
   Подключается в <head>, чтобы тема включалась до показа страницы — без белой вспышки. */
(function () {
  var KEY = 'urfu-theme', root = document.documentElement;
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  if (get() === 'dark') root.setAttribute('data-theme', 'dark');

  var MOON = '<svg class="i-moon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"></path></svg>';
  var SUN = '<svg class="i-sun" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg>';

  function isDark() { return root.getAttribute('data-theme') === 'dark'; }
  function label(b) {
    var d = isDark();
    b.setAttribute('aria-pressed', String(d));
    b.setAttribute('aria-label', 'Тёмная тема');
    b.title = d ? 'Включить светлую тему' : 'Включить тёмную тему';
  }
  function toggle() {
    root.classList.add('theme-anim');
    if (isDark()) { root.removeAttribute('data-theme'); save('light'); } else { root.setAttribute('data-theme', 'dark'); save('dark'); }
    document.querySelectorAll('.theme-btn').forEach(label);
    document.querySelectorAll('.theme-row').forEach(rowLabel);
    setTimeout(function () { root.classList.remove('theme-anim'); }, 450);
  }
  /* шапка перерисовывается движком, поэтому кнопку добавляем после каждой перерисовки */
  function inject() {
    var a11y = document.querySelector('.tools .a11y-lbl');
    if (!a11y || a11y.parentNode.querySelector('.theme-btn')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'ico theme-btn';
    b.style.cssText = 'border:0;background:transparent;cursor:pointer;font:inherit';
    b.innerHTML = MOON + SUN;
    b.addEventListener('click', toggle);
    label(b);
    a11y.insertAdjacentElement('afterend', b);
  }
  function rowLabel(r) { r.setAttribute('aria-pressed', String(isDark())); r.lastChild.textContent = 'Тёмная тема: ' + (isDark() ? 'вкл.' : 'выкл.'); }
  function injectRow() {
    var panel = document.querySelector('.mnav-panel');
    if (!panel || panel.querySelector('.theme-row')) return;
    var r = document.createElement('button');
    r.type = 'button'; r.className = 'theme-row';
    r.innerHTML = MOON.replace('class="i-moon"', '') + '<span></span>';
    r.addEventListener('click', toggle);
    rowLabel(r);
    panel.appendChild(r);
  }
  function start() {
    inject(); injectRow();
    var r = document.getElementById('dc-root');
    if (r) new MutationObserver(function () { inject(); injectRow(); }).observe(r, { childList: true, subtree: false });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
