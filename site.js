/* УрФУ — общие мелочи для всех страниц */
/* анимация появления — только при первой загрузке, не при каждом клике */
setTimeout(function(){document.documentElement.classList.add("ready")},1500);
/* мобильное меню закрывается клавишей Esc */
document.addEventListener("keydown",function(e){if(e.key==="Escape"){var m=document.querySelector(".mnav[open]");if(m){m.open=false;m.querySelector("summary").focus();}}});
/* Enter в строке поиска на главной — перейти к результатам */
document.addEventListener("keydown",function(e){if(e.key==="Enter"&&e.target&&e.target.id==="q"){var b=e.target.closest(".search-box");var a=b&&b.querySelector("a.btn");if(a){e.preventDefault();location.href=a.href;}}});
/* Всплывающие окна: фокус внутрь, Tab не уходит на страницу, Esc закрывает, фокус возвращается на кнопку */
(function(){
  var opener=null, wasOpen=false;
  function dlg(){return document.querySelector('[role="dialog"][aria-modal="true"]');}
  function items(d){return Array.prototype.filter.call(d.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])'),function(e){return e.getClientRects().length;});}
  document.addEventListener('focusin',function(e){if(!dlg())opener=(e.target.innerText||'').trim();});
  new MutationObserver(function(){
    var d=dlg();
    if(d&&!wasOpen){wasOpen=true;var f=items(d)[0];if(f)f.focus();}
    else if(!d&&wasOpen){wasOpen=false;if(opener){var b=Array.prototype.find.call(document.querySelectorAll('button,a'),function(x){return (x.innerText||'').trim()===opener;});if(b)b.focus();}}
  }).observe(document.body,{childList:true,subtree:true});
  document.addEventListener('keydown',function(e){
    var d=dlg(); if(!d) return;
    if(e.key==='Escape'){var c=d.querySelector('[data-close]');if(c){e.preventDefault();c.click();}}
    else if(e.key==='Tab'){var it=items(d);if(!it.length)return;var a=it[0],z=it[it.length-1];
      if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}
      else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();}
      else if(!d.contains(document.activeElement)){e.preventDefault();a.focus();}}
  });
})();
/* На странице 404 стоит <base>, из-за него ссылки вида #main уводили бы на стартовую — обрабатываем их вручную */
document.addEventListener("click",function(e){if(!document.querySelector("base"))return;var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a)return;var id=a.getAttribute("href").slice(1),t=id&&document.getElementById(id);if(!t)return;e.preventDefault();t.scrollIntoView();if(t.focus)t.focus();history.replaceState(null,"",location.pathname+location.search+"#"+id);});
/* Кнопка «Наверх»: появляется после двух экранов прокрутки */
(function(){
  var b=document.createElement("button");
  var up=document.documentElement.lang==="en"?"Back to top":"Наверх";
  b.type="button";b.className="to-top";b.setAttribute("aria-label",up);b.title=up;
  b.innerHTML='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"></path></svg>';
  b.addEventListener("click",function(){
    var r=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({top:0,behavior:r?"auto":"smooth"});
    var m=document.getElementById("main");if(m)m.focus({preventScroll:true});
  });
  function upd(){b.classList.toggle("on",window.scrollY>window.innerHeight*1.5);}
  window.addEventListener("scroll",upd,{passive:true});
  if(document.body)document.body.appendChild(b);else document.addEventListener("DOMContentLoaded",function(){document.body.appendChild(b);});
  upd();
})();
/* Объявления для программ чтения с экрана («Найдено: 15 программ», «Вопрос 2 из 3»).
   Движок перерисовывает страницу целиком, и новые aria-live-блоки читалки не замечают —
   поэтому текст переносится в один постоянный блок вне перерисовки. */
(function(){
  var root=document.getElementById("dc-root");if(!root)return;
  var box=document.createElement("div");box.className="sr";box.id="sr-live";
  box.setAttribute("aria-live","polite");box.setAttribute("aria-atomic","true");
  document.body.appendChild(box);
  var last=null,t=null;
  function scan(){
    var els=root.querySelectorAll('[aria-live]:not([aria-live="off"])');
    var txt=[].map.call(els,function(e){return e.textContent.replace(/\s+/g," ").trim();}).filter(Boolean).join(". ");
    [].forEach.call(els,function(e){e.setAttribute("aria-live","off");});
    if(last===null){last=txt;return;}
    if(txt===last)return;
    last=txt;clearTimeout(t);box.textContent="";t=setTimeout(function(){box.textContent=txt;},120);
  }
  new MutationObserver(scan).observe(root,{childList:true});scan();
})();
/* Версия для слабовидящих: панель настроек по кнопке с глазом в шапке.
   Размер текста, цветовая схема, изображения, интервал. Выбор сохраняется в этом браузере и действует на всех страницах. */
