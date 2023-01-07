# Generated by Django 4.0.2 on 2022-12-31 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0022_alter_clientemodel_escolaridade'),
        ('enderecos', '0002_alter_enderecoclientemodel_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enderecoclientemodel',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enderecos', to='clientes.clientemodel'),
        ),
    ]
