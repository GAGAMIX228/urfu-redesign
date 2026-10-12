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
