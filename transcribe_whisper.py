import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor
import time


def process_audio(recognizer, audio, model, fn):
    text = recognizer.recognize_whisper(audio, model=model)
    print("[whisper] transcript: ", text)

    # Cancels the noise words to some extent
    if (len(text) > 8):
        fn(text)
    else:
        print("[whisper] ignored cause noise:", text)


voice_recognition_executor = ThreadPoolExecutor(4)


def get_callback(fn):

    def callback(recognizer, audio):
        try:
            print("[whisper] processing audio")
            voice_recognition_executor.submit(process_audio, recognizer, audio,
                                              "tiny.en", fn)
        except sr.UnknownValueError:
            print("[whisper] could not understand audio")
        except sr.RequestError as e:
            print(
                "[whisper] Could not request results from whisper; {0}".format(
                    e))

    return callback


def transcribe_whisper(fn):
    recognizer = sr.Recognizer()
    callback = get_callback(fn)
    microphone = sr.Microphone()
    with microphone as source:
        print("[whisper] Calibrating...")
        recognizer.adjust_for_ambient_noise(source)

    stop_listening = recognizer.listen_in_background(microphone,
                                                     callback,
                                                     phrase_time_limit=10)
    while True:
        time.sleep(0.1)
