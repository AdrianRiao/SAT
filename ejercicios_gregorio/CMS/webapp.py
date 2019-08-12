#!/usr/bin/python3

"""
webApp class
 Root for hierarchy of classes implementing web applications

 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket

def dihola():
    return("hola")

class webApp(): ## Es una Clase
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>") ## Devuelve una tupla

    def __init__(self, hostname, port): ## Es el método constructor de la clase, tiene dos parámetros, hostname y port.
                                        ## Nota: en Python como regla los métodos tienen un primer parámetro que es self.
                                        ## Cuando se llama al método el primer parámetro self se obvia, y no se pone.
                                        ## El self es el propio objeto con el que llamas al método
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048).decode('utf-8')
            print(request)
            parsedRequest = self.parse(request) ## Llamo al método parse de mi clase
            (returnCode, htmlAnswer) = self.process(parsedRequest) ## Llamo al método process
            print('Answering back...')
            recvSocket.send(b"HTTP/1.1 " + bytes(returnCode, "utf-8") + b" \r\n\r\n"
                            + bytes(htmlAnswer, "utf-8") + b"\r\n")
            recvSocket.close()

class Aleat(webApp): ## Clase que llamamos Aleat y deriva de la clase webApp, tiene todos sus métodos

    def process(self, parsedRequest):
        import random
        num = str(random.randrange(1,10000000000000))
        return ("200 OK", "<html><body><h1><a href=' " + num + " '>Dame otra</a></h1></body></html>")

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234) ## Creo un objeto llamando a la clase, que se guarda en la variable testWebApp
                                           ## Cuando instancio el objeto de la clase llamo al constructor
