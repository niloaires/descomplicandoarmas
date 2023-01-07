from django.db import models
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from weasyprint import HTML
from enderecos.models import enderecoClienteModel
from clientes.models import clienteModel, clienteCurso
from armas.models import armasClientes
from documentos.models import arquivosModel
import datetime
from django.utils.timezone import now
from django.core.files import File
from uuid import uuid4
import secrets
# Create your models here.
from servicos.managers import *

opcaoSistema=(
    ("EB", "Exército Brasileiro"),
    ("PF", "Polícia Federal"),
)
opcaoFinalidade=(
    ("cacador", "Caçador"),
    ("atirador", "Atirador"),
    ("colecionador", "Colecionador")
)
opcoesStatusServico=(
    ("aguardandopagamento", "Aguardando pagamento"),
    ("iniciado", "Iniciado"),
    ("documentacao", "Juntando documentação"),
    ("protocolado", "Protoloado"),
    ("analise", "Em análise pelo órgão"),
    ("deferido", "Deferido"),
    ("indeferido", "Indeferido"),
)
class exigenciasModel(models.Model):
    descricao=models.CharField(max_length=200, verbose_name="Descrição da exigência")
    ExtensaoArquivo=models.CharField(max_length=5, default="pdf", verbose_name="Extensão do arquivo")
    class Meta:
        verbose_name = 'Exigência'
        verbose_name_plural = 'Exigências'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao
class listaServicos(models.Model):
    nome=models.CharField(max_length=200, verbose_name="Nome do Serviço", blank=False, null=False)
    exigencias = models.ManyToManyField(exigenciasModel, related_name='exigencias')
    vinculoSistema=models.CharField(max_length=3, choices=opcaoSistema, blank=False, null=False)
    valor = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True,
                                verbose_name="Valor do serviço")
    link=models.CharField(blank=False, null=False, max_length=200, verbose_name="Link do sistema", default="#")
    ativo=models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Lista de serviços'
        ordering = ['vinculoSistema', 'nome']
    def __str__(self):
        return self.nome
    def get_abolute_url(self):
        return reverse(self.link)
class servicosModel(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='servicos')
    descricaServico=models.CharField(max_length=200, verbose_name="Descrição", blank=True, null=False, default="Sem descrição")
    tipoServico=models.ForeignKey(listaServicos, on_delete=models.CASCADE, related_name='tipo_servico', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    valor = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True, default=0.00,
                                verbose_name="Valor do serviço")
    adicional = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True, default=0.00,
                                    verbose_name="Valor adicional")
    observacao = models.TextField(blank=True, default="Sem observações")
    arquivos = GenericRelation(arquivosModel)
    servicoAtivo = models.BooleanField(default=True, verbose_name='Serviço ativo')
    dataConclusao = models.DateField(blank=True, null=True, verbose_name='Data de conclusão')
    dataRegistro = models.DateTimeField(auto_now=True)

    objects=ServicosManager()
    def __str__(self):
        return self.cliente.nome
    class Meta:
        verbose_name_plural = 'Serviços'
        verbose_name = 'Serviço'
        ordering = ['cliente', 'dataRegistro']

    def status(self):
        if self.servicoAtivo:
            return "Em andamento"
        else:
            return "Finalizado"

class movimentacoesServico(models.Model):
    servico=models.ForeignKey(servicosModel, on_delete=models.CASCADE, related_name='movimentacoes')
    statusServico = models.CharField(blank=False, choices=opcoesStatusServico, null=False,
                                     default="aguardandopagamento", max_length=30, verbose_name="Status do serviço")
    dataMovimentacao=models.DateField(blank=False, null=False, verbose_name="Data da movimentação")
    dataRegistro=models.DateTimeField(auto_now=True)
    movimentacaoAtiva=models.BooleanField(default=True)
    class Meta:
        ordering=['servico', 'dataMovimentacao']
    
    def __str__(self):
        return self.servico
        hoje= datetime.date.today()
        #ultima_movimentacao=datetime.date(self.dataMovimentacao)
        #hoje=datetime.date(self.dataMovimentacao)
        diferenca=(hoje-self.dataMovimentacao)
        return int(diferenca.days)

