import socketio
from flask import Flask

sio = socketio.Server(cors_allowed_origins='*', async_mode='threading')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@sio.event
def connect(sid):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def start_recording(sid):
    print('start recording ', sid)


@sio.event
def stop_recording(sid):
    print('stop recording ', sid)


@sio.event
def reset(sid):
    print('reset', sid)


def send_transcript(text):
    sio.emit('transcript', text)


def send_ai_message(text):
    sio.emit('ai_message', text)


def start_socketio_server():
    app.run('0.0.0.0', 5000)