from django.db import models

# Create your models here.

##Nota, las tablas deben ser en singular, ya que luego se añade una 's' automáticamente.

class Grupo(models.Model):
	nombre = models.CharField(max_length=32)
	estilo = models.CharField(max_length=32)
	
	def __str__(self):
		return self.nombre
	
class Componente(models.Model):
	nombre = models.CharField(max_length=32)
	instrumento = models.CharField(max_length=32)
	edad = models.IntegerField()
	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE) ## Es una 'llave foranea'. Hace referencia a otra tabla, en este caso a la tabla Grupo.
	## Cada componente corresponderá a un determinado grupo musical. Es una relación 1 a N(1 grupo le corresponden N componentes).
	## Tendré que definir anteriormente la clase Grupo.
	## NOTA:on_delete=models.CASCADE significa que si borras la llave foranea se elimina el componente, en cascada. Mirar manual de referencia
	
	
	## Sirve para que en el administrador en el navegador se muestre el nombre del componente (al llamar a str).
	def __str__(self):
		return self.nombre
	
class Concierto(models.Model):
	fecha = models.CharField(max_length=32)
	lugar = models.DateTimeField()
	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.lugar)
	
class Entrada(models.Model):
	tipo = models.CharField(max_length=32)
	precio = models.PositiveSmallIntegerField
	concierto = models.ForeignKey(Concierto, on_delete=models.CASCADE)

'''
Faltaría:
Asistente
	nombre
	entrada
'''
