#!/usr/bin/python3

import socket

class webApp():

    def parse(self, request):
        return None

    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__(self, hostname, port):

        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        mySocket.listen(5)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = str(recvSocket.recv(2048))
            print(request)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print('Answering back...')
            recvSocket.send(b"HTTP/1.1 " + bytes(returnCode, "utf-8") + b" \r\n\r\n"
                            + bytes(htmlAnswer, "utf-8") + b"\r\n")
            recvSocket.close()

class Sumador(webApp):
    
    def parse(self, request):
        return request.split()
		
    def process(self, parsedRequest):
        resource = parsedRequest[1]
        resource_list = resource.split('/')
        
        if len(resource_list) != 3:
            returnCode = "400 Bad request"
            htmlAnswer = ("<html><body><h1>Usage: /" + 
                          "number1/number2</h1></body></html>")
        else:
            number1 = int(resource_list[1])
            number2 = int(resource_list[2])
            result = number1 + number2
            returnCode = "200 OK"
            htmlAnswer = ("<html><body><h1>La suma da como resultado: " + 
                          str(result) + "</h1></body></html>")
        
        return (returnCode, htmlAnswer)

if __name__ == "__main__":
    SumadorWebApp = Sumador("localhost", 1234)
