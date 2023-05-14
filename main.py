from transcribe_google import transcribe_gcp
from transcribe_whisper import transcribe_whisper
from threading import Thread
from app import send_transcript, start_socketio_server, send_ai_note
from state import state_store
from llm import cds_helper
from socketcallback import SocketIOCallback
import os

USE_WHISPER = os.getenv("USE_WHISPER", "false") == "true"

if USE_WHISPER:
    transcribe = transcribe_whisper
else:
    transcribe = transcribe_gcp

ai_note_set = False


def transcript_callback(text):
    global ai_note_set
    global state_store
    if state_store["patient_mode"]:
        send_transcript(text)
    else:
        state_store["transcript"] += text + "\n"
        send_transcript(state_store["transcript"])
        callbacks = None
        if not ai_note_set:
            stream_callback = SocketIOCallback(lambda x: send_ai_note(x))
            callbacks = [stream_callback]
            ai_note_set = True
        ai_note = cds_helper.run({"transcript": state_store["transcript"]},
                                 callbacks=callbacks)
        send_ai_note(ai_note)


if __name__ == "__main__":
    print("[main] Running server thread")
    thread = Thread(target=start_socketio_server)
    thread.start()
    print("[main] Running transcribe thread")
    transcribe(transcript_callback)
    thread.join()
