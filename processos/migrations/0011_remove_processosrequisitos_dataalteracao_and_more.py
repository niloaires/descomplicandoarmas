# Generated by Django 4.0.2 on 2022-07-25 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0010_historicoprocessos_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processosrequisitos',
            name='dataAlteracao',
        ),
        migrations.AddField(
            model_name='novosprocessosmodel',
            name='ultimaMovimentacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processosrequisitos',
            name='dataUltimaAlteracao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
