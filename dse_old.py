import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os, sys
import contextlib
import warnings
from modules.banner import bstring, print_banner
from creds import credentials
import argparse

parser = argparse.ArgumentParser(description='Discord Server Executor help')
parser._action_groups.pop()
requiredNamed = parser.add_argument_group('required') ### REQUIRED ARGS ###
requiredNamed.add_argument(
        "-x",
        "--xpath",
        type=str,
        required=True,
        help=("Specify XPath of target discord server. " +
            "Example: -x '/html/body/div[1]/...'"))
requiredNamed.add_argument(
        "-c",
        "--channel",
        type=str,
        required=True,
        help=("Specify XPath of target discord channel. " +
            "Example: -c '/html/body/div[1]/...'"))
requiredNamed.add_argument(
        "-m",
        "--message",
        type=str,
        required=True,
        help=("Specify message to send on channel/s. " +
            "Example: -m 'DBot attack!'"))

optionalNamed = parser.add_argument_group('optional') ### OPTIONAL ARGS ###
optionalNamed.add_argument(
        "-n",
        "--number",
        type=str,
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

args = parser.parse_args()

# Check for collisions and errors

if args.unlimited is True and args.number is not None:
    print(bstring.ERROR, "Can't use unlimited mode with limited messages. Use brain!\n")
    exit(1)

if credentials.user == '' or credentials.password == '':
    print(bstring.ERROR, "Username or password wasn't set! Go to creds folder and fill up credentials.py!\n")
    exit(1)
else:
    user = credentials.user
    password = credentials.password

if args.unlimited is False and args.number is None:
    print(bstring.ERROR, 'Unkown message number, use -u or -v option!\n')
    exit(1)

# Setup variables
discord_xpath = args.xpath 
discord_channel = args.channel
message = args.message

if args.unlimited is True:
    loop_unlimited = True
else:
    loop_unlimited = False
    message_number = args.number

# Disable warnings and selenium messages
warnings.filterwarnings("ignore", category=DeprecationWarning) 

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True) # Keep browser open after script has finished
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disble selenium messages
chrome_options.add_argument("--log-level=3") # Disable selenium messages


browser = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
element = WebDriverWait(browser, 20)

if __name__ == '__main__':
    try:
        # Start
        print_banner()

        # Open discord login page
        browser.get("https://discord.com/login")

        # Set Email
        time.sleep(0.1)
        setEmail = browser.find_element(By.XPATH, '//*[@name="email"]')
        element.until(EC.element_to_be_clickable(setEmail)).click()
        setEmail.send_keys(user)

        # Set Password
        time.sleep(0.1)
        setPassword = browser.find_element(By.XPATH, '//*[@name="password"]')
        element.until(EC.element_to_be_clickable(setPassword)).click()
        setPassword.send_keys(password)

        # Login
        time.sleep(0.1)
        browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]').click()

        # Enter choosen server
        server = element.until(EC.element_to_be_clickable((By.XPATH, discord_xpath)))
        element.until(EC.element_to_be_clickable(server)).click()

        # Enter choosen channel
        channel = element.until(EC.element_to_be_clickable((By.XPATH, discord_channel)))
        element.until(EC.element_to_be_clickable(channel)).click()

        # Click textbox field
        time.sleep(0.1)
        wrote = element.until(EC.element_to_be_clickable((By.XPATH, '//*[@role="textbox"]')))
        browser.execute_script("arguments[0].click();", wrote)

        if loop_unlimited is False:
            for x in range(message_number):
                element.until(EC.element_to_be_clickable((By.XPATH, '//*[@role="textbox"]')))
                wrote.send_keys(message)
        else:
            while(True):
                element.until(EC.element_to_be_clickable((By.XPATH, '//*[@role="textbox"]')))
                wrote.send_keys(message)


    except KeyboardInterrupt:
        pass
        print(bstring.INFO, "Interrupt received!")