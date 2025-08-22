from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from datetime import timedelta

from config.db import db, ma
from api.usuario_api import api_usuario
from api.administrador_api import api_administrador
from api.reportes_api import api_reportes
from api.mensaje_api import api_mensajes
from models.usuario import Usuario
from flask_socketio import SocketIO, Namespace, emit, join_room
from api.chatnamespace import ChatNamespace

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

   
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/semillero_vias"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "semillero_vias"

    
    app.config['JWT_SECRET_KEY'] = 'administradorjwt'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)

  
    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

  
    app.register_blueprint(api_usuario)
    app.register_blueprint(api_administrador)
    app.register_blueprint(api_reportes)
    app.register_blueprint(api_mensajes)

   
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
   
    app.extensions['socketio'] = socketio

    class ChatNamespace(Namespace):
        """
        Namespace /chat
        - on_connect: valida el JWT recibido por querystring ?token=...
        - on_join: el cliente se une a la sala del reporte: "reporte:<id>"
        """
        def on_connect(self):
            token = request.args.get('token', None)
            if not token:
               
                return False
            try:
               
                decode_token(token)
                emit('connected', {'ok': True})
            except Exception:
                
                return False

        def on_join(self, data):
            
            id_reporte = data.get('id_reporte', None)
            if id_reporte is None:
                emit('error', {'message': 'id_reporte requerido'})
                return
            room = f"reporte:{id_reporte}"
            join_room(room)
            emit('joined', {'room': room})

    socketio.on_namespace(ChatNamespace('/chat'))
 
   
    @app.route('/')
    def index():
        return "Bienvenido a la API de Semillero Vías"

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json or {}
        identificador = data.get('identificador')
        contrasena = data.get('contrasena')

        if not identificador or not contrasena:
            return jsonify({"msg": "Datos incompletos"}), 400

        usuario = Usuario.query.filter(
            (Usuario.nombre == identificador) |
            (Usuario.correo_electronico == identificador)
        ).first()

        if usuario and usuario.contrasena == contrasena:
            token = create_access_token(identity=usuario.id_usuario)
            return jsonify(
                access_token=token,
                nombre=usuario.nombre,
                id=usuario.id_usuario,
                correo=usuario.correo_electronico,
                rol=usuario.rol
            ), 200

        return jsonify({"msg": "Credenciales incorrectas"}), 401

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json or {}
        if not data or 'name' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Invalid input'}), 400

        nuevo_usuario = Usuario(
            nombre=data['name'],
            correo_electronico=data['email'],
            contrasena=data['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado exitosamente'}), 201

    
    return app, socketio



if __name__ == '__main__':
    app, socketio = create_app()

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