(function(){
  var EN=document.documentElement.lang==="en", KEY="urfu-vi";
  var T=EN?{h:"Accessibility mode",p:"Settings are saved in this browser",fs:"Text size",c:"Colours",img:"Images",sp:"Spacing",
      fsv:["A","A+","A++"],fsl:["Normal","Large","Extra large"],cv:["Site colours","Black on white","White on black","Dark blue on light blue","Brown on beige","Green on brown"],
      imgv:["Colour","Black and white","Hide"],spv:["Normal","Medium","Large"],reset:"Reset",close:"Close"}
    :{h:"Версия для слабовидящих",p:"Настройки сохраняются в этом браузере",fs:"Размер текста",c:"Цвета",img:"Изображения",sp:"Интервал",
      fsv:["А","А+","А++"],fsl:["Обычный","Крупный","Очень крупный"],cv:["Цвета сайта","Чёрным по белому","Белым по чёрному","Тёмно-синим по голубому","Коричневым по бежевому","Зелёным по коричневому"],
      imgv:["Цветные","Ч/б","Скрыть"],spv:["Обычный","Средний","Большой"],reset:"Сбросить",close:"Закрыть"};
  var S={fs:0,c:0,img:0,sp:0};
  try{var s=JSON.parse(localStorage.getItem(KEY)||"{}");for(var k in S)if(typeof s[k]==="number")S[k]=s[k];}catch(e){}
  function apply(){
    var h=document.documentElement;
    h.className=h.className.replace(/\bvi-\w+/g,"").replace(/\s+/g," ").trim();
    if(S.fs)h.classList.add("vi-fs"+S.fs);if(S.c)h.classList.add("vi-c"+S.c);if(S.img)h.classList.add("vi-img"+S.img);if(S.sp)h.classList.add("vi-sp"+S.sp);
    try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
    if(panel)[].forEach.call(panel.querySelectorAll(".vi-b[data-k]"),function(b){b.setAttribute("aria-pressed",String(S[b.dataset.k]===+b.dataset.v));});
  }
  function group(k,label,vals,extra){
    var h='<fieldset class="vi-g"><legend>'+label+'</legend><div class="vi-row">';
    vals.forEach(function(v,i){var sw=k==="c"&&i>0;h+='<button type="button" class="vi-b'+(sw?' vi-sw vi-c'+i:'')+'" data-k="'+k+'" data-v="'+i+'"'+(sw||extra?' aria-label="'+(extra?extra[i]:v)+'" title="'+(extra?extra[i]:v)+'"':'')+'>'+(sw?"Аа":v)+'</button>';});
    return h+'</div></fieldset>';
  }
  var panel=null, back=null;
  function build(){
    panel=document.createElement("div");panel.className="vi-panel";panel.id="vi-panel";panel.hidden=true;
    panel.setAttribute("role","region");panel.setAttribute("aria-label",T.h);
    panel.innerHTML='<div class="vi-in"><div class="vi-title"><div><h2>'+T.h+'</h2><p>'+T.p+'</p></div><div class="vi-acts"><button type="button" class="vi-b" data-act="reset">'+T.reset+'</button><button type="button" class="vi-b vi-close" data-act="close">'+T.close+'</button></div></div>'
      +group("fs",T.fs,T.fsv,T.fsl)+group("c",T.c,T.cv)+group("img",T.img,T.imgv)+group("sp",T.sp,T.spv)+'</div>';
    panel.addEventListener("click",function(e){
      var b=e.target.closest(".vi-b");if(!b)return;
      if(b.dataset.act==="reset"){S={fs:0,c:0,img:0,sp:0};apply();return;}
      if(b.dataset.act==="close"){close();return;}
      S[b.dataset.k]=+b.dataset.v;apply();
    });
    panel.addEventListener("keydown",function(e){if(e.key==="Escape"){e.preventDefault();close();}});
    document.body.appendChild(panel);
  }
  function open(){if(!panel)build();back=document.activeElement;panel.hidden=false;apply();var f=panel.querySelector('.vi-b[aria-pressed="true"]')||panel.querySelector(".vi-b");if(f)f.focus();sync();}
  function close(){if(!panel)return;panel.hidden=true;sync();var cb=document.getElementById("a11y");if(back&&document.contains(back)&&back!==document.body)back.focus();else if(cb)cb.focus();}
  function sync(){var o=panel&&!panel.hidden;[].forEach.call(document.querySelectorAll(".a11y-lbl"),function(l){l.setAttribute("aria-expanded",String(!!o));});}
  /* кнопка с глазом в шапке открывает панель (раньше она включала простой «крупный режим») */
  document.addEventListener("click",function(e){
    var l=e.target.closest&&e.target.closest(".a11y-lbl");if(!l)return;
    e.preventDefault();if(panel&&!panel.hidden)close();else open();
  });
  document.addEventListener("change",function(e){if(e.target&&e.target.id==="a11y"){e.target.checked=false;if(!panel||panel.hidden)open();}});
  apply();
})();
/* Появление блоков при прокрутке и «набегающие» цифры — только при первом открытии страницы.
   Не работает, если в системе отключена анимация или включена версия для слабовидящих. */
