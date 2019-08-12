from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Url
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

formulario = '''
 <form action="" method="POST">
  URL to shorten:<br>
  <input type="text" name="url"><br><br>
  <input type="submit" value="Enviar">
</form>
'''

def cmplt_url(url):
    if url[0:7] == "http://":
        return "http://" + url[7:]
    elif url[0:8] == "https://":
        return "https://" + url[8:]
    else:
        return "http://" + url

@csrf_exempt
def index(request):
    if request.method == "GET":
        urls = Url.objects.all()
        urls_list = ""
        for url in urls:
            short_url = ("http://" + request.META['SERVER_NAME'] +
                          ":" + request.META['SERVER_PORT'] + "/" + 
                          str(url.id))
            urls_list += ("<a href=" + url.name + ">" + url.name + 
                          "</a> corresponds with " +
                          "<a href=" + short_url + ">" + short_url +
                          "</a> <br>")
        response = (formulario + urls_list)

    elif request.method == "POST":
        url_post = cmplt_url(request.POST['url'])
        try:
            url = Url.objects.get(name = url_post)
        except Url.DoesNotExist:
            url = Url(name = url_post)
            url.save()
        
        short_url = ("http://" + request.META['SERVER_NAME'] +
                          ":" + request.META['SERVER_PORT'] + "/" + 
                          str(url.id))
        response = ("<a href=" + url.name + ">" + url.name + 
                    "</a> corresponds with " +
                    "<a href=" + short_url + ">" + short_url +
                    "</a>")

    return HttpResponse(response)
    
def redirect(request, entero):
    try:
        url = Url.objects.get(id=entero)
        return HttpResponseRedirect(url.name)
    except Url.DoesNotExist:
        return HttpResponse("No existe la url que se pide")
