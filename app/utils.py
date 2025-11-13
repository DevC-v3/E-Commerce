from app import db
from app.models import Producto, Usuario, Pedido

def obtener_productos_destacados(limite=8):
    """Obtener productos destacados para la página principal"""
    return Producto.query.filter_by(activo=True).limit(limite).all()

def calcular_total_carrito(id_usuario):
    """Calcular el total del carrito de un usuario"""
    from app.models import ItemCarrito
    items = ItemCarrito.query.filter_by(usuario_id=id_usuario).all()
    return sum(item.calcular_subtotal() for item in items)

def crear_pedido_desde_carrito(usuario, datos_envio):
    """Crear un pedido a partir del carrito del usuario"""
    from app.models import Pedido, ItemPedido, ItemCarrito
    
    # Crear el pedido
    pedido = Pedido(
        usuario_id=usuario.id,
        direccion_envio=datos_envio['direccion'],
        ciudad=datos_envio['ciudad'],
        codigo_postal=datos_envio['codigo_postal']
    )
    
    # Mover items del carrito al pedido
    items_carrito = ItemCarrito.query.filter_by(usuario_id=usuario.id).all()
    
    for item in items_carrito:
        item_pedido = ItemPedido(
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        pedido.items_pedido.append(item_pedido)
        
        # Actualizar stock
        item.producto.actualizar_stock(item.cantidad)
    
    # Calcular total
    pedido.total = pedido.calcular_total()
    
    # Guardar y limpiar carrito
    db.session.add(pedido)
    ItemCarrito.query.filter_by(usuario_id=usuario.id).delete()
    db.session.commit()
    
    return pedido