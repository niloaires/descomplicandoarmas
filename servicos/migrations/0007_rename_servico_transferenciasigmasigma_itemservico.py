# Generated by Django 4.0.2 on 2022-02-16 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0006_transferenciasigmasigma_responsavel_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferenciasigmasigma',
            old_name='servico',
            new_name='itemServico',
        ),
    ]