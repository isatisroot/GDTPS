# Generated by Django 3.0.6 on 2020-12-18 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20201218_1039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='addrress',
            new_name='address',
        ),
    ]
