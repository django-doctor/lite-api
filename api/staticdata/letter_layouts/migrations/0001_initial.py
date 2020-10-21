# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LetterLayout",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("filename", models.TextField()),
            ],
            options={"ordering": ["name"],},
        ),
    ]