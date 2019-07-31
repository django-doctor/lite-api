# Generated by Django 2.2.3 on 2019-07-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('end_user', '0002_enduser_organisation'),
        ('drafts', '0002_auto_20190717_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='ultimate_end_users',
            field=models.ManyToManyField(related_name='drafts', to='end_user.EndUser'),
        ),
    ]
