# Generated by Django 2.1.7 on 2019-05-23 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20190522_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tamaño',
            field=models.CharField(max_length=32),
        ),
    ]
