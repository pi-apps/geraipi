# Generated by Django 4.1.2 on 2024-03-21 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produk", "0012_deskripsiproduk"),
    ]

    operations = [
        migrations.AddField(
            model_name="deskripsiproduk",
            name="produk",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="produk.produk",
            ),
            preserve_default=False,
        ),
    ]
