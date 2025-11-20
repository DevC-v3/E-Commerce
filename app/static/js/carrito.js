function actualizarCantidad(productoId, cambio) {
    var input = document.getElementById('cantidad-' + productoId);
    if (input) {
        var nuevaCantidad = parseInt(input.value) + cambio;
        if (nuevaCantidad < 1) nuevaCantidad = 1;
        input.value = nuevaCantidad;
        alert('Cantidad actualizada: ' + nuevaCantidad);
    }
}

function actualizarCantidadInput(productoId, cantidad) {
    if (cantidad < 1) cantidad = 1;
    alert('Cantidad cambiada a: ' + cantidad);
}

function eliminarDelCarrito(productoId) {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
        alert('Producto ' + productoId + ' eliminado');
        window.location.reload();
    }
}

function procederCheckout() {
    alert('Funcionalidad de checkout en desarrollo');
}