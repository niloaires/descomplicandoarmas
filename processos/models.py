import datetime
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from clientes.models import clienteModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from documentos.models import arquivosModel


class requisitosProcessosModel(models.Model):
    titulo=models.CharField(verbose_name='Título do requisito', max_length=200, blank=False, null=False)
    descricao=models.TextField(verbose_name='Descrição do requisito', blank=False, null=False)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Requisito processual'
        verbose_name_plural = 'Requisitos processuais'
SISTEMA_OPCOES = (
        ("SIGMA", "SIGMA - EB"),
        ("SINARM", "SINARM - PF"),
        ("OUTROS", "Outros..")
    )
class modelosProcessosModel(models.Model):
    titulo=models.CharField(verbose_name='Modelo de Projeto', max_length=100, blank=False, null=False)
    sistemVinculado=models.CharField(verbose_name='Sistema Vinculado',max_length=10,
                                     choices=SISTEMA_OPCOES, blank=False, null=False)
    requisitos=models.ManyToManyField(requisitosProcessosModel)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Modelo de processo'
        verbose_name_plural = 'Modelo de processos'
        ordering  = ['titulo', 'sistemVinculado']
class novosProcessosModel(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='Responsável')
    cliente=models.ForeignKey(clienteModel, verbose_name='Cliente', on_delete=models.CASCADE, related_name='processos')
    modelo=models.ForeignKey(modelosProcessosModel, verbose_name='Modelo de processo', on_delete=models.PROTECT,
                             related_name='modelo')
    nivelPrioridade=models.SmallIntegerField(verbose_name='Nível de prioridade', default=3, validators=[MaxValueValidator(10), MinValueValidator(1)])
    dataRegistro=models.DateTimeField(auto_now=True)
    ultimaMovimentacao=models.DateTimeField(blank=True, null=True)
    dataPrevistaDeferimento=models.DateField(blank=True, null=True)
    concluido=models.BooleanField(verbose_name='Processo concluído', default=False)
    def totalRequisitos(self):
        return self.modelo.requisitos.all().count()
    def percentualConclusao(self):
        nRequisitos=self.modelo.requisitos.all().count()
        natendidos=self.processosrequisitos_set.filter(atendido=True).count()
        total=(natendidos/nRequisitos)*100
        return int(total)
    def requisitosPendentes(self):
        return self.processosrequisitos_set.filter(atendido=False).count()
    def statusAtual(self):
        if self.percentualConclusao() is 0:
            return 'Iniciado'
        elif self.percentualConclusao() is 100:
            return 'Finalizado'
        else:
            return 'Andamento'
    def __str__(self):
        return self.modelo.titulo



    def get_absolute_url(self):
        return reverse('gestao:processos:detalhar', args=[str(self.pk)])
    class Meta:
        verbose_name = 'Novo processo'
        verbose_name_plural = 'Novos processos'


class processosRequisitos(models.Model):
    processo=models.ForeignKey(novosProcessosModel, on_delete=models.CASCADE, verbose_name='processo')
    requisito=models.ForeignKey(requisitosProcessosModel, on_delete=models.CASCADE, verbose_name='requisito')
    atendido=models.BooleanField(default=False, verbose_name='Requisito Atendido')
    dataRegistro = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str("{} | {} | {}".format(self.processo.cliente.nome, self.requisito.titulo, self.atendido))
    class Meta:
        verbose_name = 'Requisito no processo'
        verbose_name_plural = 'Requisitos nos processos'

class historicoProcessos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='Responsável')
    processo = models.ForeignKey(novosProcessosModel, on_delete=models.CASCADE, verbose_name='processo')
    historico=models.TextField(blank=False, null=False, verbose_name='Histórico')
    dataRegistro = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str("{} - {} | {}".format(self.processo.modelo.titulo, self.processo.cliente.nome, self.dataRegistro))
    class Meta:
        verbose_name = 'Histórico de processo'
        verbose_name_plural = 'Históricos de processos'

class anotacoesProcessosModel(models.Model):
    processo=models.ForeignKey(novosProcessosModel, on_delete=models.CASCADE, related_name='anotacoes_processos')
    anotacao=models.TextField(blank=False, null=False, verbose_name='Anotação')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='Responsável')
    dataRegistro=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str('{} - {}'.format(self.processo, self.anotacao))
    class Meta:
        verbose_name = 'Anotação de processo'
        verbose_name_plural = 'Anotações de processos'

