# Generated by Django 2.2.3 on 2019-07-30 10:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clc_queries', '0003_auto_20190718_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='clcquery',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
