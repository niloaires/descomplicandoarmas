# Generated by Django 4.0.2 on 2022-03-16 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0043_alter_servicossisgcorpmodel_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='andamentoservicossisgcorpmodel',
            name='statusServico',
            field=models.CharField(choices=[('aguardandopagamento', 'Aguardando pagamento'), ('iniciado', 'Iniciado'), ('documentacao', 'Juntando documentação'), ('protocolado', 'Protoloado'), ('analise', 'Em análise pelo órgão'), ('deferido', 'Deferido'), ('indeferido', 'Indeferido')], max_length=20, verbose_name='Status atual do serviço'),
        ),
        migrations.AlterField(
            model_name='movimentacoesservico',
            name='statusServico',
            field=models.CharField(choices=[('aguardandopagamento', 'Aguardando pagamento'), ('iniciado', 'Iniciado'), ('documentacao', 'Juntando documentação'), ('protocolado', 'Protoloado'), ('analise', 'Em análise pelo órgão'), ('deferido', 'Deferido'), ('indeferido', 'Indeferido')], default='aguardandopagamento', max_length=30, verbose_name='Status do serviço'),
        ),
    ]