class ProcessosModel(models.Model):
    cliente = models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='consulta')
    processo=models.CharField(max_length=200, blank=False, null=False, verbose_name='Identificação do processo')
    protocolo=models.CharField(max_length=200, blank=True, null=True, verbose_name='Protocolo')
    sistemaVinculado=models.CharField(max_length=10,choices=SISTEMA_OPCOES, blank=False, null=False, verbose_name='Sistema vinculado')
    descricao=models.TextField(verbose_name='Descrição da consulta')
    consultaAtiva=models.BooleanField(default=True, verbose_name='Consulta Ativa')
    dataVerificacao=models.DateTimeField(blank=True, null=True, verbose_name='Data e hora da última verificação')
    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        ordering = ['cliente', 'dataVerificacao']
    def __str__(self):
        return str("{} - {}".format(self.cliente, self.processo))


class historicoProcessosModel(models.Model):
    consulta=models.ForeignKey(ProcessosModel, on_delete=models.CASCADE, related_name='historico')
    usuario=models.ForeignKey(User, on_delete=models.CASCADE, related_name='historicosProcessos')
    descricao = models.CharField(max_length=200, blank=False, null=False, verbose_name='Descrição da consulta')
    textoConsulta = models.TextField(verbose_name='Texto da consulta', blank=True, null=True)
    historicoAtivo = models.BooleanField(default=True, verbose_name='Histórico ativo')
    dataVerificacao = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.descricao
    def responsavel(self):
        return self.usuario.perfil
escala_prioridade_choices=(
    (1, 'Baixa'),
    (2, 'Média'),
    (3, 'Alta')
)

class pendenciasModels(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE, related_name='pendendias', default=1, blank=True)
    #processo=models.ForeignKey(ProcessosModel, on_delete=models.CASCADE, related_name='processosPendencias')
    cliente=models.ForeignKey(clienteModel, on_delete=models.CASCADE, related_name='pendencias')
    descricao=models.CharField(max_length=200, blank=False, null=False, verbose_name='Identificação da pendência')
    textoPendencia=models.TextField(blank=True, null=True, verbose_name='Detalhamento da pendência')
    statusPendencia=models.BooleanField(default=False, verbose_name='Realizado')
    escalaPrioridade=models.SmallIntegerField( verbose_name='Escala de prioridade', default=2, choices=escala_prioridade_choices)
    dataRegistro=models.DateTimeField(auto_now=True)
    dataLimite=models.DateTimeField(blank=True, null=True, verbose_name='Data Limite ou Vencimento')
    dataConclusao=models.DateTimeField(blank=True, null=True, verbose_name='Data da conclusão')

    class Meta:
        verbose_name_plural = 'Pendências'
        verbose_name = 'Pendência'
        ordering = ['escalaPrioridade', 'dataRegistro']

    def prazo(self):
        concluida=self.statusPendencia
        if concluida is True:
                if self.dataConclusao is None:
                    return str("Data do finalização não informada")
                else:
                    return str("Finalizada em {}".format(self.dataConclusao))
        else:
            if self.dataLimite is None:
                return str("Prazo limite não definido")
            else:
                return str("Prazo limite {}".format(self.dataLimite))
    def __str__(self):
        return str("{} -{}".format(self.cliente.nome, self.descricao))

@receiver(post_save, sender=historicoProcessos)
def atualizarUltimaMovimentacao(sender, instance, **kwargs):
    agora=datetime.datetime.now()
    object=instance.processo
    object.ultimaMovimentacao=agora
    object.save()

@receiver(post_save, sender=novosProcessosModel)
def registrarPendencias(sender, instance, created, **kwargs):
    if created:
        objeto=novosProcessosModel.objects.latest('pk')
        for item in objeto.modelo.requisitos.all():
            processosRequisitos.objects.create(
                processo=objeto,
                requisito=item
            )
        historicoProcessos.objects.create(
            processo=objeto,
            historico='Processo iniciado'
        )

@receiver(post_save, sender=processosRequisitos)
def atualizarStatusProcesso(sender, instance, **kwargs):
    objeto=instance.processo
    if objeto.requisitosPendentes() == 0:
        objeto.concluido=True
        objeto.save()
