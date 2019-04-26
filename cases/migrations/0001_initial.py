# Generated by Django 2.2 on 2019-04-23 13:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case', to='applications.Application')),
            ],
        ),
    ]