from concurrent.futures import ThreadPoolExecutor
from utils import recognizer, microphone
from state import state_store


def process_audio(recognizer, audio, model, fn):
    text = recognizer.recognize_whisper_api(audio)
    print("[whisper] transcript: ", text)

    # Cancels the noise words to some extent
    if (len(text) > 8):
        fn(text)
    else:
        print("[whisper] ignored cause noise:", text)


voice_recognition_executor = ThreadPoolExecutor(4)


def get_callback(fn):

    def callback(recognizer, audio):
        voice_recognition_executor.submit(process_audio, recognizer, audio,
                                          "small.en", fn)

    return callback


with microphone as source:
    print("[whisper] Calibrating...")
    recognizer.adjust_for_ambient_noise(source)


def transcribe_whisper(fn):
    callback = get_callback(fn)

    print("[whisper] Listening...")
    stop = recognizer.listen_in_background(microphone,
                                           callback,
                                           phrase_time_limit=10)
    return stop