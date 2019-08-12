from django.shortcuts import render
from django.http import HttpResponse
from .models import Concierto, Grupo
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

formulario = '''
 <form action="" method="POST">
  Nombre del Grupo:<br>
  <input type="text" name="grupo"><br><br>
  Estilo:<br>
  <input type="text" name="estilo"><br><br>
  <input type="submit" value="Enviar">
</form> 
'''


def index(request):
	conciertos = Concierto.objects.all() # Devuelve una lista
	response = ""
	for concierto in conciertos:
		response += (str(concierto.lugar) + " " + str(concierto.fecha) + " "
		+ concierto.grupo.nombre)
	return HttpResponse(response)
	
def grupo(request):
	grupos = Grupo.objects.all()
	return HttpResponse(grupos)
	
def ver_grupos(request, entero):
	try:
		grupo = Grupo.objects.get(id=entero) # Devuelve un objeto
		response = grupo.nombre + " " + grupo.estilo
	except Grupo.DoesNotExist:
		response = "No existe el grupo que se pide"
	return HttpResponse(response)

@csrf_exempt ##Esto permite que el usuario te modifique tu base de datos. Por defecto está protegida.
def new_grupo(request):
	if request.method == "GET":
		response = formulario
	elif request.method == "POST":
		grupo = Grupo(nombre=request.POST['grupo'], estilo=request.POST['estilo'])
		grupo.save()
		response = "Guardado en la base de datos"
	return HttpResponse(response)
