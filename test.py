import requests
import random




token = "NzAxMTYyNTAwMzM0NTUxMTEx.GXk5yH.WqTj6iIdZkmOToM4SgIlYaEACNhfJmGJ_E5wwc"
message = "Test"
headers = {"authorization": token , "User-Agent" : useragent, "tts" : "false"}
proxies = {"http" : proxies}
channelID = 1047596177241145375
message = {
    'content': "Test"
}

print('Using proxy:', proxies)

for i in range(5):
    x = requests.post(f"https://discord.com/api/v9/channels/{channelID}/messages", data=message, headers=headers, proxies=proxies)
    if x.status_code == 200:
        print('Sent successfully!')
    else:
        print('Failed. ', x.json())

