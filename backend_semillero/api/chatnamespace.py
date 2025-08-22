from flask_socketio import Namespace, emit, join_room
from flask_jwt_extended import decode_token
from flask import request

class ChatNamespace(Namespace):
    def on_connect(self):
        token = request.args.get('token')
        try:
            decode_token(token)  # valida
            emit('connected', {'ok': True})
        except Exception:
            return False

    def on_join(self, data):
        room = f"reporte:{data.get('id_reporte')}"
        join_room(room)
        emit('joined', {'room': room})
