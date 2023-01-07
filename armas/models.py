from django.db import models
from clientes.models import clienteModel
# Create your models here.
choices_sistemas=(
    ("SIGMA", "SIGMA"),
    ("SINARM", "SINARM")
)
class armasClientes(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.PROTECT, related_name='armas')
    funcionamento=models.CharField(max_length=100, verbose_name="Tipo de funcionamento",
                                   blank=False, null=False, default="Semi automática")
    numeroCanos=models.SmallIntegerField(verbose_name="Número de canos", blank=False, null=False, default=1)
    tamanhoCano=models.DecimalField(max_digits=13, decimal_places=2, verbose_name="Tamanho em milímetro", blank=False, null=False, default=80.0)
    capacidadeCarregador=models.SmallIntegerField(verbose_name="Capacidade do carregador", blank=False, null=False, default=15)
    raias=models.SmallIntegerField(verbose_name="Número de raias", default=6, blank=False, null=False)
    almaCano=models.CharField(max_length=20, verbose_name="Alma do cano", default="Raidada", blank=False, null=False)
    sentidoRaias=models.CharField(max_length=20, verbose_name="Sentido das raias", default="A direita", blank=False, null=False)
    tipo=models.CharField(max_length=100, blank=False, null=False, verbose_name='Tipo')
    marca=models.CharField(max_length=100, blank=False, null=False, verbose_name='Marca')
    modelo=models.CharField(max_length=100, blank=False, null=False, verbose_name='Modelo')
    calibre=models.CharField(max_length=100, blank=False, null=False, verbose_name='Calibre')
    sistemaVinculado=models.CharField(max_length=100,choices=choices_sistemas, blank=False, null=False, verbose_name='Sistema vinculado')
    paisFabricacao=models.CharField(max_length=30, verbose_name='País de fabricação', blank=False, null=False, default='Brasil')
    numeroSerie=models.CharField(max_length=100, blank=False, null=False, verbose_name='Número de série')
    numeroSistema=models.CharField(max_length=100, blank=False, null=False, verbose_name='Número de registro no sistema')
    numeroRegistro=models.CharField(max_length=100, blank=True, null=True, verbose_name='Número de registro no (SINARM)')
    orgaoExpedidor=models.CharField(max_length=100, blank=True, null=True, verbose_name='Órgão expedidor (SINARM)')
    dataRegistro=models.DateField(blank=True, null=True, verbose_name='Data do registro')
    especificacoes=models.CharField(max_length=100, blank=False, null=False, default="06 raias à direita", verbose_name='Especificações')
    acessorios=models.CharField(max_length=100, blank=False, null=False, default="Não possui", verbose_name='Acessórios')
    acabamento=models.CharField(max_length=100, blank=False, null=False, verbose_name='Acabamento')
    mudancaPropriedade=models.BooleanField(default=False, verbose_name='Em processo de mudança de propriedade')
    def idenfificacao(self):
        return str("{} - {}".format(self.tipo, self.calibre))
    def __str__(self):
        return str(self.cliente.nome+' | '+self.modelo +' - '+ self.marca +' - '+ self.numeroSerie)
    def cano(self):
        return str("{} mm".format(self.tamanhoCano))
    def capacidade(self):
        return str("{} + 1".format(self.capacidadeCarregador))
    class Meta:
        verbose_name = 'Arma'
        verbose_name_plural = 'Armas'
        ordering = ['cliente', 'pk']