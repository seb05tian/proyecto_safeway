from flask import Blueprint, jsonify, request
from config.db import db
from models.cliente import Cliente, ClienteSchema


api_cliente = Blueprint('api_cliente', __name__)
cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

# CREATE
@api_cliente.route('/clientes/create', methods=['POST'])
def create_cliente():
    data = request.json
    new_cliente = Cliente(
        direccion=data['direccion'],
        telefono=data['telefono'],
        id_usuario=data['id_usuario']
    )
    db.session.add(new_cliente)
    db.session.commit()
    return cliente_schema.jsonify(new_cliente), 201

# READ ALL
@api_cliente.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return clientes_schema.jsonify(clientes)

# READ ONE
@api_cliente.route('/clientes/<int:id_cliente>', methods=['GET'])
def get_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    return cliente_schema.jsonify(cliente)

# UPDATE
@api_cliente.route('/clientes/update/<int:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    data = request.json
    cliente = Cliente.query.get_or_404(id_cliente)
    
    cliente.direccion = data.get('direccion', cliente.direccion)
    cliente.telefono = data.get('telefono', cliente.telefono)
    
    db.session.commit()
    return cliente_schema.jsonify(cliente)

# DELETE
@api_cliente.route('/clientes/delete/<int:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'}), 204
