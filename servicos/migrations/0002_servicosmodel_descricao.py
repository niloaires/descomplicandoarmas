# Generated by Django 4.0.2 on 2022-02-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicosmodel',
            name='descricao',
            field=models.TextField(blank=True),
        ),
    ]
