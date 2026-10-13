"""Собирает страницу «Личный кабинет» (Login.dc.html и LoginEn.dc.html).
Это макет: вход и регистрация ничего никуда не отправляют, только показывают, как это будет выглядеть.
Шапка и подвал берутся с Contacts.dc.html (русская) и MainEn.dc.html (английская).
Запуск: python make_login.py"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def chrome(src):
    s = open(src, encoding='utf-8').read()
    header = s[s.index('<div><a href="#main" class="skip">'):s.index('</header>') + len('</header>')]
    footer = s[s.index('<footer'):s.index('</footer>') + len('</footer>')]
    header = header.replace(' aria-current="page"', '')
    return header, footer


CSS = """<style>
.lg{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:32px;align-items:start;margin-top:36px;margin-bottom:72px}
.lg-card{border:1px solid var(--line);border-radius:var(--r-lg);background:#FFFFFF;padding:32px;box-shadow:var(--shadow)}
.lg-proto{display:flex;gap:10px;align-items:flex-start;padding:10px 14px;border-radius:var(--r);background:var(--bg-soft);font-size:14px;line-height:1.45;margin-bottom:22px}
.lg-proto svg{flex:none;margin-top:1px}
.lg .seg{display:grid;width:100%}
.lg-mode{grid-template-columns:1fr 1fr}
.lg-roles{grid-template-columns:repeat(4,minmax(0,1fr))}
.lg .seg button{padding:0 8px}
.lg-lbl{font-size:14px;font-weight:600;margin:22px 0 8px}
.lg form .field{margin-top:18px}
.lg .input{width:100%;box-sizing:border-box}
.lg .input[aria-invalid="true"]{border-color:#B42318}
.lg-err{color:#B42318;font-size:14px;font-weight:500}
.lg-err:empty{display:none}
.pw{position:relative}
.pw .input{padding-right:116px}
.pw button{position:absolute;right:4px;top:4px;bottom:4px;min-width:104px;border:0;border-radius:var(--r-sm);background:var(--bg-soft);font:inherit;font-size:14px;font-weight:600;color:var(--text);cursor:pointer}
.pw button:hover{background:var(--blue-soft)}
.lg-row{display:flex;justify-content:space-between;align-items:center;gap:4px 16px;flex-wrap:wrap;margin-top:12px}
.lg-chk{display:inline-flex;gap:10px;align-items:center;min-height:44px;font-size:15px;font-weight:400;cursor:pointer}
.lg-chk input{width:20px;height:20px;margin:0;flex:none;accent-color:var(--blue)}
.lg-chk.top{align-items:flex-start;margin-top:14px;line-height:1.45}
.lg-chk.top input{margin-top:2px}
.linkbtn{background:none;border:0;padding:0;min-height:44px;font:inherit;font-size:15px;color:var(--blue);text-decoration:underline;cursor:pointer}
.linkbtn:hover{color:var(--blue-dark)}
.lg-submit{width:100%;margin-top:22px}
.lg-msg{margin-top:20px;padding:16px 18px;border-radius:var(--r);background:var(--blue-soft);border-left:4px solid var(--blue);line-height:1.5}
.lg-msg:focus{outline:none}
.lg-msg a{display:inline-block;margin-top:8px;font-weight:600}
.lg-note{margin-top:18px;padding:16px 18px;border-radius:var(--r);background:var(--bg-soft);line-height:1.5}
.lg-side{border:1px solid var(--line);border-radius:var(--r-lg);background:#FFFFFF;padding:28px;box-shadow:inset 0 4px 0 var(--qc,var(--blue))}
.lg-side h2{font-size:22px}
.lg-side ul{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:12px}
.lg-side li{display:flex;gap:10px;align-items:flex-start;line-height:1.4}
.lg-side li::before{content:"";flex:none;width:8px;height:8px;margin-top:8px;border-radius:2px;background:var(--qc,var(--blue))}
.lg-help{margin-top:24px;padding-top:20px;border-top:1px solid var(--line);font-size:15px;line-height:1.6}
.lg-help a{display:inline-block;padding:2px 0}
@media (max-width:860px){.lg{grid-template-columns:1fr}}
@media (max-width:520px){.lg-card{padding:20px}.lg-side{padding:20px}.lg-roles{grid-template-columns:1fr 1fr}}
</style>
"""

INFO = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 11v6M12 7.5v.5"></path></svg>'

L = {
 'ru': dict(
  src='Contacts.dc.html', out='Login.dc.html', lang='ru', home='Main.dc.html', other='LoginEn.dc.html',
  title='Личный кабинет — УрФУ',
  desc='Единый личный кабинет УрФУ для абитуриентов, студентов, сотрудников и партнёров.',
  crumbs='<a href="Main.dc.html">Главная</a> / Личный кабинет',
  h1='Личный кабинет',
  lead='Один вход для всех: абитуриентов, студентов, сотрудников и партнёров. Вместо четырёх разных кабинетов — один.',
  proto='Это макет: вход и регистрация не подключены, введённые данные никуда не отправляются.',
  modeLbl='Вход или регистрация', mIn='Вход', mReg='Регистрация', who='Кто вы?',
  login='Логин или почта', pw='Пароль', show='Показать', hide='Скрыть', showA='Показать пароль', hideA='Скрыть пароль',
  rem='Запомнить меня', forgot='Забыли пароль?', submitIn='Войти', submitReg='Зарегистрироваться',
  name='Фамилия и имя', email='Электронная почта', pass1='Придумайте пароль', pass2='Повторите пароль', passHint='Не короче 8 символов',
  consent='Даю согласие на обработку персональных данных',
  noReg='Студентам и сотрудникам регистрироваться не нужно: логин и пароль выдаёт университет [уточнить, где и когда их получают].',
  toLogin='Перейти ко входу',
  sideTitle='Что будет в кабинете', help='Не получается войти?', helpTxt='Техподдержка',
  roles=[('abit', 'abit', 'Абитуриент'), ('student', 'student', 'Студент'), ('staff', 'staff', 'Сотрудник'), ('partner', 'intl', 'Партнёр')],
  feat={
   'abit': ['Статус заявления и согласия на зачисление', 'Мои программы и место в конкурсных списках', 'Загрузка документов онлайн', 'Сообщения приёмной комиссии'],
   'student': ['Расписание занятий', 'Оценки и электронная зачётка', 'Справки онлайн — без очереди', 'Стипендия и выплаты', 'Общежитие: договор и оплата'],
   'staff': ['Корпоративная почта', 'Документы и заявки', 'Расписание преподавателя', 'Справки и расчётный листок'],
   'partner': ['Договоры и заявки на сотрудничество', 'Совместные проекты и их статус', 'Контакты кураторов в университете']},
  eLogin='Введите логин или почту', ePass='Введите пароль', eName='Введите фамилию и имя', eEmail='Введите почту в формате name@example.ru',
  ePass1='Пароль должен быть не короче 8 символов', ePass2='Пароли не совпадают', eConsent='Нужно согласие на обработку данных',
  okIn='Здесь открылся бы ваш кабинет. Но это макет — настоящий вход пока не подключён.',
  okReg='Здесь создался бы ваш кабинет, а на почту пришло бы письмо для подтверждения. В макете это не работает.',
  okForgot='В настоящем кабинете здесь можно восстановить пароль по почте. В макете это не работает — если не получается войти, позвоните в техподдержку.',
  example='Посмотреть, как выглядит расписание →'),
 'en': dict(
  src='MainEn.dc.html', out='LoginEn.dc.html', lang='en', home='MainEn.dc.html', other='Login.dc.html',
  title='Sign in — UrFU',
  desc='One UrFU account for applicants, students, staff and partners.',
  crumbs='<a href="MainEn.dc.html">Home</a> / Sign in',
  h1='Sign in',
  lead='One account for everyone: applicants, students, staff and partners. One sign-in instead of four separate accounts.',
  proto='This is a mock-up: sign-in and registration are not connected, nothing you type is sent anywhere.',
  modeLbl='Sign in or register', mIn='Sign in', mReg='Register', who='Who are you?',
  login='Login or email', pw='Password', show='Show', hide='Hide', showA='Show password', hideA='Hide password',
  rem='Remember me', forgot='Forgot password?', submitIn='Sign in', submitReg='Create account',
  name='Full name', email='Email', pass1='Create a password', pass2='Repeat the password', passHint='At least 8 characters',
  consent='I agree to the processing of my personal data',
  noReg='Students and staff do not need to register: the university issues their login and password [check where and when].',
  toLogin='Go to sign in',
  sideTitle='What the account will have', help='Can’t sign in?', helpTxt='Tech support',
  roles=[('abit', 'abit', 'Applicant'), ('student', 'student', 'Student'), ('staff', 'staff', 'Staff'), ('partner', 'intl', 'Partner')],
  feat={
   'abit': ['Application status and consent to enrol', 'My programmes and ranking lists', 'Upload documents online', 'Messages from the Admissions Office'],
   'student': ['Class timetable', 'Grades and electronic record book', 'Certificates online, no queues', 'Scholarship and payments', 'Dormitory: contract and payment'],
   'staff': ['Corporate email', 'Documents and requests', 'Teaching timetable', 'Certificates and payslip'],
   'partner': ['Contracts and partnership requests', 'Joint projects and their status', 'Contacts of university coordinators']},
  eLogin='Enter your login or email', ePass='Enter your password', eName='Enter your full name', eEmail='Enter an email like name@example.com',
  ePass1='The password must be at least 8 characters', ePass2='The passwords do not match', eConsent='Your consent is required',
  okIn='You would be signed in here, but this is a mock-up: real sign-in is not connected yet.',
  okReg='Your account would be created here and a confirmation email sent. This does not work in the mock-up.',
  okForgot='In the real account you could reset your password by email here. This does not work in the mock-up; if you cannot sign in, call tech support.',
  example='See what the timetable looks like →'),
}


def js(v):
    return "'" + v.replace('\\', '\\\\').replace("'", "\\'") + "'"


def build(t):
    header, footer = chrome(t['src'])
    if t['lang'] == 'ru':
        header = header.replace('href="MainEn.dc.html" lang="en"', 'href="LoginEn.dc.html" lang="en"')
        footer = footer.replace('href="MainEn.dc.html" lang="en"', 'href="LoginEn.dc.html" lang="en"')
    else:
        header = header.replace('href="Main.dc.html" lang="ru"', 'href="Login.dc.html" lang="ru"')
        footer = footer.replace('href="Main.dc.html" lang="ru"', 'href="Login.dc.html" lang="ru"')
    head = f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<meta name="robots" content="noindex">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/IBMPlexSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/IBMPlexSans-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="logo-live.css">
{CSS}</head>
<body>
<template id="dc-tpl">
"""
    main = f"""<main id="main" tabindex="-1" style="outline:none"><section class="phead"><div class="wrap">
<div class="crumbs">{t['crumbs']}</div>
<h1 class="big" style="font-size:48px">{t['h1']}</h1>
<p class="muted" style="margin-top:12px;font-size:19px;max-width:720px">{t['lead']}</p>
</div></section>
<div class="wrap lg">
<div class="lg-card">
<p class="lg-proto">{INFO}<span>{t['proto']}</span></p>
<div class="seg lg-mode" role="group" aria-label="{t['modeLbl']}">
<button type="button" id="m-in" aria-pressed="{{{{isInS}}}}" onClick="{{{{toIn}}}}">{t['mIn']}</button><button type="button" id="m-reg" aria-pressed="{{{{isRegS}}}}" onClick="{{{{toReg}}}}">{t['mReg']}</button>
</div>
<p class="lg-lbl" id="who-l">{t['who']}</p>
<div class="seg lg-roles" role="group" aria-labelledby="who-l" data-role="{{{{roleKey}}}}">
<sc-for list="{{{{roles}}}}" as="r" hint-placeholder-count="4"><button type="button" id="{{{{r.id}}}}" aria-pressed="{{{{r.on}}}}" onClick="{{{{r.pick}}}}">{{{{r.label}}}}</button></sc-for>
</div>

<sc-if value="{{{{isIn}}}}" hint-placeholder-val="{{{{true}}}}"><form novalidate onSubmit="{{{{submitIn}}}}">
<div class="field"><label for="f-login">{t['login']}</label><input id="f-login" class="input" autocomplete="username" value="{{{{login}}}}" onChange="{{{{onLogin}}}}" aria-invalid="{{{{invLogin}}}}" aria-describedby="e-login"><p class="lg-err" id="e-login">{{{{eLogin}}}}</p></div>
<div class="field"><label for="f-pass">{t['pw']}</label><div class="pw"><input id="f-pass" class="input" type="{{{{pwType}}}}" autocomplete="current-password" value="{{{{pass}}}}" onChange="{{{{onPass}}}}" aria-invalid="{{{{invPass}}}}" aria-describedby="e-pass"><button type="button" id="pw-t" aria-label="{{{{pwA}}}}" onClick="{{{{togglePw}}}}">{{{{pwTxt}}}}</button></div><p class="lg-err" id="e-pass">{{{{ePass}}}}</p></div>
<div class="lg-row"><label class="lg-chk"><input type="checkbox" id="f-rem" checked="{{{{rem}}}}" onChange="{{{{onRem}}}}">{t['rem']}</label><button type="button" class="linkbtn" id="f-forgot" onClick="{{{{forgot}}}}">{t['forgot']}</button></div>
<button type="submit" class="btn lg-submit" id="f-go">{t['submitIn']}</button>
</form></sc-if>

<sc-if value="{{{{isRegOk}}}}" hint-placeholder-val="{{{{false}}}}"><form novalidate onSubmit="{{{{submitReg}}}}">
<div class="field"><label for="r-name">{t['name']}</label><input id="r-name" class="input" autocomplete="name" value="{{{{name}}}}" onChange="{{{{onName}}}}" aria-invalid="{{{{invName}}}}" aria-describedby="e-name"><p class="lg-err" id="e-name">{{{{eName}}}}</p></div>
<div class="field"><label for="r-email">{t['email']}</label><input id="r-email" class="input" type="email" autocomplete="email" value="{{{{email}}}}" onChange="{{{{onEmail}}}}" aria-invalid="{{{{invEmail}}}}" aria-describedby="e-email"><p class="lg-err" id="e-email">{{{{eEmail}}}}</p></div>
<div class="field"><label for="r-p1">{t['pass1']}</label><div class="pw"><input id="r-p1" class="input" type="{{{{pwType}}}}" autocomplete="new-password" value="{{{{p1}}}}" onChange="{{{{onP1}}}}" aria-invalid="{{{{invP1}}}}" aria-describedby="h-p1 e-p1"><button type="button" id="pw-t2" aria-label="{{{{pwA}}}}" onClick="{{{{togglePw}}}}">{{{{pwTxt}}}}</button></div><p class="muted" id="h-p1" style="font-weight:400">{t['passHint']}</p><p class="lg-err" id="e-p1">{{{{eP1}}}}</p></div>
<div class="field"><label for="r-p2">{t['pass2']}</label><input id="r-p2" class="input" type="{{{{pwType}}}}" autocomplete="new-password" value="{{{{p2}}}}" onChange="{{{{onP2}}}}" aria-invalid="{{{{invP2}}}}" aria-describedby="e-p2"><p class="lg-err" id="e-p2">{{{{eP2}}}}</p></div>
<label class="lg-chk top"><input type="checkbox" id="r-ok" checked="{{{{consent}}}}" onChange="{{{{onConsent}}}}" aria-invalid="{{{{invConsent}}}}" aria-describedby="e-ok"><span>{t['consent']}</span></label><p class="lg-err" id="e-ok">{{{{eConsent}}}}</p>
<button type="submit" class="btn lg-submit" id="r-go">{t['submitReg']}</button>
</form></sc-if>

<sc-if value="{{{{isRegNo}}}}" hint-placeholder-val="{{{{false}}}}"><div class="lg-note"><p>{t['noReg']}</p><button type="button" class="btn2" id="r-back" style="margin-top:12px" onClick="{{{{toIn}}}}">{t['toLogin']}</button></div></sc-if>

<sc-if value="{{{{hasMsg}}}}" hint-placeholder-val="{{{{false}}}}"><div class="lg-msg" id="lg-msg" tabindex="-1" role="status"><p>{{{{msg}}}}</p><sc-if value="{{{{hasEx}}}}" hint-placeholder-val="{{{{true}}}}"><a href="Schedule.dc.html">{t['example']}</a></sc-if></div></sc-if>
</div>

<aside class="lg-side" data-role="{{{{roleKey}}}}" aria-labelledby="side-h">
<h2 id="side-h">{t['sideTitle']}: {{{{roleName}}}}</h2>
<ul><sc-for list="{{{{feat}}}}" as="f" hint-placeholder-count="4"><li>{{{{f}}}}</li></sc-for></ul>
<div class="lg-help"><b>{t['help']}</b><br>{t['helpTxt']}: <a href="tel:+73432272070">+7 (343) 227-20-70</a>, <a href="mailto:support@urfu.ru">support@urfu.ru</a></div>
</aside>
</div>
</main>"""
    roles = ', '.join(f"[{js(k)}, {js(c)}, {js(n)}]" for k, c, n in t['roles'])
    feat = ', '.join(f"{k}: [{', '.join(js(x) for x in v)}]" for k, v in t['feat'].items())
    T = {k: t[k] for k in ['eLogin', 'ePass', 'eName', 'eEmail', 'ePass1', 'ePass2', 'eConsent', 'okIn', 'okReg', 'okForgot', 'show', 'hide', 'showA', 'hideA']}
    tx = ', '.join(f"{k}: {js(v)}" for k, v in T.items())
    logic = """<script type="text/x-dc" id="dc-logic">
class Component extends DCLogic {
renderVals() {
const ROLES = [""" + roles + """];
const FEAT = {""" + feat + """};
const TX = {""" + tx + """};
if (!this.state) {
  let r0 = 'student', m0 = 'in';
  try { const p = new URLSearchParams(location.search); if (FEAT[p.get('role')]) r0 = p.get('role'); if (p.get('mode') === 'reg') m0 = 'reg'; } catch (e) {}
  this.state = { role: r0, mode: m0, login: '', pass: '', rem: true, name: '', email: '', p1: '', p2: '', consent: false, err: {}, msg: '', showPw: false };
}
const s = this.state, err = s.err || {};
const canReg = s.role === 'abit' || s.role === 'partner';
const focusLater = id => { const n = document.getElementById(id); if (n) n.focus(); };
const set = (k, v) => this.setState({ [k]: v, err: { ...err, [k]: '' } });
const done = text => { this.setState({ err: {}, msg: text }); focusLater('lg-msg'); };
const fail = (e, order) => { this.setState({ err: e, msg: '' }); const first = order.find(([k]) => e[k]); if (first) focusLater(first[1]); };
const submitIn = ev => {
  ev.preventDefault();
  const e = {};
  if (!s.login.trim()) e.login = TX.eLogin;
  if (!s.pass) e.pass = TX.ePass;
  if (Object.keys(e).length) fail(e, [['login', 'f-login'], ['pass', 'f-pass']]); else done(TX.okIn);
};
const submitReg = ev => {
  ev.preventDefault();
  const e = {};
  if (!s.name.trim()) e.name = TX.eName;
  if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(s.email.trim())) e.email = TX.eEmail;
  if (s.p1.length < 8) e.p1 = TX.ePass1;
  else if (s.p2 !== s.p1) e.p2 = TX.ePass2;
  if (!s.consent) e.consent = TX.eConsent;
  if (Object.keys(e).length) fail(e, [['name', 'r-name'], ['email', 'r-email'], ['p1', 'r-p1'], ['p2', 'r-p2'], ['consent', 'r-ok']]); else done(TX.okReg);
};
const R = ROLES.find(r => r[0] === s.role) || ROLES[1];
return {
  isIn: s.mode === 'in', isRegOk: s.mode === 'reg' && canReg, isRegNo: s.mode === 'reg' && !canReg,
  isInS: String(s.mode === 'in'), isRegS: String(s.mode === 'reg'),
  toIn: () => this.setState({ mode: 'in', err: {}, msg: '' }), toReg: () => this.setState({ mode: 'reg', err: {}, msg: '' }),
  roles: ROLES.map(([k, c, label]) => ({ id: 'role-' + k, label, on: String(k === s.role), pick: () => this.setState({ role: k, err: {}, msg: '' }) })),
  roleKey: R[1], roleName: R[2], feat: FEAT[R[0]],
  login: s.login, pass: s.pass, rem: s.rem, name: s.name, email: s.email, p1: s.p1, p2: s.p2, consent: s.consent,
  onLogin: e => set('login', e.target.value), onPass: e => set('pass', e.target.value), onRem: e => this.setState({ rem: e.target.checked }),
  onName: e => set('name', e.target.value), onEmail: e => set('email', e.target.value), onP1: e => set('p1', e.target.value), onP2: e => set('p2', e.target.value),
  onConsent: e => set('consent', e.target.checked),
  pwType: s.showPw ? 'text' : 'password', pwTxt: s.showPw ? TX.hide : TX.show, pwA: s.showPw ? TX.hideA : TX.showA,
  togglePw: () => this.setState({ showPw: !s.showPw }),
  forgot: () => done(TX.okForgot),
  submitIn, submitReg,
  eLogin: err.login || '', ePass: err.pass || '', eName: err.name || '', eEmail: err.email || '', eP1: err.p1 || '', eP2: err.p2 || '', eConsent: err.consent || '',
  invLogin: String(!!err.login), invPass: String(!!err.pass), invName: String(!!err.name), invEmail: String(!!err.email), invP1: String(!!err.p1), invP2: String(!!err.p2), invConsent: String(!!err.consent),
  hasMsg: !!s.msg, msg: s.msg, hasEx: s.msg === TX.okIn
};
}
}
</script>
<script src="dc-lite.js"></script>
<script src="site.js"></script>
<script src="logo-live.js"></script>
</body>
</html>
"""
    page = head + header + main + footer + '</div>\n</template>\n<div id="dc-root"></div>\n' + logic
    open(t['out'], 'w', encoding='utf-8', newline='\n').write(page)
    print('ok', t['out'], len(page))


for t in L.values():
    build(t)
