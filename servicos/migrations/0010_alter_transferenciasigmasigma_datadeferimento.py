# Generated by Django 4.0.2 on 2022-02-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0009_remove_transferenciasigmasigma_servico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferenciasigmasigma',
            name='dataDeferimento',
            field=models.DateField(blank=True, null=True),
        ),
    ]