# Generated by Django 2.2.4 on 2019-10-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0005_auto_20191002_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='type',
            field=models.CharField(choices=[('hmrc', 'HMRC'), ('commercial', 'Commercial Organisation'), ('individual', 'Individual')], default='commercial', max_length=20),
        ),
    ]