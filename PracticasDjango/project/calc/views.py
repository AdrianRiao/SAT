from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

## Nota: request es un objeto. Tiene métodos como 
## request.method ó request.body ó request.path ó request.COOKIES

def suma(request, numero1, numero2):
    ##Enviaré una respuesta HTTP con todas sus cabeceras
    return HttpResponse("The result is " + str(numero1 + numero2))
    
def resta(request, numero1, numero2):
    return HttpResponse("The result is " + str(numero1 - numero2))
    
def multi(request, numero1, numero2):
    return HttpResponse("The result is " + str(numero1 * numero2))
    
def div(request, numero1, numero2):
    try:
        result = numero1 / numero2
    except ZeroDivisionError:
        return HttpResponse("Can not divide by zero")
    
    return HttpResponse("The result is " + str(numero1 / numero2))
