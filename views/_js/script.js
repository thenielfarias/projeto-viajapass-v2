
function googleTranslateElementInit2() {new google.translate.TranslateElement({pageLanguage: 'pt',autoDisplay: false}, 'google_translate_element2');}

eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('6 7(a,b){n{4(2.9){3 c=2.9("o");c.p(b,f,f);a.q(c)}g{3 c=2.r();a.s(\'t\'+b,c)}}u(e){}}6 h(a){4(a.8)a=a.8;4(a==\'\')v;3 b=a.w(\'|\')[1];3 c;3 d=2.x(\'y\');z(3 i=0;i<d.5;i++)4(d[i].A==\'B-C-D\')c=d[i];4(2.j(\'k\')==E||2.j(\'k\').l.5==0||c.5==0||c.l.5==0){F(6(){h(a)},G)}g{c.8=b;7(c,\'m\');7(c,\'m\')}}',43,43,'||document|var|if|length|function|GTranslateFireEvent|value|createEvent||||||true|else|doGTranslate||getElementById|google_translate_element2|innerHTML|change|try|HTMLEvents|initEvent|dispatchEvent|createEventObject|fireEvent|on|catch|return|split|getElementsByTagName|select|for|className|goog|te|combo|null|setTimeout|500'.split('|'),0,{}))

function checkName() {
    var nameInput = document.getElementById('nameInput').value;
    var name = nameInput.replace(/\s/g, '');
    var regEx = /^[a-zA-Z]+$/;
    if (name.match(regEx)) {
        return true;
    }
    else {
        document.getElementById('nameInput').style.color = 'red';
        document.getElementById('nameInput').value = 'Somente letras sem acentos';
    }
}

function isEmail() {
    var email = document.getElementById('mailInput').value;
    var re = /\S+@\S+\.\S+/;
    var validMail = re.test(email);
    if (validMail) {
        return true;
    }
    else {
        document.getElementById('mailInput').style.color = 'red';
        document.getElementById('mailInput').value = 'Digite um endereço de e-mail válido';
    }
}

function checkEmails() {
    var m1 = document.getElementById('mailInput').value;
    var m2 = document.getElementById('mailConfirm').value;
    if (m1 != m2) {
        document.getElementById('mailConfirm').style.color = 'red';
        document.getElementById('mailConfirm').value = 'Verifique o e-mail digitado';
    }
}

function checkPhone() {
    var phone = document.getElementById('telInput').value;
    if (isNaN(phone) || phone == "" || phone.length < 9) {
        document.getElementById('telInput').style.color = 'red';
        document.getElementById('telInput').value = 'Verifique o preenchimento do telefone';
    }
}

function clearField(field) {
    if (document.getElementById(field).style.color == 'red') {
        document.getElementById(field).style.color = '#212529';
        document.getElementById(field).value = '';    
    }

}

function dateFill() {
    var dateInput = document.getElementById('dateInput').value;
    if (!isNaN(dateInput)) {
        window.alert('Verifique o preenchimento da data de início para utilização do pass.');
    }
}

function openModal(modal) {
    document.getElementById(modal).style.display = "block";
}

function closeModal(modal) {
    document.getElementById(modal).style.display = "none";
    location.replace("http://localhost/index.html")
}

function calc_total() {
    var qtd = parseInt(document.getElementById('qtd').value)
    if (isNaN(qtd)) {
        qtd = 0;
    }
    else if (qtd > 6) {
        window.alert('Selecione até 6 viajantes.')
        qtd = 0;
        document.getElementById('qtd').style.color = 'red';
        document.getElementById('tot').value = 0;
    }
    var tot = qtd * 198
    var totDec = tot.toFixed(2)
    var totVir = totDec.replace(".",",")
    document.getElementById('tot').value = totVir
}

function getQtd() {
    var getInput = parseInt(document.getElementById('qtd').value);
    localStorage.setItem("qtd",getInput);
}

function payOption() {
    var radPayOpt = getRadioValue('canal');
    localStorage.setItem("canal",radPayOpt);
}   
function getRadioValue(name){
    var rads = document.getElementsByName(name);
    
    for(var i = 0; i < rads.length; i++) {
        if(rads[i].checked){
            return rads[i].value;
        }
    }
}