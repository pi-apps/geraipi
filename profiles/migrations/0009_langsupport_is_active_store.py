# Generated by Django 4.1.2 on 2024-03-03 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0008_remove_userprofileaddress_image_profile_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="langsupport",
            name="is_active_store",
            field=models.BooleanField(default=False),
        ),
    ]
