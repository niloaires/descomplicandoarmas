from django.contrib import admin
from django.urls import path, include
from financeiro.views import *
app_name='financeiro'
urlpatterns = [
    path('', financeiroInicio, name='inicio'),
    path('registros-diverso/<int:pk>', criarRegistroFinanceiroDiverso, name='registro-diverso'),
    path('despesas', financeiroProximasDespesas, name='despesas'),
    path('receitas', financeiroProximasReceitas, name='receitas'),
    path('confirmar-pagamento/<int:pk>', confirmarPagamento, name='confirmar-pagamento')
    ]