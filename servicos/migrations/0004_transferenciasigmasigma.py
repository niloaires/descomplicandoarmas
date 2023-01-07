# Generated by Django 4.0.2 on 2022-02-16 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_clientemodel_options_alter_clientemodel_genero'),
        ('armas', '0001_initial'),
        ('servicos', '0003_alter_servicosmodel_options_itemservico_adicional_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='transferenciaSigmaSigma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataRegistro', models.DateField(auto_now=True)),
                ('dataDeferimento', models.DateField(blank=True)),
                ('deferido', models.BooleanField(default=False)),
                ('adquirente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adquirente_transferencia', to='clientes.clientemodel')),
                ('alienante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alienante_transferencia', to='clientes.clientemodel')),
                ('arma', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='armas.armasclientes')),
            ],
        ),
    ]
