from flask import Blueprint

# Blueprints para organizar las rutas
principal_bp = Blueprint('principal_bp', __name__)
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
productos_bp = Blueprint('productos_bp', __name__, url_prefix='/productos')
carrito_bp = Blueprint('carrito_bp', __name__, url_prefix='/carrito')
pedidos_bp = Blueprint('pedidos_bp', __name__, url_prefix='/pedidos')

@principal_bp.route('/')
def inicio():
    return "Página de inicio - Catálogo"

@auth_bp.route('/iniciar-sesion')
def iniciar_sesion():
    return "Página de inicio de sesión"

@auth_bp.route('/registro')
def registro():
    return "Página de registro"

@auth_bp.route('/cerrar-sesion')
def cerrar_sesion():
    return "Cerrar sesión"

@productos_bp.route('/<int:id_producto>')
def detalle_producto(id_producto):
    return f"Detalles del producto {id_producto}"

@carrito_bp.route('/')
def ver_carrito():
    return "Carrito de compras"

@carrito_bp.route('/agregar/<int:id_producto>')
def agregar_al_carrito(id_producto):
    return f"Agregar producto {id_producto} al carrito"

@carrito_bp.route('/checkout')
def proceso_pago():
    return "Proceso de pago"

@pedidos_bp.route('/confirmacion/<int:id_pedido>')
def confirmacion_pedido(id_pedido):
    return f"Confirmación del pedido {id_pedido}"

@pedidos_bp.route('/historial')
def historial_pedidos():
    return "Historial de pedidos"