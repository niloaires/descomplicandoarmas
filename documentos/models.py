import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime, timedelta
from uuid import uuid4
import datetime
from django.db.models.signals import post_save
# Create your models here.
def local_renomear(instance, filename):
    ano=datetime.datetime.now().year
    mes=datetime.datetime.now().month

    upload_to = 'docs/{ano}/{mes}'.format(ano=ano, mes=mes)
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.uuid, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
tipo_arquivo_choices=(

    ('certidao', 'Certidão'),
    ('comprovante', 'Comprovante'),
    ('declaracao', 'Declaração'),
    ('docPessoal', 'Documentação pessoal'),
    ('requerimento', 'Requerimento')
)
class arquivosModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    cliente_id = models.IntegerField(default=41, blank=False, null=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    nome=models.CharField(max_length=200, verbose_name="Nome do arquivo", blank=False, null=False)
    arquivo=models.FileField(upload_to=local_renomear, blank=True, null=True)
    #formatoArquivo=models.CharField(max_length=5, verbose_name='Nome do Arquivo', default='pdf', blank=True, null=False)
    tipoArquivo=models.CharField(choices=tipo_arquivo_choices, max_length=20, verbose_name="Tipo de arquivo", blank=False, null=False)
    validade=models.DateField(verbose_name="Validade do documento", blank=True, null=True)
    tempoValidade=models.SmallIntegerField(verbose_name="Tempo de validade", blank=True, null=True , default=30)
    dataRegistro=models.DateTimeField(auto_now=True, verbose_name='Data do registro')

    def __str__(self):
        return self.nome
    def formatoArquivo(self):
        arquivo=os.path.splitext(self.arquivo.file.name)
        return str(arquivo[1])
    def save(self, *args, **kwargs):
        if self.validade is None:
            hoje=datetime.datetime.today()
            self.validade=hoje+timedelta(days=90)
        super(arquivosModel, self).save(*args, **kwargs)


"""
def definirExtensao(sender, instance, **kwargs):
    object=arquivosModel.objects.get(pk=instance.pk)
    arquivo=object.arquivo
    nome=os.path.splitext(arquivo.file.name)
    extensao=nome[1]
    object.formatoArquivo=extensao
    object.save()

post_save.connect(definirExtensao, sender=arquivosModel, dispatch_uid="my_unique_identifier")

"""