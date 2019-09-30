# Generated by Django 2.2.4 on 2019-09-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='sub_type',
            field=models.CharField(choices=[('government', 'Government'), ('commercial', 'Commercial Organisation'), ('individual', 'Individual'), ('other', 'Other')], default='commercial', max_length=20),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='eori_number',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='registration_number',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='sic_number',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='vat_number',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]