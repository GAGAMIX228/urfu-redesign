"""Видео-проход по сайту, ~60 с, 1920×1080, 25 кадров/с.
Нужен запущенный сайт: python -m http.server 8765 (из корня репозитория).
Запуск: python design-project/video/record.py [куда.mp4]

Каждый кадр снимается отдельно: прокрутка, курсор, ползунок и набор текста двигаются по кадрам,
анимации сайта замедлены под скорость съёмки — поэтому видео плавное, даже если снимок делается дольше 40 мс."""
import base64, glob, json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request, websocket
import imageio_ffmpeg
from PIL import Image

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '.preview', 'УрФУ — видео-проход.mp4')
BASE = 'http://localhost:8765/'
FPS = 25
W, H = 1920, 1080
FR = tempfile.mkdtemp(prefix='urfu-video-')
# профиль браузера — отдельно от кадров: тысячи новых файлов рядом с профилем тормозят Edge
PROF = tempfile.mkdtemp(prefix='urfu-edge-')
# каждый раз новый свободный порт: если прошлый Edge не закрылся, не подключиться к нему по ошибке
_s = socket.socket(); _s.bind(('127.0.0.1', 0)); PORT = _s.getsockname()[1]; _s.close()

# подпись внизу кадра и курсор — рисуем поверх сайта (только в верхнем окне, не во фреймах)
OVERLAY = r"""(function(){
 // скрипт запускается до появления страницы — стиль добавляем, когда у документа появится корень
 function pause(){ var r=document.head||document.documentElement; if(!r) return setTimeout(pause,0);
  var ps=document.createElement('style'); ps.textContent='.yu-tick ul,.yu-b1,.yu-b2,.yu-badge{animation-play-state:paused!important}'; r.appendChild(ps); }
 pause();
 if (window.top !== window) return;
function mk(){ if (document.getElementById('__cap')) return;
 var st=document.createElement('style'); st.textContent='#__cap{position:fixed;left:56px;bottom:52px;z-index:2147483646;max-width:1150px;padding:20px 30px 22px;border-radius:16px;background:rgba(22,17,43,.93);color:#fff;font:700 44px/1.1 "PT Sans Narrow","IBM Plex Sans",sans-serif;box-shadow:0 6px 0 rgba(0,0,0,.18);pointer-events:none}#__cap:before{content:"";position:absolute;left:30px;top:0;width:200px;height:6px;background:linear-gradient(90deg,#E0246F 0 25%,#FFC21A 25% 50%,#00B386 50% 75%,#6B2BE8 75%)}#__cap:empty{display:none}#__cur{position:fixed;left:0;top:0;width:34px;height:34px;z-index:2147483647;pointer-events:none;transform-origin:4px 4px;filter:none}';
 document.documentElement.appendChild(st);
 var c=document.createElement('div'); c.id='__cap'; document.documentElement.appendChild(c);
 var k=document.createElement('div'); k.id='__cur'; k.innerHTML='<svg viewBox="0 0 24 24" width="34" height="34"><path d="M3 2l7 19 2.6-7.6L20 11z" fill="#fff" stroke="#16112B" stroke-width="1.6" stroke-linejoin="round"/></svg>';
 k.style.transform='translate(-100px,-100px)'; document.documentElement.appendChild(k);
}
if (document.readyState==='loading') document.addEventListener('DOMContentLoaded', mk); else mk();
window.__tick=function(){var d=document.getElementById('__tk');if(!d){d=document.createElement('div');d.id='__tk';d.style.cssText='position:fixed;left:0;top:0;width:1px;height:1px;z-index:2147483647;pointer-events:none;opacity:.01';document.documentElement.appendChild(d)}d.style.background=d.style.background==='rgb(0, 0, 0)'?'rgb(1, 1, 1)':'rgb(0, 0, 0)'};
window.__setCap=function(t){mk();document.getElementById('__cap').textContent=t};
window.__setCur=function(x,y,s){mk();document.getElementById('__cur').style.transform='translate('+x+'px,'+y+'px) scale('+(s||1)+')'};
})();"""

