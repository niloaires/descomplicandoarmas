# Generated by Django 4.0.2 on 2022-06-04 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processos', '0002_remove_pendenciasmodels_processo'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoprocessosmodel',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='historicosProcessos', to=settings.AUTH_USER_MODEL),
        ),
    ]
