import decimal
import json
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Case, When, Value
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

from documentos.models import arquivosModel
from financeiro.models import *
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from processos.forms import *
# Create your views here.
@login_required()
def pendencias(request):
    if request.method == 'POST':
        pass

    else:
        qs=pendenciasModels.objects.all().order_by('dataRegistro')
        finalizadas=qs.filter(statusPendencia=True)
        naoFinalizadas=qs.filter(statusPendencia=False)
        contexto={
            'object_list':qs,
            'finalizadas':finalizadas,
            'emAndamento':naoFinalizadas,
            'form':pendenciasForm
        }
        return render(request, 'gestao_v2/processos/listagemPendencias.html', contexto)
@login_required()
def concluirPendendia(request, pk):
    object=get_object_or_404(pendenciasModels, pk=pk)
    object.statusPendencia=True
    object.dataConclusao=datetime.datetime.now()
    object.save()
    messages.add_message(request, messages.SUCCESS, 'A pendência {} foi finalizada!'.format(object.descricao))
    return redirect(request.META['HTTP_REFERER'])
@login_required()
def deletarPendendia(request, pk):
    object=get_object_or_404(pendenciasModels, pk=pk)
    object.delete()
    messages.add_message(request, messages.SUCCESS, 'A pendência {} foi deletada!'.format(object.descricao))
    return redirect(request.META['HTTP_REFERER'])
class criarProcessoView(SuccessMessageMixin, CreateView):
    model = novosProcessosModel
    template_name = 'gestao3/processos/criarProcesso.html'
    form_class = novoFormProcessosModel
    success_message = 'Um novo processo foi criado com êxito!'
    def get_success_url(self):
        return reverse('gestao:processos:detalhar', kwargs={'pk' : self.object.pk})
@login_required()
def deletarProcesso(request, pk):
    objeto=novosProcessosModel.objects.get(pk=pk)
    cliente=objeto.cliente
    objeto.delete()
    return redirect('gestao:clientes:detalhar', cliente.pk)
class detalharProcessoView(DetailView):
    model = novosProcessosModel
    template_name = 'gestao3/processos/processoDetalhes.html'

    def get_context_data(self, **kwargs):
        processo=self.object
        requisitos=processosRequisitos.objects.filter(processo=processo.pk)
        context = super().get_context_data(**kwargs)
        #context['listaAnotacoes'] = anotacoesProcessosModel.objects.filter(processo=processo)
        context['requisitos'] = requisitos.order_by('-atendido', 'requisito__titulo')
        context['pendencias'] = requisitos.filter(atendido=False)
        context['formDataPrevista'] = formDataPrevistaDeferimento
        context['formAnotacao'] = formRegistrarAnotacaoProcesso
        return context
@login_required()
def informarDataPrevistaDeferimento(request, pk):
    if request.method=='POST':
        data = datetime.datetime.strptime(request.POST.get('dataPrevistaDeferimento'), "%d/%m/%Y").strftime("%Y-%m-%d")
        objeto=novosProcessosModel.objects.get(pk=pk)
        objeto.dataPrevistaDeferimento=data
        objeto.save()
        return redirect(request.META['HTTP_REFERER'])
@login_required()
def RegistrarAnotacaoProcesso(request, pk):
    if request.method=='POST':
        usuario=User.objects.get(id=request.user.id)
        formulario=formRegistrarAnotacaoProcesso(request.POST)
        if formulario.is_valid():
            objeto=novosProcessosModel.objects.get(pk=pk)
            anotacoesProcessosModel.objects.create(
                usuario=usuario,
                processo=objeto,
                anotacao=request.POST.get('anotacao')
            )

        return redirect(request.META['HTTP_REFERER'])
