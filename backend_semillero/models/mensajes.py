from config.db import app, db, ma 
from datetime import datetime
from sqlalchemy.sql import func
from models.usuario import Usuario  

class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    
    id_mensaje = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, server_default=func.now())

    def __init__(self, id_usuario, descripcion):
        self.id_usuario = id_usuario
        self.descripcion = descripcion


class MensajesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mensaje
        fields = ('id_mensaje', 'id_usuario', 'nombre', 'descripcion', 'fecha')

    nombre = ma.Method("get_nombre")  

    def get_nombre(self, obj):
        usuario = Usuario.query.get(obj.id_usuario)  
        return usuario.nombre if usuario else None  
