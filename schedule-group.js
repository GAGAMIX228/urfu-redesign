/* Расписание: поиск по номеру группы. Работает вне движка страницы (делегирование событий). */
(function () {
  var KEY = 'urfu-group';
  var LAT = { A: 'А', B: 'В', C: 'С', E: 'Е', H: 'Н', K: 'К', M: 'М', O: 'О', P: 'Р', T: 'Т', X: 'Х', Y: 'У' };
  function norm(v) {
    v = (v || '').toUpperCase().trim().replace(/[\s–—_]+/g, '-').replace(/-+/g, '-');
    v = v.replace(/[ABCEHKMOPTXY]/g, function (c) { return LAT[c]; });
    if (/^[А-ЯЁ]{1,6}\d{6}$/.test(v)) v = v.replace(/^([А-ЯЁ]+)/, '$1-');
    return v;
  }
  function ok(v) { return /^[А-ЯЁ]{1,6}-\d{6}$/.test(v); }
  // набрали в английской раскладке: «hb-140944» → «РИ-140944»
  var EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`", RU = 'йцукенгшщзхъфывапролджэячсмитьбюё';
  function layout(v) {
    return norm(v.toLowerCase().replace(/[a-z\[\];',.`]/g, function (c) { return RU.charAt(EN.indexOf(c)); }));
  }
  function fix(v) {
    // буквы целиком латинские — скорее всего, забыли переключить раскладку
    var lat = /^[\sa-z\[\];',.`]+[\s\-–—_]*\d{6}\s*$/i.test(v);
    var a = lat ? layout(v) : norm(v), b = lat ? norm(v) : layout(v);
    return ok(a) ? a : ok(b) ? b : a;
  }
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function saved() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f.classList || !f.classList.contains('sg-form')) return;
    var inp = f.querySelector('input[name="g"]'), err = f.querySelector('.sg-err');
    var v = fix(inp.value);
    if (!ok(v)) {
      e.preventDefault();
      inp.setAttribute('aria-invalid', 'true');
      err.textContent = v ? 'Так номер группы не пишут. Нужно буквы, дефис и 6 цифр — например, РИ-140944.' : 'Введите номер группы — например, РИ-140944.';
      err.hidden = false;
      inp.focus();
      return;
    }
    inp.value = v;
    store(v);
  });
  document.addEventListener('input', function (e) {
    var t = e.target;
    if (t.name === 'g' && t.getAttribute('aria-invalid')) {
      t.removeAttribute('aria-invalid');
      var err = t.form && t.form.querySelector('.sg-err');
      if (err) err.hidden = true;
    }
  });

  // без ?g= — подставляем запомненную группу
  function fill() {
    var q = new URLSearchParams(location.search).get('g');
    if (q) { var n = fix(q); if (ok(n)) store(n); return; }
    var g = saved();
    if (!g) return;
    document.querySelectorAll('.sg-form input[name="g"]').forEach(function (i) { if (!i.value) i.value = g; });
  }
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(fill).observe(root, { childList: true });
  document.addEventListener('DOMContentLoaded', fill);
  fill();
})();
