# Generated by Django 3.0.6 on 2021-01-20 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_auto_20210119_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shareholderinfo',
            name='meno',
        ),
        migrations.AlterField(
            model_name='onsitemeeting',
            name='meno',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]