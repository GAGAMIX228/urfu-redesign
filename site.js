/* УрФУ — общие мелочи для всех страниц */
/* анимация появления — только при первой загрузке, не при каждом клике */
setTimeout(function(){document.documentElement.classList.add("ready")},1500);
/* мобильное меню закрывается клавишей Esc */
document.addEventListener("keydown",function(e){if(e.key==="Escape"){var m=document.querySelector(".mnav[open]");if(m){m.open=false;m.querySelector("summary").focus();}}});
/* Enter в строке поиска на главной — перейти к результатам */
document.addEventListener("keydown",function(e){if(e.key==="Enter"&&e.target&&e.target.id==="q"){var b=e.target.closest(".search-box");var a=b&&b.querySelector("a.btn");if(a){e.preventDefault();location.href=a.href;}}});
