from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib import messages
from servicos.models import *
from servicos.forms import *
from documentos.forms import arquivosForm
from django.db import transaction
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# Create your views here.
from documentos.renderizadores import renderizarReqApostimaneto, renderizarSgimaSigma, renderizarReqFisicoPCE, \
    renderizarSinarmSigma, renderizarReqSINARMFisicio, renderizarRequerimentoRenovacaoCRAFSIGMA, renderizadorTermoDoacao
from relatorios.views import SigmaSigma as RelatorioSigmaSigma
@login_required()
def Servicos(request):
    if request.method == 'POST':
        formulario=servicoForm(request.POST)
        if formulario.is_valid():
            servico=formulario
            servico.save()
            return redirect(request.META['HTTP_REFERER'])

    else:
        contexto={
            'form_servico':servicoForm(),
            'object_list':servicosModel.objects.all().order_by('-dataRegistro')


        }
        return render(request, 'gestao/servicos/servicosInicio.html', contexto)
@login_required()
def servicosDetalhes(request, pk):
    object=get_object_or_404(servicosModel, pk=pk)
    pendencias=cumprimentoExigenciasModel.objects.filter(servico=object, cumprida=False)
    valorPactuado=object.valor+object.adicional
    totalPago=0
    for i in object.pagamentos.filter(confirmado=True):
        totalPago+=i.valorPago
    if totalPago < valorPactuado:
        messages.add_message(request, messages.WARNING, "Este serviço não está completamente pago")
        exibirCobranca=True
    else:
        exibirCobranca=False
    contexto={
        'object':object,
        'exibirCobranca':exibirCobranca,
        'listaPagamentos':object.pagamentos.filter(confirmado=True),
        'listaExigencias':pendencias,
        'formCobranca':cobrancaForm,
        'valorPactuado':int(valorPactuado),
        'valorPago':int(totalPago),
        'listaMovimentacoes':movimentacoesServico.objects.filter(servico=object, movimentacaoAtiva=True).order_by('-dataMovimentacao'),
        'form_pendencias':FormDocsExigidos(servico_id=object.id),
        'form_movimentacoes':formMovimentacoes
    }

    return render(request, 'gestao/servicos/servicosDetalhes.html', contexto)
@login_required()
def servicosExcluir(request, pk):
    object=get_object_or_404(servicosModel, pk=pk)
    object.servicoAtivo=False
    object.save()
    messages.add_message(request, messages.SUCCESS, "O serviço {} foi removido com êxito".format(object.descricaServico))
    return redirect('gestao:servicos:inicio')
@login_required()
def registrarPagamento(request, pk):
    object=servicosModel.objects.get(id=pk)
    formulario=cobrancaForm(request.POST)
    if request.method=='POST':
        if formulario.is_valid():
            novoPagamento=formulario.save(commit=False)
            novoPagamento.servico=object
            novoPagamento.save()
            messages.add_message(request, messages.SUCCESS, "O pagamento foi registrado com sucesso!")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.WARNING, "Houve um erro ao registrar o pagamento")
            return redirect(request.META['HTTP_REFERER'])
