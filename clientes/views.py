from django.db.models import Sum
from django.forms.models import construct_instance
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, UpdateView

from clientes.forms import clienteForm, clientePesquisarForm
from processos.forms import andamentoProcessoForm, edicaoAndamentoForm, historicoFormset, historicoConsultaForm, \
    novoFormProcessosModel, formProcessosModelCliente
from armas.forms import armasForm
from clientes.models import *
from processos.models import *
from servicos.models import listaServicos, servicosModel
from enderecos.models import enderecoClienteModel
from enderecos.forms import enderecosClientesFormSet, enderecoClienteForm
from servicos.forms import servicosSisgCorpForm, servicoForm
from documentos.models import arquivosModel
from documentos.forms import arquivosForm
from financeiro.models import registrosFinanceiroModel
from financeiro.forms import registrosFinanceirosForm, registroFinanceiroClienteForm
from declaracoes.forms import declaracoesDiversasForm, declaracoesResidenciaDiversaForm
from processos.forms import pendenciasForm, iniciarProcessoForm
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
def autoCompletar(request):
    data=list(clienteModel.objects.all().values('nome').order_by('nome'))
    return JsonResponse(data, safe=False)

class registrarClienteView(SessionWizardView):
    template_name = 'gestao3/clientes/cadastrarCliente.html'
    form_list = [clienteForm, enderecoClienteForm]
    file_storage=FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'fotos_clientes'))
    def done(self, form_list, **kwargs):

        #Registra novo cliente
        formCliente=form_list[0]
        formCliente.save()

        novoCliente=clienteModel.objects.latest('pk')
        messages.add_message(self.request, messages.SUCCESS, '{} foi registrado com sucesso!'.format(novoCliente.nome),
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})

        # Registra primeiro endereço do cliente
        formEndereco=form_list[1]
        enderecoClienteModel.objects.create(
            cliente=novoCliente,
            principal=True,
            logradouro=formEndereco.cleaned_data['logradouro'],
            estadoMunicipio=formEndereco.cleaned_data['estadoMunicipio'],
            cep=formEndereco.cleaned_data['cep'],

        ).save()

        messages.add_message(self.request, messages.SUCCESS, 'O endereço de {} foi registrado com sucesso!'.format(novoCliente.nome),
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})

        #Registrar primeira movimentação financeira



        """
        formFinanceiro = form_list[2]

        valorResidual=(decimal.Decimal(formFinanceiro.cleaned_data['valor'])-decimal.Decimal(formFinanceiro.cleaned_data['valorPago']))
        dataPrevista=formFinanceiro.cleaned_data['dataPrevista'],
        dataEfetivacao=formFinanceiro.cleaned_data['dataEfetivacao'],
        descricao=formFinanceiro.cleaned_data['descricao'],
        formaPagamento=formFinanceiro.cleaned_data['formaPagamento'],
        efetivado=formFinanceiro.cleaned_data['efetivado'],
        valor=decimal.Decimal(formFinanceiro.cleaned_data['valor']),

        registrosFinanceiroModel.objects.create(
            cliente=novoCliente,
            descricao=descricao,
            formaPagamento=formaPagamento,
            valor=decimal.Decimal(formFinanceiro.cleaned_data['valor']),
            efetivado=formFinanceiro.cleaned_data['efetivado'],
            dataPrevista='2022-01-01',
            dataEfetivacao=formFinanceiro.cleaned_data['dataEfetivacao']
        ).save()
        ultimaMovimentacao = registrosFinanceiroModel.objects.latest('pk')

        if valorResidual > 0:
            registroPendenciaFinanceira = registrosFinanceiroModel.objects.create(
                cliente=novoCliente,
                descricao='Valor residual do contrato, no valor de R$:{}'.format(valorResidual),
                formaPagamento=formFinanceiro.cleaned_data['formaPagamento'],
                valor=valorResidual,
                efetivado=False,
                dataPrevista=ultimaMovimentacao.dataEfetivacao + datetime.timedelta(days=30),
            ).save()
            ultimaMovimentacao = registrosFinanceiroModel.objects.latest('pk')
            messages.add_message(self.request, messages.SUCCESS,
                                 'Uma movimentação no valor de R$:{} foi registrada, com vencimento para 30 dias'.format(ultimaMovimentacao.valor),
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})

        #Registrar Consulta de processos
        consultaProcessosModel.objects.create(
            cliente=novoCliente,
            processo=formFinanceiro.cleaned_data['descricao']
        ).save()

        ultimaConsulta=consultaProcessosModel.objects.latest('pk')
        historicoConsultasProcessosModel.objects.create(
            consulta=ultimaConsulta,
            descricao='Processo pendente!',
            textoConsulta='Registro gerado automaticamente quando o cliente foi cadastrado',
            historicoAtivo=True
        ).save()
        """
        return  redirect('gestao:clientes:detalhar', novoCliente.pk)
@login_required()
def clientesView(request):
    processos=ProcessosModel.objects.all()
    processos_finalizados=processos.filter(consultaAtiva=False)
    processos_em_andamento=processos.filter(consultaAtiva=True)
    contexto={
            'total_processos':processos.count(),
            'total_processos_finalizados':processos_finalizados.count(),
            'total_processos_andamento':processos_em_andamento.count(),
            'object_list':clienteModel.objects.all().order_by('-dataRegistro'),
            'form':clienteForm,
            'form_endereco':enderecosClientesFormSet,
            'form_pesquisa':clientePesquisarForm

        }
    #return render(request, 'gestao/clientes/clientes.html', contexto)
    return render(request, 'gestao_v2/clientes/clienteLista.html', contexto)




    #def get_success_url(self):
       # return reverse_lazy('mycollections:collection_detail', kwargs={'pk': self.object.pk})
