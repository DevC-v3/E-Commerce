from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario, Producto, Categoria
from app.forms import FormularioLogin, FormularioRegistro, FormularioProducto
from werkzeug.utils import secure_filename
import os
from flask import jsonify

main = Blueprint('main', __name__)

# RUTAS PÚBLICAS
@main.route('/')
def index():
    # Obtener productos aleatorios para la sección destacada
    productos_destacados = Producto.query.order_by(db.func.random()).limit(4).all()
    return render_template('index.html', productos_destacados=productos_destacados)

@main.route('/catalogo')
def catalogo():
    """Página de catálogo de productos con filtros"""
    # Obtener parámetros de filtro
    categoria_id = request.args.get('categoria', type=int)
    orden = request.args.get('orden', 'nombre')
    
    # Consulta base
    query = Producto.query
    
    # Filtrar por categoría
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    
    # Ordenar
    if orden == 'precio_asc':
        query = query.order_by(Producto.precio.asc())
    elif orden == 'precio_desc':
        query = query.order_by(Producto.precio.desc())
    else:
        query = query.order_by(Producto.nombre.asc())
    
    productos = query.all()
    categorias = Categoria.query.all()
    
    return render_template('catalogo.html',
                         productos=productos,
                         categorias=categorias,
                         categoria_actual=categoria_id,
                         orden_actual=orden)

@main.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    """Página de detalle de producto"""
    producto = Producto.query.get_or_404(producto_id)
    return render_template('detalle_producto.html', producto=producto)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = FormularioLogin()
    
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario and usuario.verificar_contraseña(form.contraseña.data):
            login_user(usuario)
            flash(f'Bienvenido {usuario.nombre}!', 'success')
            
            if usuario.administrador:
                return redirect(url_for('main.index'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('main.index'))

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    
    if form.validate_on_submit():
        # Verificar si el email ya existe
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash('Este email ya está registrado', 'error')
            return render_template('registro.html', form=form)
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data
        )
        nuevo_usuario.establecer_contraseña(form.contraseña.data)
        
        # Guardar en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('registro.html', form=form)

@main.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
    # Verificar que el usuario es administrador
    if not current_user.administrador:
        flash('No tienes permisos para acceder al panel', 'error')
        return redirect(url_for('main.index'))
    
    # Formulario de producto
    form = FormularioProducto()
    
    # Obtener categorías para el select
    categorias = Categoria.query.all()
    form.categoria_id.choices = [(0, 'Sin categoría')] + [(c.id, c.nombre) for c in categorias]
    
    if form.validate_on_submit():
        try:
            # Crear nuevo producto
            nuevo_producto = Producto(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data,
                precio=form.precio.data,
                stock=form.stock.data,
                categoria_id=form.categoria_id.data if form.categoria_id.data != 0 else None
            )
            
            # Manejar la imagen si se subió
            if form.imagen.data:
                filename = secure_filename(form.imagen.data.filename)
                # Crear directorio si no existe
                os.makedirs('app/static/uploads', exist_ok=True)
                filepath = os.path.join('app/static/uploads', filename)
                form.imagen.data.save(filepath)
                nuevo_producto.imagen_url = f'/static/uploads/{filename}'
            
            # Guardar en la base de datos
            db.session.add(nuevo_producto)
            db.session.commit()
            
            flash('¡Producto agregado exitosamente!', 'success')
            return redirect(url_for('main.panel'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar el producto', 'error')
    
    # Obtener productos y usuarios para mostrar
    productos = Producto.query.all()
    usuarios = Usuario.query.all()
    
    return render_template('panel.html', form=form, productos=productos, usuarios=usuarios, categorias=categorias)

@main.route('/agregar-categoria', methods=['POST'])
@login_required
def agregar_categoria():
    if not current_user.administrador:
        flash('No tienes permisos', 'error')
        return redirect(url_for('main.index'))
    
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    if nombre:
        nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_categoria)
        db.session.commit()
        flash('Categoría agregada exitosamente', 'success')
    
    return redirect(url_for('main.panel'))

@main.route('/eliminar-producto/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    """Eliminar un producto"""
    if not current_user.administrador:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('main.index'))
    
    producto = Producto.query.get_or_404(producto_id)
    
    try:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el producto', 'error')
    
    return redirect(url_for('main.panel'))

# RUTA PARA AGREGAR AL CARRITO
@main.route('/agregar-al-carrito/<int:producto_id>')
def agregar_al_carrito(producto_id):
    """Agregar producto al carrito"""
    producto = Producto.query.get_or_404(producto_id)
    flash(f'✅ {producto.nombre} agregado al carrito', 'success')
    return redirect(url_for('main.ver_carrito'))

# RUTAS DEL CARRITO
@main.route('/carrito')
def ver_carrito():
    """Página del carrito de compras"""
    carrito_items = []
    subtotal = 0
    
    productos_en_carrito = Producto.query.limit(2).all()
    
    for producto in productos_en_carrito:
        carrito_items.append({
            'producto': producto,
            'cantidad': 1
        })
        subtotal += producto.precio
    
    # Cálculos de ejemplo
    envio = 10.00 if subtotal > 0 else 0
    impuestos = subtotal * 0.18  # 18% de impuestos
    total = subtotal + envio + impuestos
    
    return render_template('carrito.html',
                         carrito_items=carrito_items,
                         subtotal=subtotal,
                         envio=envio,
                         impuestos=impuestos,
                         total=total)

@main.route('/actualizar-carrito/<int:producto_id>', methods=['POST'])
@login_required
def actualizar_carrito(producto_id):
    """Actualizar la cantidad de un producto en el carrito"""
    try:
        data = request.get_json()
        cantidad = data.get('cantidad', 1)
        
        # Aquí iría la lógica para actualizar en la base de datos
        # Por ahora solo retornamos éxito
        return jsonify({'success': True, 'message': 'Carrito actualizado'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@main.route('/eliminar-del-carrito/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(producto_id):
    """Eliminar un producto del carrito"""
    try:
        # Aquí iría la lógica para eliminar de la base de datos
        # Por ahora solo retornamos éxito
        return jsonify({'success': True, 'message': 'Producto eliminado del carrito'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400