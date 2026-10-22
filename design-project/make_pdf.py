"""Собирает PDF «Дизайн-проект» из DesignProject.html через Edge.
Нужен запущенный сайт: python -m http.server 8765 (из корня репозитория).
Запуск: python design-project/make_pdf.py [куда сохранить.pdf]"""
import base64, json, os, socket, subprocess, sys, time, urllib.request, websocket

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '.preview', 'УрФУ — дизайн-проект.pdf')

# каждый раз новый свободный порт и Edge без «усыпления» скрытого окна (см. video/record.py)
_s = socket.socket(); _s.bind(('127.0.0.1', 0)); PORT = _s.getsockname()[1]; _s.close()
p = subprocess.Popen([EDGE, '--headless=new', '--disable-gpu', '--no-first-run', '--remote-debugging-port=%d' % PORT, '--disable-features=CalculateNativeWinOcclusion,UseEcoQoSForBackgroundProcess',
                      '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding',
                      '--user-data-dir=' + os.path.join(os.environ.get('TEMP', HERE), 'edge-dp-pdf'), 'about:blank'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try:
            page = [t for t in json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % PORT)) if t['type'] == 'page'][0]; break
        except Exception:
            time.sleep(0.3)
    ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=180, suppress_origin=True); n = [0]

    def cmd(m, **pr):
        n[0] += 1; ws.send(json.dumps({'id': n[0], 'method': m, 'params': pr}))
        while True:
            r = json.loads(ws.recv())
            if r.get('id') == n[0]: return r.get('result', r)
    ev = lambda e: cmd('Runtime.evaluate', expression=e, returnByValue=True, awaitPromise=True)['result'].get('value')
    cmd('Page.enable'); cmd('Network.enable'); cmd('Network.setCacheDisabled', cacheDisabled=True)
    cmd('Page.navigate', url='http://localhost:8765/design-project/DesignProject.html'); time.sleep(2)
    ev("document.fonts.ready.then(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))))")
    # проверка: ничего не вылезает за край листа
    over = ev("""[...document.querySelectorAll('.s')].map((s,i)=>{const b=s.getBoundingClientRect();
      const bad=[...s.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();
        return r.width&&!e.closest('.shots,.bg')&&(r.bottom>b.bottom-1||r.right>b.right+1)}).map(e=>e.className||e.tagName);
      return bad.length?(i+1)+': '+[...new Set(bad)].slice(0,5).join(', '):''}).filter(Boolean)""")
    print('вылезает:', over or 'ничего')
    d = cmd('Page.printToPDF', printBackground=True, preferCSSPageSize=True, marginTop=0, marginBottom=0, marginLeft=0, marginRight=0)['data']
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    open(OUT, 'wb').write(base64.b64decode(d))
    print(os.path.abspath(OUT), os.path.getsize(OUT) // 1024, 'КБ')
finally:
    # закрываем Edge целиком, вместе с дочерними процессами
    subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
