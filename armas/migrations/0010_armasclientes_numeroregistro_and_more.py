# Generated by Django 4.0.2 on 2022-05-22 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armas', '0009_armasclientes_paisfabricacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='armasclientes',
            name='numeroRegistro',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número de registro no (SINARM)'),
        ),
        migrations.AddField(
            model_name='armasclientes',
            name='orgaoExpedidor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Órgão expedidor'),
        ),
    ]