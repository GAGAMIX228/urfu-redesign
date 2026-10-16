/* Карта кампусов на странице «Кампус и общежития»: вкладки, фильтр по типу места, подсветка выбранного места.
   Работает отдельно от движка страниц; после перерисовки состояние восстанавливается. */
(function () {
  var st = { area: 'vtuz', cat: 'all', n: null };
  function apply() {
    var box = document.querySelector('.cm'); if (!box) return;
    [].forEach.call(box.querySelectorAll('.cm-tab'), function (b) { b.setAttribute('aria-pressed', String(b.dataset.area === st.area)); });
    [].forEach.call(box.querySelectorAll('.cm-cat'), function (b) { b.setAttribute('aria-pressed', String(b.dataset.cat === st.cat)); });
    [].forEach.call(box.querySelectorAll('.cm-area'), function (a) {
      a.hidden = a.dataset.area !== st.area;
      [].forEach.call(a.querySelectorAll('[data-cat]'), function (el) {
        var off = st.cat !== 'all' && el.dataset.cat !== st.cat;
        el.classList.toggle('cm-off', off);
        var on = a.dataset.area === st.area && el.dataset.n === String(st.n);
        el.classList.toggle('cm-on', on);
        if (el.tagName === 'LI') { var b = el.querySelector('button'); if (b) b.setAttribute('aria-pressed', String(on)); }
      });
    });
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('.cm-tab,.cm-cat,.cm-it,.cm-pin'); if (!t) return;
    if (t.classList.contains('cm-tab')) { st.area = t.dataset.area; st.n = null; }
    else if (t.classList.contains('cm-cat')) { st.cat = t.dataset.cat; st.n = null; }
    else if (t.classList.contains('cm-it')) { var n = t.closest('li').dataset.n; st.n = st.n === n ? null : n; }
    else { st.n = t.dataset.n; var li = document.querySelector('.cm-area:not([hidden]) li[data-n="' + st.n + '"]'); if (li) li.scrollIntoView({ block: 'nearest' }); }
    apply();
  });
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(apply).observe(root, { childList: true });
  apply();
})();
