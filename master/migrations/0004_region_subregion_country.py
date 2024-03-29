# Generated by Django 4.1.2 on 2024-03-21 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("master", "0003_negara"),
    ]

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("wiki_id", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SubRegion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("wiki_id", models.CharField(max_length=100)),
                (
                    "region_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="master.region"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("iso3", models.CharField(blank=True, max_length=50, null=True)),
                ("iso2", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "numeric_code",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("phone_code", models.CharField(blank=True, max_length=50, null=True)),
                ("capital", models.CharField(blank=True, max_length=50, null=True)),
                ("currency", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "currency_name",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "currency_symbol",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("tld", models.CharField(blank=True, max_length=50, null=True)),
                ("native", models.CharField(blank=True, max_length=50, null=True)),
                ("nationality", models.CharField(blank=True, max_length=50, null=True)),
                ("timezones", models.JSONField(default=[])),
                (
                    "region_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="master.region"
                    ),
                ),
                (
                    "subregion_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="master.subregion",
                    ),
                ),
            ],
        ),
    ]
