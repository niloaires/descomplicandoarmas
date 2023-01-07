# Generated by Django 4.0.2 on 2022-02-17 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armas', '0002_armasclientes_mudandapropriedade'),
        ('clientes', '0003_clientemodel_senhaacessogov'),
        ('servicos', '0011_alter_transferenciasigmasigma_arma'),
    ]

    operations = [
        migrations.CreateModel(
            name='emissaoGuiaTrafego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municoes', models.CharField(blank=True, max_length=100, null=True)),
                ('municoesQuantidade', models.SmallIntegerField(default=0)),
                ('dataRegistro', models.DateField(auto_now=True)),
                ('dataDeferimento', models.DateField(blank=True, null=True)),
                ('deferido', models.BooleanField(default=False)),
                ('arma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emissao_gt', to='armas.armasclientes')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emissao_gt', to='clientes.clientemodel')),
            ],
        ),
    ]