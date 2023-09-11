import pyaudio
import speech_recognition as sr


def get_mic_index(name):
    for i in range(pyaudio.PyAudio().get_device_count()):
        info = pyaudio.PyAudio().get_device_info_by_index(i)
        if info.get('name') == name:
            return i


recognizer = sr.Recognizer()
device_index = get_mic_index("Ecamm Live Virtual Mic")
microphone = sr.Microphone(device_index=device_index)