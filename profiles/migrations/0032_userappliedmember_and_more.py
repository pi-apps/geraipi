# Generated by Django 4.1.2 on 2024-06-17 05:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0030_alter_userwithdrawltransactionrequest_kode'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAppliedMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateTimeField(auto_created=True, auto_now=True)),
                ('is_accept', models.BooleanField(default=False)),
                ('accept_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userwithdrawltransactionrequest',
            name='kode',
            field=models.CharField(default='3TLCW', max_length=255),
        ),
        migrations.CreateModel(
            name='UserSettingsMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('quota_withdrawl', models.IntegerField(default=0)),
                ('bypass_waiting', models.BooleanField(default=False)),
                ('updated_information', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCodeGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('quota_withdrawl', models.IntegerField(default=0)),
                ('bypass_waiting', models.BooleanField(default=False)),
                ('updated_information', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user_apply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.userappliedmember')),
            ],
        ),
    ]