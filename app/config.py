import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-cambiar-en-produccion'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Si hay DATABASE_URL definida (para producción)
        if os.environ.get('DATABASE_URL'):
            return os.environ.get('DATABASE_URL')
        
        # Si hay variables de MySQL definidas
        elif all(os.environ.get(key) for key in ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']):
            host = os.environ.get('DB_HOST')
            port = os.environ.get('DB_PORT', '3306')
            db_name = os.environ.get('DB_NAME')
            user = os.environ.get('DB_USER')
            password = os.environ.get('DB_PASSWORD')
            
            return f'mysql://{user}:{password}@{host}:{port}/{db_name}'
        
        # Por defecto SQLite (desarrollo)
        else:
            return 'sqlite:///ecommerce.db'