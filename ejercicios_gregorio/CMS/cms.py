#!/usr/bin/python3

'''
Pido contenido y me lo sirve
(Content Managment System)
'''

import webapp
import socket

contentDict = { '/Fuenlabrada': "Es una ciudad muy bonita",
'/Mostoles': "Yo no soy galactico, soy de Mostoles"}

formulario = '''
 <form action="" method="POST">
  Eslogan:<br>
  <input type="text" name="eslogan"><br><br>
  <input type="submit" value="Enviar">
</form> 
'''

class CMS(webapp.webApp):
    
    def parse(self, request):
        method, resource, _ = request.split(' ', 2) ##Troceo dos veces, los dos primeros espacios, y me salen 3 trozos. El primero es el método, el segundo el recurso, el resto lo tiro.
        try:
            body = request.split('\r\n\r\n', 1)[1]
        except IndexError:
            body = ""
        return method, resource, body
		
    def process(self, parsedRequest):
		
        method, resource, body = parsedRequest
		
        if method == "POST":
            contentDict[resource] = body.split('=')[1]
        if method == "PUT":
            contentDict[resource] = body
        
        try:
            contenido = contentDict[resource]
        except KeyError:
            return ("404 Not Found", "<html><body><h1> not found<br>" + formulario + "</h1></body></html>")

        return ("200 OK", "<html><body><h1>" + contenido + "<br>" + formulario + "</h1></body></html>")

if __name__ == "__main__":
    CMSWebApp = CMS("localhost", 1234)


## Nota: Los navegadores no entienden los métodos PUT u otros. Debemos
## instalar un pluging para firefox (HTTP request maker) para poder trabajar
## con otros metodos: (HEAD, OPTIONS)

## NOTA: el método HEAD te vale para comprobar si tu enlace está bien.
## solo se queda con las cabeceras para ver si es 200 OK, y no con el contenido

## el método OPTIONS sirve para ver las opciones del servidor

## Podemos utilizar POST para no tener que instalar el pluging. Debemos
## enviar un formulario al cliente.
