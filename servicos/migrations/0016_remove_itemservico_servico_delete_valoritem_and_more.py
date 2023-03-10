# Generated by Django 4.0.2 on 2022-02-17 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('clientes', '0003_clientemodel_senhaacessogov'),
        ('servicos', '0015_alter_emissaoguiatrafego_municoes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemservico',
            name='servico',
        ),
        migrations.DeleteModel(
            name='valorItem',
        ),
        migrations.AlterModelOptions(
            name='servicosmodel',
            options={'ordering': ['cliente', 'dataRegistro'], 'verbose_name': 'Serviço', 'verbose_name_plural': 'Serviços'},
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='dataConclusao',
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='dataContrato',
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='dataRegistro',
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='servicoAtivo',
        ),
        migrations.RemoveField(
            model_name='contratosmodel',
            name='servicoConcluido',
        ),
        migrations.RemoveField(
            model_name='servicosmodel',
            name='ativo',
        ),
        migrations.RemoveField(
            model_name='servicosmodel',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='servicosmodel',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='servicosmodel',
            name='sistemaVinculado',
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='adicional',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=13, null=True, verbose_name='Valor adicional'),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='servicos', to='clientes.clientemodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='dataConclusao',
            field=models.DateField(blank=True, null=True, verbose_name='Data de conclusão'),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='dataRegistro',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='descricaServico',
            field=models.CharField(blank=True, default='Sem descrição', max_length=200, verbose_name='Descrição'),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='observacao',
            field=models.TextField(blank=True, default='Sem observações'),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='servicoAtivo',
            field=models.BooleanField(default=True, verbose_name='Serviço ativo'),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='servicoConcluido',
            field=models.BooleanField(default=False, verbose_name='Serviço concluído'),
        ),
        migrations.AddField(
            model_name='servicosmodel',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=13, null=True, verbose_name='Valor do serviço'),
        ),
        migrations.DeleteModel(
            name='ItemServico',
        ),
    ]
