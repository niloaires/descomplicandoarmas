from django.contrib import admin
from django.urls import path, include
from gestao.views import *
from processos.views import *

app_name='gestao'
urlpatterns = [
    path('', dashBoardView, name='inicio'),
    path('busca/', buscaGeral, name='busca'),
    path('registrar-pendencia/<int:pk>', registrarPendencia, name='registrar-pendencia'),
    path('pendencias', pendencias, name='pendencias'),
    path('concluir-pendencia/<int:pk>', concluirPendendia, name='concluir-pendencia'),
    path('deletar-pendencia/<int:pk>', deletarPendendia, name='deletar-pendencia'),
    path('servicos/', include('servicos.urls')),
    path('armas/', include('armas.urls')),
    path('clientes/', include('clientes.urls')),
    path('enderecos/', include('enderecos.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('declaracoes/', include('declaracoes.urls')),
    path('documentos/', include('documentos.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('processos/', include('processos.urls')),


    ]