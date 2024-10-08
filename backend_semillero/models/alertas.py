from config.db import app, db, ma

class Alertas(db.Model):
    __tablename__ = "Alertas"

    id_alerta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255))
    ubicacion = db.Column(db.String(255))
    id_reporte = db.Column(db.Integer, db.ForeignKey('Reportes.id_reporte'))

    def __init__(self, descripcion, ubicacion, id_reporte):
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.id_reporte = id_reporte

with app.app_context():
    db.create_all()


class AlertasSchema(ma.Schema):
    class Meta:
        fields = ('id_alerta', 'descripcion', 'ubicacion', 'id_reporte')
