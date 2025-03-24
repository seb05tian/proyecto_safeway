from config.db import db, app, ma

class Administrador(db.Model):
    __tablename__ = 'Administrador'
    id_administrador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), unique=True, nullable=False)
    nivel_acceso = db.Column(db.String(50), default='alto')

    def __init__(self, id_usuario, nivel_acceso='alto'):
        self.id_usuario = id_usuario
        self.nivel_acceso = nivel_acceso




class AdministradorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Administrador
        fields = ('id_administrador', 'nivel_acceso', 'id_usuario')
