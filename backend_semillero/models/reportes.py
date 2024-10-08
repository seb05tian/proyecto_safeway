from config.db import app, db, ma

class Reportes(db.Model):
    __tablename__ = 'Reportes'
    id_reporte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    fecha_hora = db.Column(db.DateTime)
    ubicacion = db.Column(db.String(255))
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
   
    def __init__(self, descripcion, imagen, fecha_hora, ubicacion, id_usuario):
        self.descripcion = descripcion
        self.imagen  = imagen
        self.fecha_hora= fecha_hora
        self.ubicacion = ubicacion
        self.id_usuario = id_usuario

with app.app_context():
    db.create_all()
    

class ReportesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reportes
        fields = ('id_reporte', 'descripcion', 'imagen', 'fecha_hora', 'ubicacion', 'id_usuario')