# Windows считает невидимое окно безголового Edge закрытым и «усыпляет» отрисовку — через минуту кадры идут по 2–3 с
# или не приходят совсем. Эти флаги запрещают усыплять.
p = subprocess.Popen([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--remote-debugging-port=%d' % PORT,
                      '--disable-features=CalculateNativeWinOcclusion,UseEcoQoSForBackgroundProcess,IntensiveWakeUpThrottling',
                      '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding', '--disable-background-timer-throttling',
                      '--user-data-dir=' + PROF, 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
STEADY = "(()=>{const d=(window.top===window?document:document);document.documentElement.classList.add('rv-done');document.querySelectorAll('.rv').forEach(e=>e.classList.add('rv-in'));document.querySelectorAll('*').forEach(e=>{if(getComputedStyle(e).contentVisibility==='auto')e.style.contentVisibility='visible'});return 1})()"
failed = ''; n = [0]; frames = [0]; cur = [W * 0.6, H * 0.6]; cap = ['']
try:
    for _ in range(60):
        try:
            page = [t for t in json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % PORT)) if t['type'] == 'page'][0]; break
        except Exception:
            time.sleep(0.3)
    ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=20, suppress_origin=True)

    def cmd(m, **pr):
        n[0] += 1; want = n[0]; ws.send(json.dumps({'id': want, 'method': m, 'params': pr}))
        while True:
            try:
                r = json.loads(ws.recv())
            except websocket.WebSocketTimeoutException:
                raise SystemExit('браузер не ответил на %s (кадр %d)' % (m, frames[0]))
            if r.get('method') == 'Page.screencastFrame':  # кадр «будильника» — только подтверждаем
                n[0] += 1; ws.send(json.dumps({'id': n[0], 'method': 'Page.screencastFrameAck', 'params': {'sessionId': r['params']['sessionId']}}))
                continue
            if r.get('id') == want: return r.get('result', r)
    ev = lambda e: cmd('Runtime.evaluate', expression=e, returnByValue=True, awaitPromise=True)['result'].get('value')

    cmd('Page.enable'); cmd('Network.enable'); cmd('Network.setCacheDisabled', cacheDisabled=True)
    cmd('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1, mobile=False)
    cmd('Page.addScriptToEvaluateOnNewDocument', source=OVERLAY)
    # «будильник»: крошечный поток кадров не даёт Edge перестать рисовать; сами кадры видео — снимками ниже
    cmd('Page.startScreencast', format='jpeg', quality=10, maxWidth=64, maxHeight=36, everyNthFrame=1)

    def still(sec):
        """Неподвижная картинка (заставка): повторяем последний кадр, браузер не трогаем."""
        src = os.path.join(FR, '%05d.png' % frames[0])
        for _ in range(round(sec * FPS)):
            frames[0] += 1; shutil.copyfile(src, os.path.join(FR, '%05d.png' % frames[0]))

    def shot():
        ev('window.__tick && window.__tick()')  # без изменений на странице безголовый Edge может не отдать кадр
        d = cmd('Page.captureScreenshot', format='png')['data']
        frames[0] += 1
        open(os.path.join(FR, '%05d.png' % frames[0]), 'wb').write(base64.b64decode(d))

    def hold(sec):
        for _ in range(round(sec * FPS)): shot()

    def caption(t):
        cap[0] = t; ev('window.__setCap(%s)' % json.dumps(t))

    def place_cursor():
        ev('window.__setCur(%f,%f)' % tuple(cur))


    def last_frame():
        return Image.open(os.path.join(FR, '%05d.png' % frames[0])).convert('RGB') if frames[0] else Image.new('RGB', (W, H), 'black')

    def crossfade(prev, sec=0.4):
        """Плавный переход: от последнего кадра прошлой сцены к первому кадру новой."""
        ev('window.__tick && window.__tick()')
        d = cmd('Page.captureScreenshot', format='png')['data']
        import io
        new = Image.open(io.BytesIO(base64.b64decode(d))).convert('RGB')
        k = round(sec * FPS)
        for i in range(1, k + 1):
            frames[0] += 1
            Image.blend(prev, new, ease(i / (k + 1))).save(os.path.join(FR, '%05d.png' % frames[0]), compress_level=1)

    def fade_out(sec=0.6):
        prev = last_frame(); k = round(sec * FPS)
        for i in range(1, k + 1):
            frames[0] += 1
            Image.blend(prev, Image.new('RGB', (W, H), 'black'), ease(i / k)).save(os.path.join(FR, '%05d.png' % frames[0]), compress_level=1)

    def go(url, wait=2.2, fade=True):
        print('→', url, 'с кадра', frames[0] + 1, flush=True)
        prev = last_frame()
        cmd('Storage.clearDataForOrigin', origin=BASE.rstrip('/'), storageTypes='local_storage,session_storage')
        cmd('Page.navigate', url=url if url.startswith('http') else BASE + url); time.sleep(wait)
        ev("document.fonts.ready.then(()=>1)")
        ev(STEADY); time.sleep(0.4)
        ev('window.__setCap(%s)' % json.dumps(cap[0])); place_cursor()
        if fade: crossfade(prev)

    ease = lambda t: t * t * (3 - 2 * t)

    def scroll_to(y, sec):
        y0 = ev('scrollY')
        k = round(sec * FPS)
        for i in range(1, k + 1):
            ev('window.scrollTo({top:%f,behavior:"instant"})' % (y0 + (y - y0) * ease(i / k))); shot()

    def center(sel, frame=None):
        js = "document.querySelector(%s)" % json.dumps(sel)
        if frame: js = "document.getElementById('f').contentDocument.querySelector(%s)" % json.dumps(sel)
        return ev("(()=>{const e=%s;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,r.top]})()" % js)

    def move(x, y, sec=0.6):
        x0, y0 = cur; k = max(1, round(sec * FPS))
        for i in range(1, k + 1):
            t = ease(i / k); cur[0] = x0 + (x - x0) * t; cur[1] = y0 + (y - y0) * t
            place_cursor(); shot()

    def click(sel, sec=0.6, fade=0):
        x, y, _ = center(sel)
        move(x, y, sec)
        for s in (0.85, 0.85):
            ev('window.__setCur(%f,%f,%f)' % (x, y, s)); shot()
        cmd('Input.dispatchMouseEvent', type='mousePressed', x=x, y=y, button='left', clickCount=1)
        cmd('Input.dispatchMouseEvent', type='mouseReleased', x=x, y=y, button='left', clickCount=1)
        place_cursor()
        # страница после нажатия перестраивается (роль, тёмная схема, расписание) — плавный переход вместо рывка
        if fade: prev = last_frame(); time.sleep(0.3); crossfade(prev, fade)
        else: shot()

    def type_text(t, per=3):
        for ch in t:
            cmd('Input.insertText', text=ch)
            for _ in range(per): shot()

    def ensure_visible(sel, top=320, sec=0.9):
        y = ev("(()=>{const e=document.querySelector(%s);return e.getBoundingClientRect().top+scrollY})()" % json.dumps(sel))
        scroll_to(max(0, y - top), sec)

    # скорость анимаций сайта — под скорость съёмки
    go('Main.dc.html', fade=False)
    t0 = time.time()
    for _ in range(8): cmd('Page.captureScreenshot', format='png')
    per = (time.time() - t0) / 8
    rate = max(0.1, min(1.0, (1000 / FPS) / (per * 1000)))
    print('снимок %.0f мс' % (per * 1000), flush=True)

    # 0. Заставка
    caption(''); cur[:] = [-100, -100]; go('design-project/video/card.html', 1.5); still(4.0)
    cur[:] = [W * 0.55, H * 0.55]

    # 1. Главная под роль
    caption('Главная перестраивается под роль'); go('Main.dc.html'); hold(0.8)
    click('button[data-urole="student"]', fade=0.4); hold(2.6)
    click('button[data-urole="abit"]', fade=0.4); hold(2.0)

    # 2. Хватит ли баллов
    caption('«Хватит ли баллов?» — прямо на главной')
    ensure_visible('#calc-r', 420, 1.9)
    x, y, _ = center('#calc-r'); move(x - 40, y, 0.5)
    k = round(1.6 * FPS)
    for i in range(1, k + 1):
        v = round(240 + 35 * ease(i / k))
        ev("(()=>{const r=document.querySelector('#calc-r');r.value=%d;r.dispatchEvent(new Event('input',{bubbles:true}));const b=r.getBoundingClientRect();window.__setCur(b.left+b.width*(r.value-r.min)/(r.max-r.min),b.top+b.height/2)})()" % v)
        shot()
    hold(2.2)

    # 3. Каталог
    caption('Каталог: отметьте предметы ЕГЭ — увидите, куда проходите'); go('Catalog.dc.html'); hold(0.6)
    ensure_visible('#subj-phys', 520, 0.9)
    click('#subj-phys'); hold(0.7)
    click('#sc', 0.5); type_text('250'); hold(0.6)
    scroll_to(380, 1.0); hold(2.6)

    # 4. Поиск
    caption('Поиск понимает «общагу» и «стипуху»'); go('Search.dc.html'); hold(0.4)
    click('#sq', 0.5); ev("(()=>{const i=document.querySelector('#sq');i.value='';i.dispatchEvent(new Event('input',{bubbles:true}))})()"); hold(0.4); cmd('Input.insertText', text='общага'); hold(3.6)

    # 5. Общежития
    caption('Цена каждого общежития — по приказам УрФУ'); go('Dorms.dc.html'); hold(0.6)
    ensure_visible('#dall-h', 140, 1.6); hold(3.2)

    # 6. Расписание
    caption('Расписание группы — в один клик'); go('Schedule.dc.html'); hold(0.5)
    click('#sg-n', 0.5); type_text('140944', 2); hold(0.3)
    click('main button[type="submit"]', 0.5, fade=0.4); hold(2.8)

    # 7. Для слабовидящих
    caption('Версия для слабовидящих — на любой странице')
    click('.a11y-lbl', 0.7, fade=0.3); hold(0.8)
    click('.vi-c2', 0.6, fade=0.5); hold(2.6)

    # 8. Телефон
    caption('С телефона — так же удобно'); cur[:] = [-100, -100]
    go('design-project/video/phone.html#Main.dc.html', 3.0); hold(1.2)
    fs = lambda js: ev("(()=>{const w=document.getElementById('f').contentWindow;%s})()" % js)
    IN_FRAME = "const D=w.document;D.documentElement.classList.add('rv-done');D.querySelectorAll('.rv').forEach(e=>e.classList.add('rv-in'));D.querySelectorAll('*').forEach(e=>{if(w.getComputedStyle(e).contentVisibility==='auto')e.style.contentVisibility='visible'});return 1"
    fs(IN_FRAME); time.sleep(0.4)
    k = round(1.6 * FPS)
    for i in range(1, k + 1):
        fs("w.scrollTo({top:%f,behavior:'instant'})" % (900 * ease(i / k))); shot()
    hold(1.4)
    prev = last_frame()
    fs("w.location.href='../../Catalog.dc.html'"); time.sleep(2.2); fs(IN_FRAME); time.sleep(0.4); crossfade(prev); hold(2.6)

    # 9. Финал
    caption(''); cur[:] = [-100, -100]; go('design-project/video/card.html#end', 1.5); still(4.5); fade_out(0.8)
    print('кадров:', frames[0], '≈ %.1f с' % (frames[0] / FPS), flush=True)
except SystemExit as e:
    failed = str(e)
finally:
    # закрываем Edge целиком, вместе с дочерними процессами
    subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # процессы, которые отцепились от главного, находим по папке профиля
    subprocess.run(['powershell', '-NoProfile', '-Command',
                    "Get-CimInstance Win32_Process -Filter \"name='msedge.exe'\" | ? { $_.CommandLine -like '*%s*' } | %% { Stop-Process -Id $_.ProcessId -Force -EA SilentlyContinue }" % os.path.basename(PROF)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if failed:
    # редкий случай: Edge перестал отдавать кадры — пишем всё заново в новом браузере
    shutil.rmtree(FR, ignore_errors=True)
    att = int(os.environ.get('REC_TRY', '1'))
    print(failed, '— попытка', att, 'из 3', flush=True)
    if att >= 3: sys.exit('не удалось записать за 3 попытки')
    sys.exit(subprocess.run([sys.executable, __file__] + sys.argv[1:], env=dict(os.environ, REC_TRY=str(att + 1))).returncode)

# сборка видео
ff = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
subprocess.run([ff, '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(FR, '%05d.png'),
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], check=True)
# кадры для проверки — каждые 2 с
chk = os.path.join(HERE, '..', '..', '.preview', 'video-check'); shutil.rmtree(chk, ignore_errors=True); os.makedirs(chk)
for f in sorted(glob.glob(os.path.join(FR, '*.png')))[::FPS * 2]:
    Image.open(f).convert('RGB').resize((640, 360)).save(os.path.join(chk, os.path.basename(f)[:-4] + '.jpg'), quality=80)
if os.environ.get('KEEP'): print('кадры:', FR)
else: shutil.rmtree(FR, ignore_errors=True)
print(os.path.abspath(OUT), os.path.getsize(OUT) // 1024, 'КБ')
