# Generated by Django 4.0.2 on 2022-05-26 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0016_clientemodel_dataemissao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicoconsultasprocessosmodel',
            name='consulta',
        ),
        migrations.DeleteModel(
            name='consultaProcessosModel',
        ),
        migrations.DeleteModel(
            name='historicoConsultasProcessosModel',
        ),
    ]