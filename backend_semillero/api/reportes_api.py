from flask import Blueprint, jsonify, request
from config.db import db
from models.reportes import Reportes, ReportesSchema

api_reportes = Blueprint('api_reportes', __name__)
reporte_schema = ReportesSchema()
reportes_schema = ReportesSchema(many=True)

# CREATE
@api_reportes.route('/reportes/create', methods=['POST'])
def create_reporte():
    data = request.json
    new_reporte = Reportes(
        descripcion=data['descripcion'],
        imagen=data['imagen'],
        fecha_hora=data['fecha_hora'],
        ubicacion=data['ubicacion'],
        id_usuario=data['id_usuario']
    )
    db.session.add(new_reporte)
    db.session.commit()
    return reporte_schema.jsonify(new_reporte), 201

# READ ALL
@api_reportes.route('/reportes', methods=['GET'])
def get_reportes():
    reportes = Reportes.query.all()
    return reportes_schema.jsonify(reportes)

# READ ONE
@api_reportes.route('/reportes/<int:id_reporte>', methods=['GET'])
def get_reporte(id_reporte):
    reporte = Reportes.query.get_or_404(id_reporte)
    return reporte_schema.jsonify(reporte)

# UPDATE
@api_reportes.route('/reportes/update/<int:id_reporte>', methods=['PUT'])
def update_reporte(id_reporte):
    data = request.json
    reporte = Reportes.query.get_or_404(id_reporte)
    
    reporte.descripcion = data.get('descripcion', reporte.descripcion)
    reporte.imagen = data.get('imagen', reporte.imagen)
    reporte.fecha_hora = data.get('fecha_hora', reporte.fecha_hora)
    reporte.ubicacion = data.get('ubicacion', reporte.ubicacion)
    
    db.session.commit()
    return reporte_schema.jsonify(reporte)

# DELETE
@api_reportes.route('/reportes/delete/<int:id_reporte>', methods=['DELETE'])
def delete_reporte(id_reporte):
    reporte = Reportes.query.get_or_404(id_reporte)
    db.session.delete(reporte)
    db.session.commit()
    return jsonify({'message': 'Reporte eliminado'}), 204


@api_reportes.route('/reportes/historial', methods=['GET'])
def obtener_historial():
    id_usuario = request.args.get('id_usuario')  # Debes obtener el ID del usuario desde la sesión o autenticación
    
    # Obtener los reportes hechos por este usuario
    reportes = Reportes.query.filter_by(id_usuario=id_usuario).all()
    
    if not reportes:
        return jsonify({'message': 'No hay reportes para este usuario'}), 404
    
    return reportes_schema.jsonify(reportes), 200


@api_reportes.route('/reportes/notificaciones', methods=['GET'])
def obtener_notificaciones():
    id_usuario = request.args.get('id_usuario')  # ID del usuario en sesión
    
    # Obtener reportes hechos por otros usuarios
    reportes = Reportes.query.filter(Reportes.id_usuario != id_usuario).all()
    
    if not reportes:
        return jsonify({'message': 'No hay reportes de otros usuarios'}), 404
    
    return reportes_schema.jsonify(reportes), 200

