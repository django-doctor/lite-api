# Generated by Django 2.2.11 on 2020-03-16 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("decisions", "0001_initial"),
        ("letter_templates", "0002_lettertemplate_decisions"),
    ]

    operations = [
        migrations.RemoveField(model_name="lettertemplate", name="decisions",),
        migrations.AddField(
            model_name="lettertemplate",
            name="decisions",
            field=models.ManyToManyField(related_name="letter_templates", to="decisions.Decision"),
        ),
    ]
