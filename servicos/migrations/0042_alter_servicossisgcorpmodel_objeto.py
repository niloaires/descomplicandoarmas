# Generated by Django 4.0.2 on 2022-03-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0041_alter_servicosmodel_tiposervico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicossisgcorpmodel',
            name='objeto',
            field=models.CharField(choices=[('Registro CR', 'Concessão de registro CR'), ('Autorização de compra', 'Autorização de Aquisição de PCE'), ('Registro PCE', 'Apostilamento e Registro do PCE'), ('Guia de tráfego PCE', 'Emissão de Guia de Tráfego do PCE')], max_length=30, verbose_name='Objeto do serviço'),
        ),
    ]
