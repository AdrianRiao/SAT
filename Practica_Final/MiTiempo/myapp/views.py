from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound, Http404
from . import json_municipios_parser, xml_parser
from .forms import LoginForm, TempForm, ComentForm
from .forms import CssForm, TituloForm, AñadirPuebloForm
from .models import Usuario, Pueblo, Comentario, Pueblo_Usuario

# Create your views here.

muni = json_municipios_parser.main("municipios.json")
num_coment = 10 # Indica el máximo número
                # de comentarios a mostrar
vista_defecto = 0


def is_registered_user(usuario):
    found = False
    users = User.objects.all()
    for user in users:
        if str(user) == usuario:
            found = True
            break
    return found
    
def user_in_db(user):
    found = False
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        if str(user) == usuario.nombre:
            found = True
            break
    return found
    
def list_pueblos_user(usuario):
    lista = []
    pueblos_user = Pueblo_Usuario.objects.filter\
                   (usuario__nombre=usuario).order_by('-id')
    if not pueblos_user:
        return lista
    for pueblo_user in pueblos_user:
        lista.append(pueblo_user.pueblo)
    return lista
    
def list_pueblos_coment(vista):
    if vista == 0:
        return list(Pueblo.objects.order_by('-num_coment')[:num_coment])
    elif vista == 1:
        return list(Pueblo.objects.filter(prob_precipitacion__gt=0)\
                    .order_by('-num_coment')[:num_coment])
    else:
        return list(Pueblo.objects.filter(prob_precipitacion=0)\
                    .order_by('-num_coment')[:num_coment])

def list_pueblos_selec(minimo, maximo):
    if minimo != "" and maximo != "":
        return list(Pueblo.objects.filter(seleccionado=True,
                    max_temp__gte=minimo, max_temp__lte=maximo))
    else:
        return list(Pueblo.objects.filter(seleccionado=True))

def actualizar_pueblo(pueblo):
    url = ("http://www.aemet.es/xml/municipios/localidad_" +
           pueblo.ident[2:] + ".xml")
    data = xml_parser.main(url)
    pueblo.prob_precipitacion = data['prob_precipitacion']
    pueblo.descripcion = data['descripcion']
    pueblo.direc_viento = data['direc_viento']
    pueblo.vel_viento = data['vel_viento']
    pueblo.max_temp = data['max_temp']
    pueblo.min_temp = data['min_temp']
    pueblo.max_sens_termica = data['max_sens_termica']
    pueblo.min_sens_termica = data['min_sens_termica']
    pueblo.max_hum_relativa = data['max_hum_relativa']
    pueblo.min_hum_relativa = data['min_hum_relativa']
    pueblo.save()
    
def save_pueblo(name_pueblo, ident):
    pueblo = Pueblo(nombre=name_pueblo, ident=ident,
                    altitud=muni[name_pueblo]['alt'],
                    latitud=muni[name_pueblo]['lat'],
                    longitud=muni[name_pueblo]['long'],
                    num_coment=0,
                    seleccionado=False)

    actualizar_pueblo(pueblo)

def actualizar_usuarios():
    users = list(User.objects.all())
    for user in users:
        if not user_in_db(user):
            usuario = Usuario(nombre=str(user), titulo="")
            usuario.save()

def save_coment(texto, username, ident):
    usuario = Usuario.objects.get(nombre=username)
    pueblo = Pueblo.objects.get(ident=ident)
    comentario = Comentario(texto=texto, pueblo=pueblo, usuario=usuario)
    comentario.save()

def act_coment_pueblo(ident):
    pueblo = Pueblo.objects.get(ident=ident)
    pueblo.num_coment = pueblo.num_coment + 1
    pueblo.save()
    
def tratar_cssform(request, usuario):
    form = CssForm(request.POST)
    if form.is_valid():
        tamaño = form.cleaned_data['tamaño']
        color_letra = form.cleaned_data['color_letra']
        color_fondo = form.cleaned_data['color_fondo']
        usuario = Usuario.objects.get(nombre=usuario)
        usuario.tamaño = tamaño
        usuario.color_letra = color_letra
        usuario.color_fondo = color_fondo
        usuario.save()

def tratar_tituloform(request, usuario):
    form = TituloForm(request.POST)
    if form.is_valid():
        titulo = form.cleaned_data['titulo']
        usuario = Usuario.objects.get(nombre=usuario)
        usuario.titulo = titulo
        usuario.save()

def tratar_añadirform(request, usuario):
    form = AñadirPuebloForm(request.POST)
    if form.is_valid():
        name_pueblo = form.cleaned_data['pueblo']
        ident = muni[name_pueblo]['id']
        try:
            pueblo = Pueblo.objects.get(ident=ident)
        except Pueblo.DoesNotExist:
            save_pueblo(name_pueblo, ident)
            pueblo = Pueblo.objects.get(ident=ident)
        
        usuario = Usuario.objects.get(nombre=usuario)
        try:
            pueblo_usuario = Pueblo_Usuario.objects.get(pueblo=pueblo, usuario=usuario)
        except Pueblo_Usuario.DoesNotExist:
            pueblo_usuario = Pueblo_Usuario(pueblo=pueblo, usuario=usuario)
            pueblo_usuario.save()
            pueblo.seleccionado = True
            pueblo.save()
        
    

