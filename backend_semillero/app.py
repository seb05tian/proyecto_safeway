from flask import Flask, jsonify, request
from config.db import db, ma, app
from api.usuario_api import api_usuario
from api.administrador_api import api_administrador
from api.reportes_api import api_reportes
from api.mensaje_api import api_mensajes
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import timedelta

from models.usuario import Usuario, UsuarioSchema  
from models.mensajes import Mensaje, MensajesSchema
from models.administrador import Administrador, AdministradorSchema
from models.reportes import Reportes, ReportesSchema

with app.app_context():
    db.create_all()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/semillero_vias"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "semillero_vias"
app.config['JWT_SECRET_KEY'] = 'administradorjwt'  
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)




app.register_blueprint(api_usuario)
app.register_blueprint(api_administrador)
app.register_blueprint(api_reportes)
app.register_blueprint(api_mensajes)


@app.route('/')
def index():
    return "Bienvenido a la API de Semillero Vías"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    identificador = data.get('identificador', None) 
    contrasena = data.get('contrasena', None)

    usuario = Usuario.query.filter(
        (Usuario.nombre == identificador) | 
        (Usuario.correo_electronico == identificador)
    ).first()

    if usuario and usuario.contrasena == contrasena:
        access_token = create_access_token(identity=usuario.id_usuario)
        return jsonify(
            access_token=access_token,
            nombre=usuario.nombre,
            id=usuario.id_usuario,
            correo=usuario.correo_electronico
        ), 200
    else:
        return jsonify({"msg": "Credenciales incorrectas"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid input'}), 400

    nuevo_usuario = Usuario(
        nombre=data['name'],
        correo_electronico=data['email'],
        contrasena=data['password'],  
        
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201




if __name__ == '__main__':
    app.run(debug=True, port=5000)
        