(function(){
  var h=document.documentElement, root=document.getElementById("dc-root");
  if(!root||!("IntersectionObserver" in window))return;
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  function start(){
    if(/\bvi-/.test(h.className))return;
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("rv-in");io.unobserve(e.target);count(e.target);}});},{rootMargin:"0px 0px -8% 0px"});
    var sel="main .sec>*,main .fd-sec .wrap>*,main .card,main .fd-gem,main .yu-i,main .yu-l,main .yu-calc,main .yu-ask-list>a,main .yu-dates li,main .yu-collage";
    var vh=window.innerHeight;
    [].forEach.call(document.querySelectorAll(sel),function(el,i){
      if(el.getBoundingClientRect().top<vh*0.92){count(el);return;}
      el.classList.add("rv");el.style.transitionDelay=(i%4)*70+"ms";io.observe(el);
    });
    h.classList.add("rv-on");
    /* запасной путь: при любой прокрутке показываем всё, что уже на экране или выше */
    var tick=false;
    function sweep(){tick=false;var lim=window.innerHeight*0.98;[].forEach.call(document.querySelectorAll(".rv:not(.rv-in)"),function(el){if(el.getBoundingClientRect().top<lim){el.classList.add("rv-in");count(el);}});}
    window.addEventListener("scroll",function(){if(!tick){tick=true;requestAnimationFrame(sweep);}},{passive:true});
    window.addEventListener("resize",sweep);
    var k=0,iv=setInterval(function(){sweep();if(++k>90||!document.querySelector(".rv:not(.rv-in)"))clearInterval(iv);},1000);
    /* после первой перерисовки (клик по фильтру и т. п.) всё просто видно */
    new MutationObserver(function(){h.classList.add("rv-done");}).observe(root,{childList:true});
  }
  function count(el){
    [].forEach.call(el.querySelectorAll?el.querySelectorAll("[data-count]"):[],function(n){
      var to=parseInt(n.getAttribute("data-count"),10);if(isNaN(to)||n.dataset.done)return;n.dataset.done=1;
      var from=to>1000?to-120:0,t0=null;
      function step(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1100);n.textContent=Math.round(from+(to-from)*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(step);}
      requestAnimationFrame(step);
    });
  }
  if(root.children.length)setTimeout(start,30);else new MutationObserver(function(m,o){o.disconnect();setTimeout(start,30);}).observe(root,{childList:true});
})();
/* Нижнее меню на телефоне — как в приложении: главная, поиск, каталог, расписание, кабинет */
(function(){
  if(!document.querySelector(".hd")||document.querySelector(".phone"))return;
  var EN=document.documentElement.lang==="en";
  var I={home:'<path d="M3 11l9-7 9 7v9h-6v-6H9v6H3z"/>',search:'<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',cat:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h10M7 13h10M7 17h6"/>',
    cal:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',user:'<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>'};
  var L=EN?[["MainEn.dc.html","home","Home"],["Search.dc.html","search","Search"],["CatalogEn.dc.html","cat","Programmes"],["Schedule.dc.html","cal","Timetable"],["LoginEn.dc.html","user","Sign in"]]
          :[["Main.dc.html","home","Главная"],["Search.dc.html","search","Поиск"],["Catalog.dc.html","cat","Каталог"],["Schedule.dc.html","cal","Расписание"],["Login.dc.html","user","Кабинет"]];
  var here=(location.pathname.split("/").pop()||"index.html");
  var nav=document.createElement("nav");nav.className="tabbar";nav.setAttribute("aria-label",EN?"Quick menu":"Быстрое меню");
  nav.innerHTML=L.map(function(x){var on=here===x[0];return '<a href="'+x[0]+'"'+(on?' aria-current="page"':'')+'><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+I[x[1]]+'</svg>'+x[2]+'</a>';}).join("");
  document.body.appendChild(nav);document.documentElement.classList.add("has-tabbar");
})();
/* Кнопка «Поделиться»: на телефоне — системное меню, на компьютере — копируем ссылку.
   data-share="" — текущий адрес; data-share="?g=…" — адрес с параметрами. */
document.addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('[data-share]');
  if (!b) return;
  var extra = b.getAttribute('data-share') || '';
  var url = extra ? location.href.split('?')[0].split('#')[0] + extra : location.href;
  function done(t) {
    var old = document.querySelector('.share-ok'); if (old) old.remove();
    var m = document.createElement('div'); m.className = 'share-ok'; m.setAttribute('role', 'status'); m.textContent = t;
    document.body.appendChild(m); setTimeout(function () { m.remove(); }, 2600);
  }
  if (navigator.share && matchMedia('(pointer:coarse)').matches) { navigator.share({ title: document.title, url: url }).catch(function () {}); return; }
  if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { done('Ссылка скопирована'); }, function () { done(url); });
  else done(url);
});
/* Быстрый поиск с клавиатуры: Ctrl+K (⌘K на Mac) или «/» — где угодно, кроме полей ввода */
document.addEventListener('keydown', function (e) {
  var t = e.target, typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
  var k = (e.key || '').toLowerCase();
  var combo = (e.ctrlKey || e.metaKey) && (k === 'k' || k === 'л');
  if (!combo && !(k === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey)) return;
  e.preventDefault();
  var q = document.querySelector('#search-q, .srch-in input, input[type=search]');
  if (q && /Search\.dc\.html$/.test(location.pathname)) { q.focus(); q.select && q.select(); return; }
  location.href = 'Search.dc.html';
});
/* подсказка о сочетании клавиш у кнопки поиска в шапке */
(function () {
  function hint() { [].forEach.call(document.querySelectorAll('.hd a.ico[href="Search.dc.html"]'), function (a) { if (!a.title) a.title = 'Поиск (Ctrl+K)'; a.setAttribute('aria-keyshortcuts', 'Control+K'); }); }
  var root = document.getElementById('dc-root'); if (root) new MutationObserver(hint).observe(root, { childList: true }); hint();
})();

