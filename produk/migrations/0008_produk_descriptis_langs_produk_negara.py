# Generated by Django 4.1.2 on 2024-03-03 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0010_alter_langsupport_is_active_store"),
        ("produk", "0007_produk_cross_boarder_alter_gambarproduk_gambar"),
    ]

    operations = [
        migrations.AddField(
            model_name="produk",
            name="descriptis_langs",
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="produk",
            name="negara",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="profiles.langsupport",
            ),
        ),
    ]
