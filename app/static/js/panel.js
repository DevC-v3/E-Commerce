// Funciones para el modal de productos
function abrirModal() {
    document.getElementById('modalProducto').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modalProducto').classList.add('hidden');
}

// Funciones para el modal de categorías
function abrirModalCategoria() {
    document.getElementById('modalCategoria').classList.remove('hidden');
}

function cerrarModalCategoria() {
    document.getElementById('modalCategoria').classList.add('hidden');
}

// Función para confirmar eliminación
function confirmarEliminacion() {
    return confirm('¿Estás seguro de que quieres eliminar este producto? Esta acción no se puede deshacer.');
}

// Función para mostrar/ocultar secciones
function mostrarSeccion(seccion) {
    // Oculta todas las secciones
    document.querySelectorAll('.seccion-contenido').forEach(sec => {
        sec.classList.add('hidden');
    });
    
    // Muestra la sección seleccionada
    document.getElementById(seccion).classList.remove('hidden');
    
    // Actualiza el menú activo
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('bg-[#f0f2f4]', 'rounded');
    });
    event.currentTarget.classList.add('bg-[#f0f2f4]', 'rounded');
}

// Cerrar modales al hacer click fuera
document.addEventListener('DOMContentLoaded', function() {
    const modalProducto = document.getElementById('modalProducto');
    const modalCategoria = document.getElementById('modalCategoria');
    
    if (modalProducto) {
        modalProducto.addEventListener('click', function(e) {
            if (e.target.id === 'modalProducto') {
                cerrarModal();
            }
        });
    }
    
    if (modalCategoria) {
        modalCategoria.addEventListener('click', function(e) {
            if (e.target.id === 'modalCategoria') {
                cerrarModalCategoria();
            }
        });
    }
    
    // Cerrar modales con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            cerrarModal();
            cerrarModalCategoria();
        }
    });
});