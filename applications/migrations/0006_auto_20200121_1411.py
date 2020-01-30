# Generated by Django 2.2.8 on 2020-01-21 14:11

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0005_baseapplication_licence_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="goodonapplication",
            name="created_at",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now, editable=False, verbose_name="created_at"
            ),
        ),
        migrations.AddField(
            model_name="goodonapplication",
            name="updated_at",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now, editable=False, verbose_name="updated_at"
            ),
        ),
    ]