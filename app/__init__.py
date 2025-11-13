from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'mi-clave-secreta'  # Para seguridad de formularios
    
    # Importamos y registramos las rutas
    from app.routes import main
    app.register_blueprint(main)
    
    return app