# Generated by Django 4.0.2 on 2022-05-18 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0015_remove_clientemodel_processosemandamento'),
        ('servicos', '0047_delete_consultaprocessomodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferenciasigmasigma',
            name='adquirente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adquirente_transferencia', to='clientes.clientemodel', verbose_name='Adquirente (comprador)'),
        ),
        migrations.AlterField(
            model_name='transferenciasigmasigma',
            name='alienante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alienante_transferencia', to='clientes.clientemodel', verbose_name='Alienante (vendedor)'),
        ),
        migrations.AlterField(
            model_name='transferenciasigmasigma',
            name='responsavel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='responsavel_transferencia', to='clientes.clientemodel', verbose_name='Responsável pela transferênia'),
        ),
    ]