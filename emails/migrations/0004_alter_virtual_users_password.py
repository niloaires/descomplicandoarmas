# Generated by Django 4.0.2 on 2022-04-16 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_alter_virtual_users_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtual_users',
            name='password',
            field=models.CharField(blank=True, db_column='password', max_length=250, null=True),
        ),
    ]
