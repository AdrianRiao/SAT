"""MiTiempo URL Configuration

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
from myapp import views

urlpatterns = [
    path("", views.main),
    path('municipios/', views.municipios_view),
    path('info/', views.info_view),
    path('logout/', views.logout_view),
    path('login/', views.login_view),
    path('main.css/', views.css_view),
    path('municipios/<str:ident>', views.municipio_view),
    path('change_view/', views.change_view),
    path('admin/', admin.site.urls),
    path('<str:usuario>/', views.usuario_view),
    path('<str:usuario>/<str:ident>', views.delete_pueblo),
]
