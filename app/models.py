from app import db, gestor_login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_contrasena = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    items_carrito = db.relationship('ItemCarrito', backref='usuario', lazy=True)
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    reseñas = db.relationship('Reseña', backref='usuario', lazy=True)

    def establecer_contrasena(self, contrasena):
        self.hash_contrasena = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.hash_contrasena, contrasena)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    imagen_url = db.Column(db.String(500))
    categoria = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    items_carrito = db.relationship('ItemCarrito', backref='producto', lazy=True)
    items_pedido = db.relationship('ItemPedido', backref='producto', lazy=True)
    reseñas = db.relationship('Reseña', backref='producto', lazy=True)
    
    def actualizar_stock(self, cantidad):
        self.stock -= cantidad
        return self
    
    def esta_disponible(self):
        return self.stock > 0 and self.activo

class ItemCarrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calcular_subtotal(self):
        return self.cantidad * self.producto.precio

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, confirmado, enviado, entregado
    direccion_envio = db.Column(db.Text, nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    items_pedido = db.relationship('ItemPedido', backref='pedido', lazy=True)
    pago = db.relationship('Pago', backref='pedido', uselist=False, lazy=True)
    
    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.items_pedido)

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    
    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)  # tarjeta, paypal, etc.
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, completado, fallido
    id_transaccion = db.Column(db.String(100))
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)

class Reseña(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # 1-5 estrellas
    comentario = db.Column(db.Text)
    fecha_reseña = db.Column(db.DateTime, default=datetime.utcnow)
    aprobado = db.Column(db.Boolean, default=False)

@gestor_login.user_loader
def cargar_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))