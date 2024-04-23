document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("pizzaAleatoria").addEventListener("click", function() {
        // Obtener todos los elementos del formulario
        var sizeSelect = document.getElementById("size");
        var masaSelect = document.getElementById("corteza");
        var cantidadSelect = document.getElementById("cantidad");
        var vegetalesCheckboxes = document.getElementsByName("checkbox_vegetales");
        var proteinaCheckboxes = document.getElementsByName("checkbox_proteina");
        var salsaRadios = document.getElementsByName("radio_salsa");

        // Obtener longitud de las opciones para cada tipo de elemento
        var sizeOptionsLength = sizeSelect.options.length;
        var masaOptionsLength = masaSelect.options.length;
        var cantidadOptionsLength = cantidadSelect.options.length;
        var vegetalesCheckboxesLength = vegetalesCheckboxes.length;
        var proteinaCheckboxesLength = proteinaCheckboxes.length;
        var salsaRadiosLength = salsaRadios.length;

        // Seleccionar aleatoriamente para cada tipo de elemento
        sizeSelect.selectedIndex = Math.floor(Math.random() * sizeOptionsLength);
        masaSelect.selectedIndex = Math.floor(Math.random() * masaOptionsLength);
        cantidadSelect.selectedIndex = Math.floor(Math.random() * cantidadOptionsLength);

        // Desmarcar todos los checkbox de vegetales y seleccionar aleatoriamente uno
        for (var i = 0; i < vegetalesCheckboxesLength; i++) {
            vegetalesCheckboxes[i].checked = false;
        }
        vegetalesCheckboxes[Math.floor(Math.random() * vegetalesCheckboxesLength)].checked = true;

        // Desmarcar todos los checkbox de proteínas y seleccionar aleatoriamente uno
        for (var j = 0; j < proteinaCheckboxesLength; j++) {
            proteinaCheckboxes[j].checked = false;
        }
        proteinaCheckboxes[Math.floor(Math.random() * proteinaCheckboxesLength)].checked = true;

        // Desmarcar todos los radios de salsa y seleccionar aleatoriamente uno
        for (var k = 0; k < salsaRadiosLength; k++) {
            salsaRadios[k].checked = false;
        }
        salsaRadios[Math.floor(Math.random() * salsaRadiosLength)].checked = true;

        actualizarIngredientes();
    });
});

document.getElementById('agregarPedidoForm').addEventListener('submit', function(event) {
    event.preventDefault(); 
    
    var checkboxes_vegetales = document.querySelectorAll('input[name="checkbox_vegetales"]:checked');
    var checkboxes_proteinas = document.querySelectorAll('input[name="checkbox_proteina"]:checked');
    var radio_salsa = document.querySelector('input[name="radio_salsa"]:checked');
    
    var total_checkboxes = checkboxes_vegetales.length + checkboxes_proteinas.length;
    
    if (total_checkboxes < 1 || !radio_salsa) {
        var message = '';
        if (total_checkboxes == 0) {
            message += 'Debes seleccionar al menos 1 ingrediente.\n';
        }
        if (!radio_salsa) {
            message += 'Debes seleccionar al menos 1 tipo de salsa.';
        }
        Swal.fire({
            title: '¡Cuidado!',
            text: message,
            icon: 'warning',
            confirmButtonText: 'Aceptar'
        });
    } else {
        // Si se cumplen todas las condiciones de validación, puedes enviar el formulario
        this.submit();
    }
});

// Obtener todos los checkboxes
const checkboxes = document.querySelectorAll('input[type="checkbox"]');
// Variable para contar ingredientes seleccionados
let ingredientCount = 0;
let precio_base = 10000;

const cantidad = document.getElementById('cantidad');

document.getElementById('precio_base').textContent = precio_base;

function actualizarSubtotal() {
    const extraPrice = Math.max(0, (ingredientCount - 3)) * 1000;
    const subtotal = (precio_base + extraPrice) * cantidad.value;
    document.getElementById('sub_total').textContent = subtotal; 

        document.getElementById('hidden_sub_total').value = subtotal;
}


checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {

        if (checkbox.checked) {
            ingredientCount++;
        } else {
            ingredientCount--;
        }

        document.getElementById('ingredientCount').textContent = ingredientCount;
        

        const extraPrice = Math.max(0, (ingredientCount - 3)) * 1000;
        document.getElementById('extraPrice').textContent = extraPrice;
        

        actualizarSubtotal();
    });
});

function actualizarIngredientes() {
    ingredientCount = 0;

    const checkboxesVegetales = document.getElementsByName("checkbox_vegetales");
    checkboxesVegetales.forEach(checkbox => {
        if (checkbox.checked) {
            ingredientCount++;
        }
    });

    const checkboxesProteinas = document.getElementsByName("checkbox_proteina");
    checkboxesProteinas.forEach(checkbox => {
        if (checkbox.checked) {
            ingredientCount++;
        }
    });

    document.getElementById('ingredientCount').textContent = ingredientCount;
    
    const extraPrice = Math.max(0, (ingredientCount - 3)) * 1000;
    document.getElementById('extraPrice').textContent = extraPrice;
    
    actualizarSubtotal();
}

cantidad.addEventListener('change', () => {
    actualizarSubtotal();
});

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        actualizarIngredientes();
    });
});
