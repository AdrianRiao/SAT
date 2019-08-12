#!/usr/bin/python3

import webapp

class Sumador(webapp.webApp):
    def parse(self, request):
        request_list = request()[1]
        _, op1, op2 = request_list.split('/')
        return (op1, op2)
		
    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>La suma es " + str(int(parsedRequest[0]) + int(parsedRequest[1])) + "</h1></body></html>")

if __name__ == "__main__":
    testWebApp = Sumador("localhost", 1234) ## Nota: el constructor, si no lo encuentra en Sumador, mira en las clases madres.
