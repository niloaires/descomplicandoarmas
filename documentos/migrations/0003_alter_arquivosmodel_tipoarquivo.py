# Generated by Django 4.0.2 on 2022-03-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0002_alter_arquivosmodel_tipoarquivo_delete_tipoarquivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivosmodel',
            name='tipoArquivo',
            field=models.CharField(choices=[('certidao', 'Certidão'), ('comprovante', 'Comprovante'), ('declaracao', 'Declaração'), ('requerimento', 'Requerimento')], max_length=20, verbose_name='Tipo de arquivo'),
        ),
    ]
