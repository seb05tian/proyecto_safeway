from config.db import app, db, ma 
from datetime import datetime
from sqlalchemy.sql import func
from models.usuario import Usuario  
from models.reportes import Reportes
from config.db import app, db, ma
from datetime import datetime
from sqlalchemy.sql import func
from models.usuario import Usuario
from models.reportes import Reportes

class Mensaje(db.Model):
    __tablename__ = 'mensaje'

    id_mensaje = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_reporte = db.Column(db.Integer, db.ForeignKey('Reportes.id_reporte'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, server_default=func.now())

    usuario = db.relationship('Usuario', backref='mensajes')
    reporte = db.relationship('Reportes', backref='mensajes')

    def __init__(self, id_usuario, id_reporte, descripcion):
        self.id_usuario = id_usuario
        self.id_reporte = id_reporte
        self.descripcion = descripcion


class MensajesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mensaje
        fields = ('id_mensaje', 'id_usuario', 'id_reporte', 'nombre', 'descripcion', 'fecha')

    nombre = ma.Method("get_nombre")

    def get_nombre(self, obj):
        return obj.usuario.nombre if obj.usuario else None
