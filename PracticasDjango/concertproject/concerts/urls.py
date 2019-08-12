from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('grupo/', views.grupo),
	path('grupo/<int:entero>/', views.ver_grupos),
	path('grupo/new/', views.new_grupo),
]
