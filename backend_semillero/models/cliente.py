from config.db import app, db, ma

class Cliente(db.Model):
    __tablename__ = 'Clientes'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), unique=True)

    def __init__(self, direccion, telefono, id_usuario):
        
        self.direccion = direccion
        self.telefono  = telefono 
        self.id_usuario= id_usuario
        
with app.app_context():
    db.create_all()


class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        fields = ('id_cliente', 'direccion', 'telefono', 'id_usuario')
