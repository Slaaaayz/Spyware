import subprocess
import os

with open('passwords.txt', 'w') as f:
	f.write("Availabe Wi-Fi credentials on the machine:\n")
	f.close()


command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True).stdout.decode()

path = os.getcwd()

wifi_files = []
for filename in os.listdir(path):
	if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
		wifi_files.append(filename)

for i in wifi_files:
	with open(i, 'r') as f:
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

	with open('passwords.txt', 'a') as f:
		f.write("\n[*] SSID: " + creds[0] + "\n" + "[!] Password: " + creds[1] + "\n")
		f.close()

for i in wifi_files:
	os.remove(i)