# Generated by Django 3.2.5 on 2021-07-27 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='private_key',
            field=models.CharField(max_length=1024, unique=True),
        ),
    ]