@login_required()
@transaction.non_atomic_requests
def SigmaSigma(request):
    if request.method == 'POST':

        formulario=servicoTransferenciaSigmaSigma(request.POST)
        #cliente = clienteModel.objects.get(pk=pk)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS,
                                 'O processo de Transferência foi registrado com êxito',
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
            arma = formulario.cleaned_data['arma']
            arma.mudancaPropriedade = True
            arma.save()
            messages.add_message(request, messages.SUCCESS,
                                 "A arma {} agora está em processo de transferência de propriedade".format(arma),
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
            """
            tipoServico = listaServicos.objects.get(pk=2)
            object=transferenciaSigmaSigma.objects.latest('pk')
            #Registrar novo serviço
            
            registrarServico=servicosModel.objects.create(
                cliente=cliente,
                tipoServico=tipoServico,
                descricaServico=str("TRANSFERÊNCIA SIGMA-SIGMA {}".format(cliente.nome)),
                valor=decimal.Decimal(formulario.cleaned_data['valor']),
                content_object=object
            ).save()
           
            
            messages.add_message(request, messages.SUCCESS, "Serviço registrado com sucesso!")
            
            lista_exigencias = servico.tipoServico.exigencias.all()
            for item in lista_exigencias:
                cumprimentoExigenciasModel.objects.create(
                    servico=servico,
                    exigencia=item,
                    cumprida=False
                ).save()
            """
            servico = transferenciaSigmaSigma.objects.latest('pk')
            renderizarSgimaSigma(servico=servico, objeto=servico.pk)
            messages.add_message(request, messages.SUCCESS,
                                 "O requerimento PDF já está disponível",
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})


            return redirect('gestao:clientes:detalhar', servico.responsavel.pk)
        else:
            contexto = {
                'form': formulario,
                'object_list': transferenciaSigmaSigma.objects.all().order_by('dataRegistro')
            }
            return render(request, 'gestao3/servicos/transferenciaSigmaSigma.html', contexto)
    else:
        contexto={
            'form':servicoTransferenciaSigmaSigma,
            'object_list':transferenciaSigmaSigma.objects.all().order_by('dataRegistro')
        }
        return render(request, 'gestao3/servicos/transferenciaSigmaSigma.html', contexto)
@login_required()
def SinarmSigma(request, pk):
    if request.method == 'POST':
        formulario=formTransferenciaSinarmSigma(request.POST)
        cliente = clienteModel.objects.get(pk=pk)
        if formulario.is_valid():
            novoRegistro=formulario.save(commit=True)
            if not novoRegistro:
                pass
            arma = formulario.cleaned_data['arma']
            arma.mudancaPropriedade = True
            arma.save()
            messages.add_message(request, messages.INFO, "A arma {} agora está em processo de transferência de propriedade".format(arma))
            tipoServico = listaServicos.objects.get(pk=11)
            object=transferenciaSinarmSigma.objects.latest('pk')
            #Registrar novo serviço
            registrarServico=servicosModel.objects.create(
                cliente=cliente,
                tipoServico=tipoServico,
                descricaServico=str("TRANSFERÊNCIA SNARM-SIGMA {}".format(cliente.nome)),
                valor=decimal.Decimal(formulario.cleaned_data['valor']),
                content_object=object
            ).save()
            messages.add_message(request, messages.SUCCESS, "Serviço registrado com sucesso!")
            servico = servicosModel.objects.latest('pk')
            lista_exigencias = servico.tipoServico.exigencias.all()
            for item in lista_exigencias:
                cumprimentoExigenciasModel.objects.create(
                    servico=servico,
                    exigencia=item,
                    cumprida=False
                ).save()
            registrar_pdf=renderizarSinarmSigma(servico=servico, objeto=object.pk)
            messages.add_message(request, messages.SUCCESS,
                                     "O requerimento PDF já está disponível")

            return redirect('gestao:servicos:detalhes', servico.pk)
        else:
            contexto = {
                'form': formulario,
                'object_list': transferenciaSigmaSigma.objects.all().order_by('dataRegistro')
            }
            return render(request, 'gestao/servicos/sigmaSigma.html', contexto)
    else:
        contexto={
            'form':formTransferenciaSinarmSigma(cliente_id=pk),
            'object_list':transferenciaSinarmSigma.objects.all().order_by('dataRegistro')
        }
        return render(request, 'gestao/servicos/sigmaSigma.html', contexto)

@login_required()
def SinarmSigmaRequerimento(request):
    if request.method=='POST':
        formulario=formTransferenciaSinarmSigma(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, 'Requerimento registrado com sucesso!')
            objeto=transferenciaSinarmSigma.objects.latest('pk')

            renderizarSinarmSigma(responsavel=objeto.responsavel, objeto=objeto)
            return redirect('gestao:clientes:detalhar', objeto.responsavel.pk)
        else:
            contexto ={
                'form':formulario
            }
            return render(request, 'gestao3/servicos/transferenciaSinarmSigma.html', contexto)
    else:
        contexto={
            'form':formTransferenciaSinarmSigma
        }
        return render(request, 'gestao3/servicos/transferenciaSinarmSigma.html', contexto)
