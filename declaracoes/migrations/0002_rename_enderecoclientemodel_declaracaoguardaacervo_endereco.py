# Generated by Django 4.0.2 on 2022-03-04 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('declaracoes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='declaracaoguardaacervo',
            old_name='enderecoClienteModel',
            new_name='endereco',
        ),
    ]
