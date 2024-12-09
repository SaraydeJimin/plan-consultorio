from flask import Blueprint, request, jsonify, current_app
from flaskr import db
from flaskr.modelos import Usuario, Medico, Especialidad, Cita, Agendamiento, Servicio, Categoria
from flaskr.serializacion import (
    serialize_user, serialize_medico, serialize_especialidad,
    serialize_cita, serialize_agendamiento, serialize_servicio,
    serialize_categoria
)
from flask_login import login_user, logout_user, login_required

vistas = Blueprint('vistas', __name__)

@vistas.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = current_app.bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = Usuario(username=data['username'], email=data['email'], password_hash=hashed_password)

    # Asignar roles al nuevo usuario
    admin_role = Rol(nombre='admin', usuario=user)
    db.session.add(user)
    db.session.add(admin_role)
    db.session.commit()

    return jsonify(serialize_user(user)), 201

@vistas.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(email=data['email']).first()

    if user and current_app.bcrypt.check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify(serialize_user(user)), 200
    return jsonify({"message": "Usuario o contraseña incorrectos!"}), 401

@vistas.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Cierre de sesión exitoso!"}), 200

@vistas.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    return jsonify(serialize_user(user)), 200

@vistas.route('/medico', methods=['GET'])
def get_medicos():
    medicos = Medico.query.all()
    return jsonify([serialize_medico(m) for m in medicos]), 200

@vistas.route('/medico/<int:medico_id>', methods=['GET'])
def get_medico(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    return jsonify(serialize_medico(medico)), 200

@vistas.route('/especialidad', methods=['GET'])
def get_especialidades():
    especialidades = Especialidad.query.all()
    return jsonify([serialize_especialidad(e) for e in especialidades]), 200

@vistas.route('/especialidad/<int:especialidad_id>', methods=['GET'])
def get_especialidad(especialidad_id):
    especialidad = Especialidad.query.get_or_404(especialidad_id)
    return jsonify(serialize_especialidad(especialidad)), 200

@vistas.route('/cita', methods=['GET'])
def get_citas():
    citas = Cita.query.all()
    return jsonify([serialize_cita(c) for c in citas]), 200

@vistas.route('/cita/<int:cita_id>', methods=['GET'])
def get_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    return jsonify(serialize_cita(cita)), 200

@vistas.route('/agendamiento', methods=['GET'])
def get_agendamientos():
    agendamientos = Agendamiento.query.all()
    return jsonify([serialize_agendamiento(a) for a in agendamientos]), 200

@vistas.route('/agendamiento/<int:agendamiento_id>', methods=['GET'])
def get_agendamiento(agendamiento_id):
    agendamiento = Agendamiento.query.get_or_404(agendamiento_id)
    return jsonify(serialize_agendamiento(agendamiento)), 200

@vistas.route('/servicio', methods=['GET'])
def get_servicios():
    servicios = Servicio.query.all()
    return jsonify([serialize_servicio(s) for s in servicios]), 200

@vistas.route('/servicio/<int:servicio_id>', methods=['GET'])
def get_servicio(servicio_id):
    servicio = Servicio.query.get_or_404(servicio_id)
    return jsonify(serialize_servicio(servicio)), 200

@vistas.route('/categoria', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([serialize_categoria(c) for c in categorias]), 200

@vistas.route('/categoria/<int:categoria_id>', methods=['GET'])
def get_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    return jsonify(serialize_categoria(categoria)), 200
