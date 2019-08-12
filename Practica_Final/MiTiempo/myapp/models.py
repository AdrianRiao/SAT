from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=32)
    titulo = models.CharField(max_length=32, blank=True)
    tamaño = models.CharField(max_length=32)
    color_letra = models.CharField(max_length=32)
    color_fondo = models.CharField(max_length=32)
    
    def __str__(self):
        return self.nombre

class Pueblo(models.Model):
    nombre = models.CharField(max_length=32)
    ident = models.CharField(max_length=32)
    altitud = models.CharField(max_length=32)
    latitud = models.CharField(max_length=32)
    longitud = models.CharField(max_length=32)
    prob_precipitacion = models.IntegerField()
    descripcion = models.CharField(max_length=32)
    direc_viento = models.CharField(max_length=32)
    vel_viento = models.IntegerField()
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    max_sens_termica = models.IntegerField()
    min_sens_termica = models.IntegerField()
    max_hum_relativa = models.IntegerField()
    min_hum_relativa = models.IntegerField()
    num_coment = models.IntegerField()
    seleccionado = models.BooleanField()
    
    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    texto = models.CharField(max_length=100)
    pueblo = models.ForeignKey(Pueblo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Pueblo_Usuario(models.Model):
    pueblo = models.ForeignKey(Pueblo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