@login_required()
def criarProcessoPorCliente(request, pk):
    if request.method=='POST':
        cliente=clienteModel.objects.get(pk=pk)
        formulario=formProcessosModelCliente(request.POST)
        if formulario.is_valid():
            formulario.save(commit=False)
            novosProcessosModel.objects.create(
                modelo=formulario.cleaned_data['modelo'],
                dataPrevistaDeferimento=formulario.cleaned_data['dataPrevistaDeferimento'],
                cliente=cliente
            )
            processo=novosProcessosModel.objects.latest('pk')
            messages.add_message(request, messages.SUCCESS, 'Um novo processo foi criado')

            if request.POST.get('registroFinanceiro') is not None:
                registrosFinanceiroModel.objects.create(
                    cliente=cliente,
                    descricao=processo.modelo.titulo,
                    content_object=processo,
                    formaPagamento=formulario.cleaned_data['formaPagamento'],
                    valor=formulario.cleaned_data['valorPago'],
                    dataPrevista=datetime.datetime.strptime(formulario.cleaned_data['dataPrevista'], "%d/%m/%Y").strftime("%Y-%m-%d"),
                )
                registroFinanceiro=registrosFinanceiroModel.objects.latest('pk')
                if request.POST.get('dataEfetivacao') is not None:
                    registroFinanceiro.dataEfetivacao=datetime.datetime.strptime(formulario.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
                    registroFinanceiro.save()

            else:
                pass
            messages.add_message(request, messages.SUCCESS, 'Um novo registro financeiro foi criado')
            return redirect('gestao:clientes:detalhar', pk=cliente.id)
        else:
            messages.add_message(request, messages.ERROR, 'Há um erro no preenchimento do formulário')
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.add_message(request, messages.ERROR, 'Não é possível atender a requisição')
        return redirect(request.META['HTTP_REFERER'])
def atualizarPendencias(request, pk):
    requisicao=dict(request.POST.lists())
    del requisicao['csrfmiddlewaretoken']

    for item in requisicao:
        chave=int(item)
        listaRequisicao=requisicao.get(item)
        valor=listaRequisicao[-1]
        requisito=processosRequisitos.objects.get(pk=chave)

        if valor == 'atendido' and requisito.atendido == False:
            requisito.atendido = True
            historicoProcessos.objects.create(
                processo=novosProcessosModel.objects.get(pk=pk),
                historico=str("O requisito {} foi atendido".format(requisito.requisito.titulo))

            )
        elif valor == 'nao' and requisito.atendido == True:
            requisito.atendido = False
            historicoProcessos.objects.create(
                processo=novosProcessosModel.objects.get(pk=pk),
                historico=str("O requisito {} deixou de ser considerado atendido".format(requisito.requisito.titulo))

            )
        else:
            pass
        requisito.save()
    return redirect(request.META['HTTP_REFERER'])
class processosView(ListView):
    model = novosProcessosModel
    template_name = 'gestao3/processos/processos.html'
    context_object_name = 'object_list'
    queryset = novosProcessosModel.objects.all().order_by('ultimaMovimentacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = self.queryset
        context['finalizados'] = self.queryset.filter(concluido=True)
        context['emAndamento'] = self.queryset.filter(concluido=False)
        return context
class processosClienteView(ListView):
    model = ProcessosModel
    template_name = 'gestao_v2/processos/listagem.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        self.processo = get_object_or_404(clienteModel, pk=self.kwargs['pk'])
        return ProcessosModel.objects.filter(cliente_id=self.kwargs['pk'])
class processoDetalhesView(DetailView):
    model = ProcessosModel
    template_name = 'gestao_v2/processos/detalhes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['formulario_historio'] = adicionarRegistroConsulta
        return context

    def post(self, request, *args, **kwargs):
        formulario = adicionarRegistroConsulta(request.POST, request.FILES)
        if formulario.is_valid():
            #formulario.cleaned_data.get('his')
            consulta=self.get_object()
            historicoProcessosModel.objects.create(
                usuario=request.user,
                consulta=consulta,
                descricao=formulario.cleaned_data['descricao'],
                textoConsulta=formulario.cleaned_data['textoConsulta']
            ).save()
            messages.add_message(request, messages.SUCCESS, 'Movimentação realizada com sucesso!')
            return redirect(request.META['HTTP_REFERER'])
@login_required()
def clienteIniciarProcesso(request, pk):
    usuario=User.objects.get(pk=request.user.pk)
    object=clienteModel.objects.get(pk=pk)
    if request.method == 'POST':
        formulario=iniciarProcessoForm(request.POST)
        if formulario.is_valid():
            efetuarRegistro = False
            if formulario.cleaned_data['registroFinanceiro'] is True:
                efetuarRegistro = True




            ProcessosModel.objects.create(

                cliente=object,
                processo=formulario.data['processo'],
                descricao=formulario.data['descricao'],
            ).save()
            ultimaConsulta=ProcessosModel.objects.latest('pk')
            historicoProcessosModel.objects.create(
                usuario=usuario,
                consulta=ultimaConsulta,
                descricao=formulario.data['descricaoHistorico']
            ).save()
            ultimoHistorico=ProcessosModel.objects.latest('pk')
            messages.add_message(request, messages.SUCCESS,
                                 'O processo {processo} foi registrado e encontra-se {descricao}'.
                                 format(processo=ultimaConsulta.processo, descricao=ultimoHistorico.descricao),
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
            if efetuarRegistro is True:
                valor = decimal.Decimal(formulario.data['valor'])
                valorPago = decimal.Decimal(formulario.data['valorPago'])
                valorResidual = decimal.Decimal((valor - valorPago))
                dataPrevista = datetime.datetime.strptime(formulario.data['dataPrevista'], "%d/%m/%Y").strftime(
                    "%Y-%m-%d")
                if formulario.data['dataEfetivacao'] is not '':
                    dataEfetivacao = datetime.datetime.strptime(formulario.data['dataEfetivacao'], "%d/%m/%Y").strftime(
                        "%Y-%m-%d")
                else:
                    dataEfetivacao = None
                registrosFinanceiroModel.objects.create(
                    cliente=object,
                    descricao=formulario.data['descricao'],
                    content_object=ultimaConsulta,
                    formaPagamento=formulario.data['formaPagamento'],
                    efetivado=True,
                    dataPrevista=dataPrevista,
                    dataEfetivacao=dataEfetivacao,
                    valor=formulario.data['valor']

                ).save()
                messages.add_message(request, messages.SUCCESS,
                                     'Um novo registro financeiro foi realizado',
                                     extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
                if valorResidual > 0:
                    registrosFinanceiroModel.objects.create(
                        cliente=object,
                        descricao=formulario.data['descricao'],
                        content_object=ultimaConsulta,
                        formaPagamento=formulario.data['formaPagamento'],
                        efetivado=False,
                        dataPrevista=dataPrevista,
                        dataEfetivacao=dataEfetivacao,
                        valor=valorResidual

                    ).save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Um novo registro financeiro foi realizado',
                                         extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
                    return redirect(request.META['HTTP_REFERER'])
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Não foi possível registrar o novo processo para o cliente {}'.format(object.nome),
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
            return redirect(request.META['HTTP_REFERER'])

    else:
        messages.add_message(request, messages.SUCCESS,
                             'Não foi possível registrar o novo processo para o cliente {}'.format(object.nome),
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
        return redirect(request.META['HTTP_REFERER'])
@login_required()
def proximosDeferimentos(request):
    hoje = datetime.datetime.now()
    sessentaDiasAntes = hoje - datetime.timedelta(days=60)
    quarentaeCincoDiasDepois = hoje + datetime.timedelta(days=45)
    busca = novosProcessosModel.objects.annotate(tag=Case(When(dataPrevistaDeferimento__lte=hoje, then=Value('danger')),
                                                       When(dataPrevistaDeferimento__gt=hoje, then=Value('success')))). \
        filter(concluido=False, dataPrevistaDeferimento__range=[sessentaDiasAntes, quarentaeCincoDiasDepois]).order_by(
        'dataPrevistaDeferimento')

    contexto={
        'object_list':busca
    }
    return render(request, 'gestao3/processos/processosProximosDeferimentos.html', contexto)