from datetime import datetime
from flaskr import db, bcrypt
from flask_login import UserMixin
from flask import jsonify

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Rol', backref='usuario', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': [rol.nombre for rol in self.roles]
        }

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'usuario_id': self.usuario_id
        }

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)
    especialidad = db.relationship('Especialidad', back_populates='medicos')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'especialidad': self.especialidad.nombre
        }

class Especialidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    medicos = db.relationship('Medico', back_populates='especialidad')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hora = db.Column(db.Time, nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    medico = db.relationship('Medico', back_populates='citas')

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat(),
            'hora': self.hora.isoformat(),
            'medico': self.medico.nombre
        }

class Agendamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('cita.id'), nullable=False)
    cita = db.relationship('Cita', back_populates='agendamientos')

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat(),
            'hora_inicio': self.hora_inicio.isoformat(),
            'hora_fin': self.hora_fin.isoformat(),
            'cita': self.cita.id
        }

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', back_populates='servicios')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria.nombre
        }

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    servicios = db.relationship('Servicio', back_populates='categoria')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }
    

#serializacion
def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'roles': [rol.nombre for rol in user.roles]
    }

def serialize_medico(medico):
    return {
        'id': medico.id,
        'nombre': medico.nombre,
        'especialidad': medico.especialidad.nombre
    }

def serialize_especialidad(especialidad):
    return {
        'id': especialidad.id,
        'nombre': especialidad.nombre
    }

def serialize_cita(cita):
    return {
        'id': cita.id,
        'fecha': cita.fecha.isoformat(),
        'hora': cita.hora.isoformat(),
        'medico': cita.medico.nombre
    }

def serialize_agendamiento(agendamiento):
    return {
        'id': agendamiento.id,
        'fecha': agendamiento.fecha.isoformat(),
        'hora_inicio': agendamiento.hora_inicio.isoformat(),
        'hora_fin': agendamiento.hora_fin.isoformat(),
        'cita': agendamiento.cita.id
    }

def serialize_servicio(servicio):
    return {
        'id': servicio.id,
        'nombre': servicio.nombre,
        'categoria': servicio.categoria.nombre
    }

def serialize_categoria(categoria):
    return {
        'id': categoria.id,
        'nombre': categoria.nombre
    }
