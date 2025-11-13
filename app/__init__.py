from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
gestor_login = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def crear_aplicacion():
    aplicacion = Flask(__name__)
    
    # Configuración
    aplicacion.config.from_object('app.config.Config')
    
    # Inicializar extensiones
    db.init_app(aplicacion)
    gestor_login.init_app(aplicacion)
    migrate.init_app(aplicacion, db)
    csrf.init_app(aplicacion)
    
    # Configurar Gestor de Login
    gestor_login.vista_login = 'auth_bp.iniciar_sesion'
    gestor_login.mensaje_login = 'Por favor inicia sesión para acceder a esta página.'
    
    # Importar y registrar blueprints
    from app.routes import principal_bp, auth_bp, productos_bp, carrito_bp, pedidos_bp
    
    aplicacion.register_blueprint(principal_bp)
    aplicacion.register_blueprint(auth_bp)
    aplicacion.register_blueprint(productos_bp)
    aplicacion.register_blueprint(carrito_bp)
    aplicacion.register_blueprint(pedidos_bp)
    
    return aplicacion