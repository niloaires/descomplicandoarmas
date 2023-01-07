# Generated by Django 4.0.2 on 2022-02-16 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_clientemodel_options_alter_clientemodel_genero'),
        ('servicos', '0005_transferenciasigmasigma_local'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferenciasigmasigma',
            name='responsavel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='responsavel_transferencia', to='clientes.clientemodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transferenciasigmasigma',
            name='servico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='item_servico', to='servicos.itemservico'),
            preserve_default=False,
        ),
    ]