# Generated by Django 2.2.4 on 2019-09-18 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statuses', '0001_initial'),
        ('organisations', '0001_initial'),
        ('parties', '0001_initial'),
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='consignee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_consignee', to='parties.Consignee'),
        ),
        migrations.AddField(
            model_name='application',
            name='end_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_end_user', to='parties.EndUser'),
        ),
        migrations.AddField(
            model_name='application',
            name='organisation',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.Organisation'),
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_status', to='statuses.CaseStatus'),
        ),
        migrations.AddField(
            model_name='application',
            name='third_parties',
            field=models.ManyToManyField(related_name='application_third_parties', to='parties.ThirdParty'),
        ),
        migrations.AddField(
            model_name='application',
            name='ultimate_end_users',
            field=models.ManyToManyField(related_name='application_ultimate_end_users', to='parties.UltimateEndUser'),
        ),
    ]