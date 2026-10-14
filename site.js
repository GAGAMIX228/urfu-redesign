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
