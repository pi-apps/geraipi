# Generated by Django 4.1.2 on 2024-02-17 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produk", "0005_alter_addressuserchartitem_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="gambarproduk",
            name="sortings",
            field=models.IntegerField(default=0),
        ),
    ]