#!/usr/bin/env python3
# Contador implementado con cookies de datos para
# que varios clientes puedan acceder concurrentemente,
# guardando un estado para cada uno.


import argparse
import http.server
import http.cookies
import socketserver
import urllib

PORT = 1234

PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>The value of count is: {cont}.</p>
  </body>
</html>
"""

def parse_args ():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('-p', '--port', type=int, default=PORT,
                        help="TCP port for the server")
    args = parser.parse_args()
    return args

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        print("Received: GET " + self.path)
        parsed_resource = urllib.parse.urlparse(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")

        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))

        if 'cont' in cookies:
            cont = (int(cookies['cont'].value) - 1) % 6
        else:
            cont = 5

        cookie = http.cookies.SimpleCookie()
        cookie['cont'] = cont
        self.send_header("Set-Cookie", cookie.output(header='', sep=''))

        self.end_headers()
        self.wfile.write(bytes(PAGE.format(cont=cont),
                               'utf-8'))

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()
