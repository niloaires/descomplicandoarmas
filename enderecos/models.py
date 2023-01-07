from django.db import models
from clientes.models import clienteModel
# Create your models here.
class enderecoClienteModel(models.Model):
    cliente=models.ForeignKey(clienteModel, on_delete=models.PROTECT, related_name='enderecos')
    principal=models.BooleanField(default=True)
    logradouro = models.CharField(verbose_name='Logradouro', max_length=200, blank=True, null=False,
                                default='Sem informação')
    estadoMunicipio = models.CharField(verbose_name='Estado e município do endereço', max_length=60, blank=True,
                                       null=False, default='Sem informação')
    cep = models.CharField(verbose_name='CEP', max_length=9, blank=False, null=False)


    def __str__(self):
        return str(self.cliente.nome +' | '+self.logradouro)

    def cepFormatado(self):
        return str("{parte1}-{parte2}".format(parte1=self.cep[:5],
                                              parte2=self.cep[5:8]))
    def enderecoCompleto(self):
        return str("{}, {} - CEP: {}".format(self.logradouro, self.estadoMunicipio, self.cepFormatado()))
    class Meta:
        db_table = 'clientes_enderecoclientemodel'
        verbose_name='Endereço do cliente'
        verbose_name_plural='Endereços de clientes'