# Generated by Django 3.0.6 on 2021-02-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0027_remove_meeting_has_tongji'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_tongji',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
