from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
from armas.models import armasClientes
from clientes.models import clienteModel
from documentos.models import arquivosModel
from laudoPsicologico.models import laudosPsicologicosModel
from servicos.models import transferenciaSigmaSigma, aquisicaoPCE, servicosModel, transferenciaSinarmSigma, \
    requerimentosFisicosSinarm, renovacaoCRAF, termoDoacaoModel
from django.contrib import messages
from declaracoes.models import *
import datetime

from django.conf import settings

def renderizarReqApostimaneto(apostilamento, endereco):
    object=apostilamento
    hoje = datetime.date.today()
    contexto={
        'object':object,
        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,
        'endereco': endereco
    }

    html_string = render_to_string('relatorios/requerimentoApostilamento.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=object.cliente,
        tipoArquivo='requerimento',
        nome=str('REQUERIMENTO DE APOSTILAMENTO {}'.format(object.cliente.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True
def renderizarDecGuardaAcervo( objeto):
    objeto=declaracaoGuardaAcervo.objects.get(pk=objeto.pk)
    cliente=objeto.cliente
    endereco=objeto.endereco
    hoje = datetime.date.today()
    contexto={
        'cliente':cliente,
        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,

        'endereco': endereco
    }

    html_string = render_to_string('relatorios/declaracaoGuardaArcervo.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    nome_arquivo = uuid4().hex
    html.write_pdf(settings.MEDIA_ROOT +'docs/{}/{}/{}.pdf'.format(ano, mes, nome_arquivo))
    with open('docs/{}/{}/{}.pdf'.format(ano, mes, nome_arquivo), 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=objeto,
        tipoArquivo='declaracao',
        nome=str('DECLARACAO DE GUARDA DE ACERVO {}'.format(cliente.nome)),
        arquivo=documento.file.name
    ).save()
    finalizada = True
def renderizarSgimaSigma(servico, objeto):

    objeto=transferenciaSigmaSigma.objects.get(pk=objeto)



    hoje = datetime.date.today()
    contexto={
        'objeto':objeto,
        'cliente':objeto.responsavel,
        'adquirente':objeto.adquirente,
        'alienante':objeto.alienante,
        'arma':objeto.arma,
        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,


    }


    html_string = render_to_string('relatorios/SigmaSigma.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)
    arquivosModel.objects.create(
        content_object=objeto.responsavel,
        cliente_id=objeto.responsavel.pk,
        tipoArquivo='declaracao',
        nome=str('REQUERIMENTO DE TRANSFERÊNCIA DE PROPRIEDADE DE ARMA DE FOGO  - SIGMA PARA SIGMA {}'
                 .format(objeto.responsavel.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True
def renderizarReqFisicoPCE(cliente, objeto, servico):
    cliente=clienteModel.objects.get(pk=cliente)
    objeto=aquisicaoPCE.objects.get(pk=objeto)
    itens=objeto.armaseAcessorios.all()
    hoje = datetime.date.today()
    contexto={
        'cliente':cliente,
        'object':objeto,
        'itens':itens,
        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,


    }

    html_string = render_to_string('relatorios/aquisicaoPCE.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo=str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT+nome_arquivo)
    with open(settings.MEDIA_ROOT+nome_arquivo, 'r') as f:
        documento = File(f)
    #ultimo_servico=servicosModel.objects.latest('pk')
    arquivosModel.objects.create(
        content_object=servico,
        cliente_id=cliente.pk,
        tipoArquivo='declaracao',
        nome=str('AUTORIZAÇÃO DE COMPRA - {}'
                 .format(cliente.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True
def renderizarDeclaracoes(cliente):
    objeto=clienteModel.objects.get(pk=cliente)
    endereco=enderecoClienteModel.objects.filter(principal=True, cliente=objeto).first()
    hoje = datetime.date.today()
    contexto={
        'cliente':objeto,
        'endereco':endereco,
        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,


    }

    html_string = render_to_string('relatorios/declaracoes_unificadas.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=objeto,
        cliente_id=objeto.pk,
        tipoArquivo='declaracao',
        nome=str('DECLARAÇÕES UNIFICADAS {}'
                 .format(objeto.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True

def renderizarDeclaracoesDiversas(pk):
    objeto=declaracoesDiversas.objects.get(pk=pk)

    hoje = datetime.date.today()
    contexto={
        'objeto':objeto,
        'data': objeto.dataRegistro


    }

    html_string = render_to_string('relatorios/declaracoesDiversas.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo=str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT+nome_arquivo)
    with open(settings.MEDIA_ROOT+nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=objeto.cliente,
        cliente_id=objeto.cliente.pk,
        tipoArquivo='declaracao',
        nome=str('{} - {}'
                 .format(objeto.titulo, objeto.cliente.nome.u)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True

def renderizarSinarmSigma(responsavel, objeto):
    objeto=transferenciaSinarmSigma.objects.get(pk=objeto.pk)
    endereco=enderecoClienteModel.objects.filter(principal=True, cliente=objeto.alienante).first()
    hoje = datetime.date.today()
    contexto={
        'objeto':objeto,
        'cliente':objeto.responsavel,
        'adquirente':objeto.adquirente,
        'alienante':objeto.alienante,
        'endereco':endereco,
        'arma':objeto.arma,
        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,


    }
    html_string = render_to_string('relatorios/SinarmSigma.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=responsavel,
        cliente_id=responsavel.pk,
        tipoArquivo='declaracao',
        nome=str('TRANSFERÊNCIA SIRMAR - SIGMA | {}'
                 .format(responsavel.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True

def renderizardeclaracaoResidenciaDiversa(objeto):
    objeto=declarcoesResidencia.objects.get(pk=objeto)
    hoje = datetime.date.today()
    contexto={
        'objeto':objeto,
        'cliente':objeto.cliente,

        'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                     mes=hoje.strftime('%B'),
                                                     ano=hoje.strftime('%Y'))),
        'hoje': hoje,


    }
    html_string = render_to_string('relatorios/declaracaoResidenciaDiversa.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=objeto.cliente,
        cliente_id=objeto.cliente.pk,
        tipoArquivo='declaracao',
        nome=str('DECLARAÇÃO DE RESIDÊNCIA | {}'
                 .format(objeto.cliente.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True

def renderizarReqSINARMFisicio(object, endereco):
    cliente=object.cliente
    hoje = datetime.date.today()
    contexto={
        'object':object,
        'endereco':endereco
    }
    html_string = render_to_string('relatorios/requerimentoFisicoSinarm.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=object.cliente,
        cliente_id=object.cliente.pk,
        tipoArquivo='requerimento',
        nome=str('REQUERIMENTO FÍSICIO SINARM | {}'
                 .format(cliente.nome)),
        arquivo=nome_arquivo
    ).save()
    finalizada = True

def renderizarRequerimentoRenovacaoCRAFSIGMA(requerimento):
    object = renovacaoCRAF.objects.get(pk=requerimento)
    hoje = datetime.date.today()
    contexto ={
        'hoje':datetime.date.today(),
        'object':object
    }
    html_string = render_to_string('relatorios/requerimentoRenovacaoCRAFSIGMA.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=object.cliente,
        cliente_id=object.cliente.pk,
        tipoArquivo='requerimento',
        nome=str('REQUERIMENTO RENOVAÇÃO CRAF - {} | {}'
                 .format(object.cliente.nome, object.arma.modelo)),
        arquivo=nome_arquivo
    ).save()

def renderizarTermoDoacaoSINARM(requerimento):
    object = renovacaoCRAF.objects.get(pk=requerimento)
    hoje = datetime.date.today()
    contexto ={
        'hoje':datetime.date.today(),
        'object':object
    }
    html_string = render_to_string('relatorios/requerimentoRenovacaoCRAFSIGMA.html', contexto)
    html = HTML(string=html_string)
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=object.cliente,
        cliente_id=object.cliente.pk,
        tipoArquivo='requerimento',
        nome=str('REQUERIMENTO RENOVAÇÃO CRAF - {} | {}'
                 .format(object.cliente.nome, object.arma.modelo)),
        arquivo=nome_arquivo
    ).save()


def renderizadorTermoDoacao(requerimento):
    object = termoDoacaoModel.objects.get(pk=requerimento)
    enderecoDoador = enderecoClienteModel.objects.filter(cliente=object.doador, principal=True).first()
    enderecoDonatario = enderecoClienteModel.objects.filter(cliente=object.donatario, principal=True).first()
    enderecoDoador= enderecoDoador
    enderecoDonatario= enderecoDonatario
    contexto = {
        'hoje': object.dataRegistro,
        'object': object,
        'enderecoDoador':enderecoDoador,
        'enderecoDonatario':enderecoDonatario
    }
    html_string = render_to_string('relatorios/requerimentoTermoDoacao.html', contexto)
    html = HTML(string=html_string)
    hoje = datetime.datetime.today()
    ano = hoje.year
    mes = hoje.month
    uuid = uuid4().hex
    nome_arquivo = str("docs/{ano}/{mes}/{uuid}.pdf".format(ano=ano, mes=mes, uuid=uuid))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)

    arquivosModel.objects.create(
        content_object=object.doador,
        cliente_id=object.doador.pk,
        tipoArquivo='requerimento',
        nome=str('TERMO DOAÇÃO - {} | {}'
                 .format(object.doador.nome, object.arma.modelo)),
        arquivo=nome_arquivo
    ).save()

def renderizarLaudoPsicologico(pk):
    objeto=laudosPsicologicosModel.objects.get(pk=pk)
    contexto={
        'object':objeto
    }
    html_string=render_to_string('gestao3/laudosPsicologicos/modelo01.html', contexto)
    html=HTML(string=html_string)
    hoje=datetime.datetime.today()
    nome_arquivo=str("laudosPsicologicos{psicologo}-{nome} - {data}.pdf".format(psicologo=objeto.psicologo.nome, nome=objeto.nome, data=hoje ))
    html.write_pdf(settings.MEDIA_ROOT + nome_arquivo)
    with open(settings.MEDIA_ROOT + nome_arquivo, 'r') as f:
        documento = File(f)