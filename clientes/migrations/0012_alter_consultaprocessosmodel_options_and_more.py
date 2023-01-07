# Generated by Django 4.0.2 on 2022-04-03 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_alter_consultaprocessosmodel_consultaativa'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultaprocessosmodel',
            options={'ordering': ['cliente'], 'verbose_name': 'Consulta ao processo', 'verbose_name_plural': 'Consultas a processos'},
        ),
        migrations.RemoveField(
            model_name='consultaprocessosmodel',
            name='dataVerificacao',
        ),
        migrations.AlterField(
            model_name='consultaprocessosmodel',
            name='processo',
            field=models.CharField(max_length=200, verbose_name='Identificação do processo'),
        ),
        migrations.CreateModel(
            name='historicoConsultasProcessosModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição da consulta')),
                ('textoConsulta', models.TextField(blank=True, null=True, verbose_name='Descrição da consulta')),
                ('historicoAtivo', models.BooleanField(default=True, verbose_name='Histórico ativo')),
                ('dataVerificacao', models.DateTimeField(auto_now=True)),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico', to='clientes.consultaprocessosmodel')),
            ],
        ),
    ]
