# Generated by Django 4.0.2 on 2022-02-17 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0013_remove_contratosmodel_servicos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissaoguiatrafego',
            name='municoesLote',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]