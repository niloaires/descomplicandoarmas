from django.contrib import admin
from django.urls import path, include
from declaracoes.views import *
app_name='declaracoes'
urlpatterns = [
        path('guarda_acervo_criar/<int:pk>', criarGuardaAcervo, name='guarda_acervo_criar'),
        path('gerar-declaracoes-unificada/<int:pk>', gerarDeclaracoesUnificadas, name='gerar-declaracoes-unificada'),
        path('gerar-declaracao-diversa/<int:pk>', gerarDeclaracaoDiversa, name='gerar-declaracao-diversa'),
        path('gerar-declaracao-residencia/<int:pk>', gerarDeclaracaoEnderecoDiversa, name='gerar-declaracao-endereco-diversa'),

        ]