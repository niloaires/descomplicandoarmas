from django.urls import path
from documentos.views import *

app_name='documentos'
urlpatterns = [
    path('listar_documentos', listarDocumentos,name='inicio'),
    path('listar_documentos_cliente/<int:pk>', listarDocumentosClientes,name='listar'),
    path('carregar_arquivos_cliente/<int:pk>', carregarDocsClientes,name='carregar_arquivos_cliente'),
    path('deletar/<int:pk>', deletarArquivo,name='deletar')


]