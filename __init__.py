from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from cloudinary import config as cloudinary_config
from flask import current_app
from flaskr.modelos import Usuario, Rol
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cloudinary_config(app.config['CLOUDINARY_URL'])  # Configurar Cloudinary

    # Registrar blueprints
    from flaskr.vistas import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app


#superadmin
def create_superadmin():
    if not Usuario.query.filter_by(username='superadmin').first():
        hashed_password = bcrypt.generate_password_hash(os.environ.get('SUPERADMIN_PASSWORD')).decode('utf-8')
        superadmin_user = Usuario(username='superadmin', email='superadmin@example.com', password_hash=hashed_password)
        admin_role = Rol(nombre='admin', usuario=superadmin_user)
        db.session.add(superadmin_user)
        db.session.add(admin_role)
        db.session.commit()
        print("Superadmin creado exitosamente.")

# Crear aplicación
app = create_app()

# Ejecutar create_superadmin() dentro de una app_context al inicializar la aplicación
with app.app_context():
    create_superadmin()