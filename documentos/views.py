from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from documentos.renderizadores import renderizarDeclaracoes
from django.contrib import messages
from documentos.forms import *
from clientes.models import clienteModel
# Create your views here.
@login_required()
def carregarDocsClientes(request, pk):
    if request.method == 'POST':
        formulario=arquivosForm(request.POST,request.FILES)
        cliente = clienteModel.objects.get(pk=pk)
        if formulario.is_valid():
            arquivosModel.objects.create(
                content_object=cliente,
                cliente_id=cliente.pk,
                nome=formulario.cleaned_data['nome'],
                validade=formulario.cleaned_data['validade'],
                tipoArquivo=formulario.cleaned_data['tipoArquivo'],
                arquivo=formulario.cleaned_data['arquivo'],
            ).save()

            messages.add_message(request, messages.SUCCESS,
                                 'O documento de {} foi registrado com sucesso!'.format(cliente.nome),
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'O documento de {} não foi registrado!'.format(cliente.nome),
                                 extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
            return redirect(request.META['HTTP_REFERER'])

    else:
        messages.add_message(request, messages.WARNING, "Esta solicitação é impossível de ser atendida!")
        return redirect(request.META['HTTP_REFERER'])
@login_required()
def listarDocumentos(request):
    clientes=clienteModel.objects.all()
    object_list=arquivosModel.objects.all()
    contexto={
        'listaClientes':clientes.order_by('nome'),
        'object_list':object_list
    }
    return render(request, 'gestao_v2/listarArquivos.html', contexto)
@login_required()
def listarDocumentosClientes(request, pk):
    cliente=get_object_or_404(clienteModel, pk=pk)
    object_list=cliente.arquivos.all()
    contexto={
        'object':cliente,
        'object_list':object_list
    }
    return render(request, 'gestao_v2/listarArquivosCliente.html', contexto)
@login_required()
def deletarArquivo(request, pk):
    object=arquivosModel.objects.get(pk=pk)
    object.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Arquivo deletado!',
                         extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
    return redirect(request.META['HTTP_REFERER'])