class pagamentosServico(models.Model):
    servico=models.ForeignKey(servicosModel, on_delete=models.PROTECT, related_name='pagamentos')
    dataPagamento=models.DateField(default=now, blank=False, null=False, verbose_name="Data do pagamento")
    formaPagamento=models.CharField(default="Pix", verbose_name="Forma de pagamento", max_length=100, blank=False, null=False)
    valorPago = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True,
                                verbose_name="Valor pago")
    confirmado=models.BooleanField(default=True)




class transferenciaSigmaSigma(models.Model):
    alienante=models.ForeignKey(clienteModel,verbose_name='Alienante (vendedor)',  on_delete=models.PROTECT, related_name="alienante_transferencia")
    adquirente=models.ForeignKey(clienteModel, verbose_name='Adquirente (comprador)', on_delete=models.PROTECT,  related_name="adquirente_transferencia")
    responsavel=models.ForeignKey(clienteModel,verbose_name='Responsável pela transferênia',  on_delete=models.PROTECT,  related_name="responsavel_transferencia")
    servico = GenericRelation(servicosModel)
    arma=models.ForeignKey(armasClientes, on_delete=models.PROTECT)
    local=models.CharField(max_length=150, blank=False, null=False, default="São Luís - MA")
    dataRegistro=models.DateField(auto_now=True)
    dataDeferimento=models.DateField(blank=True, null=True)
    deferido=models.BooleanField(default=False)


    def __str__(self):
        return str(self.responsavel)
class transferenciaSinarmSigma(models.Model):
    alienante=models.ForeignKey(clienteModel, on_delete=models.PROTECT, related_name="alienante_transferencia_sinarm_sigma")
    adquirente=models.ForeignKey(clienteModel, on_delete=models.PROTECT,  related_name="adquirente_transferencia_sinarm_sigma")
    responsavel=models.ForeignKey(clienteModel, on_delete=models.PROTECT,  related_name="responsavel_transferencia_sinarm_sigma")
    servico = GenericRelation(servicosModel)
    arma=models.ForeignKey(armasClientes, on_delete=models.PROTECT)
    local=models.CharField(max_length=150, blank=False, null=False, default="São Luís - MA")
    dataRegistro=models.DateField(auto_now=True)
    dataDeferimento=models.DateField(blank=True, null=True)
    deferido=models.BooleanField(default=False)


    def __str__(self):
        return str(self.responsavel)
class registroCR(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.PROTECT, related_name='registro_CR')
    clube=models.CharField(verbose_name="Clube a filiar", default="CLAM", max_length=200, blank=False, null=False)
    servico = GenericRelation(servicosModel)

    dataRegistro = models.DateField(auto_now=True)
    dataDeferimento = models.DateField(blank=True, null=True)
    deferido = models.BooleanField(default=False)
    def get_abolute_url(self):
        return reverse('gestao:servicos:requerimento-registro-cr', kwargs={'pk':self.pk})
    def __str__(self):
        return self.cliente.nome


class emissaoGuiaTrafego(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='emissao_gt')
    servico=GenericRelation(servicosModel)
    arma=models.ForeignKey(armasClientes, on_delete=models.CASCADE, related_name='emissao_gt')
    municoesLote=models.CharField(verbose_name="Lote da munição", max_length=100, blank=True, null=True)
    municoes=models.CharField(verbose_name="Espeficicações da munição" ,max_length=100, blank=True, null=True)
    municoesQuantidade=models.SmallIntegerField(default=0, verbose_name="Quantidadede de Munições")
    dataRegistro = models.DateField(auto_now=True)
    dataDeferimento = models.DateField(blank=True, null=True)
    deferido = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Emissão de Guia de tráfego'
    def get_abolute_url(self):
        return reverse('gestao-servicos-emissao-gt-ver', kwargs={'pk':self.pk})

class aquisicaoPCE(models.Model):

    cliente = models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='aquisicaoPCE')
    servico = GenericRelation(servicosModel, on_delete=models.CASCADE)
    finalidade = models.CharField(max_length=20, verbose_name="Finalidade da aquisição",
                                  choices=opcaoFinalidade, blank=False, null=False, default="atirador")

    dadosTecnicos=models.CharField(max_length=200,verbose_name="Dados técnicos esclarecedores do acessório", blank=True, null=True, default="Sem informações")
    fornecedor=models.CharField(max_length=50, blank=False, null=False, verbose_name="Fornecedor")
    cR=models.CharField(max_length=15, blank=False, null=False, verbose_name="CR do fornecedor")
    anexos=models.CharField(max_length=200, blank=True, null=True, verbose_name="Anexos")
    outrasInformacoes=models.CharField(max_length=200, blank=True, null=True, verbose_name="Outras informações")
    local=models.CharField(max_length=100, default="São Luís - MA", blank=True, null=False)
    dataRegistro=models.DateField(auto_now=True)
    def get_abolute_url(self):
        return reverse('gestao-servicos-requerimento-pce-ver', kwargs={'pk':self.pk})
    def __str__(self):
        return str("Processo físico de aquisição de PCE {}".format(self.cliente.nome))

