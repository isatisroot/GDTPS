# Generated by Django 3.0.6 on 2021-07-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0038_voterecorddetail_gdid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareholderinfo',
            name='gdxm',
            field=models.CharField(max_length=120),
        ),
    ]
