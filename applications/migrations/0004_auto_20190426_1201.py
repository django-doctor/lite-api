# Generated by Django 2.2 on 2019-04-26 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_remove_goodonapplication_end_use_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodonapplication',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='applications.Application'),
        ),
    ]