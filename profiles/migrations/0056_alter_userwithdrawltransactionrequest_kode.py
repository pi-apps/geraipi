# Generated by Django 4.1.2 on 2024-07-31 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0055_alter_userwithdrawltransactionrequest_kode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwithdrawltransactionrequest',
            name='kode',
            field=models.CharField(default='V1BEQ', max_length=255),
        ),
    ]