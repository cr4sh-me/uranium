from flask import Flask, redirect, url_for, request, render_template, request
from modules.banner import bstring, print_banner_server
import os
import argparse
import datetime
import subprocess
import flask.cli
import logging
import re

# pip3 install flask argparse

parser = argparse.ArgumentParser(description='DSE server help')
parser._action_groups.pop()
requiredNamed = parser.add_argument_group('required') ### REQUIRED ARGS ###
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
        "-v",
        "--verbose",
        action='store_true',
        required=False,
        help=("Unhide default flask messages like GET/POST etc. " +
            "Example: -v"))

args = parser.parse_args()

HOST_NAME = "127.0.0.1"
PORT = (args.port)

flask.cli.show_server_banner = lambda *args: None # disable flask app default messages

if args.verbose is False:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    
    error = None
    code = None
    if request.method == "POST":
        # current_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
        channel_id = request.form['a']
        time = request.form['b']
        message = request.form['c']
        unlimited = request.form.get('e') # returns None or 'on'
        mode = request.form.get('options')
        image = request.form['img']

        print('\n', image, '\n')

        if unlimited == 'on' :
            unlimited_run = True
        else:
            unlimited_run = False
            message_count = request.form['d']

        # Catch errors
        if unlimited_run == False:
            if channel_id == '' or message == '' or message_count == '':
                print(bstring.INFO, "Empty input error!")
                error = "Empty imput. Use brain!"
                return render_template('/index.html', error=error) 
        elif unlimited_run == True:
            if channel_id == '' or message == '':
                print(bstring.INFO, "Empty input error!")
                error = "Empty imput. Use brain!"
                return render_template('/index.html', error=error)
        
        print(bstring.INFO, "Launching DSE...\n")
        # Set up the dse.py command
        code = 'python3 dse.py -c ' + channel_id 
        if mode == 'mode1':
            code = code + ' -m "' + message +  '"' + ' -md 1 '
        elif mode == 'mode2':
            code = code + ' -i "' + image +  '"' + ' -md 2 '
        else:
            code = code + ' -m "' + message +  '"' + ' -i "' + image +  '"' + ' -md 3 '

        if unlimited_run == True:
            code = code + ' -u'
        elif message_count != '':
            code = code + ' -n ' + message_count
        

        if time != '':
            code = code + ' -t ' + time

        os.system(r'"%s"' % code) 
        render_template('/redirect.html', error=code)
        return render_template('/redirect.html', error=code) # Not an error, just sending cmd to redirect.html 

    else:
        print(bstring.INFO, 'DSE panel loaded!')
        return render_template('/index.html') 


if __name__ == '__main__':
    os.system('cls') # Windows
    print_banner_server()
    print(bstring.INFO, "Server started http://%s:%s" % (HOST_NAME,PORT))
    try:
        app.run(host=HOST_NAME, port=PORT)
    except KeyboardInterrupt:
        pass
        print(bstring.ERROR + "Server stopped!")
        app.stop()