class armaseAcessorios(models.Model):
    processo=models.ForeignKey(aquisicaoPCE, on_delete=models.CASCADE, related_name='armaseAcessorios')
    tipo=models.CharField(max_length=100, verbose_name="Tipo", blank=False, null=False)
    calibre=models.CharField(max_length=100, verbose_name="Calibre", blank=False, null=False)
    marcaModelo=models.CharField(max_length=100, verbose_name="Marca/Modelo", blank=False, null=False)
    quantidade=models.SmallIntegerField(default=1, verbose_name="Quantidade", null=False, blank=False)
opcoesObjeto=(
    ('concessao', 'Concessão de registro'),
    ('revalidacao', 'Revalidação de registro'),
    ('apostilamento', 'Apostilamento ao registro'),
    ('segundavia', '2ª via do registro'),
    ('cancelamento', 'Cancelamento de registro'),
    ('outros', 'Outros'),
)
opcoesAtividade=(
    ('atirador', 'TIRO DESPORTIVO'),
    ('cacador', 'CAÇA'),
    ('colecionador', 'COLECIONAMENTO'),
    ('aquisicaoAcessorios', 'AQUISIÇÃO DE ACESSÓRIOS DE ARMA DE FOGO PARA TIRO DESPORTIVO/ ENDTIDADE DE TIRO DESPORTIVO / CAÇA'),
)
class apostilamentosExercito(models.Model):
    cliente = models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='apostilamentos')
    #servico = GenericRelation(servicosModel)
    rM=models.CharField(max_length=5, verbose_name='Região Militar', blank=False, null=False, default="8ª")
    objeto=models.CharField(max_length=200, choices=opcoesObjeto, verbose_name='Objeto de apostilamento', blank=False, null=False)
    atividade=models.CharField(max_length=20, verbose_name='Atividade', blank=False, null=False, choices=opcoesAtividade)
    apostilamento=models.CharField(max_length=200, verbose_name='Apostilamento', blank=False, null=False)
    outrasInformacoes=models.TextField(verbose_name='Outras informações', blank=True, null=True)
    anexos = models.TextField(verbose_name='Anexos', blank=False, null=False)
    dataRegistro = models.DateField(auto_now=True)
opcoesObjetoSisgCorp=(
    ('Registro CR', 'Concessão de registro CR'),
    ('Autorização de compra', 'Autorização de Aquisição de PCE'),
    ('Registro PCE', 'Apostilamento e Registro do PCE'),
    ('Guia de tráfego PCE', 'Emissão de Guia de Tráfego do PCE'),
)
class itensRequerimentoApostilamento(models.Model):
    apostilamento=models.ForeignKey(apostilamentosExercito, on_delete=models.CASCADE, related_name='itens')
    tipo=models.CharField(max_length=100, verbose_name='Tipo', blank=False, null=False)
    marcaModelo=models.CharField(max_length=100, verbose_name='Marca/Modelo', blank=False, null=False)
    quantidade=models.SmallIntegerField(verbose_name='Quantidade', default=1)
    fornecedor=models.CharField(max_length=100, verbose_name='Fornecedor', blank=False, null=False)
    crfornecedor=models.CharField(max_length=20, verbose_name='CR do Fornecedor', blank=False, null=False)
    notaFiscalData=models.CharField(max_length=30, verbose_name='Nota fiscal | data', blank=False, null=False)
    atorizacaoData=models.CharField(max_length=30, verbose_name='Autorização | data', blank=False, null=False)
    #
    class Meta:
        verbose_name= 'Item de requerimento de apostilamento'
        verbose_name_plural= 'Itens de requerimento de apostilamento'
    def __str__(self):
        return str("{} - {}".format(self.tipo, self.apostilamento.cliente))
