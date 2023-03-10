# Generated by Django 4.0.2 on 2022-03-16 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0008_alter_clientemodel_escolaridade'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='registrosFinanceiroModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição do registro')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('formaPagamento', models.CharField(choices=[('pix', 'Pix'), ('transferencia', 'Transferência'), ('cartao', 'Cartão de Crédito'), ('parcelamento', 'Parcelamento sem cartão'), ('gru', 'GRU')], max_length=20, verbose_name='Forma de pagamento')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Valor do serviço')),
                ('ativo', models.BooleanField(default=True, verbose_name='Registro ativo')),
                ('efetivado', models.BooleanField(default=False, verbose_name='Registro efetivado')),
                ('dataPrevista', models.DateField(verbose_name='Data prevista')),
                ('dataEfetivacao', models.DateField(blank=True, null=True, verbose_name='Data da efetivação')),
                ('dataRegistro', models.DateTimeField(auto_now=True, verbose_name='Data e hora do registro')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registrosFinanceiros', to='clientes.clientemodel')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Registro financeiro',
                'verbose_name_plural': 'Registros financeiros',
            },
        ),
    ]
