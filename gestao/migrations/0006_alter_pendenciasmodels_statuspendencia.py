# Generated by Django 4.0.2 on 2022-04-25 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0005_alter_pendenciasmodels_dataconclusao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendenciasmodels',
            name='statusPendencia',
            field=models.BooleanField(default=False, verbose_name='Realizado'),
        ),
    ]