class cumprimentoExigenciasModel(models.Model):
    servico=models.ForeignKey(servicosModel, on_delete=models.CASCADE, related_name='cumprimento_exigencias_servico')
    exigencia=models.ForeignKey(exigenciasModel, on_delete=models.CASCADE, related_name='cumprimento_exigencias')
    cumprida=models.BooleanField(default=False)
    dataRegistro=models.DateField(auto_now=True)
    def __str__(self):
        return self.exigencia.descricao

class servicosSisgcorpModel(models.Model):
    servico = GenericRelation(servicosModel)
    cliente=models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='servicos_sisgcorp', verbose_name='Cliente')
    objeto=models.CharField(max_length=30, verbose_name='Objeto do serviço', choices=opcoesObjetoSisgCorp, blank=False, null=False)
    pce=models.ForeignKey(armasClientes, on_delete=models.CASCADE, blank=True, null=True, related_name='servicos_sisgcorp')
    gru=models.CharField(max_length=60, verbose_name='Código de barrras GRU', blank=False, null=False)
    ativo=models.BooleanField(default=True)
    dataInicio=models.DateField(blank=False, null=False, verbose_name='Data de início do processo')
    dataRegistro = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Serviços SISGCRP'
        verbose_name = 'Serviço SISGCRP'
    def __str__(self):
        return str("{} - {}".format(self.get_objeto_display(), self.cliente.nome ))

class andamentoServicosSisgCorpModel(models.Model):
    referencia=models.ForeignKey(servicosSisgcorpModel, on_delete=models.CASCADE, related_name='andamento')
    statusServico = models.CharField(max_length=20, verbose_name='Status atual do serviço', choices=opcoesStatusServico,
                                     blank=False, null=False)
    ativo = models.BooleanField(default=True)
    dataRegistro = models.DateField(auto_now=True)
TIPO_REQUERIMENTO_CHOICE= (
        ("sinarmsigma", "TRANSFERÊNCIA DO SINARM PARA O SIGMA"),
        ("sigmasinarm", "TRANSFERÊNCIA DO SIGMA PARA O SINARM"),
        ("reimpressao", "REIMPRESSÃO DE CRAF"),
        ("portefuncional", "PORTE FUNCIONAL"),
        ("outros", "OUTROS")
    )
PORTE_CHOICE= (
        ("defesa", "Defesa Pessoal"),
        ("seguranca", "Segurança de Diginatários"),
        ("funcionar", "Funcional"),
        ("cacacor", "Caçador de subsisistência"),
    )
class requerimentosFisicosSinarm(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.PROTECT)
    tipoRequerimento=models.CharField(max_length=20, choices=TIPO_REQUERIMENTO_CHOICE, verbose_name='Objetivo do requerimento', blank=False, null=False)
    especificacoes=models.CharField(max_length=200, verbose_name='Especificações', blank=True, null=True)
    arma=models.ForeignKey(armasClientes, on_delete=models.PROTECT)
    opcaoPorte = models.CharField(max_length=20, choices=PORTE_CHOICE,
                                        verbose_name='Opções de Porte', blank=True, null=True)
    empresa=models.CharField(max_length=200, blank=False, null=False, verbose_name='Empresa/Órgão de trabalho')
    cnpj=models.CharField(max_length=20, blank=False, null=False, verbose_name='CNPJ')
    enderecoCcomercial=models.CharField(max_length=200, blank=False, null=False, verbose_name='Endereço comercial')
    bairro=models.CharField(max_length=50, blank=False, null=False, verbose_name='Distrito/Bairro')
    municipio=models.CharField(max_length=70, blank=False, null=False, verbose_name='Município')
    uf=models.CharField(max_length=2, blank=False, null=False, verbose_name='Estado')
    cep=models.CharField(max_length=9, blank=False, null=False, verbose_name='CEP')
    telefoneComercial=models.CharField(max_length=15, blank=False, null=False, verbose_name='Telefone Comercial')
    dataRegistro=models.DateTimeField(auto_now=True)

class renovacaoCRAF(models.Model):
    cliente = models.ForeignKey(clienteModel, on_delete=models.PROTECT)
    endereco=models.ForeignKey(enderecoClienteModel, on_delete=models.PROTECT)
    arma=models.ForeignKey(armasClientes, on_delete=models.PROTECT, related_name='renovacaoCRAFSIGMA')
    localRequerimento=models.CharField(max_length=200, verbose_name='Local de solicitação', default='São Luís - MA', blank=True, null=False)
    dataRegistro = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Requerimento renovação CRAF/SIGMA'
        verbose_name_plural = 'Requerimentos renovações CRAF/SIGMA'

