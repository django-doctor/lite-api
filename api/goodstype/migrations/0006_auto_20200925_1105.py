# Generated by Django 2.2.16 on 2020-09-25 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("goodstype", "0005_auto_20200924_1731"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="goodstype", options={"default_related_name": "goods_type", "ordering": ["-created_at"]},
        ),
        migrations.AlterField(
            model_name="goodstype",
            name="application",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="goods_type",
                to="applications.BaseApplication",
            ),
        ),
        migrations.AlterField(
            model_name="goodstype",
            name="control_list_entries",
            field=models.ManyToManyField(related_name="goods_type", to="control_list_entries.ControlListEntry"),
        ),
    ]