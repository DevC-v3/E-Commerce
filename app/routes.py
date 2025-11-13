from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Ruta para la página de inicio
@main.route('/')
def index():
    return render_template('administrador.html')