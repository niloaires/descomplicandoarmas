# Generated by Django 4.0.2 on 2022-06-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0018_alter_clientemodel_estadocivil'),
    ]

    operations = [
        migrations.CreateModel(
            name='clienteCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome completo')),
                ('cpf', models.CharField(max_length=11, verbose_name='Número do CPF')),
                ('telefone', models.CharField(max_length=14, verbose_name='Número de telefone (WhatsApp)')),
                ('endereco', models.TextField(verbose_name='Endereço completo, incluindo CEP')),
            ],
            options={
                'verbose_name': 'Cliente de curso',
                'verbose_name_plural': 'Clientes de cursos',
            },
        ),
    ]