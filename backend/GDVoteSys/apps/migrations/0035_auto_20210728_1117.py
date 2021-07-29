# Generated by Django 3.0.6 on 2021-07-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0034_networkvotecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='onsitemeeting',
            name='huibi_descr',
            field=models.CharField(default=None, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='onsitemeeting',
            name='vote',
            field=models.SmallIntegerField(choices=[(1, '赞成'), (2, '反对'), (3, '弃权'), (4, '回避')], null=True),
        ),
    ]
