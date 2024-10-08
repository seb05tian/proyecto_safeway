from flask import Blueprint, jsonify, request
from config.db import db
from models.administrador import Administrador, AdministradorSchema

api_administrador = Blueprint('api_administrador', __name__)
administrador_schema = AdministradorSchema()
administradores_schema = AdministradorSchema(many=True)

# CREATE
@api_administrador.route('/administradores', methods=['POST'])
def create_administrador():
    data = request.json
    new_administrador = Administrador(
        nivel_acceso=data['nivel_acceso'],
        id_usuario=data['id_usuario']
    )
    db.session.add(new_administrador)
    db.session.commit()
    return administrador_schema.jsonify(new_administrador), 201

# READ ALL
@api_administrador.route('/administradores', methods=['GET'])
def get_administradores():
    administradores = Administrador.query.all()
    return administradores_schema.jsonify(administradores)

# READ ONE
@api_administrador.route('/administradores/<int:id_administrador>', methods=['GET'])
def get_administrador(id_administrador):
    administrador = Administrador.query.get_or_404(id_administrador)
    return administrador_schema.jsonify(administrador)

# UPDATE
@api_administrador.route('/administradores/<int:id_administrador>', methods=['PUT'])
def update_administrador(id_administrador):
    data = request.json
    administrador = Administrador.query.get_or_404(id_administrador)
    
    administrador.nivel_acceso = data.get('nivel_acceso', administrador.nivel_acceso)
    
    db.session.commit()
    return administrador_schema.jsonify(administrador)

# DELETE
@api_administrador.route('/administradores/<int:id_administrador>', methods=['DELETE'])
def delete_administrador(id_administrador):
    administrador = Administrador.query.get_or_404(id_administrador)
    db.session.delete(administrador)
    db.session.commit()
    return jsonify({'message': 'Administrador eliminado'}), 204
