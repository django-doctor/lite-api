# Generated by Django 2.2 on 2019-05-28 14:33

import uuid

from django.db import migrations, models


def init(apps, schema_editor):
    # We can't import the Team model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Team = apps.get_model('teams', 'Team')
    if not Team.objects.all():
        team = Team(id='00000000-0000-0000-0000-000000000001',
                    name='Admin')
        team.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=60)),
            ],
        ),
        migrations.RunPython(init),
    ]