# Generated by Django 2.2.2 on 2019-07-02 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20190702_1259'),
        ('clc_queries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clcquery',
            name='good',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='goods.Good'),
            preserve_default=False,
        ),
    ]
