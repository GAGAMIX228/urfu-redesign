"""Снимки экранов для PDF «Дизайн-проект».
Нужен запущенный сайт: python -m http.server 8765 (из корня репозитория).
Запуск: python design-project/shoot.py [имя ...]  — без имён снимает всё."""
import base64, json, os, socket, subprocess, sys, time, urllib.request, websocket

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'img')
BASE = 'http://localhost:8765/'
os.makedirs(OUT, exist_ok=True)

OPEN_A11Y = "(()=>{const c=document.getElementById('a11y');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))})()"
OPEN_MENU = "document.querySelector('details.mnav').open=true"

# имя, адрес, ширина, высота, что сделать перед снимком, к какому элементу прокрутить
SHOTS = [
    ('d-main', 'Main.dc.html', 1440, 900, None, None),
    ('d-main-abit', 'Main.dc.html?role=abit', 1440, 900, None, None),
    ('d-main-student', 'Main.dc.html?role=student', 1440, 900, None, None),
    ('d-a11y', 'Main.dc.html', 1440, 900, OPEN_A11Y, None),
    ('t-catalog', 'Catalog.dc.html', 1440, 1800, None, None),
    ('t-program', 'Program.dc.html?p=Программная инженерия', 1440, 1800, None, None),
    ('t-admission', 'Admission.dc.html', 1440, 1800, None, None),
    ('t-schedule', 'Schedule.dc.html', 1440, 2050, None, None),
    ('t-cabinet', 'Cabinet.dc.html', 1440, 2050, None, None),
    ('t-help', 'Help.dc.html', 1440, 2050, None, None),
    ('t-dorms', 'Dorms.dc.html', 1440, 2050, None, None),
    ('m-main', 'Main.dc.html', 390, 844, None, None),
    ('m-catalog', 'Catalog.dc.html', 390, 844, None, None),
    ('m-schedule', 'Schedule.dc.html', 390, 844, None, None),
    ('m-cabinet', 'Cabinet.dc.html', 390, 844, None, None),
    ('m-dorms', 'Dorms.dc.html', 390, 844, None, None),
    ('m-menu', 'Main.dc.html', 390, 844, OPEN_MENU, None),
    ('old-urfu', 'https://web.archive.org/web/20261012000000if_/https://urfu.ru/ru/', 1440, 900, None, None),
]
only = set(sys.argv[1:])

# каждый раз новый свободный порт и Edge без «усыпления» скрытого окна (см. video/record.py)
_s = socket.socket(); _s.bind(('127.0.0.1', 0)); PORT = _s.getsockname()[1]; _s.close()
p = subprocess.Popen([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
                      '--remote-debugging-port=%d' % PORT, '--disable-features=CalculateNativeWinOcclusion,UseEcoQoSForBackgroundProcess',
                      '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding', '--user-data-dir=' + os.path.join(os.environ.get('TEMP', HERE), 'edge-dp-shoot'),
                      'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try:
            page = [t for t in json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % PORT)) if t['type'] == 'page'][0]; break
        except Exception:
            time.sleep(0.3)
    ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=120, suppress_origin=True); n = [0]

    def cmd(m, **pr):
        n[0] += 1; ws.send(json.dumps({'id': n[0], 'method': m, 'params': pr}))
        while True:
            r = json.loads(ws.recv())
            if r.get('id') == n[0]: return r.get('result', r)
    ev = lambda e: cmd('Runtime.evaluate', expression=e, returnByValue=True)['result'].get('value')
    cmd('Page.enable'); cmd('Network.enable'); cmd('Network.setCacheDisabled', cacheDisabled=True)
    cmd('Emulation.setEmulatedMedia', features=[{'name': 'prefers-reduced-motion', 'value': 'reduce'}])

    for name, url, w, h, js, scroll_to in SHOTS:
        if only and name not in only: continue
        mobile = w < 600
        cmd('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=3 if mobile else 1.5, mobile=mobile)
        cmd('Storage.clearDataForOrigin', origin=BASE.rstrip('/'), storageTypes='local_storage,session_storage')
        cmd('Page.navigate', url=url if url.startswith('http') else BASE + url)
        time.sleep(30 if url.startswith('http') else 2.5)
        ev("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
        if js: ev(js); time.sleep(0.8)
        if scroll_to: ev(f"document.querySelector('{scroll_to}').scrollIntoView()"); time.sleep(0.6)
        d = cmd('Page.captureScreenshot', format='jpeg', quality=82)['data']
        open(os.path.join(OUT, name + '.jpg'), 'wb').write(base64.b64decode(d))
        print(name, os.path.getsize(os.path.join(OUT, name + '.jpg')) // 1024, 'КБ')
finally:
    # закрываем Edge целиком, вместе с дочерними процессами
    subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
