#!/bin/bash
# check_update.sh for Uranium

check_internet() {
    printf "\e[0m[\e[93maction\e[0m] Checking for internet connection... \n"
    if ! ping -q -c1 google.com &>/dev/null; then
        printf "\e[0m[\e[91merror\e[0m] Network isn't avaiable! \n"
        exit
    fi
}

check_update() {
    check_internet
    changed=0
    git remote update && LC_ALL=C git status -uno | grep -q 'Your branch is behind' && changed=1
    if [ $changed = 1 ]; then
        printf "\n\e[0m[\e[92minfo\e[0m] Update avaiable!"
        printf "\n\e[0m[\e[93maction\e[0m] Updating! Please wait... \n"
        git stash
        git stash drop
        git pull
    else
        printf "\n\e[0m[\e[91merror\e[0m] No updates avaiable!"
        exit
    fi
}

check_update
