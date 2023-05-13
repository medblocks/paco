from serve import serve
from transcribe_google import transcribe_gcp
from transcribe_whisper import transcribe_whisper
if __name__ == "__main__":
    print("Running transcribe thread")

    print("Running server thread")
    transcribe_gcp(lambda x: print(x))