# Generated by Django 4.0.2 on 2022-02-14 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clienteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome completo')),
                ('email', models.CharField(blank=True, max_length=100, verbose_name='Endereço de email')),
                ('naturalidade', models.CharField(blank=True, default='Sem informação', max_length=60, verbose_name='Naturalidade')),
                ('ocupacao', models.CharField(blank=True, default='Sem informação', max_length=60, verbose_name='Ocupação')),
                ('genero', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')], default='M', max_length=1, verbose_name='Gênero')),
                ('nascimento', models.DateField(verbose_name='Data de nascimento')),
                ('estadoCivil', models.CharField(choices=[('S', 'Solteiro'), ('C', 'Casado'), ('V', 'Viúvo'), ('D', 'Divorciado')], default='S', max_length=1, verbose_name='Estado civil')),
                ('registroGeral', models.CharField(blank=True, default='Sem informação', max_length=30, verbose_name='Número do registro geral')),
                ('cpf', models.CharField(blank=True, default='00000000000', max_length=11, verbose_name='Número do CPF')),
                ('cR', models.CharField(blank=True, max_length=15, null=True, verbose_name='CR')),
                ('tituloEleitor', models.CharField(blank=True, default='-', max_length=12, verbose_name='Título de eleitor')),
                ('telefone', models.CharField(blank=True, default='Não informado', max_length=14, verbose_name='Número de telefone')),
                ('dataRegistro', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]
