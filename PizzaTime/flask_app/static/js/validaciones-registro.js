var formRegistro = document.getElementById("formRegistro")

formRegistro.onsubmit = function (evento) {

    evento.preventDefault();

    var formulario = new FormData(formRegistro);

    fetch("/register", { method: 'POST', body: formulario }).then(response => response.json()).then(data => {
        if (data.message == "registro correcto") {
            window.location.href = "/menu-principal";
        } else {
            var erroresRegistro = document.getElementById("erroresRegistro");
            erroresRegistro.classList.add('alert');
            erroresRegistro.classList.add('alert-danger');
            erroresRegistro.innerText = data.message;
        }
    })
}

mapboxgl.accessToken = 'pk.eyJ1IjoiYXJpZWxjdmN4IiwiYSI6ImNsdmJuNXBvYjBhbHkya3FtZ2d1dG50cTIifQ.0m8_eMRY8yqswpGtGwy8iw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-70.738129,-33.710423], // Lo deje centrado en mi casa :p
    zoom: 9
});

var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    container: 'geocoder-container'
});

map.addControl(geocoder);

geocoder.on('result', function (ev) {
    map.flyTo({
        center: ev.result.geometry.coordinates,
        zoom: 14
    });
    // Actualizar el valor del campo oculto con la información de la ubicación
    document.getElementById('ubicacion').value = JSON.stringify(ev.result);
});