class termoDoacaoModel(models.Model):
    doador = models.ForeignKey(clienteModel,  verbose_name='Doador', on_delete=models.PROTECT,
                               related_name='doadorTermoDoacao')
    donatario = models.ForeignKey(clienteModel,  verbose_name='Donatário', on_delete=models.PROTECT,
                                  related_name='donatarioTermoDoacao')
    arma = models.ForeignKey(armasClientes, on_delete=models.PROTECT, related_name='termoDoacao')
    localRequerimento = models.CharField(max_length=200, verbose_name='Local de solicitação', default='São Luís - MA',
                                         blank=True, null=False)
    dataRegistro = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Termo de doação'
        verbose_name_plural = 'Termos de Doação'
        ordering = ['dataRegistro', 'doador', 'donatario']
class cursosModel(models.Model):
    titulo=models.CharField(max_length=200, verbose_name='Título do curso')
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    def __str__(self):
        return self.titulo
def gerarCodigo(bytes):
    codigo=secrets.token_bytes(nbytes=bytes)
    return str(codigo)
class clientesCursosModel(models.Model):
    cliente=models.ForeignKey(clienteCurso, on_delete=models.PROTECT)
    curso = models.ForeignKey(cursosModel, on_delete=models.PROTECT)
    codigo=models.CharField(unique=True, blank=True, max_length=15, verbose_name='Código da matrícula')
    matriculado=models.BooleanField(default=False)
    dataRegistro = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Cliente por curso'
        verbose_name_plural = 'Clientes por cursos'
        ordering = ['dataRegistro', 'cliente']
    def save(self, *args, **kwargs):
        if not self.id:
            self.codigo=secrets.token_hex(nbytes=6)
        super(clientesCursosModel, self).save(*args, **kwargs)

    def __str__(self):
        return str("{} - {}".format(self.cliente.nome, self.curso.titulo))

@receiver(post_save, sender=registroCR)
def declaracoesUnificadasGerarArquivo(sender, instance, created, **kwargs):
    if created:
        object = registroCR.objects.get(pk=instance.pk)
        cliente = clienteModel.objects.get(pk=object.cliente.pk)
        endereco = enderecoClienteModel.objects.filter(principal=True, cliente=cliente).first()

        hoje = datetime.date.today()
        contexto = {
            'cliente': cliente,
            'endereco': endereco,
            'data': str("{dia} de {mes} de {ano}".format(dia=hoje.strftime('%d'),
                                                         mes=hoje.strftime('%B'),
                                                         ano=hoje.strftime('%Y'))),
            'hoje': hoje
        }
        html_string = render_to_string('relatorios/declaracoes_unificadas.html', contexto)
        html = HTML(string=html_string)
        ano = hoje.year
        mes = hoje.month
        nome_arquivo=uuid4().hex
        resultado = html.write_pdf('media/docs/{}/{}/{}.pdf'.format(ano, mes, nome_arquivo))



        #Registrar nos DOcumentos



        with open('media/docs/{}/{}/{}.pdf'.format(ano, mes, nome_arquivo), 'r') as f:
            documento=File(f)

        arquivosModel.objects.create(
            content_object=cliente,
            tipoArquivo='declaracao',
            nome=str('DECLARAÇÕES CR {}'.format(cliente.nome)),
            arquivo=documento.file.name
        ).save()

#Criar primeira movimentação do serviço
@receiver(post_save, sender=servicosModel)
def registrarMovimentacaoInicial(sender, instance, created, **kwargs):
    if created:
        servico=servicosModel.objects.get(pk=instance.pk)
        movimentacoesServico.objects.create(
            servico=servico,
            statusServico='aguardandopagamento',
            dataMovimentacao=datetime.datetime.today()
        ).save()


@receiver(post_save, sender=servicosSisgcorpModel)
def registarAndamentoServico(sender, instance, created, **kwargs):
    if created:
        objeto=servicosSisgcorpModel.objects.get(pk=instance.pk)
        andamentoServicosSisgCorpModel.objects.create(
            referencia=objeto,
            statusServico='aguardandopagamento',

        ).save()