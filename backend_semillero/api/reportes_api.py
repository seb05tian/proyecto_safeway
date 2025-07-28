from flask import Blueprint, jsonify, request
from config.db import db
from models.reportes import Reportes, ReportesSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

api_reportes = Blueprint('api_reportes', __name__)
reporte_schema = ReportesSchema()
reportes_schema = ReportesSchema(many=True)

@api_reportes.route('/reportes/create', methods=['POST'])
def create_reporte():
    data = request.json
    new_reporte = Reportes(
        descripcion=data.get('descripcion'),
        imagen=data.get('imagen'),
        ubicacion=data.get('ubicacion'),
        id_usuario=data.get('id_usuario'),
        latitud=data.get('latitud'),
        longitud=data.get('longitud')
    )
    db.session.add(new_reporte)
    db.session.commit()
    return reporte_schema.jsonify(new_reporte), 201

@api_reportes.route('/reportes', methods=['GET'])
def get_reportes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if page and per_page:
        pagination = Reportes.query.paginate(page=page, per_page=per_page, error_out=False)
        reportes = pagination.items
        return jsonify({
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "reportes": reportes_schema.dump(reportes)
        }), 200
    else:
        reportes = Reportes.query.all()
        return reportes_schema.jsonify(reportes)


@api_reportes.route('/reportes/<int:id_reporte>', methods=['GET'])
def get_reporte(id_reporte):
    reporte = Reportes.query.get_or_404(id_reporte)
    return reporte_schema.jsonify(reporte)

@api_reportes.route('/reportes/update/<int:id_reporte>', methods=['PUT'])
def update_reporte(id_reporte):
    data = request.json
    reporte = Reportes.query.get_or_404(id_reporte)
    reporte.descripcion = data.get('descripcion', reporte.descripcion)
    reporte.imagen = data.get('imagen', reporte.imagen)
    reporte.ubicacion = data.get('ubicacion', reporte.ubicacion)
    reporte.latitud = data.get('latitud', reporte.latitud)
    reporte.longitud = data.get('longitud', reporte.longitud)
    db.session.commit()
    return reporte_schema.jsonify(reporte)

@api_reportes.route('/reportes/delete/<int:id_reporte>', methods=['DELETE'])
def delete_reporte(id_reporte):
    reporte = Reportes.query.get_or_404(id_reporte)
    db.session.delete(reporte)
    db.session.commit()
    return jsonify({'message': 'Reporte eliminado'}), 204

@api_reportes.route('/reportes/historial/paginated', methods=['GET'])
@jwt_required()
def get_historial_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    id_usuario = get_jwt_identity()
    pagination = Reportes.query.filter_by(id_usuario=id_usuario).paginate(page=page, per_page=per_page, error_out=False)
    reportes = pagination.items
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "nextPage": pagination.has_next,
        "reportes": reportes_schema.dump(reportes)
    }), 200

@api_reportes.route('/reportes/notificaciones/paginated', methods=['GET'])
def get_notificaciones_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Reportes.query.paginate(page=page, per_page=per_page, error_out=False)
    reportes = pagination.items
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "nextPage": pagination.has_next,
        "reportes": reportes_schema.dump(reportes)
    }), 200
