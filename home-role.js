/* Главная под роль: «Я — поступаю / учусь / работаю / International».
   Роль запоминается в браузере; порядок блоков и заголовки меняет CSS по html[data-urole].
   Работает вне движка страницы: делегирование событий + наблюдатель за перерисовкой. */
(function () {
  var KEY = 'urfu-role', ROLES = ['abit', 'student', 'staff', 'partner', 'intl'];
  var role = '';
  try { role = localStorage.getItem(KEY) || ''; } catch (e) {}
  // ссылка вида Main.dc.html?role=student сразу открывает главную под роль
  var qr = new URLSearchParams(location.search).get('role');
  if (qr && ROLES.indexOf(qr) !== -1) { role = qr; try { localStorage.setItem(KEY, role); } catch (e) {} }
  if (ROLES.indexOf(role) === -1) role = '';
  // пример расписания — тот же, что на странице «Расписание»
  var T = [['08:30', '10:00'], ['10:15', '11:45'], ['12:00', '13:30'], ['14:15', '15:45'], ['16:00', '17:30']];
  var PLAN = [
    [[0, 'Математический анализ', 'Лекция'], [1, 'Программирование', 'Практика'], [2, 'Английский язык', 'Практика']],
    [[1, 'Физика', 'Лекция'], [2, 'Алгоритмы и структуры данных', 'Лабораторная'], [3, 'Физическая культура', 'Практика']],
    [[0, 'Основы российской государственности', 'Семинар'], [1, 'Математический анализ', 'Практика']],
    [[0, 'Программирование', 'Лекция'], [1, 'Программирование', 'Лабораторная'], [2, 'Физика', 'Практика'], [3, 'История России', 'Лекция']],
    [[1, 'Алгебра и геометрия', 'Лекция'], [2, 'Алгебра и геометрия', 'Практика']],
    [], []
  ];

  function apply() {
    var html = document.documentElement;
    if (role) html.setAttribute('data-urole', role); else html.removeAttribute('data-urole');
    document.querySelectorAll('.yu-who-b').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-urole') === role));
    });
    fill();
  }

  function setText(sel, v) { document.querySelectorAll(sel).forEach(function (el) { if (el.textContent !== v) el.textContent = v; }); }

  function fill() {
    // абитуриент: дни до 20 июня
    var now = new Date(), y = now.getFullYear();
    var t = new Date(y, 5, 20); if (now > new Date(y, 7, 20)) t = new Date(y + 1, 5, 20);
    var d = Math.max(0, Math.ceil((t - new Date(y, now.getMonth(), now.getDate())) / 864e5));
    var w = (d % 10 === 1 && d % 100 !== 11) ? 'день' : (d % 10 >= 2 && d % 10 <= 4 && (d % 100 < 12 || d % 100 > 14)) ? 'дня' : 'дней';
    setText('[data-me="days"]', String(d));
    setText('[data-me="daysw"]', w + ' до начала приёма документов');
    // студент: пары на сегодня для запомненной группы
    var g = ''; try { g = localStorage.getItem('urfu-group') || ''; } catch (e) {}
    var wd = (now.getDay() + 6) % 7;
    setText('[data-me="grp"]', g ? 'Группа ' + g : 'Пример расписания');
    document.querySelectorAll('[data-me="grpbtn"]').forEach(function (a) {
      var txt = g ? 'Расписание на неделю' : 'Укажите свою группу';
      if (a.textContent !== txt) a.textContent = txt;
    });
    // сегодня пар нет — показываем ближайший учебный день
    var DN = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье'];
    var day = wd, k = 0;
    while (!PLAN[day].length && k < 7) { day = (day + 1) % 7; k++; }
    setText('[data-me="dayk"]', day === wd ? 'Сегодня' : 'Сегодня пар нет · в ' + DN[day]);
    document.querySelectorAll('[data-me="pairs"]').forEach(function (ul) {
      if (ul.getAttribute('data-day') === String(day)) return;
      ul.setAttribute('data-day', String(day));
      var ps = PLAN[day];
      ul.innerHTML = '';
      if (!ps.length) { var li = document.createElement('li'); li.className = 'me-free'; li.textContent = 'Пар нет — отдыхайте.'; ul.appendChild(li); return; }
      ps.forEach(function (p) {
        var li = document.createElement('li'), tm = document.createElement('span'), b = document.createElement('b');
        tm.textContent = T[p[0]][0]; b.textContent = p[1];
        li.appendChild(tm); li.appendChild(b); ul.appendChild(li);
      });
    });
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-urole]');
    if (!b || !(b.classList.contains('yu-who-b') || b.classList.contains('me-reset') || b.classList.contains('fd-pick'))) return;
    var r = b.getAttribute('data-urole');
    role = (r === role && b.classList.contains('yu-who-b')) ? '' : r;
    try { if (role) localStorage.setItem(KEY, role); else localStorage.removeItem(KEY); } catch (err) {}
    apply();
    if (b.classList.contains('me-reset') || b.classList.contains('fd-pick')) {
      var sec = document.getElementById('roles-h'); if (sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(function () { apply(); }).observe(root, { childList: true });
  document.addEventListener('DOMContentLoaded', apply);
  apply();
})();

/* «Этой осенью»: прошедшие сроки скрываем, показываем не больше пяти ближайших. */
(function () {
  function prune() {
    var list = document.querySelector('.yu-now'); if (!list) return;
    var t = new Date(), today = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0'), shown = 0;
    list.querySelectorAll('li[data-end]').forEach(function (li) {
      var keep = li.getAttribute('data-end') >= today && (li.getAttribute('data-start') || '') <= today && shown < 5;
      if (keep) shown++;
      if (li.hidden !== !keep) li.hidden = !keep;
    });
    var sec = list.closest('section'); if (sec && sec.hidden !== !shown) sec.hidden = !shown;
  }
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(prune).observe(root, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', prune);
  prune();
})();
