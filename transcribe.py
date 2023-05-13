from threading import Thread
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor
from ai import doctor_helper

recognizer = sr.Recognizer()
microphone = sr.Microphone()

transcript_futures = []
last_transcript = ""
voice_recognition_executor = ThreadPoolExecutor(5)


def process_audio(recognizer, audio, model):
    text = recognizer.recognize_whisper(audio, model=model)
    print("transcript", text)
    # Cancels the noise words to some extent
    if (len(text) > 8):
        last_transcript += text
        ai_response = doctor_helper(inputs={"transcript": "Hello there!"})
    else:
        print("ignored noise", text)
    return {"transcript": last_transcript, "ai_response": ai_response}


def transcribe_google():
    pass


def transcribe_whisper():

    def callback(recognizer, audio):
        try:
            print("processing audio")
            future = voice_recognition_executor.submit(process_audio,
                                                       recognizer, audio,
                                                       "tiny.en")
            transcript_futures.append(future)
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from whisper; {0}".format(e))

    with microphone as source:
        print("Calibrating...")
        recognizer.adjust_for_ambient_noise(source)
        stop_listening = recognizer.listen_in_background(microphone,
                                                         callback,
                                                         phrase_time_limit=10)
        stop_listening()