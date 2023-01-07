from django.urls import path, include
from django.contrib.auth.decorators import login_required
from processos.views import *
app_name='processos'
urlpatterns = [

    path('', login_required(processosView.as_view()), name='inicio'),
    path('criar-processo', login_required(criarProcessoView.as_view()), name='criar'),
    path('criar-processo-por-cliente/<int:pk>', criarProcessoPorCliente, name='criar-por-cliente'),
    path('deletar-processo/<int:pk>', deletarProcesso, name='deletar'),
    path('detalhar-processo/<int:pk>', login_required(detalharProcessoView.as_view()), name='detalhar'),
    path('atualizar-pendencias-processo/<int:pk>', atualizarPendencias, name='atualizar-pendencias-processo'),
    path('informar-previsao-deferimento-processo/<int:pk>', informarDataPrevistaDeferimento, name='informar-previsao-deferimento-processo'),
    path('registrar-anotacao-processo/<int:pk>', RegistrarAnotacaoProcesso, name='registrar-anotacao-processo'),

    path('iniciar-processo/<int:pk>', clienteIniciarProcesso, name='iniciar-processo'),
    path('proximos-deferimentos', proximosDeferimentos, name='proximos-deferimentos'),
    #path('<int:pk>', login_required(processoDetalhesView.as_view()), name='detalhes'),
    #path('cliente/<int:pk>', login_required(processosClienteView.as_view()), name='cliente'),
    #path('finalizar-consulta-processos/<int:pk>', concluirAndamento, name='finalizar-consulta'),
    #path('deletar-consulta-processos/<int:pk>', deletarAndamento, name='deletar-consulta'),
    #path('pendencias', pendencias, name='pendencias'),

]