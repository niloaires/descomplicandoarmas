from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from clientes.models import *
from servicos.models import *
from processos.models import *
from processos.forms import pendenciasForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.functions import TruncWeek
import datetime
from financeiro.models import registrosFinanceiroModel
from django.db.models import Sum, F, Q, Count, Case, When
import calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from itertools import chain
def loginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.perfil.funcao=='Psicologo(a)':
                return redirect('parceiros:laudos-psicologicos:inicio')
            elif request.user.perfil.funcao is 'Diretor Adm.' or 'Colaborador':
                return redirect('gestao:inicio')
            else:
                return redirect('frontend:inicio')

            #return redirect('gestao:clientes:inicio')
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Erro au tentar acessar o sistema de gestão. Verifique seus dados. ',
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
            return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'login.html')
def logoutView(request):
    logout(request)
    return redirect('login')

# Create your views here.

def buscaGeral(request):
    termo=request.GET.get('termo')
    clientes=clienteModel.objects.filter(nome__icontains=termo)
    processos=novosProcessosModel.objects.filter(cliente__nome__icontains=termo)
    resultados =chain(clientes)
    contexto={
        'resultadosClientes':clientes,
        'resultadosProcessos':processos,
        'termo':str(termo)
    }
    return render(request, 'gestao3/busca.html',contexto )
@login_required()
def gestaoInicio(request):
    hoje=datetime.date.today()
    calendario=calendar.monthrange(hoje.year, hoje.month)
    clientes=clienteModel.objects.all()
    servicos=servicosModel.objects.all()
    processos=ProcessosModel.objects.all()
    rankingProcessos=processos.values('processo').annotate(contagem=Count('processo')).annotate(percentual=(F('contagem')/processos.count())*100).order_by('-contagem')[:4]
    movimentacoes=historicoProcessosModel.objects.all().order_by('-dataVerificacao')
    registrosFinanceiros=registrosFinanceiroModel.objects.filter(ativo=True)
    inicio_mes=str("{}-{}-{}".format(hoje.year, hoje.month, 1))
    fim_mes=str("{}-{}-{}".format(hoje.year, hoje.month, calendario[1]))
    movimentacaoMensal=registrosFinanceiros.filter(efetivado=True).filter(dataRegistro__range=[inicio_mes, fim_mes])
    despesaMensal=movimentacaoMensal.filter(efetivado=True).filter(valor__lte=0)
    receitaMensal=movimentacaoMensal.filter(efetivado=True).filter(valor__gte=0)
    pendenciaMensal=movimentacaoMensal.filter(efetivado=False)
    contexto={
        'clientes': clientes,
        'servicos':servicos,
        'servicos_pendentes':servicos.filter(servicoAtivo=True),
        'servicos_concluidos':servicos.filter(servicoAtivo=False),
        'ultimos_servicos':servicos.order_by('dataRegistro')[:8],
        'ultimas_movimentacoes':movimentacoes,
        'movimentacaoMensalTotal':movimentacaoMensal.aggregate(total=Sum('valor')),
        'despesaMensalTotal':despesaMensal.aggregate(total=Sum('valor')),
        'receitaMensalTotal':receitaMensal.aggregate(total=Sum('valor')),
        'pendenciaMensalTotal':pendenciaMensal.aggregate(total=Sum('valor')),
        'rankingProcessos':rankingProcessos

    }
    return render(request, 'gestao_v2/inicio.html', contexto)

@login_required()
def dashBoardView(request):
    hoje = datetime.date.today()
    calendario = calendar.monthrange(hoje.year, hoje.month)
    inicioMes = str("{}-{}-{}".format(hoje.year, hoje.month, 1))
    fimMes = str("{}-{}-{}".format(hoje.year, hoje.month, calendario[1]))
    registrosFinanceiros = registrosFinanceiroModel.objects.filter(ativo=True)
    movimentacaoMensal = registrosFinanceiros.filter(efetivado=True).filter(dataRegistro__range=[inicioMes, fimMes])
    entradasMes=movimentacaoMensal.filter(valor__gt=0).aggregate(total=Sum('valor'))
    saidasMes=movimentacaoMensal.filter(valor__lt=0).aggregate(total=Sum('valor'))
    saldoMes=movimentacaoMensal.aggregate(total=Sum('valor'))
    contexto ={
        'entradasNoMes':entradasMes['total'],
        'saidasNoMes':saidasMes['total'],
        'saldoNoMes':saldoMes['total'],
    }
    return render(request, 'gestao3/inicio.html', contexto)
@login_required()
def registrarPendencia(request, pk):
    if request.method=='POST':
        formulario=pendenciasForm(request.POST)
        cliente=clienteModel.objects.get(pk=pk)
        if formulario.is_valid():
            novaPendencia=formulario.save(commit=False)
            novaPendencia.cliente=cliente
            novaPendencia.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Pendência registrada com sucesso!',
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Pendência registrada com êxito!',
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.add_message(request, messages.SUCCESS,
                             'Pendência registrada com êxito!',
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
        return redirect(request.META['HTTP_REFERER'])


