from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from enderecos.forms import *
from django.contrib import messages
# Create your views here.
@login_required()
def enderecoAdicionar(request, pk):
    cliente=clienteModel.objects.get(pk=pk)
    form=enderecoClienteForm(request.POST)
    if request.POST and form.is_valid():
        for endereco in cliente.enderecos_cliente.all():
            endereco.principal=False
            endereco.save()
        novo_endereco=form.save(commit=False)
        novo_endereco.cliente=cliente
        novo_endereco.principal=True
        novo_endereco.save()
        messages.add_message(request, messages.SUCCESS, "Um novo endereço foi adicioado ao cliente {}".format(cliente.nome.upper()))
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.add_message(request, messages.ERROR, "Houve um erro na sua solicitação")
        return redirect(request.META['HTTP_REFERER'])
@login_required()
def definirEnderecoPrincipal(request, pk):
    objeto=enderecoClienteModel.objects.get(pk=pk)
    cliente=objeto.cliente
    for endereco in cliente.enderecos_cliente.all():
        endereco.principal=False
        endereco.save()
    objeto.principal=True
    objeto.save()
    messages.add_message(request, messages.SUCCESS,
                         "Um novo endereço foi definido como principal para o cliente {}".format(cliente.nome.upper()))
    return redirect(request.META['HTTP_REFERER'])