# Generated by Django 4.0.2 on 2022-02-19 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0017_listaservicos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emissaoguiatrafego',
            options={'verbose_name': 'Emissão de Guia de tráfego'},
        ),
        migrations.RemoveField(
            model_name='servicosmodel',
            name='servicoConcluido',
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='statusServico',
            field=models.CharField(choices=[('aguardandopagamento', 'Aguardando pagamentoo'), ('iniciado', 'Iniciado'), ('documentacao', 'Juntando documentação'), ('protocolado', 'Protoloado'), ('analise', 'Em análise pelo órgão'), ('deferido', 'Deferido'), ('indeferido', 'Indeferido')], default='aguardandopagamento', max_length=30, verbose_name='Status do serviço'),
        ),
    ]