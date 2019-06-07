# Generated by Django 2.2 on 2019-04-18 09:13

from django.db import migrations

import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190418_0901'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='organisation',
        ),
    ]
