# Generated by Django 4.0.2 on 2022-07-16 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0019_clientecurso'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processos', '0006_modelosprocessosmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='novosProcessosModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataRegistro', models.DateTimeField(auto_created=True)),
                ('concluido', models.BooleanField(default=False, verbose_name='Processo concluído')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='processos', to='clientes.clientemodel', verbose_name='Cliente')),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='modelo', to='processos.modelosprocessosmodel', verbose_name='Modelo de processo')),
                ('usuario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Responsável')),
            ],
            options={
                'verbose_name': 'Novo processo',
                'verbose_name_plural': 'Novos processos',
            },
        ),
        migrations.CreateModel(
            name='processosRequisitos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataRegistro', models.DateTimeField(auto_created=True)),
                ('atendido', models.BooleanField(default=False, verbose_name='Requisito Atendido')),
                ('dataAlteracao', models.DateTimeField(blank=True, null=True)),
                ('processo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processos.novosprocessosmodel', verbose_name='Processo')),
                ('requisito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processos.requisitosprocessosmodel', verbose_name='Requisito')),
            ],
        ),
    ]
