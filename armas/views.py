from django.shortcuts import render, redirect, get_object_or_404
from armas.models import armasClientes
from django.contrib import messages
from armas.forms import *
def armasInicio(request):
    if request.method=='POST':
        formulario=armasForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            novo_registro=armasClientes.objects.latest('pk')
            messages.add_message(request, messages.SUCCESS, "A arma {} foi registrada com sucesso".format(novo_registro.idenfificacao()))
            return redirect(request.META['HTTP_REFERER'])
        else:
            contexto={
                'object_list': armasClientes.objects.all().order_by('cliente'),
                'form':formulario

            }
            return render(request, 'gestao/armas/armasInicio.html', contexto)
    else:
        contexto={
            'object_list':armasClientes.objects.all().order_by('cliente'),
            'form':armasForm
        }
        return render(request, 'gestao_v2/armas/listagemArmas.html', contexto)
def armaEditar(request, pk):
    object=get_object_or_404(armasClientes, pk=pk)
    if request.method=='POST':
        formulario=armasForm(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, "A arma {} foi editada com sucesso".format(object.idenfificacao()))
            return redirect('gestao:armas:inicio')
        else:
            contexto={
                'object':object,
                'form':formulario
            }
            return render(request, 'gestao/armas/armaEditar.html', contexto)
    else:
        contexto={
            'object':object,
            'form':armasForm(instance=object)
        }
        return render(request, 'gestao/armas/armaEditar.html', contexto)
def armaDeletar(request, pk):
    object=armasClientes.objects.get(pk=pk)
    object.delete()
    messages.add_message(request, messages.SUCCESS, "Arma excluída com sucesso!")
    return redirect(request.META['HTTP_REFERER'])
def clientesArmas(request, pk):
    if request.method == 'POST':
        cliente=clienteModel.objects.get(pk=pk)
        form=armasForm(request.POST)
        if form.is_valid():
            novaArma=form.save(commit=False)
            novaArma.cliente=cliente
            novaArma.save()
            messages.add_message(request, messages.SUCCESS, "Uma nova arma foi adicionada")
            return redirect(request.META['HTTP_REFERER'])
        else:
            contexto ={
                'form': form,
                'object_list': armasClientes.objects.filter(cliente_id=pk).order_by('pk')
            }
            messages.add_message(request, messages.WARNING, "Houve um erro ao registrar a arma")
            return render(request, 'gestao/armas/armasCliente.html', contexto)

    else:
        contexto = {
            'form': armasForm(cliente_id=pk),
            'object_list': armasClientes.objects.filter(cliente_id=pk).order_by('pk')

        }
        return render(request, 'gestao/armas/armasCliente.html', contexto)