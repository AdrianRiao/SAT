class Alumno():
	def __init__(self, nombre):
		self.nombre = nombre
		self._dni = "002123" ## Al ponerlo así el DNI es variable interna, se podrá acceder desde fuera pero indico que mejor no lo hagas
		
	def quieneres(self):
		return "Soy " + self.nombre
		
	def matricularse(self):
		return "Soy " + self.nombre + " y tengo este DNI: " + self._dni

class Malabarista():
	pass ## Indico que no la defino
	
class SuperAlumno(Alumno, Malabarista): ## Herencia múltiple. En python puedo herar de varias clases. En Java no
	pass

j = Alumno("Joshua")
print(j.quieneres())
print(j.matricularse())
print(j.nombre) ## Esto en python se puede hacer, en java el compilador no te deja
				## Si quieres acceder a un atributo en java debes crearte un método (getters y setters)
