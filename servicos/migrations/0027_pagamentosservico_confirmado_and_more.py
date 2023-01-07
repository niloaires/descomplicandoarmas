# Generated by Django 4.0.2 on 2022-02-20 23:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0026_pagamentosservico_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamentosservico',
            name='confirmado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pagamentosservico',
            name='dataPagamento',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data do pagamento'),
        ),
    ]
