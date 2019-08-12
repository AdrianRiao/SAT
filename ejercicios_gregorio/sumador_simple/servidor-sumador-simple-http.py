#!/usr/bin/python3

import socket
import calculadora

PORT = 1234

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((socket.gethostname(), PORT))

mySocket.listen(5)

operator = ""
saved = {}

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        request = str(recvSocket.recv(2048))
        print(request)
        request_list = request.split()
        resource = request_list[1]
        resource_list = resource.split('/')

        if len(resource_list) != 3:
            recvSocket.send(b"HTTP/1.1 400 Bad request\r\n\r\n" +
                            b"Usage: /operator/number!")
            recvSocket.close()
            continue

        operator = resource_list[1]
        try:
            number = int(resource_list[2])
        except ValueError:
            recvSocket.send(b"HTTP/1.1 400 Bad request\r\n\r\n" +
                            b"Incorrect entered values!")
            recvSocket.close()
            continue

        print('Answering back...')

        if address[0] not in saved:
            saved[address[0]] = number
            content = ("You have sent " + str(number) +
                       " and " + operator +
                       ". Please, send another one!")
        else:
            result = calculadora.main(operator, saved[address[0]], number)
            content = ("I had " + str(saved[address[0]]) +
                       " and " + operator + ". You have sent " +
                       str(number) + ". The result is: " + str(result))
            del saved[address[0]]

        recvSocket.send(b"HTTP/1.1 200 OK\r\n\r\n" +
                        b"<html><body>" +
                        b"<p>" +
                        bytes(content, 'utf-8') +
                        b"</p>" +
                        b"</body></html>" +
                        b"\r\n")
        recvSocket.close()
except KeyboardInterrupt:
    print()
    print("Closing binded socket")
    mySocket.close()
