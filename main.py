from transcribe_google import transcribe_gcp
from transcribe_whisper import transcribe_whisper
from threading import Thread
from app import send_transcript, start_socketio_server, send_ai_note, send_patient_transcript, send_cds_ddx, send_cds_qa
from state import state_store
from llm import cds_helper, cds_helper_ddx, cds_helper_qa
from socketcallback import SocketIOCallback
from concurrent.futures import ThreadPoolExecutor
import os

USE_WHISPER = os.getenv("USE_WHISPER", "false") == "true"

if USE_WHISPER:
    transcribe = transcribe_whisper
else:
    transcribe = transcribe_gcp

ai_note_set = 0


def run_on_transcript(text, sendFn, chain):
    global ai_note_set
    print("[tread] running transcript", text)
    callbacks = None
    if ai_note_set < 2:
        callbacks = [SocketIOCallback(sendFn)]
        ai_note_set += 1
    print("[thread] runnin chain", text, sendFn, chain)
    final_result = chain.run({"transcript": text}, callbacks=callbacks)
    print("[thread] final_result", final_result)
    sendFn(final_result)
    print("[thread] final_result sent", sendFn.__name__)


def transcript_callback(text):
    global ai_note_set
    global state_store
    global run_transcript
    global cds_helper_ddx
    print("[main] transcript callback. patient_mode:{}, patient_recording:{}".
          format(state_store["patient_mode"],
                 state_store["patient_recording"]))
    if state_store["patient_mode"] and state_store["patient_recording"]:
        send_patient_transcript(text)
    if not state_store["patient_mode"]:
        state_store["transcript"] += text + "\n"
        send_transcript(state_store["transcript"])
        with ThreadPoolExecutor(4) as e:
            e.submit(run_on_transcript, state_store["transcript"], send_cds_qa,
                     cds_helper_qa)
            e.submit(run_on_transcript, state_store["transcript"],
                     send_cds_ddx, cds_helper_ddx)
        # callbacks = None
        # if not ai_note_set:
        #     stream_callback = SocketIOCallback(lambda x: send_ai_note(x))
        #     callbacks = [stream_callback]
        #     ai_note_set = True
        # ai_note = cds_helper.run({"transcript": state_store["transcript"]},
        #                          callbacks=callbacks)
        # send_ai_note(ai_note)


if __name__ == "__main__":
    # cds_helper_ddx.run({"transcript": "hello world"}, callbacks=None)
    print("[main] Running server thread")
    thread = Thread(target=start_socketio_server)
    thread.start()
    print("[main] Running transcribe thread")
    transcribe(transcript_callback)
    thread.join()
