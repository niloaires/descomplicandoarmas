# Generated by Django 4.0.2 on 2022-03-07 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armas', '0002_armasclientes_mudandapropriedade'),
    ]

    operations = [
        migrations.AddField(
            model_name='armasclientes',
            name='funcionamento',
            field=models.CharField(default='Semi automática', max_length=100, verbose_name='Tipo de funcionamento'),
        ),
    ]
