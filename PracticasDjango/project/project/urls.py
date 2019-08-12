"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from calc import views

urlpatterns = [
    path('suma/<int:numero1>/<int:numero2>', views.suma),
    path('resta/<int:numero1>/<int:numero2>', views.resta),
    path('multi/<int:numero1>/<int:numero2>', views.multi),
    path('div/<int:numero1>/<int:numero2>', views.div),
    path('admin/', admin.site.urls),
]
# Los angulitos indican que los números son parámetros. Además se tiene que cumplir
# que sean dos ints, sino no se cumple esta regla no se cumpliría. Si no ponemos el int serían strings.
