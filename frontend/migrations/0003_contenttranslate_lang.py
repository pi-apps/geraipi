# Generated by Django 4.1.2 on 2024-02-18 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_contenttranslate'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttranslate',
            name='lang',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
