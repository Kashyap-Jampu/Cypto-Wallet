# Generated by Django 3.2.5 on 2021-07-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0003_auto_20210727_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='private_key',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='user',
            name='public_key',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
