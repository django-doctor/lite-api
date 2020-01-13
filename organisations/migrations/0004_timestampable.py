# Generated by Django 2.2.8 on 2020-01-07 16:38

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0003_auto_20191219_1431"),
    ]

    operations = [
        migrations.RemoveField(model_name="organisation", name="last_modified_at",),
        migrations.AddField(
            model_name="externallocation",
            name="created_at",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now, editable=False, verbose_name="created_at"
            ),
        ),
        migrations.AddField(
            model_name="externallocation",
            name="updated_at",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now, editable=False, verbose_name="updated_at"
            ),
        ),
        migrations.AddField(
            model_name="organisation",
            name="updated_at",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now, editable=False, verbose_name="updated_at"
            ),
        ),
        migrations.AddField(
            model_name="site",
            name="created_at",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now, editable=False, verbose_name="created_at"
            ),
        ),
        migrations.AddField(
            model_name="site",
            name="updated_at",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now, editable=False, verbose_name="updated_at"
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="created_at",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now, editable=False, verbose_name="created_at"
            ),
        ),
    ]