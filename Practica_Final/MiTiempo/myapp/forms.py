from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

class TempForm(forms.Form):
    minimo = forms.IntegerField(label='min', min_value=-100, max_value=100)
    maximo = forms.IntegerField(label='max', min_value=-100, max_value=100)

class ComentForm(forms.Form):
    texto = forms.CharField(label='Escribe un comentario', max_length=100)
    
class CssForm(forms.Form):
    tamaño = forms.CharField(label='Tamaño de la letra', max_length=10)
    color_letra = forms.CharField(label='Color de la letra', max_length=10)
    color_fondo = forms.CharField(label='Color de fondo', max_length=10)

class TituloForm(forms.Form):
    titulo = forms.CharField(label='Título página personal', max_length=20)

class AñadirPuebloForm(forms.Form):
    pueblo = forms.CharField(label='Añadir municipio', max_length=50)
    
