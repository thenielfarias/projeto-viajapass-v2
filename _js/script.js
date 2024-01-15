
function googleTranslateElementInit2() {new google.translate.TranslateElement({pageLanguage: 'pt',autoDisplay: false}, 'google_translate_element2');}

eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('6 7(a,b){n{4(2.9){3 c=2.9("o");c.p(b,f,f);a.q(c)}g{3 c=2.r();a.s(\'t\'+b,c)}}u(e){}}6 h(a){4(a.8)a=a.8;4(a==\'\')v;3 b=a.w(\'|\')[1];3 c;3 d=2.x(\'y\');z(3 i=0;i<d.5;i++)4(d[i].A==\'B-C-D\')c=d[i];4(2.j(\'k\')==E||2.j(\'k\').l.5==0||c.5==0||c.l.5==0){F(6(){h(a)},G)}g{c.8=b;7(c,\'m\');7(c,\'m\')}}',43,43,'||document|var|if|length|function|GTranslateFireEvent|value|createEvent||||||true|else|doGTranslate||getElementById|google_translate_element2|innerHTML|change|try|HTMLEvents|initEvent|dispatchEvent|createEventObject|fireEvent|on|catch|return|split|getElementsByTagName|select|for|className|goog|te|combo|null|setTimeout|500'.split('|'),0,{}))

function openModal(modal) {
    document.getElementById(modal).style.display = "block";
    slidesClass = document.getElementsByClassName(modal)
}
  
function closeModal(modal) {
    document.getElementById(modal).style.display = "none";
}
  
var slideIndex = 1;
showSlides(slideIndex);
  
function plusSlides(n) {
    showSlides(slideIndex += n);
}
  
function currentSlide(n) {
    showSlides(slideIndex = n);
  } 
  
function showSlides(n) {
    var i;
    var slides = slidesClass;
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
slides[slideIndex-1].style.display = "block";
}

function redirect() {
    var userSelect = document.getElementById("select");
    var dest = userSelect.options[userSelect.selectedIndex].value;
    if (dest == "1") {
        location.replace("http://localhost/atracoes-fln.html");
    }
    if (dest == "2") {
        location.replace("http://localhost/atracoes-bc.html");
    }
}

function redirectCheckOut() {
    var userSelect = document.getElementById("select");
    var dest = userSelect.options[userSelect.selectedIndex].value;
    if (dest == "1") {
        //location.replace("views/checkout-fln.html");
        location.replace("http://localhost:3000/checkout-fln.html");
    }
    if (dest == "2") {
        //location.replace("views/checkout-bc.html");
        location.replace("http://localhost:3000/checkout-bc.html");
    }
}


