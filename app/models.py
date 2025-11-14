from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# TABLA USUARIO
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    administrador = db.Column(db.Boolean, default=False)
    
    #Relaciones
    direcciones = db.relationship('Direccion', backref='usuario', lazy=True)
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    items_carrito = db.relationship('ItemCarrito', backref='usuario', lazy=True)

    def establecer_contraseña(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)
    
    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)

# TABLA DIRECCION
class Direccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    distrito = db.Column(db.String(100), nullable=False)

# TABLA CATEGORIA
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    
    productos = db.relationship('Producto', backref='categoria', lazy=True)

# TABLA PRODUCTO
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    imagen_url = db.Column(db.String(200))
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))

# TABLA ITEM CARRTITO
class ItemCarrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    
    producto = db.relationship('Producto')

# TABLA PEDIDO
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    numero_pedido = db.Column(db.String(50), unique=True, nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    direccion_envio = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('ItemPedido', backref='pedido', lazy=True)
    pago = db.relationship('Pago', backref='pedido', uselist=False)

# TABLA ITEM PEDIDO
class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    
    producto = db.relationship('Producto')

# TABLA PAGO
class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    id_transaccion = db.Column(db.String(100), unique=True)
    estado = db.Column(db.String(20), default='pendiente')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))