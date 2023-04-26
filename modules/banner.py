class bstring:
    ERROR = '[\033[91merror\033[0m]'
    INFO = '[\033[92minfo\033[0m]'
    ACTION = '[\033[93maction\033[0m]'
    CREDS = '[\033[1;95;5mcreds\033[0m]'
    INPUT = '[\033[94minput\033[0m]'
    VIOLET = '\033[95m' 
    BLUE = '\033[96m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():

    print(bstring.VIOLET + """\
 ____ ___                      .__                  _____          
|    |   \____________    ____ |__|__ __  _____    /  _  \ ______  
|    |   /\_  __ \__  \  /    \|  |  |  \/     \  /  /_\  \\____ \ 
|    |  /  |  | \// __ \|   |  \  |  |  /  Y Y  \/    |    \  |_> >
|______/   |__|  (____  /___|  /__|____/|__|_|  /\____|__  /   __/
                      \/     \/               \/         \/|__|""" + bstring.RESET +
bstring.BOLD + """
[ UraniumAp v1 ] [ Created by github.com/cr4sh-me ]
""" + bstring.RESET)