@login_required()
def SigmaSigmaDetalhes(request, pk):
    object=get_object_or_404(transferenciaSigmaSigma, pk=pk)
    if request.method=='POST':
        pass
    else:
        contexto = {
            'object': object,
            'form': servicoTransferenciaSigmaSigma(instance=object),
            'object_list': transferenciaSigmaSigma.objects.exclude(pk=object.pk).order_by('dataRegistro')
        }
        return render(request, 'gestao/servicos/sigmaSigma.html', contexto)
@login_required()
@transaction.non_atomic_requests
def apostilamentoCR(request, pk):
    formSetarquivos = formset_factory(arquivosForm, extra=1, validate_min=1)
    if request.method=='POST':
        formulario=apostimanetosCRForm(request.POST)
        form_set=formSetarquivos(request.POST, request.FILES)
        if formulario.is_valid() and form_set.is_valid():
            novoApostilamento=formulario
            novoApostilamento.save()
            objeto=apostilamentosExercito.objects.latest('pk')

            servicosModel.objects.create(
                cliente=objeto.cliente,
                descricaServico='APOSTILAMENTO',
                tipoServico=listaServicos.objects.get(pk=8),
                content_object=objeto,
                valor=formulario.cleaned_data['valor']

            ).save()
            novo_servico=servicosModel.objects.latest('pk')
            numero_arquivos=0
            for item in form_set:
                arquivosModel.objects.create(
                    content_object=novo_servico,
                    nome=item.cleaned_data['nome'],
                    tipoArquivo=item.cleaned_data['tipoArquivo'],
                    arquivo=item.cleaned_data['arquivo']
                ).save()
                numero_arquivos+=1

            #Criar arquivo de apostilamento
            renderizarReqApostimaneto(apostilamento=objeto, servico=novo_servico, endereco=novo_servico.cliente.enderecos_cliente.first())

            messages.add_message(request, messages.SUCCESS, "O serviço de apostilamento foi registrado com sucesso")
            messages.add_message(request, messages.SUCCESS, "{} arquivos foram vinculados ao serviço".format(numero_arquivos))
            return redirect('gestao:servicos:detalhes', pk=novo_servico.pk)
    else:

        contexto={
            'form':apostimanetosCRForm(cliente_id=pk),
            'object_list':apostilamentosExercito.objects.all(),
            'form_set':formSetarquivos
        }
        return render(request, 'gestao/servicos/reqApostilamentoCR.html', contexto)
@login_required()
def emissaoGT(request, pk):
    cliente=get_object_or_404(clienteModel, pk=pk)
    formulario = servicoEmissaoGTForm(request.POST)
    if request.method=='POST':
        if formulario.is_valid():
            nova_gt=formulario.save()
            object=emissaoGuiaTrafego.objects.latest('pk')
            servicosModel.objects.create(
                cliente=cliente,
                descricaServico=str("Emissão de GT {}".format(cliente.nome)),
                content_object=object,
            ).save()
            messages.add_message(request, messages.SUCCESS, "O pedido de Emissão de Guia de Tráfego foi registrado com êxito")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.WARNING,
                                 "Há um problema com a requisição da Guia de Tráfego!")
            contexto = {
                'object_list': emissaoGuiaTrafego.objects.all()[:10],
                'form': formulario
            }
            return render(request, 'gestao/servicos/emissaoGT.html', contexto)
    else:
        contexto={
            'object_list':emissaoGuiaTrafego.objects.all()[:10],
            'form':servicoEmissaoGTForm(cliente_id=cliente.pk)
        }
        return render(request, 'gestao/servicos/emissaoGT.html', contexto)
