import threading
import asyncio
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from game_logic.gamebroker import GameBroker

REFRESH_RATE = 15

broker = GameBroker(7, 6, 5)
broker.add_agent()
broker.add_agent()

port = 63343
app = Flask(__name__)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect', namespace='/')
def on_connect():
    print('Client connected:', request.sid)
    broker.add_user(request.sid)
    data = broker.get_data(sid=request.sid)
    emit('room_data_response', data)


@socketio.on('info_request', namespace='/')
def on_info_request():
    data = broker.get_data()
    emit('room_data_response', data)


@app.route('/')
@socketio.on('move', namespace='/')
def on_move(column):
    if gameroom.is_player(request.sid):
        gameroom.move(request.sid, column)
        print(request.sid)
        print(column)
    emit('room_data_response', gameroom.get_data(), broadcast=True)


@socketio.on('disconnect', namespace='/')
def on_disconnect():
    broker.remove_user(request.sid)
    print('Client disconnected:', request.sid)


if __name__ == '__main__':
    threading.Thread(target=socketio.run, args=(app, ), kwargs={'port': port}).start()
    # asyncio.run(socketio.run(app, port))
    broker.execute_batch()







