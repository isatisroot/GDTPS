# Generated by Django 3.0.6 on 2021-01-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0013_auto_20210120_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareholderinfo',
            name='dlr',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='shareholderinfo',
            name='frA',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shareholderinfo',
            name='gdtype',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='shareholderinfo',
            name='gzA',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shareholderinfo',
            name='gzB',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shareholderinfo',
            name='sfz',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
