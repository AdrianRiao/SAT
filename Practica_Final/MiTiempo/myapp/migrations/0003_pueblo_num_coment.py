# Generated by Django 2.1.7 on 2019-05-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_pueblo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pueblo',
            name='num_coment',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]