from django.db import models

# Create your models here.

# Aquí estará mi modelo de la aplicación. En nuestro caso tenemos un
# bar, por lo tanto tendremos bebidas y precios.

# Nuestro modelo será la estructura de base de datos.

# En la documentacion existen un monton de campos de models.
class Producto(models.Model):
    bebida = models.CharField(max_length=32)
    precio = models.FloatField()

# Deberemos migrar nuestro modelo a nuestra base de datos

"""
makemigrations (me preparo para migrar)
---------
migrate (migro los datos a las base de datos)
--------
createsuperuser
"""

## Para migrar debemos ejecutar 'python3 manage.py makemigrations'
## El segundo paso es ejecutar 'python3 manage.py migrate'

## Podemos crearnos un usuario y contraseña con 'python3 manage.py createsuperuser'
## Con esto cada vez que entremos en la url 'admin/' podremos entrar en el administrador de Django
## desde el navegador.
