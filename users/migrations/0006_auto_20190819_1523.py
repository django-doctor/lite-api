# Generated by Django 2.2.4 on 2019-08-19 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_baseuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='last_login',
        ),
    ]