from flask import Blueprint, jsonify, request
from config.db import db
from models.mensajes import Mensaje, MensajesSchema
api_mensajes = Blueprint('api_mensajes', __name__)
mensaje_schema = MensajesSchema()
mensajes_schema = MensajesSchema(many=True)


@api_mensajes.route('/mensajes_post', methods=['POST'])
def crear_mensaje():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    descripcion = data.get('descripcion')

    if not id_usuario or not descripcion:
        return jsonify({'error': 'Faltan datos'}), 400

    nuevo_mensaje = Mensaje(id_usuario=id_usuario, descripcion=descripcion)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    return jsonify({
        'id_mensaje': nuevo_mensaje.id_mensaje,
        'id_usuario': id_usuario,
        'descripcion': descripcion,
        'fecha': nuevo_mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if nuevo_mensaje.fecha else None
    }), 201


@api_mensajes.route('/mensajes_get', methods=['GET'])
def obtener_mensajes():
    mensajes = Mensaje.query.order_by(Mensaje.fecha).all()

    return jsonify([{
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if mensaje.fecha else None
    } for mensaje in mensajes])

@api_mensajes.route('/mensajes_get_specific/<int:id_mensaje>', methods=['GET'])
def obtener_mensaje(id_mensaje):
    mensaje = Mensaje.query.get(id_mensaje)

    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    return jsonify({
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if mensaje.fecha else None
    })



@api_mensajes.route('/mensajes_delete/<int:id_mensaje>/<int:id_usuario>', methods=['DELETE'])
def eliminar_mensaje(id_mensaje, id_usuario):
    mensaje = Mensaje.query.get(id_mensaje)

    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    if mensaje.id_usuario != id_usuario:
        return jsonify({'error': 'No tienes permiso para eliminar este mensaje'}), 403

    db.session.delete(mensaje)
    db.session.commit()

    return jsonify({'mensaje': 'Mensaje eliminado correctamente'}), 200



@api_mensajes.route('/mensajes_update/<int:id_mensaje>/<int:id_usuario>', methods=['PUT'])
def actualizar_mensaje(id_mensaje, id_usuario):
    mensaje = Mensaje.query.get(id_mensaje)

    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    if mensaje.id_usuario != id_usuario:
        return jsonify({'error': 'No tienes permiso para actualizar este mensaje'}), 403

    data = request.get_json()
    nueva_descripcion = data.get('descripcion')

    if not nueva_descripcion:
        return jsonify({'error': 'Debe enviar una nueva descripción'}), 400

    mensaje.descripcion = nueva_descripcion
    db.session.commit()

    return jsonify({
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S")
    })
