from django.contrib import admin
from django.urls import path, include
from servicos.views import *
app_name='servicos'
urlpatterns = [
    path('', Servicos, name='inicio'),
    path('detalhes/<int:pk>', servicosDetalhes, name='detalhes'),
    path('deltar/<int:pk>', servicosExcluir, name='excluir'),
    path('registrar-pagamento/<int:pk>', registrarPagamento, name='detalhes-registrar-pagamento'),
    path('sigma-sigma', SigmaSigma, name='sigma-sigma'),
    path('requerimento-fisico-sinarm', requerimentoFisicoSinarm, name='requerimento-fisico-sinarm'),

    path('termo-doacao-sinarm', termoDoacaoSinarm, name='termo-doacao-sinarm'),
    path('ver-termo-doacao/<int:pk>', verTermoDoacao, name='visualizar-termo-doacao'),
    path('renderizar-termo-doacao/<int:pk>', viewRenderizerTermoDoacao, name='renderizar-termo-doacao'),

    path('requerimento-apostilamento-sigma-criar', apostilamentoSIGMACriar, name='requerimento-apostilamento-sigma-criar'),
    path('visualizar-requerimento-fisico-sigma/<int:pk>', visualizarRequerimentoFisicoSIGMA, name='visualizar-requerimento-fisico-sigma'),
    path('renderizar-requerimento-fisico-sigma/<int:pk>', renderizerRequerimentoFisicoApostilamentoSIGMA, name='renderizar-requerimento-fisico-sigma'),
    path('visualizar-requerimento-fisico-sinarm/<int:pk>', visualizarRequerimentoFisicoPF, name='visualizar-requerimento-fisico-sinarm'),
    path('renderizar-requerimento-fisico-sinarm/<int:pk>', viewRendererizarRequerimentoFisicoSinarm, name='renderizar-requerimento-fisico-sinarm'),
    path('sinarm-sigma', SinarmSigmaRequerimento, name='sinarm-sigma'),
   # path('sigma-sigma/ver/<int:pk>', SigmaSigmaDetalhes, name='sigma-sigma-detalhes'),
    path('emissao-guia/<int:pk>', emissaoGT, name='emissao-gt'),
    path('emissao-guia/ver/<int:pk>', emissaoGT, name='emissao-gt-ver'),
    path('requerimento-aquisicaoPCE/<int:pk>', requerimentoArmasAcessorios, name='requerimento-pce'),
    path('requerimento-aquisicaoPCE/ver/<int:pk>', requerimentoArmasAcessoriosVisualizar, name='requerimento-pce-ver'),
    path('requerimento-registro-cr/<int:pk>', requerimentoRegistroCR, name='requerimento-registro-cr'),
    path('requerimento-apostilamento-cr/<int:pk>', apostilamentoCR, name='requerimento-apostilamento'),
    path('registrar-servico-sisgcorp/<int:pk>', registrarServicoSisgCOrp, name='requerimento-sisgcorp'),
    path('movimentacoes/', movimentacoesView, name='movimentacoes'),
    path('renovacao-craf-SIGMA/', requerimentoRenovacaoCRAFSIGMAview, name='renovacao-craf-sigma'),
    path('ver-renovacao-craf-SIGMA/<int:pk>', verReqRenovacaoCRAFSIGMA, name='ver-renovacao-craf-sigma'),
    path('renderizar-renovacao-craf-SIGMA/<int:pk>', viewRenderizerRequerimentoRenovacaoCRAFSIGMA, name='renderizar-renovacao-craf-sigma'),
    ]