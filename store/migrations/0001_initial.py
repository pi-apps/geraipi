# Generated by Django 4.1.2 on 2023-12-24 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.TextField()),
                ('coin', models.FloatField(default=0)),
                ('deskripsi', models.TextField(blank=True, null=True)),
                ('is_active_store', models.BooleanField(default=False)),
                ('aggrement', models.BooleanField(default=False)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserStoreWdHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, auto_now=True)),
                ('jumlah', models.FloatField(default=0)),
                ('userstore', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.userstore')),
            ],
        ),
        migrations.CreateModel(
            name='UserStoreAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('rt', models.CharField(blank=True, max_length=10, null=True)),
                ('rw', models.CharField(blank=True, max_length=10, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=10, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('distric', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master.distric')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master.provinsi')),
                ('regency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master.regency')),
                ('userstore', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.userstore')),
                ('village', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master.village')),
            ],
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notificationfrom', models.CharField(blank=True, max_length=255, null=True)),
                ('notificationfor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
