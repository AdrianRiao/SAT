#!/usr/bin/python3

import webapp

class Damemirecurso(webapp.webApp): ## La clase Damemirecurso sobreescribe algunos métodos de webApp
    def parse(self, request):
         return request()[1][1:]
		
    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>Me has pedido " + parsedRequest + "</h1></body></html>")
