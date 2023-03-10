# Generated by Django 4.0.2 on 2022-02-24 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0031_exigenciasmodel_listaservicos_exigencias'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exigenciasmodel',
            options={'ordering': ['descricao'], 'verbose_name': 'ExigĂȘncia', 'verbose_name_plural': 'ExigĂȘncias'},
        ),
        migrations.RemoveField(
            model_name='listaservicos',
            name='exigencias',
        ),
        migrations.AddField(
            model_name='registrocr',
            name='exigencias',
            field=models.ManyToManyField(related_name='exigencias', to='servicos.exigenciasModel'),
        ),
    ]
