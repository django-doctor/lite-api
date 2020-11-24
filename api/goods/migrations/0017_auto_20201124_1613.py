# Generated by Django 2.2.16 on 2020-11-24 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0016_firearmgooddetails_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='firearmgooddetails',
            name='has_proof_mark',
            field=models.BooleanField(help_text='Has been proofed (by a proof house) indicating it is safe to be used.', null=True),
        ),
        migrations.AddField(
            model_name='firearmgooddetails',
            name='no_proof_mark_details',
            field=models.TextField(blank=True, default=''),
        ),
    ]