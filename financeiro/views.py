from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from clientes.models import clienteModel
from documentos.models import arquivosModel
from financeiro.models import registrosFinanceiroModel
from financeiro.forms import registrosFinanceirosForm, registrarPagamentoForm, registroFinanceiroClienteForm
import datetime
import calendar
from django.db.models import Sum
# Create your views here.
@login_required()
def criarRegistroFinanceiroDiverso(request, pk):
    cliente=clienteModel.objects.get(pk=pk)
    if request.method=='POST':
        formulario=registroFinanceiroClienteForm(request.POST)

        if formulario.is_valid():
            if formulario.data['dataEfetivacao'] is not '':
                dataEfetivacao = datetime.datetime.strptime(formulario.data['dataEfetivacao'], "%d/%m/%Y").strftime(
                    "%Y-%m-%d")
            else:
                dataEfetivacao = None
            dataPrevista = datetime.datetime.strptime(formulario.data['dataPrevista'], "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            registrosFinanceiroModel.objects.create(
               cliente=cliente,
                descricao=formulario.data['descricao'],
                content_object=cliente,
                formaPagamento=formulario.data['formaPagamento'],
                codigoBarra=formulario.data['codigoBarra'],
                valor=formulario.data['valor'],
                dataPrevista= dataPrevista,
                dataEfetivacao=dataEfetivacao
            ).save()
            messages.add_message(request, messages.SUCCESS,
                                 'Movimentações financeira registrada com sucesso!',
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})

            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Erro ao processar a solicitação',
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})

            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.add_message(request, messages.SUCCESS,
                             'Erro ao processar a solicitação',
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})

        return redirect(request.META['HTTP_REFERER'])
@login_required()
def financeiroInicio(request):
    registros_financeiros = registrosFinanceiroModel.objects.filter(ativo=True).order_by('-dataPrevista')
    hoje = datetime.datetime.today()
    calendario = calendar.monthrange(hoje.year, hoje.month)

    registros_mes_atual=registros_financeiros.filter(dataRegistro__gte=datetime.date(hoje.year, hoje.month, 1),
                                         dataRegistro__lte=datetime.date(hoje.year, hoje.month, calendario[1])).aggregate(total=Sum('valor'))
    if request.method == 'POST':
        formulario=registrosFinanceirosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, "A movimentação foi registrada com êxito")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            page = request.GET.get('page', 1)
            paginator = Paginator(registros_financeiros, 50)

            try:
                object_list =paginator.page(page)
            except PageNotAnInteger:
                object_list=paginator.page(1)
            except EmptyPage:
                object_list = paginator.page(paginator.num_pages)

            contexto={
                'movimentacao_mensal':registros_mes_atual,
                'object_list': object_list,
                'form': formulario,
                'form_pagamento':registrarPagamentoForm
            }
            return render(request, 'gestao_v2/listaFinanceiro.html', contexto)
    else:

        page = request.GET.get('page', 1)
        paginator = Paginator(registros_financeiros, 50)

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        contexto = {
            'movimentacao_mensal': registros_mes_atual,
            'object_list': object_list,
            'form': registrosFinanceirosForm,
            'form_pagamento': registrarPagamentoForm
        }
        return render(request, 'gestao_v2/listaFinanceiro.html', contexto)
@login_required()
def financeiroProximasDespesas(request):
    registros=registrosFinanceiroModel.objects.filter(ativo=True)
    contexto={
        'object_list':registros.filter(efetivado=False, valor__lt=0).order_by('dataPrevista'),
        'form_pagamento':registrarPagamentoForm
    }
    return render(request, 'gestao/financeiro/despesasLista.html', contexto)
@login_required()
def financeiroProximasReceitas(request):
    registros=registrosFinanceiroModel.objects.filter(ativo=True)
    contexto={
        'object_list':registros.filter(efetivado=False, valor__gt=0).order_by('dataPrevista'),
        'form_pagamento':registrarPagamentoForm
    }
    return render(request, 'gestao/financeiro/receitasLista.html', contexto)
@login_required()
def confirmarPagamento(request, pk):
    if request.method=='POST':
        registro = get_object_or_404(registrosFinanceiroModel, pk=pk)
        formulario = registrarPagamentoForm(request.POST, request.FILES, instance=registro)
        #arquivoComprovante=request.FILES['comprovante']
        if formulario.is_valid():
            formulario.save(commit=False)
            #formulario.efetivado=True
            formulario.save()
            registro.efetivado=True
            registro.save()
            if request.POST.get('comprovante') is not '':
                arquivosModel.objects.create(
                    content_object=registro.cliente,
                    nome=str('Comprovante de pagamento - {}'.format(registro.__str__())),
                    arquivo=request.FILES['comprovante'],
                    tipoArquivo='comprovante',
                    cliente_id=registro.cliente.pk
                ).save()
            messages.add_message(request, messages.SUCCESS, "O PAGAMENTO {} FOI CONFIRMADO COM ÊXITO".format(registro.descricao.upper()))
            return redirect('gestao:financeiro:inicio')
        else:
            messages.add_message(request, messages.ERROR, "Erro")
            return redirect(request.META.get('HTTP_REFERER'))