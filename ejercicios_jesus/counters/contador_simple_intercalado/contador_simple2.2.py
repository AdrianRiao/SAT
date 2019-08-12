#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contador implementado con cookies de sesión para
# que varios clientes puedan acceder concurrentemente,
# guardando un estado para cada uno. Además este servidor
# tiene la capacidad de guardar el estado de los usuarios
# cuando el servidor se caiga.

import argparse
import http.server
import http.cookies
import random
import socketserver
import string
import urllib
import shelve

PORT = 1234

PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>The value of count is: {cont}.</p>
  </body>
</html>
"""

PAGE_NOT_FOUND = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Resource not found: {resource}.</p>
  </body>
</html>
"""

# Dictionary for counts for each id
counters = shelve.open("/tmp/data.txt") # Hacemos que el diccionario counters
# se guarde en un fichero que le decimos. Siempre que nos refiramos a esta
# variable el contenido irá al fichero.

def parse_args ():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('-p', '--port', type=int, default=PORT,
                        help="TCP port for the server")
    args = parser.parse_args()
    return args

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        print("Received: GET " + self.path)
        resource = self.path
        
        if resource == '/':
            self.send_response(200)

            cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))

            if 'id' in cookies and cookies['id'].value in counters:
                id = cookies['id'].value
                cont = (counters[id] - 1) % 6
            else:
                id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
                cookie = http.cookies.SimpleCookie()
                cookie['id'] = id
                self.send_header("Set-Cookie", cookie.output(header='', sep=''))
                cont = 5
        
            counters[id] = cont
            page = PAGE.format(cont=cont)
        else:
            self.send_response(404)
            page = PAGE_NOT_FOUND.format(resource=resource)
            
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page, 'utf-8'))

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()
    counter.close ## Debemos cerrar el ficher para volcar todos los datos

if __name__ == "__main__":
    main()
