var formLogin = document.getElementById("formLogin")

formLogin.onsubmit = function(evento) {
    //evento es el submit que estamos escuchando. Lo que queremos hacer es prevenir el evento por default
    evento.preventDefault();
    //Obtenemos la info del formulario

    var formulario = new FormData(formLogin);
    /*
    formulario {
        "email" : "arielcvcx@gmail.com"
        "password" : "123123123"
    }
    */

    fetch("/login", {method: 'POST', body: formulario}).then(response => response.json()).then(data =>{
        if (data.message == "login correcto"){
            window.location.href = "/menu-principal";
        }else{
            //crear mensaje de error
            var erroresLogin = document.getElementById("erroresLogin");
            erroresLogin.classList.add("alert");
            erroresLogin.classList.add("alert-danger");
            erroresLogin.innerText = data.message;
        }
    })   
}