#----------------------VIEWS----------------------#

def main(request):
    try:
        vista = request.session['vista']
    except KeyError:
        vista = vista_defecto
        request.session['vista'] = vista_defecto
        
    pueblos = list_pueblos_coment(vista)
    if request.GET.get('format') == "xml":
        xml = render(request, 'document.xml', {'pueblos': pueblos})
        return HttpResponse(xml, content_type="text/xml")
        
    actualizar_usuarios()
    usuarios = list(Usuario.objects.all())
    return(render(request, 'main.html', {'login_form': LoginForm(),
                                         'pueblos': pueblos,
                                         'usuarios': usuarios,
                                         'vista': vista}))

def municipios_view(request):
    minimo = ""
    maximo = ""
    if request.method == 'POST':
        form = TempForm(request.POST)
        if form.is_valid():
            minimo = form.cleaned_data['minimo']
            maximo = form.cleaned_data['maximo']
        else:
            return HttpResponseRedirect("/municipios/")

    pueblos = list_pueblos_selec(minimo, maximo)
    if request.GET.get('format') == "xml":
        xml = render(request, 'document.xml', {'pueblos': pueblos})
        return HttpResponse(xml, content_type="text/xml")

    return(render(request, 'municipios.html', {'login_form': LoginForm(),
                                               'temp_form': TempForm(),
                                               'pueblos': pueblos}))

def municipio_view(request, ident):
    try:
        pueblo = Pueblo.objects.get(ident=ident)
        actualizar_pueblo(pueblo)
    except Pueblo.DoesNotExist:
        raise Http404
        
    if request.method == 'POST':
        form = ComentForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            save_coment(texto, request.user.username, ident)
            act_coment_pueblo(ident)

    comentarios = list(Comentario.objects.filter(pueblo__ident=ident))
    if request.user.is_authenticated:
        identity = ident
        coment_form = ComentForm()
        template = "muni_priv.html"
    else:
        identity = ""
        coment_form = ""
        template = "muni.html"

    return(render(request, template, {'login_form': LoginForm(),
            'ident': identity, 'coment_form': coment_form,
            'pueblo': pueblo, 'comentarios': comentarios}))
    
def usuario_view(request, usuario):
    actualizar_usuarios()
    if not is_registered_user(usuario):
        raise Http404
        
    if request.method == 'POST':
        if 'Cambiar CSS' in request.POST:
            tratar_cssform(request, usuario)
        elif "Cambiar titulo" in request.POST:
            tratar_tituloform(request, usuario)
        elif "Añadir municipio" in request.POST:
            try:
                tratar_añadirform(request, usuario)
            except KeyError:
                return(render(request, 'base.html', {'form': LoginForm(),
                       'info_text': "No existe el municipio"}))

    pueblos = list_pueblos_user(usuario)
    if request.GET.get('format') == "xml":
        xml = render(request, 'document.xml', {'pueblos': pueblos})
        return HttpResponse(xml, content_type="text/xml")

    if request.user.is_authenticated and request.user.username == usuario:
        css_form = CssForm()
        titulo_form = TituloForm()
        añadir_form = AñadirPuebloForm()
        template = "user_priv.html"
    else:
        css_form = ""
        titulo_form = ""
        añadir_form = ""
        template = "user.html"
    return(render(request, template, {'login_form': LoginForm(),
            'pueblos': pueblos, 'usuario': usuario,
            'css_form': css_form, 'titulo_form': titulo_form,
            'añadir_form': añadir_form}))

def info_view(request):
    return(render(request, 'info.html', {'login_form': LoginForm()}))

def change_view(request):
    if not request.method == 'POST':
        raise Http404
    request.session['vista'] = (request.session['vista']+1) % 3
    return HttpResponseRedirect("/")
    
def delete_pueblo(request, usuario, ident):
    if not request.method == 'POST':
        raise Http404
    pueblo_usuario = Pueblo_Usuario.objects.get(pueblo__ident=ident,
                                                usuario__nombre=usuario)
    pueblo_usuario.delete()
    return HttpResponseRedirect("/" + usuario)

def login_view(request):
    if not request.method == 'POST':
        raise Http404

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['user']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            info = "Usuario o contraseña invalidos"
            return(render(request, 'base.html', {'login_form': LoginForm(),
                                                 'info_text':info}))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
    
def css_view(request):
    tamaño = ""
    color_letra = ""
    color_fondo = ""
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(nombre=request.user.username)
        tamaño = usuario.tamaño
        color_letra = usuario.color_letra
        color_fondo = usuario.color_fondo

    css = render(request, 'main.css', {'tamaño':tamaño,
                 'color_letra':color_letra, 'color_fondo':color_fondo})
    return HttpResponse(css, content_type="text/css")
