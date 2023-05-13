import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor


def process_audio(recognizer, audio, fn):
    print("[gcp] in thread: ", audio)
    text = recognizer.recognize_google_cloud(audio, show_all=True)

    print("[gcp] transcript: ", text)

    # Cancels the noise words to some extent
    if (len(text) > 8):
        fn(text)
    else:
        print("[gcp] ignored cause noise:", text)


voice_recognition_executor = ThreadPoolExecutor(4)


def get_callback(fn):

    def callback(recognizer, audio):
        try:
            print("[gcp] processing audio")
            voice_recognition_executor.submit(process_audio, recognizer, audio,
                                              fn)
        except sr.UnknownValueError:
            print("[gcp] could not understand audio")
        except sr.RequestError as e:
            print("[gcp] Could not request results from gcp; {0}".format(e))

    return callback


def transcribe_gcp(fn):
    recognizer = sr.Recognizer()
    callback = get_callback(fn)
    microphone = sr.Microphone()
    with microphone as source:
        print("[gcp] Calibrating...")
        recognizer.adjust_for_ambient_noise(source)
    recognizer.listen_in_background(microphone, callback, phrase_time_limit=10)
