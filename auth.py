from flask import Blueprint, request, jsonify, current_app
from flaskr import db, bcrypt
from flaskr.modelos import Usuario, Rol
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = Usuario(username=data['username'], email=data['email'], password_hash=hashed_password)

    # Asignar roles al nuevo usuario
    admin_role = Rol(nombre='admin', usuario=user)
    db.session.add(user)
    db.session.add(admin_role)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({"message": "Inicio de sesión exitoso!"}), 200
    return jsonify({"message": "Usuario o contraseña incorrectos!"}), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Cierre de sesión exitoso!"}), 200
