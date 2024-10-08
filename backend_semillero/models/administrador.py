from config.db import app, db, ma

class Administrador(db.Model):
    __tablename__ = 'Administradores'
    id_administrador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nivel_acceso = db.Column(db.String(50), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), unique=True)

    def __init__(self, nivel_acceso, id_usuario):
        self.nivel_acceso = nivel_acceso
        self.id_usuario = id_usuario


with app.app_context():
    db.create_all()

class AdministradorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Administrador
        fields = ('id_administrador', 'nivel_acceso', 'id_usuario')
