from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto

# Create your views here.

def barra(request):
    productos = Producto.objects.all() # Esto es una lista
    respuesta = ""
    for producto in productos:
        respuesta += producto.bebida + "a" + str(producto.precio) + "euros<br/>"
    return HttpResponse("Esto es la barra, y esto es lo que hay:<br/>" + str(respuesta))
