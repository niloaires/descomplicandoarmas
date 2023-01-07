from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from clientes.models import clienteModel
# Create your models here.
formaPagamentoChoice=(
    ('pix', 'Pix'),
    ('transferencia', 'Transferência'),
    ('cartao', 'Cartão de Crédito'),
    ('parcelamento', 'Parcelamento sem cartão'),
    ('gru', 'GRU')
)
class registrosFinanceiroModel(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.PROTECT, related_name='registrosFinanceiros')
    descricao=models.CharField(max_length=200, verbose_name='Descrição do registro', blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object=GenericForeignKey('content_type', 'object_id')
    formaPagamento=models.CharField(max_length=20, choices=formaPagamentoChoice, blank=False, null=False, verbose_name='Forma de pagamento')
    codigoBarra=models.CharField(max_length=200, verbose_name='Código de barras', blank=True, null=True)
    valor = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True,
                                verbose_name="Valor do serviço")
    ativo=models.BooleanField(default=True, verbose_name='Registro ativo')
    efetivado=models.BooleanField(default=False, verbose_name='Registro efetivado')
    dataPrevista=models.DateField(blank=False, null=False, verbose_name='Data prevista')
    dataEfetivacao=models.DateField(blank=True, null=True, verbose_name='Data da efetivação')
    dataRegistro=models.DateTimeField(auto_now=True, verbose_name='Data e hora do registro')
    class Meta:
        verbose_name_plural= 'Registros financeiros'
        verbose_name= 'Registro financeiro'
    def __str__(self):
        return str("{} - {} {}".format(self.cliente, self.descricao, self.valor))
    def status(self):
        if self.efetivado is True and self.dataEfetivacao is not None:
            return str("PAGO")
        else:
            return str("PREVISTO")
    def classificacao(self):
        if self.valor < 0:
            return str('Despesa')
        else:
            return str('Receita')

    def save(self, *args, **kwargs):
        if self.dataEfetivacao is None:
            self.efetivado=False
        else:
            self.efetivado=True
        super(registrosFinanceiroModel, self).save(*args, **kwargs)

