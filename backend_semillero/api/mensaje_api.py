from flask import Blueprint, jsonify, request
from config.db import db
from models.mensajes import Mensaje, MensajesSchema
from models.usuario import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity

api_mensajes = Blueprint('api_mensajes', __name__)
mensaje_schema = MensajesSchema()
mensajes_schema = MensajesSchema(many=True)


@api_mensajes.route('/mensajes/create', methods=['POST'])
@jwt_required()
def crear_mensaje():
    data = request.get_json()
    descripcion = data.get('descripcion')
    user_id = get_jwt_identity()  

    if not descripcion:
        return jsonify({'error': 'Falta la descripción'}), 400

    nuevo_mensaje = Mensaje(id_usuario=user_id, descripcion=descripcion)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    usuario = Usuario.query.get(user_id)  

    return jsonify({
        'id_mensaje': nuevo_mensaje.id_mensaje,
        'id_usuario': user_id,
        'nombre': usuario.nombre if usuario else None,  
        'descripcion': descripcion,
        'fecha': nuevo_mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if nuevo_mensaje.fecha else None
    }), 201


@api_mensajes.route('/mensajes', methods=['GET'])
def obtener_mensajes():
    mensajes = Mensaje.query.order_by(Mensaje.fecha).all()
    return jsonify([{
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'nombre': Usuario.query.get(mensaje.id_usuario).nombre if Usuario.query.get(mensaje.id_usuario) else None,  # Agregado el nombre
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if mensaje.fecha else None
    } for mensaje in mensajes])


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

    usuario = Usuario.query.get(mensaje.id_usuario)  

    return jsonify({
        'id_mensaje': mensaje.id_mensaje,
        'id_usuario': mensaje.id_usuario,
        'nombre': usuario.nombre if usuario else None,  
        'descripcion': mensaje.descripcion,
        'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S") if mensaje.fecha else None
    }), 200
