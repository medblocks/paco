import pyaudio
import asyncio
import base64
import json
import websockets

FRAMES_PER_BUFFER = 32000
FORMAT = pyaudio.paInt16
CHANNELS = 1

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000&speaker_labels=true&speakers_expected=2"
auth_key = "83dd675b820c41199099ac460c476f08"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=16000,
                input=True,
                frames_per_buffer=FRAMES_PER_BUFFER)


async def send_receive():

    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
            URL,
            extra_headers=(("Authorization", auth_key),),
            ping_interval=5,
            ping_timeout=20
    ) as _ws:

        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

                await asyncio.sleep(0.01)

            return True

        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(str(result_str))
                    # print(result_str)
                    if result['message_type'] == 'FinalTranscript':
                        print(f"Final transcript received: {result_str}")
                    elif result['message_type'] == 'PartialTranscript':
                        print(f"Partial transcript received: {result['text']}")


                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())

while True:
    asyncio.run(send_receive())