@login_required()
def requerimentoRegistroCR(request, pk):
    cliente=get_object_or_404(clienteModel, pk=pk)
    tipoServico=listaServicos.objects.get(pk=7)
    if request.method=='POST':
        formulario=servicoRegistroCRForm(request.POST)
        if formulario.is_valid():

            novoRegistro=formulario.save(commit=False)
            novoRegistro.cliente=cliente
            novoRegistro.save()
            object=registroCR.objects.latest('pk')
            servicosModel.objects.create(
                cliente=cliente,
                tipoServico=tipoServico,
                descricaServico=str("Emissão de CR {}".format(cliente.nome)),
                valor=decimal.Decimal(formulario.cleaned_data['valor']),
                content_object=object
            ).save()
            if novoRegistro:
                servico=servicosModel.objects.latest('pk')
                lista_exigencias = servico.tipoServico.exigencias.all()
                for item in lista_exigencias:
                    cumprimentoExigenciasModel.objects.create(
                        servico=servico,
                        exigencia=item,
                        cumprida=False
                    ).save()
            messages.add_message(request, messages.SUCCESS, "O serviço de Emissão de CR foi registrado com sucesso!")
            return redirect('gestao:servicos:detalhes', servico.pk)
    else:
        contexto={
            'object':cliente,
            'form':servicoRegistroCRForm(cliente_id=cliente.pk)

        }
        return render(request, 'gestao/servicos/reqRegistroCR.html', contexto)
@login_required()
def requerimentoArmasAcessorios(request, pk):
    cliente=get_object_or_404(clienteModel, pk=pk)
    if request.method=='POST':
        formulario=servicoAquisicaoPCEForm(request.POST)
        formSet=formSetArmaseAcessorios(request.POST)
        if formulario.is_valid() and formSet.is_valid():
            novoRequerimento=formulario.save(commit=False)
            novoRequerimento.save()
            object=aquisicaoPCE.objects.latest('pk')
            for form in formSet:
                item=form.save(commit=False)
                item.processo=object
                item.save()
            servicosModel.objects.create(
                cliente=cliente,
                descricaServico=str("Requerimento físico aquisição de PCE {}".format(cliente.nome)),
                content_object=object,
            ).save()
            ultimo_servico=servicosModel.objects.latest('pk')

            messages.add_message(request, messages.SUCCESS, "O requerimento de aquisição foi registrado com sucessso")
            renderizarReqFisicoPCE(cliente=cliente.pk, objeto=object.pk, servico=ultimo_servico)
            messages.add_message(request, messages.SUCCESS, "O arquivo já está disponível")
            return redirect('gestao:servicos:detalhes', ultimo_servico.pk)
        else:
            contexto = {

                'object_list': aquisicaoPCE.objects.all().order_by('cliente'),
                'form': formulario,
                'form_set': formSet
            }
            return render(request, 'gestao/servicos/reqAquisicaoPCE.html', contexto)
    else:
        contexto={
            'object_list':aquisicaoPCE.objects.all().order_by('cliente'),
            'form':servicoAquisicaoPCEForm(cliente_id=pk),
            'form_set':formSetArmaseAcessorios
        }
        return render(request, 'gestao/servicos/reqAquisicaoPCE.html', contexto)
@login_required()
def requerimentoArmasAcessoriosVisualizar(request, pk):
    if request.method=='POST':
        pass
    else:
        object=get_object_or_404(aquisicaoPCE, pk=pk)
        contexto={
            'object':object,
        }
        return render(request, 'gestao/servicos/reqAquisicaoPCEVisualizar.html', contexto)
@login_required()
@transaction.non_atomic_requests
def registrarServicoSisgCOrp(request, pk):
    if request.method=='POST':
        formulario=servicosSisgCorpForm(request.POST)
        if formulario.is_valid():
            formulario.save(commit=True)
            ultimo_registro=servicosSisgcorpModel.objects.latest('pk')
            #Registar em Serviços
            servicosModel.objects.create(
                cliente=ultimo_registro.cliente,
                descricaServico=formulario.cleaned_data['objeto'],
                content_object=ultimo_registro,
                valor=formulario.cleaned_data['valor'],
                observacao=formulario.cleaned_data['observacoes']
            ).save()
            messages.add_message(request, messages.SUCCESS, 'Registro realizado com êxito!')
            return redirect('gestao:clientes:detalhes',ultimo_registro.cliente.pk)

    else:
        messages.add_message(request, messages.WARNING, 'É impossível atender esta requisição')
        return redirect(request.META['HTTP_REFERER'])
