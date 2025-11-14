from app import create_app, db
from app.models import Usuario, Producto, Categoria

app = create_app()

# Solo crear tablas, sin usuarios
with app.app_context():
    db.create_all()
    print("✅ Base de datos inicializada")

if __name__ == '__main__':
    app.run(debug=True)