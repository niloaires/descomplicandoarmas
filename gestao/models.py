from django.db import models
from django.contrib.auth.models import User
from clientes.models import clienteModel
import datetime
# Create your models here.
class perfilUsuarioModel(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    funcao=models.CharField(max_length=20, blank=False, null=False, default='Colaborador')
    nivelAcesso=models.SmallIntegerField(default=1, verbose_name='Nível de acesso')
    avatar=models.ImageField(verbose_name='Imagem do perfil', upload_to='usuarios')
    class Meta:
        verbose_name = 'Perfil de usuário'
        verbose_name_plural = 'Perfis de usuários'
    def __str__(self):
        return self.usuario.get_full_name()
