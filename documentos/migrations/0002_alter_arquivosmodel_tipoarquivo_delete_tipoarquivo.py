# Generated by Django 4.0.2 on 2022-02-24 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivosmodel',
            name='tipoArquivo',
            field=models.CharField(choices=[('certidao', 'Certidão'), ('comprovante', 'Comprovante'), ('declaracao', 'Declaração')], max_length=20, verbose_name='Tipo de arquivo'),
        ),
        migrations.DeleteModel(
            name='tipoArquivo',
        ),
    ]
