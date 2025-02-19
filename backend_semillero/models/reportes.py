from config.db import db, ma
from datetime import datetime

class Reportes(db.Model):
    __tablename__ = 'Reportes'
    id_reporte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    ubicacion = db.Column(db.String(255))
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    coordenadas = db.Column(db.String(100))  

    def __init__(self, descripcion, imagen, ubicacion, id_usuario, coordenadas=''):
        self.descripcion = descripcion
        self.imagen = imagen
        self.ubicacion = ubicacion
        self.id_usuario = id_usuario
        self.coordenadas = coordenadas

class ReportesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reportes
        fields = ('id_reporte', 'descripcion', 'imagen', 'fecha_hora', 'ubicacion', 'id_usuario', 'coordenadas')

