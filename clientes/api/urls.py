from django.urls import path
from clientes.api.viewSets import *

app_name='api-clientes'
urlpatterns=[
    path('/', clientesViewSets.as_view(), name='clientes'),
    path('/busca', BuscaClienteView.as_view(), name='busca'),
    path('/listar', clientes_list, name='clientes-listar'),
    path('/criar', clientes_criar, name='clientes-criar'),
    path('/detalhar/<int:pk>', cliente_detalhar, name='clientes-detalhar')
]