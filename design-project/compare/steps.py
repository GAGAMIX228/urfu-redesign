"""Робот проходит 8 задач из «Концепции» на опубликованном прототипе: считает нажатия до ответа
и проверяет, что ответ действительно появился на экране (без прокрутки или после неё — пишем отдельно).
python design-project/compare/steps.py [адрес сайта]"""
import json, os, re, socket, tempfile, subprocess, sys, time, urllib.request, websocket

BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://gagamix228.github.io/urfu-redesign/'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
DESK = bool(os.environ.get('DESK'))
W, H = (1440, 900) if DESK else (390, 844)  # компьютер или телефон

# задача: (название, шаги, что должно появиться). Шаг: ('click', css) — нажатие; ('type', css, текст) — ввод
TASKS = [
    ('Хватит ли моих баллов на бюджет', [], r'Хватит ли баллов'),
    ('Когда подавать документы', [], r'Приём документов — с 20 июня'),
    ('Сколько стоит обучение', [('click', 'a[href="Catalog.dc.html"]')], r'\d[\d\s]*\d\s?₽'),
    ('Адрес общежития', [('click', 'a[href^="Dorms.dc.html"]')], r'ул\.\s?[А-ЯЁ][а-яё]+,?\s?\d+'),
    ('Сколько стоит общежитие', [('click', 'a[href^="Dorms.dc.html"]')], r'в месяц'),
    ('Расписание своей группы', [('click', 'a[href="Schedule.dc.html"]'), ('type', '.sg-n', '140944'),
                                 ('click', '.sg-form button[type="submit"]')], r'РИ-140944'),
    ('Телефон приёмной комиссии', [], r'\+7 \(343\) 375-44-74\s*Приёмная комиссия'),
    ('Версия для слабовидящих', [('click', '.a11y-lbl')], r'Версия для слабовидящих'),
]

s = socket.socket(); s.bind(('127.0.0.1', 0)); PORT = s.getsockname()[1]; s.close()
p = subprocess.Popen([EDGE, '--headless=new', '--disable-gpu', '--no-first-run', '--remote-debugging-port=%d' % PORT,
                      '--disable-features=CalculateNativeWinOcclusion', '--user-data-dir=' + tempfile.mkdtemp(prefix='urfu-edge-'),
                      'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
rows = []
try:
    for _ in range(60):
        try: pg = [t for t in json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % PORT)) if t['type'] == 'page'][0]; break
        except Exception: time.sleep(0.3)
    ws = websocket.create_connection(pg['webSocketDebuggerUrl'], timeout=60, suppress_origin=True); n = [0]
    def cmd(m, **pr):
        n[0] += 1; ws.send(json.dumps({'id': n[0], 'method': m, 'params': pr}))
        while True:
            r = json.loads(ws.recv())
            if r.get('id') == n[0]: return r.get('result', r)
    ev = lambda e: cmd('Runtime.evaluate', expression=e, returnByValue=True, awaitPromise=True)['result'].get('value')
    cmd('Page.enable'); cmd('Network.enable'); cmd('Network.setCacheDisabled', cacheDisabled=True)
    cmd('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1 if DESK else 2, mobile=not DESK)
    def settle():
        time.sleep(0.4)
        for _ in range(40):
            if ev('document.readyState') == 'complete' and ev("!!document.querySelector('#dc-root') && document.querySelector('#dc-root').children.length > 0"): break
            time.sleep(0.25)
        time.sleep(0.6)
    # текст на экране и на всей странице
    SEEN = """(re => { const rx = new RegExp(re); const vis = [];
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) { const n = w.currentNode, el = n.parentElement; if (!el || !n.textContent.trim()) continue;
        const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        const r = el.getBoundingClientRect(); if (r.width && r.bottom > 0 && r.top < innerHeight) vis.push(n.textContent); }
      return { screen: rx.test(vis.join(' ').replace(/\\s+/g, ' ')), page: rx.test(document.body.innerText.replace(/\\s+/g, ' ')) }; })(%s)"""
    for name, steps, answer in TASKS:
        if os.environ.get('ONLY') and os.environ['ONLY'] not in name: continue
        cmd('Storage.clearDataForOrigin', origin=re.match(r'https?://[^/]+', BASE).group(0), storageTypes='all')
        cmd('Page.navigate', url=BASE + 'Main.dc.html'); settle()
        t0 = time.time(); clicks = 0; pages = 1; err = ''
        for st in steps:
            if st[0] == 'click':
                # первый элемент, который реально виден и не закрыт другим (как палец на телефоне)
                pos = ev("""(() => { for (const e of document.querySelectorAll(%s)) { if (!e.getClientRects().length) continue;
                    e.scrollIntoView({block: 'center'}); const r = e.getBoundingClientRect(); const x = r.left + r.width / 2, y = r.top + r.height / 2;
                    const hit = document.elementFromPoint(x, y); if (hit && (hit === e || e.contains(hit))) return [x, y]; } return null; })()""" % json.dumps(st[1]))
                if not pos:
                    err = 'нет элемента ' + st[1] + ' ' + json.dumps(ev("""[...document.querySelectorAll(%s)].map(e => { const r = e.getBoundingClientRect();
                        const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return [e.textContent.trim().slice(0, 20), Math.round(r.top), Math.round(r.width), h && (h.className || h.tagName)]; })""" % json.dumps(st[1])), ensure_ascii=False); break
                url0 = ev('location.href')
                for t in ('mousePressed', 'mouseReleased'):
                    cmd('Input.dispatchMouseEvent', type=t, x=pos[0], y=pos[1], button='left', clickCount=1)
                clicks += 1; settle()
                if ev('location.href') != url0: pages += 1
            else:
                # вводим в первое видимое поле (у телефона и компьютера разные формы)
                ok = ev("""(() => { const e = [...document.querySelectorAll(%s)].find(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
                    if (!e) return false; e.scrollIntoView({block: 'center'}); e.focus(); return true; })()""" % json.dumps(st[1]))
                if not ok: err = 'нет поля ' + st[1]; break
                cmd('Input.insertText', text=st[2])
        if os.environ.get('DUMP') and os.environ['DUMP'] in name: print(ev('location.href'), ev('document.body.innerText.slice(0, 1500)'))
        ev('scrollTo(0,0)'); time.sleep(0.3)
        seen = ev(SEEN % json.dumps(answer)) or {}; scrolls = 0
        while seen.get('page') and not seen.get('screen') and scrolls < 30:
            ev('scrollBy(0, innerHeight * 0.8)'); time.sleep(0.35); scrolls += 1
            seen = ev(SEEN % json.dumps(answer)) or {}
        rows.append((name, clicks, pages, scrolls, bool(seen.get('screen')), err))
        print('%-32s нажатий %d, страниц %d, прокруток экрана %d, ответ найден: %s %s' %
              (name, clicks, pages, scrolls, 'да' if seen.get('screen') else 'НЕТ', err), flush=True)
finally:
    subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps-desktop.json' if DESK else 'steps-phone.json')
json.dump([dict(zip(('задача', 'нажатий', 'страниц', 'прокруток', 'ответ_найден', 'ошибка'), r)) for r in rows],
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('сохранено:', out)