@login_required()
def movimentacoesView(request):
    movimentacoes=movimentacoesServico.objects.all()
    servicos=servicosModel.objects.all()
    contexto={
        'object_list':servicos.prefetch_related('movimentacoes').order_by('dataRegistro', 'movimentacoes__dataMovimentacao')
    }
    return render(request, 'gestao/servicos/movimentacaoInicio.html', contexto)
@login_required()
def termoDoacaoSinarm(request):
    if request.method == 'POST':
        formulario=formTermoDoacao(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.WARNING, 'Requisição atendida.')
            return redirect(request.META['HTTP_REFERER'])
        else:
            contexto={
                'formulario':formulario,
                'object_list':termoDoacaoModel.objects.all()

            }
            return render(request, 'gestao_v2/servicos/termoDoacao.html', contexto)
    else:
        contexto={
            'formulario':formTermoDoacao,
            'object_list':termoDoacaoModel.objects.all()
        }
        return render(request, 'gestao_v2/servicos/termoDoacao.html', contexto)
@login_required()
def verTermoDoacao(request, pk):
    object = get_object_or_404(termoDoacaoModel, pk=pk)
    enderecoDoador=enderecoClienteModel.objects.filter(cliente=object.doador, principal=True).first()
    enderecoDonatario=enderecoClienteModel.objects.filter(cliente=object.donatario, principal=True).first()
    contexto = {
        'object':object,
        'enderecoDoador':enderecoDoador,
        'enderecoDonatario':enderecoDonatario
    }
    return render(request, 'relatorios/requerimentoTermoDoacao.html', contexto)
@login_required()
def requerimentoFisicoSinarm(request):
    if request.method == 'POST':
        formulario=requerimentosFisicosSinarmForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.WARNING, 'É impossível atender esta requisição')
            return redirect(request.META['HTTP_REFERER'])
        else:
            contexto={
                'formulario':formulario,
                'object_list':requerimentosFisicosSinarm.objects.all().order_by('dataRegistro')

            }
            return render(request, 'gestao_v2/servicos/requerimentoFisicoSinarm.html', contexto)
    else:
        contexto={
            'formulario':requerimentosFisicosSinarmForm,
            'object_list':requerimentosFisicosSinarm.objects.all().order_by('dataRegistro')
        }
        return render(request, 'gestao_v2/servicos/requerimentoFisicoSinarm.html', contexto)
@login_required()
def visualizarRequerimentoFisicoPF(request, pk):
    object=requerimentosFisicosSinarm.objects.get(pk=pk)
    cliente=object.cliente
    endereco=enderecoClienteModel.objects.filter(cliente=cliente).filter(principal=True)
    if endereco.exists():
        #enderecoPrincipal=endereco.objects.latest('pk')
        contexto={
            'object':object,
            'endereco':endereco.latest('pk')
        }
        return render(request, 'relatorios/requerimentoFisicoSinarm.html', contexto)
    else:
        messages.add_message(request, messages.WARNING, 'O cliente não possui endereço ou não é o endereço principal')
        return redirect(request.META['HTTP_REFERER'])
@login_required()
def viewRendererizarRequerimentoFisicoSinarm(request, pk):
    object = requerimentosFisicosSinarm.objects.get(pk=pk)
    cliente = object.cliente
    endereco = enderecoClienteModel.objects.filter(cliente=cliente).filter(principal=True)
    if endereco.exists():
        object=object
        endereco=endereco
        renderizarReqSINARMFisicio(object=object, endereco=endereco)
        messages.add_message(request, messages.SUCCESS, 'O requerimento está disponível')
        return redirect('gestao:clientes:detalhes', object.cliente.pk)
def renderizarTermoDoacao(request, pk):
    object=termoDoacaoModel.objects.get(pk=pk)

