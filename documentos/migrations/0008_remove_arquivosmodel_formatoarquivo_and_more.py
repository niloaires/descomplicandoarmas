# Generated by Django 4.0.2 on 2022-05-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0007_arquivosmodel_formatoarquivo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arquivosmodel',
            name='formatoArquivo',
        ),
        migrations.AlterField(
            model_name='arquivosmodel',
            name='nome',
            field=models.CharField(max_length=200, verbose_name='Nome do arquivo'),
        ),
    ]
