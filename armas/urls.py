from django.contrib import admin
from django.urls import path, include
from armas.views import *
app_name='armas'
urlpatterns = [
    path('', armasInicio, name='inicio'),
    path('editar/<int:pk>', armaEditar, name='editar'),
    path('deletar/<int:pk>', armaDeletar, name='deletar'),
    path('cliente/<int:pk>', clientesArmas, name='cliente')
]