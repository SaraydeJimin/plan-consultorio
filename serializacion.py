from flaskr.modelos import Usuario, Medico, Especialidad, Cita, Agendamiento, Servicio, Categoria

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
