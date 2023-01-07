# Generated by Django 4.0.2 on 2022-03-28 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armas', '0007_remove_armasclientes_mudandapropriedade_and_more'),
        ('clientes', '0009_clientemodel_nomemae_clientemodel_nomepai'),
        ('servicos', '0044_alter_andamentoservicossisgcorpmodel_statusservico_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='transferenciaSinarmSigma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(default='São Luís - MA', max_length=150)),
                ('dataRegistro', models.DateField(auto_now=True)),
                ('dataDeferimento', models.DateField(blank=True, null=True)),
                ('deferido', models.BooleanField(default=False)),
                ('adquirente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adquirente_transferencia_sinarm_sigma', to='clientes.clientemodel')),
                ('alienante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alienante_transferencia_sinarm_sigma', to='clientes.clientemodel')),
                ('arma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='armas.armasclientes')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='responsavel_transferencia_sinarm_sigma', to='clientes.clientemodel')),
            ],
        ),
    ]