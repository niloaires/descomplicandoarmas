# Generated by Django 4.0.2 on 2022-08-15 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0012_remove_processosrequisitos_dataultimaalteracao'),
    ]

    operations = [
        migrations.AddField(
            model_name='novosprocessosmodel',
            name='dataPrevistaDeferimento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
