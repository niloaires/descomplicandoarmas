from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from clientes.models import clienteModel
from enderecos.models import enderecoClienteModel
from documentos.models import arquivosModel
import datetime
# Create your models here.
class declaracaoGuardaAcervo(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='declaracaoGuardaAcervo')
    endereco=models.ForeignKey(enderecoClienteModel, on_delete=models.CASCADE)
    dataRegistro=models.DateField(auto_now=True)
    dataValidade=models.DateField(blank=True, null=True)
    arquivos = GenericRelation(arquivosModel, related_name='declaracaoGuardaAcervo')
    local=models.CharField(max_length=200, verbose_name='Local', default="São Luís, MA")
    def save(self, *args, **kwargs):
        self.dataValidade=(datetime.datetime.today()+datetime.timedelta(days=90))
        super(declaracaoGuardaAcervo, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Declarações de guarda de acervo'
        verbose_name = 'Declaração de guarda de acervo'

class declaracoesDiversas(models.Model):
    cliente = models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='declaracoesDiversas')
    titulo=models.CharField(verbose_name='Título', blank=False, null=False, max_length=200)
    destinatario=models.CharField(verbose_name='Destinatário', blank=False, null=False, max_length=200)
    texto=models.TextField(blank=False, null=False, verbose_name='Texto')
    local = models.CharField(max_length=200, verbose_name='Local', default="São Luís - MA")
    dataRegistro = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Declarações diversas'
        verbose_name = 'Declaração diversa'

    def __str__(self):
        return str("self.cliente.nome + self.titulo")

class declarcoesResidencia(models.Model):
    nomeDeclarante=models.CharField(max_length=200, verbose_name='Nome do declarante', blank=False, null=False)
    rG = models.CharField(verbose_name='Número do RG do declarante', max_length=40, blank=True, null=False, unique=False)
    cpf = models.CharField(verbose_name='Número do CPF do declarante', max_length=14, blank=True, null=False, unique=False)
    cliente=models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='declaracaoResidencia')
    logradouro = models.CharField(verbose_name='Logradouro', max_length=200, blank=True, null=False,
                                  default='Sem informação')
    estadoMunicipio = models.CharField(verbose_name='Estado e município do endereço', max_length=60, blank=True,
                                       null=False, default='Sem informação')
    cep = models.CharField(verbose_name='CEP', max_length=9, blank=False, null=False)
    dataRegistro = models.DateField(auto_now=True)


    def cpfFormatado(self):
        return str("{parte1}.{parte2}.{parte3}-{parte4}".format(parte1=self.cpf[:3],
                                                                parte2=self.cpf[3:6],
                                                                parte3=self.cpf[6:9],
                                                                parte4=self.cpf[9:11]))
    def cepFormatado(self):
        return str("{parte1}-{parte2}".format(parte1=self.cep[:5],
                                              parte2=self.cep[5:8]))
    def enderecoCompleto(self):
        return str("{}, {} - CEP: {}".format(self.logradouro, self.estadoMunicipio, self.cepFormatado()))

    def __str__(self):
        return str("{} - {} - {}".format(self.cliente.nome, self.enderecoCompleto(), self.nomeDeclarante))