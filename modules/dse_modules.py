# Inspired some code from https://github.com/CryonicsX/Discord-Spammer :D

import random
import requests
from banner import bstring

with open("useragent.txt" , encoding="utf-8") as f:
    useragent = random.choice(f.readlines()).split("\n")[0]


with open("proxies.txt" , encoding="utf-8") as f:
    proxies = random.choice(f.readlines()).split("\n")[0]

def send_message(token, channelID, message, userAgent, proxies):
    msg = {'content': message}
    headers = {"authorization": token , "User-Agent" : userAgent , "tts" : "false"}
    proxies = {"http" : proxies}

    try:
        request = requests.post(f"https://discordapp.com/api/v10/channels/{channelID}/messages", data=msg , headers=headers , proxies=proxies)
    except Exception as err:
            print(bstring.ERROR, "Error:", err)
    if request.status_code == 200:
        print(bstring.INFO, "Message sent")
    else:
        print(bstring.ERROR, "Message not sent:", request.json())

def join_server(token, guildid, useragent, proxies):
    headers = {"content-type": "false",	"authorization": token , "User-Agent" : useragent}
    proxies = {"http" : proxies}

    try:
        request = requests.post(f"https://discordapp.com/api/v10/invite/{guildid}" , headers=headers , proxies=proxies)
    except Exception as err:
            print(bstring.ERROR, "Error:", err)
    if request.status_code == 200:
        print(bstring.INFO, "Joined server!")
    else:
        print(bstring.ERROR, "Can't join server:", request.json())

def leave_server(token, guildid, useragent, proxies):
    headers = {"content-type": "false",	"authorization": token , "User-Agent" : useragent}
    proxies = {"http" : proxies}

    try:
        request = requests.delete(f"https://discordapp.com/api/v10/invite/{guildid}" , headers=headers , proxies=proxies)
    except Exception as err:
            print(bstring.ERROR, "Error:", err)
    if request.status_code == 200:
        print(bstring.INFO, "Left server!")
    else:
        print(bstring.ERROR, "Can't leave server:", request.json())

def friend_request(token, userid, userAgent, proxies):
	headers = {"content-type": "application/json",	"authorization": token , "User-Agent" : userAgent}
	proxies = {"http" : proxies}
	try:
		request = requests.put(f"https://discordapp.com/api/v10/users/@me/relationships/{userid}" , headers=headers , proxies=proxies)
	except Exception as err:
		print(bstring.ERROR, "Error:", err)
	if request.status_code == 204:
		print(bstring.INFO, "Friend request sent!")
	else:
		print(bstring.ERROR, "Can't send friend requet:", request.json())