@login_required()
def apostilamentoSIGMACriar(request):
    object_list=apostilamentosExercito.objects.all().order_by('-dataRegistro')
    if request.method=='POST':
        formulario=apostimanetoExercitoForm(request.POST)
        formSetApostilamento=formSetitensApostilamentoExercitoForm(request.POST)
        if formulario.is_valid():# and formSetApostilamento.is_valid():
            formulario.save()
            """
            instnacia=apostilamentosExercito.objects.latest('pk')
            form_set=formSetApostilamento.save(commit=False)
            for item in form_set:
                item.apostilamento=instnacia
                item.save
            """
            messages.add_message(request, messages.SUCCESS, "Um requerimento de apostilamento foi registrado com êxito!")
            return redirect(request.META['HTTP_REFERER'])
        else:
            contexto={
                'formulario':formulario,
                'object_list':object_list
            }
            messages.add_message(request, messages.WARNING, "Houve um erro no atendimento da sua requisição")
            return render(request, 'gestao_v2/servicos/requerimentoApostilamentoSIGMA.html', contexto)
    else:
        contexto={
            'formulario': apostimanetoExercitoForm,
            #'formSetApostilamento': formSetitensApostilamentoExercitoForm,
            'object_list':object_list
        }
        return render(request, 'gestao_v2/servicos/requerimentoApostilamentoSIGMA.html', contexto)
@login_required()
def visualizarRequerimentoFisicoSIGMA(request, pk):
    object=apostilamentosExercito.objects.get(pk=pk)
    cliente=object.cliente
    endereco=cliente.enderecos_cliente.filter(principal=True).latest('pk')
    if endereco is None:
        messages.add_message(request, messages.WARNING, 'O cliente não possui um endereço válido')
        return redirect(request.META['HTTP_REFERER'])
    else:
        contexto={
            'object':object,
            'endereco':endereco

        }
        return render(request, 'relatorios/requerimentoApostilamento.html', contexto)
def renderizerRequerimentoFisicoApostilamentoSIGMA(request, pk):
    object = apostilamentosExercito.objects.get(pk=pk)
    cliente = object.cliente
    endereco = enderecoClienteModel.objects.filter(cliente=cliente).filter(principal=True).latest('pk')
    renderizarReqApostimaneto(apostilamento=object, endereco=endereco)
    messages.add_message(request, messages.SUCCESS, 'O requerimento está disponível')
    return redirect('gestao:clientes:detalhes', object.cliente.pk)

@login_required()
def requerimentoRenovacaoCRAFSIGMAview(request):
    if request.method=='POST':
        formulario=formRequerimentoRenovaCaoCRAFSIGMA(request.POST)
        if formulario.is_valid():
            novorRegistro=formulario.save(commit=False)
            cliente = formulario.cleaned_data['cliente']
            novorRegistro.endereco=cliente.enderecos_cliente.first()
            novorRegistro.save()


            messages.add_message(request, messages.SUCCESS, 'O requerimento está disponível')
            return redirect('gestao:servicos:renovacao-craf-sigma')
        else:
            contexto = {
                'formulario':formulario,
                'object_list':renovacaoCRAF.objects.all()
            }
            return render(request, 'gestao_v2/servicos/requerimentorenovacaoCRAFSIGMA.html', contexto)
    else:
        contexto={
            'formulario': formRequerimentoRenovaCaoCRAFSIGMA,
            'object_list': renovacaoCRAF.objects.all()
        }
        return render(request, 'gestao_v2/servicos/requerimentorenovacaoCRAFSIGMA.html', contexto)

@login_required()
def verReqRenovacaoCRAFSIGMA(request, pk):
    object = get_object_or_404(renovacaoCRAF, pk=pk)
    contexto = {
        'object':object
    }
    return render(request, 'relatorios/requerimentoRenovacaoCRAFSIGMA.html', contexto)
@login_required()
def viewRenderizerRequerimentoRenovacaoCRAFSIGMA(request, pk):
    object = renovacaoCRAF.objects.get(pk=pk)
    cliente = object.cliente
    #endereco = enderecoClienteModel.objects.filter(cliente=cliente).filter(principal=True).latest('pk')
    renderizarTermoDoacao(requerimento=object.pk)
    messages.add_message(request, messages.SUCCESS, 'O requerimento está disponível')
    return redirect('gestao:clientes:detalhes', object.cliente.pk)
def viewRenderizerTermoDoacao(request, pk):
    object = termoDoacaoModel.objects.get(pk=pk)

    renderizadorTermoDoacao(requerimento=object.pk)
    messages.add_message(request, messages.SUCCESS, 'O requerimento está disponível')
    return redirect('gestao:clientes:detalhes', object.doador.pk)