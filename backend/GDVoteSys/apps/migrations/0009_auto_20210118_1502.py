# Generated by Django 3.0.6 on 2021-01-18 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_auto_20201218_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='onsitemeeting',
            name='gzA',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='onsitemeeting',
            name='gzB',
            field=models.IntegerField(default=0),
        ),
    ]
