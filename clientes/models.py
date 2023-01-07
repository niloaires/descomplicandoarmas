from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from documentos.models import arquivosModel
from uuid import uuid4
import os

import datetime
# Create your models here.


SEXO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino")

    )
ESTADOCIVIL_CHOICES = (
        ("C", "Casado"),
        ("D", "Divorciado"),
        ("S", "Solteiro"),
        ("U",  "União estável"),    
        ("V", "Viúvo"),

    )
ESCOLARIDADE_CHOICES = (
        ("FUNDAMENTAL", "Fundamental Completo"),
        ("MEDIO", "Médio Completo"),
        ("SUPERIOR", "Superior Completo")
    )
def local_avatarCliente(instance, filename):
    upload_to = 'fotos_clientes'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(uuid4().hex, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
class clienteModel(models.Model):
    nome=models.CharField(max_length=200, verbose_name='Nome completo', blank=False, null=False)
    nomeMae=models.CharField(max_length=200, verbose_name='Nome da mãe', blank=True, null=True)
    nomePai=models.CharField(max_length=200, verbose_name='Nome do Pai', blank=True, null=True)
    email=models.CharField(max_length=100, verbose_name='Endereço de email', blank=True, null=False)
    fotoPerfil=models.ImageField(verbose_name='Foto do Perfil', upload_to=local_avatarCliente, blank=True, null=True, default='fotos_clientes/semAvatar.png')
    naturalidade = models.CharField(verbose_name='Naturalidade', max_length=60, blank=True,
                                       null=False, default='Sem informação')
    ocupacao = models.CharField(verbose_name='Ocupação', max_length=60, blank=True,
                                       null=False, default='Sem informação')
    genero=models.CharField(verbose_name='Gênero', max_length=1, choices=SEXO_CHOICES, blank=False, null=False, default='M' )
    nascimento=models.DateField(blank=False, null=False, verbose_name='Data de nascimento')
    estadoCivil=models.CharField(verbose_name='Estado civil', max_length=1, choices=ESTADOCIVIL_CHOICES, blank=False, null=False, default='S' )
    escolaridade=models.CharField(verbose_name="Escolaridade", max_length=15, choices=ESCOLARIDADE_CHOICES,  blank=False, null=False, default="medio")
    registroGeral=models.CharField(verbose_name='Número do registro geral', max_length=30, blank=True, null=False, default='Sem informação')
    dataEmissao=models.DateField(blank=True, null=True, verbose_name='Data da emissão do documento')
    cpf=models.CharField(verbose_name='Número do CPF', max_length=14, blank=True, null=False, unique=True)
    cR=models.CharField(verbose_name='CR', max_length=15, blank=True, null=True)
    tituloEleitor=models.CharField(verbose_name='Título de eleitor', max_length=15, blank=True, null=False, default='Sem informação')
    telefone=models.CharField(verbose_name='Número de telefone', max_length=14, blank=True, null=False, default='Não informado')
    senhaAcessoGov=models.CharField(max_length=20, verbose_name="Senha de acesso do acesso.gov", blank=True, null=True, default="Não informado")
    finalizado=models.BooleanField(verbose_name='Cliente sem Pendências', default=False)
    arquivos = GenericRelation(arquivosModel)
    dataRegistro=models.DateField(auto_now_add=True)

    def cpfFormatado(self):
        return str("{parte1}.{parte2}.{parte3}-{parte4}".format(parte1=self.cpf[:3],
                                                                parte2=self.cpf[3:6],
                                                                parte3=self.cpf[6:9],
                                                                parte4=self.cpf[9:11]))
    @property
    def telefone_formatado(self):
        original=str(self.telefone)
        if original is True:
            return str("Não informado")
        else:
            return str("({ddd}) {nonodigito} {parte1}-{parte2}".
                       format(ddd=original[:2],
                              nonodigito=original[2],
                              parte1=original[3:7],
                              parte2=original[7:11]))


    def __str__(self):
        return self.nome

    def montanteFinanceiro(self):
        total=0
        for item in self.registrosFinanceiros.all():
            total+=item.valor
        return total
    def processos(self):
        total=0
        for item in self.processos():
            total+=1
        return total
    def processosEmAndamento(self):
        total=0
        for item in self.processos.filter(concluido=False):
            total+=1
        return total
    def processosFinalizados(self):
        total=0
        for item in self.consulta.filter(consultaAtiva=False):
            total+=1
        return total


    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
        ordering = ['nome', '-dataRegistro']


class clienteCurso(models.Model):
    nome=models.CharField(max_length=200, verbose_name='Nome completo', blank=False, null=False)
    cpf = models.CharField(verbose_name='Número do CPF', max_length=11, blank=False, null=False)
    telefone = models.CharField(verbose_name='Número de telefone (WhatsApp)', max_length=14, blank=False, null=False,
                                )
    endereco=models.TextField(blank=False, verbose_name='Endereço completo, incluindo CEP')


    class Meta:
        verbose_name = 'Cliente de curso'
        verbose_name_plural = 'Clientes de cursos'
    def __str__(self):
        return self.nome