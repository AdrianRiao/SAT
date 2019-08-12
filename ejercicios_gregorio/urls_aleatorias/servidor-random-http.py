#!/usr/bin/python3

import socket
import random

port = 1234
first_rand_n = 0
last_rand_n = 10**9

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((socket.gethostname(), port))

mySocket.listen(5)

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        print(recvSocket.recv(2048))
        print('Answering back...')
        rand_int = random.randint(first_rand_n, last_rand_n)
        url_tosend = ('http://' + socket.gethostname() + 
					  ':' + str(port) + '/' + str(rand_int))
        recvSocket.send(b"HTTP/1.1 200 OK\r\n\r\n" +
                        b"<html><body>" +
                        b"<p>Hola. " +
                        b"<a href=" + 
                        bytes(url_tosend, 'utf-8') + 
                        b" >Dame otra</a>" +
                        b"</p>" +
                        b"</body></html>" +
                        b"\r\n")
        recvSocket.close()
except KeyboardInterrupt:
    print()
    print("Closing binded socket")
    mySocket.close()
