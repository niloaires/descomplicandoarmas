# Generated by Django 4.0.2 on 2022-07-17 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0008_alter_novosprocessosmodel_dataregistro'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processosrequisitos',
            options={'verbose_name': 'Requisito no processo', 'verbose_name_plural': 'Requisitos nos processos'},
        ),
        migrations.AlterModelOptions(
            name='requisitosprocessosmodel',
            options={'verbose_name': 'Requisito processual', 'verbose_name_plural': 'Requisitos processuais'},
        ),
        migrations.AlterField(
            model_name='processosrequisitos',
            name='dataRegistro',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='processosrequisitos',
            name='processo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processos.novosprocessosmodel', verbose_name='processo'),
        ),
        migrations.AlterField(
            model_name='processosrequisitos',
            name='requisito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processos.requisitosprocessosmodel', verbose_name='requisito'),
        ),
        migrations.CreateModel(
            name='historicoProcessos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('historico', models.TextField(verbose_name='Histórico')),
                ('dataRegistro', models.DateTimeField(auto_now=True)),
                ('processo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processos.novosprocessosmodel', verbose_name='processo')),
            ],
            options={
                'verbose_name': 'Histórico de processo',
                'verbose_name_plural': 'Históricos de processos',
            },
        ),
    ]
