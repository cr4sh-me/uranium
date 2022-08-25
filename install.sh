#!/bin/bash

action="\n[\e[93maction\e[0m]"
error="\n[\e[91merror\e[0m]"
info="\n[\e[92minfo\e[0m]"

if [[ $EUID -ne 0 ]]; then
   printf "$error Run me as root!\n" 
   exit 1
fi

clear

printf "$action Installing...\n"

apt update

command -v python3 >/dev/null 2>&1 || { printf >&2 "$action Installing package - python3"; apt-get install python3 -y; }
command -v pip3 >/dev/null 2>&1 || { printf >&2 "$action Installing package - pip3"; apt-get install python3-pip -y; }

pip3 install flask argparse

printf "$info Installation done!\n"