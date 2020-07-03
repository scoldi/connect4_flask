import time
import threading
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
# Hz
from game_logic.gameroom import GameRoom

gameroom = GameRoom(7, 6)

REFRESH_RATE = 15

# request.sid

port = 63343
app = Flask(__name__)
# field = field

app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# thread_lock = Lock()


@app.route('/')
@socketio.on('move', namespace='/')
def on_move(column):
    if gameroom.is_player(request.sid):
        gameroom.move(request.sid, column)
        print(request.sid)
        print(column)
    emit('room_data_response', gameroom.get_data(), broadcast=True)


@socketio.on('connect', namespace='/')
def on_connect():
    print('Client connected:', request.sid)
    gameroom.add_user(request.sid)
    data = gameroom.get_data(sid=request.sid)
    emit('room_data_response', data)


@socketio.on('disconnect', namespace='/')
def on_disconnect():
    gameroom.remove_user(request.sid)
    print('Client disconnected:', request.sid)


if __name__ == '__main__':
    socketio.run(app, port=port)




