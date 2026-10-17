/* Расписание: номер группы = буквы института + 6 цифр. Дефис и буквы подставляются сами.
   Работает вне движка страницы: делегирование событий + наблюдатель за перерисовкой. */
(function () {
  var KEY = 'urfu-group';
  // коды проверены по архиву системы расписания УрФУ
  var INST = { 'РИ': 'ИРИТ-РтФ', 'УГИ': 'УГИ', 'СТ': 'ИСА', 'ЭУ': 'ИнЭУ', 'ЭН': 'УралЭНИН', 'ФО': 'ИнФО' };
  var EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`", RU = 'йцукенгшщзхъфывапролджэячсмитьбюё';
  var LOOK = { A: 'А', B: 'В', C: 'С', E: 'Е', H: 'Н', K: 'К', M: 'М', O: 'О', P: 'Р', T: 'Т', X: 'Х', Y: 'У' };

  // буквы: латиница целиком → другая раскладка, смесь → похожие буквы
  function letters(v) {
    v = (v || '').replace(/[\s\-–—_]/g, '');
    if (/^[a-z\[\];',.`]+$/i.test(v)) v = v.toLowerCase().replace(/[a-z\[\];',.`]/g, function (c) { return RU.charAt(EN.indexOf(c)); });
    v = v.toUpperCase().replace(/[ABCEHKMOPTXY]/g, function (c) { return LOOK[c]; });
    return v.replace(/[^А-ЯЁ]/g, '');
  }
  // цифры и до двух букв в конце (например, «у», «ду» у заочных групп)
  function digits(v) {
    var m = (v || '').replace(/\s/g, '').match(/^(\d{0,6})(.*)$/);
    var tail = m[1].length === 6 ? letters(m[2]).slice(0, 2) : '';
    return m[1] + tail;
  }
  // разбор целого номера: «ри 140944», «hb-140944», «РИ140944»
  function split(v) {
    var m = (v || '').trim().match(/^([^\d]*?)[\s\-–—_]*(\d.*)$/);
    return m ? { p: letters(m[1]), n: digits(m[2]) } : { p: letters(v), n: '' };
  }
  function ok(g) { return /^[А-ЯЁ]{1,6}-\d{6}[А-ЯЁ]{0,2}$/.test(g); }
  function store(g) { try { localStorage.setItem(KEY, g); } catch (e) {} }
  function saved() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }

  function parts(f) {
    return { sel: f.querySelector('.sg-p'), po: f.querySelector('.sg-po'), n: f.querySelector('.sg-n'),
             hint: f.querySelector('.sg-hint'), err: f.querySelector('.sg-err'), box: f.querySelector('.sg-field') };
  }
  function prefix(x) { return x.sel.value === '*' ? letters(x.po.value) : x.sel.value; }
  function setPrefix(x, p) {
    if (INST[p] || !p) { x.sel.value = p || 'РИ'; x.po.value = ''; }
    else { x.sel.value = '*'; x.po.value = p; }
    syncOther(x);
  }
  function syncOther(x) {
    var other = x.sel.value === '*';
    x.po.hidden = !other;
    if (x.hint) x.hint.textContent = other
      ? 'Впишите буквы из номера группы — например, СТМ или РИЗ — и 6 цифр.'
      : 'Буквы ' + x.sel.value + ' — это ' + INST[x.sel.value] + '. Цифры — из студенческого билета.';
  }
  function clearErr(x) { x.box.classList.remove('bad'); x.n.removeAttribute('aria-invalid'); if (x.err) x.err.hidden = true; }

  document.addEventListener('change', function (e) {
    var t = e.target;
    if (!t.classList || !t.classList.contains('sg-p')) return;
    var x = parts(t.form);
    syncOther(x); clearErr(x);
    (x.sel.value === '*' ? x.po : x.n).focus();
  });

  document.addEventListener('input', function (e) {
    var t = e.target, x;
    if (!t.classList) return;
    if (t.classList.contains('sg-n')) {
      x = parts(t.form);
      // вставили номер целиком, с буквами в начале — разбираем на буквы и цифры
      if (/^\s*[^\d\s]/.test(t.value) && /\d/.test(t.value)) {
        var s = split(t.value);
        if (s.p) setPrefix(x, s.p);
        t.value = s.n;
      } else {
        t.value = digits(t.value);
      }
      clearErr(x);
    } else if (t.classList.contains('sg-po')) {
      t.value = letters(t.value).slice(0, 6);
      clearErr(parts(t.form));
    }
  });

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f.classList || !f.classList.contains('sg-form')) return;
    e.preventDefault();
    var x = parts(f), p = prefix(x), n = digits(x.n.value), g = p + '-' + n;
    if (!ok(g)) {
      x.box.classList.add('bad');
      x.n.setAttribute('aria-invalid', 'true');
      x.err.textContent = !p ? 'Впишите буквы группы — они в начале номера, например СТМ.'
        : n.replace(/\D/g, '').length < 6 ? 'Нужно 6 цифр — сейчас ' + n.replace(/\D/g, '').length + '. Например: ' + p + '-140944.'
        : 'Проверьте номер группы — например, ' + p + '-140944.';
      x.err.hidden = false;
      (p ? x.n : x.po).focus();
      return;
    }
    store(g);
    location.assign('Schedule.dc.html?g=' + encodeURIComponent(g));
  });

  // текущая группа: из адреса или запомненная
  function current() {
    var q = new URLSearchParams(location.search), g = q.get('g') || '';
    if (!g && q.get('n')) g = ((q.get('p') === '*' ? q.get('po') : q.get('p')) || '') + '-' + q.get('n');
    if (g) { var s = split(g); g = s.p + '-' + s.n; if (ok(g)) { store(g); return g; } }
    g = saved();
    return ok(g) ? g : '';
  }
  function fill() {
    var g = current(), s = g ? split(g) : null;
    document.querySelectorAll('.sg-form').forEach(function (f) {
      var x = parts(f);
      if (!x.sel || x.sel.dataset.ready) return;
      x.sel.dataset.ready = '1';
      setPrefix(x, s ? s.p : 'РИ');
      if (s && !x.n.value) x.n.value = s.n;
    });
  }
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(fill).observe(root, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', fill);
  fill();
})();
