var formEditarUsuario = document.getElementById("formEditarUsuario")

formEditarUsuario.onsubmit = function(evento) {
    //evento es el submit que estamos escuchando. Lo que queremos hacer es prevenir el evento por default
    evento.preventDefault();
    //Obtenemos la info del formulario

    var formulario = new FormData(formEditarUsuario);
    /*
    formulario {
        "email" : "arielcvcx@gmail.com"
        "password" : "123123123"
    }
    */

    fetch("/editar-usuario", {method: 'POST', body: formulario}).then(response => response.json()).then(data =>{
        if (data.message == "Edicion correcta"){
            window.location.href = "/menu-principal";
        }else{
            //crear mensaje de error
            var erroresLogin = document.getElementById("erroresEdit");
            erroresLogin.classList.add("alert");
            erroresLogin.classList.add("alert-danger");
            erroresLogin.innerText = data.message;
        }
    })   
}

var latitud = document.getElementById('latitud').value;
var longitud = document.getElementById('longitud').value;

mapboxgl.accessToken = 'pk.eyJ1IjoiYXJpZWxjdmN4IiwiYSI6ImNsdmJuNXBvYjBhbHkya3FtZ2d1dG50cTIifQ.0m8_eMRY8yqswpGtGwy8iw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [latitud, longitud],
    zoom: 13
});

new mapboxgl.Marker()
    .setLngLat([latitud, longitud])
    .addTo(map);

var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    container: 'geocoder-container',
    zoom: 14,
    flyTo: { 
        speed: 1 
    }
});
geocoder.setProximity({ longitude: longitud, latitude: latitud });

map.addControl(geocoder);

geocoder.on('result', function (ev) {
    // Actualizar el valor del campo oculto con la información de la ubicación
    document.getElementById('ubicacion').value = JSON.stringify(ev.result);
});