from flask import Blueprint, jsonify, request
from config.db import db
from models.usuario import Usuario, UsuarioSchema
from models.cliente import Cliente
from models.administrador import Administrador

api_usuario = Blueprint('api_usuario', __name__)
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@api_usuario.route('/usuarios/create', methods=['POST'])
def create_usuario():
    data = request.json

    try:
       
        new_usuario = Usuario(
            nombre=data['nombre'],
            correo_electronico=data['correo_electronico'],
            contrasena=data['contrasena'],
        )
        
        db.session.add(new_usuario)
        db.session.commit()

       
        direccion = data.get('direccion', None)
        telefono = data.get('telefono', None)
        new_cliente = Cliente(
            direccion=direccion,
            telefono=telefono,
            id_usuario=new_usuario.id_usuario
        )
        db.session.add(new_cliente)

        db.session.commit()
        
        return usuario_schema.jsonify(new_usuario), 201

    except KeyError as e:
        return jsonify({'error': f'Falta el campo: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear el usuario'}), 500


# READ ALL
# READ ALL
@api_usuario.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios_schema.jsonify(usuarios)

# READ ONE
@api_usuario.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    return usuario_schema.jsonify(usuario)

# UPDATE
@api_usuario.route('/usuarios/update/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    data = request.json
    usuario = Usuario.query.get_or_404(id_usuario)

    try:
       
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.correo_electronico = data.get('correo_electronico', usuario.correo_electronico)
        usuario.contrasena = data.get('contrasena', usuario.contrasena)
        
        
        db.session.commit()
        return usuario_schema.jsonify(usuario), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar el usuario'}), 500

# DELETE
@api_usuario.route('/usuarios/delete/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'}), 204
