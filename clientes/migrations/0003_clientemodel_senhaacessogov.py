# Generated by Django 4.0.2 on 2022-02-17 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_clientemodel_options_alter_clientemodel_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientemodel',
            name='senhaAcessoGov',
            field=models.CharField(blank=True, default='Não informado', max_length=20, null=True, verbose_name='Senha de acesso do acesso.gov'),
        ),
    ]