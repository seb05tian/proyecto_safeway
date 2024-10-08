from flask import Flask, jsonify, request
from config.db import db, ma
from api.usuario_api import api_usuario
from api.cliente_api import api_cliente
from api.administrador_api import api_administrador
from api.reportes_api import api_reportes
from api.alertas_api import api_alertas
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models.usuario import Usuario, UsuarioSchema
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/semillero_vias"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "semillero_vias"
app.config['JWT_SECRET_KEY'] = 'administradorjwt'  
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)

# Registrar los Blueprints
app.register_blueprint(api_usuario)
app.register_blueprint(api_cliente)
app.register_blueprint(api_administrador)
app.register_blueprint(api_reportes)
app.register_blueprint(api_alertas)


@app.route('/')
def index():
    return "Bienvenido a la API de Semillero Vías"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    identificador = data.get('identificador', None)  # Esto debe coincidir con el frontend
    contrasena = data.get('contrasena', None)  # Esto debe coincidir con el frontend

    usuario = Usuario.query.filter(
        (Usuario.nombre == identificador) | 
        (Usuario.correo_electronico == identificador)
    ).first()

    if usuario and usuario.contrasena == contrasena:
        access_token = create_access_token(identity=usuario.id_usuario)
        return jsonify(access_token=access_token), 200
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
        contrasena=data['password'],  # Considera hashear esta contraseña
        rol='cliente'
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
