# Generated by Django 3.0.6 on 2021-01-19 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_auto_20210119_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='gb_id',
            new_name='gb',
        ),
    ]
