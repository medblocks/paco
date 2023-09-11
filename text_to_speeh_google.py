from google.cloud import texttospeech


def save_to_audio_file(audio_content):
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(audio_content)
        print('Audio content written to file "output.mp3"')


def synthesize(text):
    print('[gcp tts] rendering', text)
    client = texttospeech.TextToSpeechClient()
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="hi-IN",
        name="hi-IN-Neural2-B",
        # language_code="ta-IN",
        # name="ta-IN-Wavenet-A"
        )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        speaking_rate=0.9, audio_encoding=texttospeech.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input,
                                        voice=voice,
                                        audio_config=audio_config)
    return response.audio_content
