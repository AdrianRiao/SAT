from django.shortcuts import render
from .models import Page
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import xml_parser_barrapunto

# Create your views here.

html_template = """<!DOCTYPE html>
<html lang="en" >
  <head>
    <meta charset="utf-8" />
    <title>Shopping list</title>
  </head>
  <body>
    {content}
  </body>
</html>
"""

form_template = '''
 <form action="/{resource}/" method="POST">
  Content:<br>
  <input type="text" name="content" value="{content_value}"><br><br>
  <input type="submit" value="Enviar">
</form>
'''

barrapunto = xml_parser_barrapunto.main()

@csrf_exempt
def index(request, name):
	if request.method == "POST":
		page = Page(name=name, content=request.POST['content'])
		page.save()
	
	if request.method == "GET" or request.method == "POST":
		try:
			page = Page.objects.get(name = name)
			content_value = page.content
		except Page.DoesNotExist:
			content_value = ""
		response = "No existe el grupo que se pide"
		form = form_template.format(resource = name,
									content_value = content_value)
		content = form + "<br/>" + barrapunto
		return HttpResponse(html_template.format(content=content))
	
