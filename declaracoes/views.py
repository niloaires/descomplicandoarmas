from django.shortcuts import render, get_object_or_404, redirect
from clientes.models import clienteModel
from declaracoes.forms import declaracaoGuardaAcervoForm, declaracoesDiversasForm, declaracoesResidenciaDiversaForm
from declaracoes.models import declaracaoGuardaAcervo, declaracoesDiversas, declarcoesResidencia
from django.contrib import messages
from documentos.renderizadores import renderizarDecGuardaAcervo, renderizarDeclaracoes, renderizarDeclaracoesDiversas, \
    renderizardeclaracaoResidenciaDiversa


# Create your views here.
def criarGuardaAcervo(request, pk):
    cliente = get_object_or_404(clienteModel, pk=pk)
    if request.method=='POST':
        formulario=declaracaoGuardaAcervoForm(request.POST)
        if formulario.is_valid():
            formulario.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "O registro da declaração foi realizado com sucesso")
            novo_declaracao=declaracaoGuardaAcervo.objects.latest('pk')
            endereco=novo_declaracao.endereco
            renderizarDecGuardaAcervo(objeto=novo_declaracao)
            messages.add_message(request, messages.SUCCESS, "O documento já está disponível")
            return redirect(request.META['HTTP_REFERER'])
        else:

            contexto = {
                'form': formulario,
                'object_list': declaracaoGuardaAcervo.objects.all().order_by('dataRegistro')
            }
            messages.add_message(request, messages.WARNING, "Houve um erro na sua reuqisição")
            return render(request, 'gestao/declaracoes/guardaAcervo.html', contexto)

    else:
        contexto={
            'form': declaracaoGuardaAcervoForm(cliente_id=pk),
            'object_list':declaracaoGuardaAcervo.objects.all().order_by('dataRegistro')
        }
        return render(request, 'gestao/declaracoes/guardaAcervo.html', contexto)

def gerarDeclaracoesUnificadas(request, pk):
    renderizador=renderizarDeclaracoes(cliente=pk)
    if renderizador:
        messages.add_message(request, messages.SUCCESS, 'As declarações já estão disponíveis',
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'notice'})
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.add_message(request, messages.SUCCESS, 'Não foi possível atender a requisição',
                             extra_tags={'titulo': 'Notificação do sistema', 'style': 'warning'})
        return redirect(request.META['HTTP_REFERER'])
def gerarDeclaracaoDiversa(request, pk):
    cliente = get_object_or_404(clienteModel, pk=pk)
    if request.method=='POST':
        formulario = declaracoesDiversasForm(request.POST)
        if formulario.is_valid():
            novaDeclaracao=formulario.save(commit=False)
            novaDeclaracao.cliente=cliente
            novaDeclaracao.texto=request.POST.get('texto')
            novaDeclaracao.save()
            objeto=declaracoesDiversas.objects.latest('pk')
            renderizarDeclaracoesDiversas(objeto.pk)
            messages.add_message(request, messages.SUCCESS, "Nova declaração criada com sucesso!")
            return redirect('gestao:clientes:detalhes', objeto.cliente.pk)
        else:
            for erro in formulario:
                messages.add_message(request, messages.WARNING, erro)
                return redirect(request.META.HTTP_REFERER)
    else:
        messages.add_message(request, messages.WARNING, 'Essa operação é impossível!')
        return redirect(request.META.HTTP_REFERER)
def gerarDeclaracaoEnderecoDiversa(request, pk):
    if request.method=='POST':
        formulario=declaracoesResidenciaDiversaForm(request.POST)
        if formulario.is_valid():
            cliente=clienteModel.objects.get(pk=pk)
            novoregistro=formulario.save(commit=False)
            novoregistro.cliente=cliente
            novoregistro.save()
            objeto=declarcoesResidencia.objects.latest('pk')
            renderizardeclaracaoResidenciaDiversa(objeto=objeto.pk)
            messages.add_message(request, messages.SUCCESS, "Nova declaração criada com sucesso!")
            return redirect('gestao:clientes:detalhar', objeto.cliente.pk)
        else:
            for erro in formulario:
                messages.add_message(request, messages.WARNING, erro)

                return redirect('gestao:clientes:detalhar', pk)

    else:
        messages.add_message(request, messages.WARNING, 'Essa operação é impossível!')
        return redirect('gestao:clientes:detalhar', pk)