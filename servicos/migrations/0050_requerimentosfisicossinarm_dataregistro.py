# Generated by Django 4.0.2 on 2022-05-18 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0049_requerimentosfisicossinarm'),
    ]

    operations = [
        migrations.AddField(
            model_name='requerimentosfisicossinarm',
            name='dataRegistro',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
