# Generated by Django 4.0.2 on 2022-03-27 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracoes', '0005_declaracoesdiversas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='declaracoesdiversas',
            options={'verbose_name': 'Declaração diversa', 'verbose_name_plural': 'Declarações diversas'},
        ),
        migrations.AddField(
            model_name='declaracoesdiversas',
            name='dataRegistro',
            field=models.DateField(auto_now=True),
        ),
    ]
