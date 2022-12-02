import time
import os, sys
import requests
from modules.banner import bstring, print_banner
from creds import credentials
import argparse

parser = argparse.ArgumentParser(description='Discord Server Executor help')
parser._action_groups.pop()
requiredNamed = parser.add_argument_group('required') ### REQUIRED ARGS ###
requiredNamed.add_argument(
        "-c",
        "--channel",
        type=str,
        required=True,
        help=("Specify channel ID of target discord server. " +
            "Example: -c 362803406077032203"))
requiredNamed.add_argument(
        "-md",
        "--mode",
        type=int,
        required=True,
        help=("Choose mode. 1 - text msg only, 2 - images only, 3 - all" +
            "Example: -c 2"))
optionalNamed = parser.add_argument_group('optional') ### OPTIONAL ARGS ###
optionalNamed.add_argument(
        "-m",
        "--message",
        type=str,
        required=False,
        help=("Specify message to send on channel/s. " +
            "Example: -m 'DBot attack!'"))
optionalNamed.add_argument(
        "-i",
        "--images",
        type=str,
        required=False,
        help=("Send images. Specify image name in 'images' folder. Images count are same as text message! " +
            "Example: -i dse_image.png"))
optionalNamed.add_argument(
        "-n",
        "--number",
        type=int,
        required=False,
        help=("Number of messages to send. " +
            "Example: -c 25"))
optionalNamed.add_argument(
        "-u",
        "--unlimited",
        action='store_true',
        required=False,
        help=("Send messages with no limit. " +
            "Example: -u"))
optionalNamed.add_argument(
        "-t",
        "--time",
        type=int,
        required=False,
        help=("Time interval in seconds. Send messages with delay. It's recommended to use at least 1s to prevent token ban. " +
            "Example: -t 1"))

args = parser.parse_args()

# Check for collisions and errors

if args.unlimited is True and args.number is not None:
    print(bstring.ERROR, "Can't use unlimited mode with limited messages. Use brain!\n")
    exit(1)

if credentials.token == '':
    print(bstring.ERROR, "Token wasn't set! Go to creds folder and fill up credentials.py!\n")
    exit(1)
else:
    headers = {"authorization": credentials.token}

if args.unlimited is False and args.number is None:
    print(bstring.ERROR, 'Unkown message number, use -u or -v option!\n')
    exit(1)

if args.images is not None:
    file_path = './{}'.format(args.images)
    if os.path.exists(file_path) is True:
        files_a = {'file': (file_path, open(file_path, 'rb'))}
    else:
        print(bstring.ERROR, 'Image path is invaild!\n')
        exit(1)
else:
    files_a = None

if args.mode == 1 and args.images is not None:
    print(bstring.ERROR, 'Cannot use text message mode with -i option. Use brain!\n')
    exit(1)
if args.mode == 2 and args.message is not None:
    print(bstring.ERROR, 'Cannot use image mode with -m option. Use brain!\n')
    exit(1)
if args.mode == 3 and args.message is None and args.images is None:
    print(bstring.ERROR, 'Img+txt mode needs -i and -m options specified. Use brain!\n')
    exit(1)


# Setup variables
channelID = args.channel

if args.message is not None:
    message = {'content': args.message}
else:
    message = None

if args.unlimited is True:
    loop_unlimited = True
else:
    loop_unlimited = False
    message_number = args.number

if args.time is not None:
    sleep_time = args.time
else:
    sleep_time = 0

if args.mode == 1:
    mode = 1
elif args.mode == 2:
    mode = 2
elif args.mode == 3:
    mode = 3
else:
    print(bstring.ERROR, 'Unknown mode! Are you kidding?\n')
    exit(1)

if __name__ == '__main__':
    try:
        # Start
        print_banner()

        def send_msg(msg):
            # print(files_a)
            requests.post(f"https://discord.com/api/v9/channels/{channelID}/messages", data=msg, headers=headers, files=files_a)
            

        # if mode == 2:
        if args.unlimited is True:
            i=0
            while True:
                i=i+1
                send_msg(message)
                print("\rSent message - {}".format(i))
                time.sleep(sleep_time)
        else:
            for i in range(message_number):
                send_msg(message)
                print("\rSent message - {}/{}".format(i+1,message_number))
                time.sleep(sleep_time)


                    
                

        # if args.unlimited is True:
        #     i=0
        #     while True:
        #         i=i+1
        #         requests.post(f"https://discord.com/api/v10/channels/{channelID}/messages", data=message, headers=headers, files=files)
        #         print("\rSent message - {}".format(i))
        #         time.sleep(sleep_time)
        # else:
        #     for i in range(message_number):
        #         requests.post(f"https://discord.com/api/v10/channels/{channelID}/messages", data=message, headers=headers, files=files)
        #         print("\rSent message - {}/{}".format(i+1,message_number))
        #         time.sleep(sleep_time)

        print('\n' + bstring.INFO, 'Job completed!\n')
        exit(0)
                
    except KeyboardInterrupt:
        pass
        print(bstring.INFO, "\nInterrupt received!\n")