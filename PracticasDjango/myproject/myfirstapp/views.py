from django.http import HttpResponse

# Este fichero contiene las vistas de mi aplicacion.
# Nota: Las vistas siempre tienen un primer parámetro que es la petición
def index(request):
	return HttpResponse('<h1>Welcome to my App!</h1>')
