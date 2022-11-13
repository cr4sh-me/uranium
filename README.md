[![GitHub license](https://img.shields.io/github/license/cr4sh-me/uranium)](https://github.com/cr4sh-me/uranium/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/cr4sh-me/uranium)](https://github.com/cr4sh-me/uranium/issues)
[![GitHub stars](https://img.shields.io/github/stars/cr4sh-me/uranium)](https://github.com/cr4sh-me/uranium/stargazers)

[<p align="left"><img src="https://github.com/cr4sh-me/uranium/blob/main/uranium_logo.png" /></p>](https://github.com/cr4sh-me/uranium/blob/main/uranium_logo.png)

# Uranium
Creates fake AP with captive portal login redirection!

## Setup
`chmod +x *`  
`sudo bash install.sh`

## uranium usage
`sudo python3 uranium.py --help`

## Nethunter
If you're getting iptables errors, try older one (1.6.2)  
`wget http://old.kali.org/kali/pool/main/i/iptables/iptables_1.6.2-1.1_arm64.deb`  
`wget http://old.kali.org/kali/pool/main/i/iptables/libip4tc0_1.6.2-1.1_arm64.deb`  
`wget http://old.kali.org/kali/pool/main/i/iptables/libip6tc0_1.6.2-1.1_arm64.deb`  
`wget http://old.kali.org/kali/pool/main/i/iptables/libiptc0_1.6.2-1.1_arm64.deb`  
`wget http://old.kali.org/kali/pool/main/i/iptables/libxtables12_1.6.2-1.1_arm64.deb`  
`dpkg -i *.deb`  
`apt-mark hold iptables`  
`apt-mark hold libip4tc0`  
`apt-mark hold libip6tc0`  
`apt-mark hold libiptc0`  
`apt-mark hold libxtables12`  
 

# Todo

+ Add support for nethunter
+ Add option for upstreaming network
+ Add more usefull options
+ Optimise code