@login_required()
def clientesPesquisa(request):
    form_pesquisa=clientePesquisarForm(request.GET)
    qs=clienteModel.objects.filter(nome__icontains=request.GET.get('nome'))
    contexto = {
        'resultado_pesquisa': qs,
        'object_list': clienteModel.objects.all().order_by('-dataRegistro')[:5],
        'form_pesquisa': clientePesquisarForm
    }
    if qs.count() == 0:
        messages.add_message(request, messages.SUCCESS,
                             'A pesquisa não encontrou resultados',
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
    return render(request, 'gestao_v2/pesquisaLista.html', contexto)

class clienteDetalharView(DetailView, UpdateView):
    model = clienteModel
    form_class = clienteForm
    template_name = 'gestao3/clientes/clienteDetalhes.html'
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("gestao:clientes:detalhar", kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formularioProcesso']=formProcessosModelCliente
        context['formularioFinanceiro']=registroFinanceiroClienteForm
        context['formularioDecResidencia']=declaracoesResidenciaDiversaForm
        context['formularioEndereco']=enderecoClienteForm
        context['listaNovosPprocessos']=novosProcessosModel.objects.filter(cliente=self.object)
        context['listaDocumentos']=arquivosModel.objects.filter(cliente_id=self.object.id).order_by('dataRegistro')

        return context


"""
@login_required()
def clienteDeatalhes(request, pk):
    object=get_object_or_404(clienteModel, pk=pk)
    #qs_listaServicos=listaServicos.objects.filter(ativo=True).values('nome', 'vinculoSistema', 'link')
    #lista=[]
    documentos=arquivosModel.objects.filter(cliente_id=object.pk)
    #movimentacoes_processuais=historicoProcessosModel.objects.filter(consulta__cliente=object).order_by('-dataVerificacao')

    registros_financeiros=registrosFinanceiroModel.objects.filter(ativo=True, cliente=object).order_by('-dataPrevista', 'valor')

    contexto={
        'object':object,
        'form':clienteForm(instance=object),
        'form_arquivo':arquivosForm,
        'object_list':clienteModel.objects.exclude(pk=pk)[:15],
        'registros_financeiros':registros_financeiros,
        'form_endereco':enderecoClienteForm,
        'form_processosSisgCorp':servicosSisgCorpForm(cliente_id=pk),
        'lista_documentos': documentos,
        'lista_processos':ProcessosModel.objects.filter(cliente=object).order_by('dataVerificacao'),
        'listaNovosPprocessos':novosProcessosModel.objects.filter(cliente=object).order_by('historicoprocessos__dataRegistro'),
        'total_movimentacoes':registros_financeiros.aggregate(total=Sum('valor')),
        'movimentacoes_financeiras':registros_financeiros,
        'formularioProcesso':novoFormProcessosModel,
        #'movimentacoes_processuais':movimentacoes_processuais,
        'formulario_declaracao':declaracoesDiversasForm,
        'formulario_declaracao_residencia_diversa':declaracoesResidenciaDiversaForm,
        'formulario_registro_financeiro':registroFinanceiroClienteForm,
        'formulario_pendencias':pendenciasForm(initial={'cliente':object}),
        'formulario_armas':armasForm,
        'formulario_movimentacao_processo': iniciarProcessoForm
    }
    return render(request, 'gestao3/clientes/clienteDetalhes.html', contexto)
"""
@login_required()
def clienteAtualizar(request, pk):

    qs_listaServicos = listaServicos.objects.filter(ativo=True).values('nome', 'vinculoSistema', 'link')
    lista = []

    for i in qs_listaServicos:
        """"
        nome = i['nome']
        vinculoSistema = i['vinculoSistema']
        link = i['link']
        dicionario = {'nome': nome, "vinculoSistema": vinculoSistema, "link": reverse(link, kwargs={'pk': pk})}
        lista.append(dicionario)
        """


    if request.POST:
        object = get_object_or_404(clienteModel, pk=pk)
        form=clienteForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'O dados de {} foram atualizados'.format(object.nome))

            return redirect('gestao:clientes:detalhes', object.pk)
        else:
            for erro in form.errors.as_json():
                messages.add_message(request, messages.WARNING, erro)
            contexto = {
                'object': object,
                'form': clienteForm(instance=object),
                'object_list': clienteModel.objects.exclude(pk=pk)[:15],

                'form_endereco': enderecoClienteForm,
                'lista_processos': object.servicos.all()
            }
            return render(request, 'gestao/clientes/clienteDetalhes.html', contexto)
@login_required()
def clientesSenha(request):
    q=request.GET.get('nome')
    if q:
        pesquisa=clienteModel.objects.filter(nome__icontains=q)
    else:
        pesquisa=clienteModel.objects.all().order_by('nome')[:20]
    contexto={
        'form_pesquisa': clientePesquisarForm,
        'clientes':pesquisa,
        'object_list':clienteModel.objects.all().order_by('-dataRegistro')[:5]
    }
    return render(request, 'gestao/clientes/clientesSenha.html', contexto)
@login_required()
def finalizarCliente(request, pk):
    object=clienteModel.objects.get(pk=pk)
    consultas=consultaProcessosModel.objects.filter(cliente=object)
    consultas.update(consultaAtiva=False)
    for item in consultas:
        historicoConsultasProcessosModel.objects.create(
            consulta=item,
            descricao='PROCESSO FINALIZADO'

        ).save()
    object.processosEmAndamento=False
    object.save()
    messages.add_message(request, messages.SUCCESS,
                         'O cliente {} não possui processos em andamento, todos os processos foram finalizados!'.format(
                             object.nome),
                         extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})

    return redirect(request.META['HTTP_REFERER'])

class clientesView(ListView):
    model = clienteModel
    template_name = 'gestao3/clientes/clientes.html'