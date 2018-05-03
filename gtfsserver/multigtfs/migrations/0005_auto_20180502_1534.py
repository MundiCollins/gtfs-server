# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multigtfs', '0004_historicalblock_historicalfare_historicalfarerule_historicalfeedinfo_historicalfrequency_historicalr'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNewStop',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('latitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('longitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('arrival_time', models.CharField(help_text='What time did the ride arrive?', max_length=255, null=True, blank=True)),
                ('departure_time', models.CharField(help_text='What time did the ride arrive?', max_length=255, null=True, blank=True)),
                ('board', models.CharField(max_length=255, null=True, blank=True)),
                ('alight', models.CharField(max_length=255, null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical new stop',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRide',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('desc', models.CharField(help_text='Description of the ride.', max_length=255, null=True, blank=True)),
                ('notes', models.CharField(help_text='Notes on the ride.', max_length=255, null=True, blank=True)),
                ('vehicle_capacity', models.IntegerField(help_text='Number of passenger seats in the vehicle', null=True, blank=True)),
                ('vehicle_type', models.CharField(blank=True, max_length=1, null=True, help_text='What type of vehicle are you in?', choices=[('0', 'Matatu'), ('1', 'Bus'), ('2', 'TukTuk')])),
                ('start_time', models.CharField(help_text='What time did the ride start?', max_length=255, null=True, blank=True)),
                ('route_latitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('route_longitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('created', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('route', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='multigtfs.Route', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical ride',
            },
        ),
        migrations.CreateModel(
            name='NewStop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('latitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('longitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('arrival_time', models.CharField(help_text='What time did the ride arrive?', max_length=255, null=True, blank=True)),
                ('departure_time', models.CharField(help_text='What time did the ride arrive?', max_length=255, null=True, blank=True)),
                ('board', models.CharField(max_length=255, null=True, blank=True)),
                ('alight', models.CharField(max_length=255, null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('desc', models.CharField(help_text='Description of the ride.', max_length=255, null=True, blank=True)),
                ('notes', models.CharField(help_text='Notes on the ride.', max_length=255, null=True, blank=True)),
                ('vehicle_capacity', models.IntegerField(help_text='Number of passenger seats in the vehicle', null=True, blank=True)),
                ('vehicle_type', models.CharField(blank=True, max_length=1, null=True, help_text='What type of vehicle are you in?', choices=[('0', 'Matatu'), ('1', 'Bus'), ('2', 'TukTuk')])),
                ('start_time', models.CharField(help_text='What time did the ride start?', max_length=255, null=True, blank=True)),
                ('route_latitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('route_longitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('route', models.ForeignKey(to='multigtfs.Route')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newstop',
            name='ride',
            field=models.ForeignKey(to='multigtfs.Ride'),
        ),
        migrations.AddField(
            model_name='historicalnewstop',
            name='ride',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='multigtfs.Ride', null=True),
        ),
    ]
