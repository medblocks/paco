from serve import serve
from transcribe_google import transcribe_gcp
from transcribe_whisper import transcribe_whisper
from threading import Thread
from app import send_transcript

transcribe = transcribe_gcp
transcript = ""
doctor_summary = ""

def transcript_callback(text):
    global transcript
    transcript += text + "\n"
    send_transcript(transcript)


if __name__ == "__main__":
    print("Running server thread")
    # serve()
    thread = Thread(target=serve)
    thread.start()
    print("Running transcribe thread")
    transcribe(transcript_callback)
    thread.join()
