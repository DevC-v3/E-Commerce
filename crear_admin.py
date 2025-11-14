#!/usr/bin/env python3
"""
Script para crear el usuario administrador
Uso: python crear_admin.py
"""

from app import create_app, db
from app.models import Usuario

def crear_usuario_admin():
    """Crea el usuario administrador en la base de datos"""
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existe
        admin = Usuario.query.filter_by(email='admin@tienda.com').first()
        
        if admin:
            print('❌ El usuario admin ya existe:')
            print(f'   Email: {admin.email}')
            print(f'   Nombre: {admin.nombre}')
            return False
        else:
            # Crear nuevo admin
            admin = Usuario(
                email='admin@tienda.com',
                nombre='Administrador',
                apellido='Sistema',
                administrador=True
            )
            admin.establecer_contraseña('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print('✅ Usuario administrador creado exitosamente!')
            print(f'   Email: admin@tienda.com')
            print(f'   Contraseña: admin123')
            print(f'   Nombre: Administrador Sistema')
            return True

def listar_usuarios():
    """Lista todos los usuarios en la base de datos"""
    app = create_app()
    
    with app.app_context():
        usuarios = Usuario.query.all()
        
        if not usuarios:
            print('📭 No hay usuarios en la base de datos')
            return
        
        print('📋 Usuarios en la base de datos:')
        for usuario in usuarios:
            print(f'   - {usuario.email} ({usuario.nombre}) - Admin: {usuario.administrador}')

if __name__ == '__main__':
    print('🛠️  Administración de Usuarios')
    print('=' * 40)
    
    while True:
        print('\nOpciones:')
        print('1. Crear usuario administrador')
        print('2. Listar usuarios existentes')
        print('3. Salir')
        
        opcion = input('\nSelecciona una opción (1-3): ').strip()
        
        if opcion == '1':
            crear_usuario_admin()
        elif opcion == '2':
            listar_usuarios()
        elif opcion == '3':
            print('👋 ¡Hasta luego!')
            break
        else:
            print('❌ Opción no válida')