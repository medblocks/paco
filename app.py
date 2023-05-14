import socketio
from flask import Flask
from llm import patient_instructor, clinical_note_writer
from socketcallback import SocketIOCallback
from state import state_store
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
    global state_store
    state_store["doctor_summary"] = text
    print('set_summary', sid, state_store["doctor_summary"])


@sio.event
def generate_notes(sid, doctors_hints):
    global state_store
    print("transcript for note generation", state_store["transcript"])
    print("doctors_hints", doctors_hints)
    steam_handler = SocketIOCallback(lambda x: sio.emit('generate_notes', x))
    notes = clinical_note_writer.run(
        {
            "input": doctors_hints,
            "transcript": state_store["transcript"]
        },
        callbacks=[steam_handler])
    print("Generated notes", notes)
    sio.emit('generate_notes', notes)


@sio.event
def patient_mode(sid, boolean):
    global state_store
    state_store["patient_mode"] = boolean
    print('patient_mode', sid)


@sio.event
def patient_message(sid, text):
    callback = SocketIOCallback(
        lambda partial_ai_response: sio.emit('patient_message', {
            "text": partial_ai_response,
            "done": False
        }))
    memory = state_store["patient_instruction_memory"]
    history = memory.load_memory_variables({})["history"]
    print("history from memory", history)
    ai_response = patient_instructor.run(
        {
            "input": text,
            "history": history,
            "doctor_summary": state_store["doctor_summary"]
        },
        callbacks=[callback])
    memory.chat_memory.add_user_message(text)
    memory.chat_memory.add_ai_message(ai_response)
    sio.emit('patient_message', {"text": ai_response, "done": True})


# @sio.event
# def reset(sid):
#     global transcript
#     global doctor_summary
#     global patient_instruction_memory
#     transcript = ""
#     doctor_summary = ""
#     patient_instruction_memory.clear()
#     print('reset complete', sid)


def send_transcript(text):
    sio.emit('transcript', text)


def send_patient_transcript(text):
    sio.emit('patient_transcript', text)


def send_ai_note(text):
    sio.emit('ai_note', text)


def send_patient_instructions(text):
    sio.emit('patient_instructions', text)


def start_socketio_server():
    app.run('0.0.0.0', 5000)
