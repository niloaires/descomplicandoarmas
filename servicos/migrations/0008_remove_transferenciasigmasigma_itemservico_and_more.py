# Generated by Django 4.0.2 on 2022-02-16 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0007_rename_servico_transferenciasigmasigma_itemservico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferenciasigmasigma',
            name='itemServico',
        ),
        migrations.AddField(
            model_name='transferenciasigmasigma',
            name='servico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='servico', to='servicos.servicosmodel'),
            preserve_default=False,
        ),
    ]
