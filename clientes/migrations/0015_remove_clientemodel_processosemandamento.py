# Generated by Django 4.0.2 on 2022-05-15 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0014_clientemodel_fotoperfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientemodel',
            name='processosEmAndamento',
        ),
    ]
