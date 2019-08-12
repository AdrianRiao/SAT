#!/usr/bin/python3
"""
Simple HTTP Server
Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket

# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET: utilizo Ipv4
# socket.AF_INET: utilizo Ipv
# socket.SOCK_STREAM: utilizo TCP
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)
# Cola de 5 conexiones como máximo. Cuando me llegue una peticion
# la atenderé y si me llegan más las pondré en cola, hasta que
# acabe con la que estoy.

# Accept connections, read incoming data, and answer back an HTML page
#  (in an infinite loop)

while True:
    print('Waiting for connections')
    (recvSocket, address) = mySocket.accept()
    # recvSocket: Es el socket del otro lado que se me ha conectado
    # address: La ip del cliente y el puerto (es un array)
    print('HTTP request received:')
    print(recvSocket.recv(1024)) # Leo lo que me ha llegado y le paso el tamaño del buffer, los bytes que voy a leer como máximo.
    recvSocket.send(b"HTTP/1.1 200 OK\r\n\r\n" +
                    b"<html><body><h1>Hello World!</h1></body></html>" +
                    b"\r\n") # Es el cuerpo de mi mensaje HTTP. No hay cabeceras. Lo tengo que pasar a bytes.
    recvSocket.close()
