from flask import Blueprint, jsonify, request
from config.db import db
from models.mensajes import Mensaje, MensajesSchema
from models.usuario import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reportes import Reportes
api_mensajes = Blueprint('api_mensajes', __name__)
mensaje_schema = MensajesSchema()
mensajes_schema = MensajesSchema(many=True)


@api_mensajes.route('/mensajes/create/<int:id_reporte>', methods=['POST'])
@jwt_required()
def crear_mensaje(id_reporte):
    data = request.get_json()
    descripcion = data.get('descripcion')
    user_id = get_jwt_identity()

    if not descripcion:
        return jsonify({'error': 'Falta la descripción'}), 400

    nuevo_mensaje = Mensaje(id_usuario=user_id, id_reporte=id_reporte, descripcion=descripcion)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    usuario = Usuario.query.get(user_id)

    return jsonify({
        'id_mensaje': nuevo_mensaje.id_mensaje,
        'id_usuario': user_id,
        'id_reporte': id_reporte,
        'nombre': usuario.nombre if usuario else None,
        'descripcion': descripcion,
        'fecha': nuevo_mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S")
    }), 201


@api_mensajes.route('/mensajes/reporte/<int:id_reporte>', methods=['GET'])
@jwt_required()
def obtener_mensajes_por_reporte(id_reporte):
    mensajes = Mensaje.query.filter_by(id_reporte=id_reporte).order_by(Mensaje.fecha).all()

    resultado = []
    for mensaje in mensajes:
        usuario = Usuario.query.get(mensaje.id_usuario)
        resultado.append({
            'id_mensaje': mensaje.id_mensaje,
            'id_usuario': mensaje.id_usuario,
            'id_reporte': mensaje.id_reporte,
            'nombre': usuario.nombre if usuario else None,
            'descripcion': mensaje.descripcion,
            'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(resultado), 200

@api_mensajes.route('/mensajes/<int:id_mensaje>', methods=['GET'])
def obtener_mensaje(id_mensaje):
    mensaje = Mensaje.query.get(id_mensaje)
    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    usuario = Usuario.query.get(mensaje.id_usuario)  

    return jsonify({
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'nombre': usuario.nombre if usuario else None,  
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if mensaje.fecha else None
    })


@api_mensajes.route('/mensajes/delete/<int:id_mensaje>', methods=['DELETE'])
@jwt_required()
def eliminar_mensaje(id_mensaje):
    mensaje = Mensaje.query.get(id_mensaje)
    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    user_id = get_jwt_identity()

    usuario = Usuario.query.get(user_id)  
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    if mensaje.id_usuario != user_id and usuario.rol != 'administrador':
        return jsonify({'error': 'No tienes permiso para eliminar este mensaje'}), 403

    db.session.delete(mensaje)
    db.session.commit()
    return jsonify({'mensaje': 'Mensaje eliminado correctamente'}), 200


@api_mensajes.route('/mensajes/update/<int:id_mensaje>', methods=['PUT'])
@jwt_required()
def actualizar_mensaje(id_mensaje):
    mensaje = Mensaje.query.get(id_mensaje)
    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    user_id = get_jwt_identity()
    if mensaje.id_usuario != user_id:
        return jsonify({'error': 'No tienes permiso para actualizar este mensaje'}), 403

    data = request.get_json()
    nueva_descripcion = data.get('descripcion')
    if not nueva_descripcion:
        return jsonify({'error': 'Debe enviar una nueva descripción'}), 400

    mensaje.descripcion = nueva_descripcion
    db.session.commit()

    usuario = Usuario.query.get(user_id)

    return jsonify({
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'id_reporte': mensaje.id_reporte,
        'nombre': usuario.nombre if usuario else None,
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S")
    }), 200


@api_mensajes.route('/mensajes/usuario/<int:id_usuario>', methods=['GET'])
@jwt_required()
def obtener_reportes_comentados_por_usuario(id_usuario):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    mensajes_paginados = Mensaje.query \
        .filter_by(id_usuario=id_usuario) \
        .order_by(Mensaje.fecha.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    mensajes = mensajes_paginados.items

    # Obtener los reportes correspondientes
    reportes_ids = list(set([m.id_reporte for m in mensajes]))
    reportes = Reportes.query.filter(Reportes.id_reporte.in_(reportes_ids)).all()

    resultado = []
    for r in reportes:
        resultado.append({
            "id_reporte": r.id_reporte,
            "descripcion": r.descripcion,
            "imagen": r.imagen,
            "ubicacion": r.ubicacion,
            "fecha_hora": r.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            "latitud": r.latitud,
            "longitud": r.longitud
        })

    return jsonify({
        "total": mensajes_paginados.total,
        "page": mensajes_paginados.page,
        "pages": mensajes_paginados.pages,
        "per_page": mensajes_paginados.per_page,
        "reportes": resultado
    }), 200