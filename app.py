import socketio
from flask import Flask
from main import transcript, doctor_summary
from llm import patient_instruction_memory, patient_instructor
from socketcallback import SocketIOCallback

sio = socketio.Server(cors_allowed_origins='*', async_mode='threading')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@sio.event
def connect(sid, env):
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
def set_summary(sid, text):
    global doctor_summary
    doctor_summary = text
    print('set_summary ', sid, doctor_summary)


@sio.event
def patient_question(sid, text):
    callback = SocketIOCallback(lambda x: sio.emit('patient_answer', x))
    result = patient_instructor.run({
        "input": text,
        "summary": doctor_summary
    },
                                    callbacks=[callback])
    sio.emit('patient_answer_final', result)


@sio.event
def reset(sid):
    global transcript
    global doctor_summary
    global patient_instruction_memory
    transcript = ""
    doctor_summary = ""
    patient_instruction_memory.clear()
    print('reset complete', sid)


def send_transcript(text):
    sio.emit('transcript', text)


def send_ai_message(text):
    sio.emit('ai_message', text)


def send_patient_instructions(text):
    sio.emit('patient_instructions', text)


def start_socketio_server():
    app.run('0.0.0.0', 5000)
