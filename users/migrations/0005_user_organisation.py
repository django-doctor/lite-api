# Generated by Django 2.2 on 2019-04-23 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
        ('users', '0004_auto_20190418_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organisation',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.Organisation'),
        ),
    ]