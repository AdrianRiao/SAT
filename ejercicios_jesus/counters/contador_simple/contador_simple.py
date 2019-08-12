#!/usr/bin/env python3

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

cont = 5

def parse_args ():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('-p', '--port', type=int, default=PORT,
                        help="TCP port for the server")
    args = parser.parse_args()
    return args

class Handler(http.server.BaseHTTPRequestHandler):
	
    def do_GET(self):
        
        global cont # Necesito poner global para referenciar la variable de arriba
                    # Si no pongo global cada vez que asigne un valor a cont se me
                    # asignará a la variable local, no a la global. Con global le
                    # digo que en la función, cada vez que me refiera a count,
                    # me estoy referiendo a la variable global, no a la local
        print("Received: GET " + self.path)
        parsed_resource = urllib.parse.urlparse(self.path)

        self.send_response(200) # Envío un 200 0k
        self.send_header("Content-type", "text/html") # Envío cabeceras de content-type y text/html

        self.end_headers() # He acabado las cabeceras
        self.wfile.write(bytes(PAGE.format(cont=cont),
                               'utf-8')) # Envío la página HTML, y cambio en la pagina
        # el texto cont(es una plantilla) por el valor de mi variable cont
        if cont == 0:
            cont = 5
        else:
            cont = cont - 1

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()


## NOTA: Sería interesante controlar la petición del favicon
## para que no te baje el contador por arte de magia.
## Solo responder en el caso en el que el recurso solicitado
## es /.
