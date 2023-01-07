from django.contrib import admin
from django.urls import path, include
from clientes.views import *
from django.contrib.auth.decorators import login_required
app_name='clientes'
urlpatterns = [

    path('autocompletar', autoCompletar, name='autocompletar'),
    path('', login_required(clientesView.as_view()), name='inicio'),
    path('registrar', login_required(registrarClienteView.as_view()), name='registrar'),
    path('pesquisa/', clientesPesquisa, name='pesquisa'),
    path('senhas/', clientesSenha, name='senhas'),

    path('detalhar/<int:pk>', login_required(clienteDetalharView.as_view()), name='detalhar'),


    #path('detalhes/<int:pk>', clienteDeatalhes, name='detalhes'),
    path('atualizar/<int:pk>', clienteAtualizar, name='atualizar'),
    path('finalizar-cliente/<int:pk>', finalizarCliente, name='finalizar'),

]