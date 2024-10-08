from config.db import app, db, ma

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    correo_electronico = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(100))
    rol = db.Column(db.String(50), default='cliente')  

    def __init__(self, nombre, correo_electronico, contrasena, rol):
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena
        self.rol = rol 

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        fields = ('id_usuario', 'nombre', 'correo_electronico', 'contrasena', 'rol')

