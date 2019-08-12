from django.contrib import admin
from .models import Grupo, Componente, Concierto, Entrada

# Register your models here.

admin.site.register(Grupo)
admin.site.register(Componente)
admin.site.register(Concierto)
admin.site.register(Entrada)
