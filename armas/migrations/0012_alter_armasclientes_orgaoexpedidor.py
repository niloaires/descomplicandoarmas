# Generated by Django 4.0.2 on 2022-06-15 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armas', '0011_armasclientes_dataregistro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armasclientes',
            name='orgaoExpedidor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Órgão expedidor (SINARM)'),
        ),
    ]
