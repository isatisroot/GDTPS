# Generated by Django 3.0.6 on 2021-02-10 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0023_auto_20210210_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accumulatemotion',
            name='is_tongji',
        ),
        migrations.RemoveField(
            model_name='motionbook',
            name='is_tongji',
        ),
        migrations.AddField(
            model_name='meeting',
            name='is_tongji',
            field=models.BinaryField(default=False, null=True),
        ),
    ]