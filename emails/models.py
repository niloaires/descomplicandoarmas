from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import hashlib

# Create your models here.
class virtual_domains(models.Model):
    name=models.CharField(max_length=50, null=False, blank=False, db_column='name')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'virtual_domains'
        verbose_name='Domínio virtual'
        verbose_name_plural='Domínios virtuais'


class virtual_users(models.Model):
    domain_id=models.ForeignKey(virtual_domains, on_delete=models.CASCADE, db_column='domain_id')
    password=models.CharField(max_length=250, null=True, blank=True, db_column='password')
    email=models.CharField(max_length=100, null=False, blank=False, db_column='email')
    def save(self, *args, **kwargs):

        self.password=hashlib.sha512(self.password.encode()).hexdigest()
        super().save(virtual_users, *args, **kwargs)
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'virtual_users'
        verbose_name='Usuário virtual'
        verbose_name_plural='Usuários virtuais'
class virtual_aliases(models.Model):
    domain_id=models.ForeignKey(virtual_domains, on_delete=models.CASCADE, db_column='domain_id')
    source=models.CharField(max_length=100, null=False, blank=False, db_column='source')
    destination=models.CharField(max_length=100, null=False, blank=False, db_column='destination')
    class Meta:
        db_table = 'virtual_aliases'
        verbose_name='Atalho virtual'
        verbose_name_plural='Atalhos virtuais'

@receiver(post_save, sender=virtual_users)
def criar_alias(sender, instance, created, **kwargs):
    if created:
        usuario=virtual_users.objects.get(pk=instance.pk)
        virtual_aliases.objects.create(
            domain_id=usuario.domain_id,
            source=usuario.email,
            destination=usuario.email
        )
@receiver(post_delete, sender=virtual_users)
def deletar_alias(sender, instance, **kwargs):

    virtual_aliases.objects.filter(source=instance.email).delete()