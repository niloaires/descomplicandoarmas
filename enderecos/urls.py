from django.contrib import admin
from django.urls import path, include
from enderecos.views import *
app_name='enderecos'
urlpatterns = [
    path('adicionar/<int:pk>', enderecoAdicionar, name='adicionar'),
    path('definir-princial/<int:pk>', definirEnderecoPrincipal, name='definir-princial')
    ]