/* Списки со сроками: data-prune на списке, data-end (и data-start) на пунктах — прошедшее скрываем сами.
   data-max — сколько пунктов показать; [data-prune-empty] рядом показывается, когда не осталось ничего. */
(function () {
  function today() { var t = new Date(); return t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0'); }
  function prune() {
    var d = today();
    [].forEach.call(document.querySelectorAll('[data-prune]'), function (list) {
      var max = Number(list.getAttribute('data-max')) || 99, shown = 0;
      [].forEach.call(list.querySelectorAll('[data-end]'), function (li) {
        var keep = li.getAttribute('data-end') >= d && (li.getAttribute('data-start') || '') <= d && shown < max;
        if (keep) shown++;
        if (li.hidden !== !keep) li.hidden = !keep;
      });
      var box = list.parentElement, empty = box && box.querySelector('[data-prune-empty]');
      if (empty && empty.hidden !== shown > 0) empty.hidden = shown > 0;
    });
  }
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(prune).observe(root, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', prune);
  prune();
})();

/* Фото ниже первого экрана: data-bg="photos/…" — картинка грузится, только когда до неё почти долистали. */
(function () {
  function show(el) { el.style.setProperty('--img', "url('" + el.getAttribute('data-bg') + "')"); el.setAttribute('data-bg-on', ''); }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); show(e.target); } });
  }, { rootMargin: '600px 0px' }) : null;
  function scan() {
    [].forEach.call(document.querySelectorAll('[data-bg]:not([data-bg-on]):not([data-bg-wait])'), function (el) {
      if (io) { el.setAttribute('data-bg-wait', ''); io.observe(el); } else show(el);
    });
  }
  var root = document.getElementById('dc-root');
  if (root) new MutationObserver(scan).observe(root, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', scan);
  scan();
})();
