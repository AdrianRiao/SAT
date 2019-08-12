from django.contrib import admin
from .models import Usuario, Pueblo, Comentario, Pueblo_Usuario

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Pueblo)
admin.site.register(Comentario)
admin.site.register(Pueblo_Usuario)
