from flask import Blueprint, request, jsonify
from config.db import db
from models.alertas import Alertas, AlertasSchema

api_alertas = Blueprint('api_alertas', __name__)
alerta_schema = AlertasSchema()
alertas_schema = AlertasSchema(many=True)

@api_alertas.route('/alertas', methods=['POST'])
def create_alerta():
    descripcion = request.json['descripcion']
    ubicacion = request.json['ubicacion']
    id_reporte = request.json['id_reporte']

    nueva_alerta = Alertas(descripcion=descripcion, ubicacion=ubicacion, id_reporte=id_reporte)
    db.session.add(nueva_alerta)
    db.session.commit()

    return alerta_schema.jsonify(nueva_alerta)

@api_alertas.route('/alertas', methods=['GET'])
def get_alertas():
    todas_alertas = Alertas.query.all()
    return alertas_schema.jsonify(todas_alertas)

@api_alertas.route('/alertas/<int:id>', methods=['GET'])
def get_alerta(id):
    alerta = Alertas.query.get(id)
    return alerta_schema.jsonify(alerta)

@api_alertas.route('/alertas/<int:id>', methods=['PUT'])
def update_alerta(id):
    alerta = Alertas.query.get(id)

    descripcion = request.json['descripcion']
    ubicacion = request.json['ubicacion']
    id_reporte = request.json['id_reporte']

    alerta.descripcion = descripcion
    alerta.ubicacion = ubicacion
    alerta.id_reporte = id_reporte

    db.session.commit()
    return alerta_schema.jsonify(alerta)

@api_alertas.route('/alertas/<int:id>', methods=['DELETE'])
def delete_alerta(id):
    alerta = Alertas.query.get(id)
    db.session.delete(alerta)
    db.session.commit()

    return alerta_schema.jsonify(alerta)
