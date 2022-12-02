class bstring:
    ERROR = '[\033[91merror\033[0m]'
    INFO = '[\033[92minfo\033[0m]'
    ACTION = '[\033[93maction\033[0m]'
    INPUT = '[\033[94minput\033[0m]'
    VIOLET = '\033[95m' 
    BLUE = '\033[96m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():

    print(bstring.BLUE + """\
╔╦╗┬┌─┐┌─┐┌─┐┬─┐┌┬┐  ╔═╗┌─┐┬─┐┬  ┬┌─┐┬─┐  ╔═╗─┐ ┬┌─┐┌─┐┬ ┬┌┬┐┌─┐┬─┐
 ║║│└─┐│  │ │├┬┘ ││  ╚═╗├┤ ├┬┘└┐┌┘├┤ ├┬┘  ║╣ ┌┴┬┘├┤ │  │ │ │ │ │├┬┘
═╩╝┴└─┘└─┘└─┘┴└──┴┘  ╚═╝└─┘┴└─ └┘ └─┘┴└─  ╚═╝┴ └─└─┘└─┘└─┘ ┴ └─┘┴└─""" + bstring.RESET +
bstring.BOLD + """
[ Discord Server Executor v1.0 ] [ Created by github.com/cr4sh-me ]
""" + bstring.RESET)

def print_banner_server():

    print(bstring.VIOLET + """\

╔╦╗╔═╗╔═╗  ╔═╗┌─┐┬─┐┬  ┬┌─┐┬─┐
 ║║╚═╗║╣   ╚═╗├┤ ├┬┘└┐┌┘├┤ ├┬┘
═╩╝╚═╝╚═╝  ╚═╝└─┘┴└─ └┘ └─┘┴└─""" + bstring.RESET +
bstring.BOLD + """
[ DSE Server v1.0 ] [ Created by github.com/cr4sh-me ]
""" + bstring.RESET)