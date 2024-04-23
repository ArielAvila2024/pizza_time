var spans = document.querySelectorAll('#sub_total');
var valores = 0;
spans.forEach(function (span) {
    valores = valores + parseInt(span.innerText)
});

var total = valores

document.getElementById('total').innerHTML = total;
document.getElementById('hidden_total').value = total;


document.getElementById('formDetallePedido').addEventListener('submit', function(event) {
    event.preventDefault(); 
    var message = "";
    if (total == 0) {
        message = 'Parece que aún no haz hecho ningún pedido, por favor ingresa un pedido';

        Swal.fire({
            title: 'Oh no!',
            text: message,
            icon: 'warning',
            confirmButtonText: 'Aceptar'
        });
    } else {
        Swal.fire({
            title: "Ingresar pedido",
            text: "Estas seguro de que quieres hacer el pedido?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Confirmar"
        }).then((result) => {
            if (result.isConfirmed) {
                let timerInterval;
                Swal.fire({
                title: "Generando su pedido",
                timer: 2500,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                    const timer = Swal.getPopup().querySelector("b");
                    timerInterval = setInterval(() => {
                    timer.textContent = `${Swal.getTimerLeft()}`;
                    }, 100);
                },
                willClose: () => {
                    clearInterval(timerInterval);
                    this.submit();
                }
            });
        }
    });
}});

document.getElementById('eliminarPedido').addEventListener('submit', function(event) {
    event.preventDefault(); 
        
    if (total == 0) {
        var message = 'No hay pedidos que eliminar';

        Swal.fire({
            title: 'Oh no!',
            text: message,
            icon: 'warning',
            confirmButtonText: 'Aceptar'
        });
    } else {

        Swal.fire({
            title: "Eliminar pedido",
            text: "Estas seguro de que quieres eliminar el pedido?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Confirmar"
        }).then((result) => {
            if (result.isConfirmed) {
                let timerInterval;
                Swal.fire({
                title: "Eliminando su pedido",
                timer: 2500,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                    const timer = Swal.getPopup().querySelector("b");
                    timerInterval = setInterval(() => {
                    timer.textContent = `${Swal.getTimerLeft()}`;
                    }, 100);
                },
                willClose: () => {
                    clearInterval(timerInterval);
                    this.submit();
                }
            });
        }
    });
}});