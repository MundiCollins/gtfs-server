# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multigtfs', '0007_auto_20180510_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNewFare',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('stop_to', models.CharField(max_length=255, null=True, blank=True)),
                ('stop_from', models.CharField(max_length=255, null=True, blank=True)),
                ('amount', models.CharField(max_length=255, null=True, blank=True)),
                ('stop_from_id', models.CharField(max_length=255, null=True, blank=True)),
                ('route_id', models.CharField(max_length=255, null=True, blank=True)),
                ('stop_to_id', models.CharField(max_length=255, null=True, blank=True)),
                ('weather', models.CharField(max_length=255, null=True, blank=True)),
                ('traffic_jam', models.CharField(max_length=255, null=True, blank=True)),
                ('demand', models.CharField(max_length=255, null=True, blank=True)),
                ('rush_hour', models.CharField(max_length=255, null=True, blank=True)),
                ('peak', models.CharField(max_length=255, null=True, blank=True)),
                ('travel_time', models.CharField(max_length=255, null=True, blank=True)),
                ('crowd', models.CharField(max_length=255, null=True, blank=True)),
                ('safety', models.CharField(max_length=255, null=True, blank=True)),
                ('drive_safety', models.CharField(max_length=255, null=True, blank=True)),
                ('music', models.CharField(max_length=255, null=True, blank=True)),
                ('internet', models.CharField(max_length=255, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical new fare',
            },
        ),
        migrations.CreateModel(
            name='NewFare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('stop_to', models.CharField(max_length=255, null=True, blank=True)),
                ('stop_from', models.CharField(max_length=255, null=True, blank=True)),
                ('amount', models.CharField(max_length=255, null=True, blank=True)),
                ('stop_from_id', models.CharField(max_length=255, null=True, blank=True)),
                ('route_id', models.CharField(max_length=255, null=True, blank=True)),
                ('stop_to_id', models.CharField(max_length=255, null=True, blank=True)),
                ('weather', models.CharField(max_length=255, null=True, blank=True)),
                ('traffic_jam', models.CharField(max_length=255, null=True, blank=True)),
                ('demand', models.CharField(max_length=255, null=True, blank=True)),
                ('rush_hour', models.CharField(max_length=255, null=True, blank=True)),
                ('peak', models.CharField(max_length=255, null=True, blank=True)),
                ('travel_time', models.CharField(max_length=255, null=True, blank=True)),
                ('crowd', models.CharField(max_length=255, null=True, blank=True)),
                ('safety', models.CharField(max_length=255, null=True, blank=True)),
                ('drive_safety', models.CharField(max_length=255, null=True, blank=True)),
                ('music', models.CharField(max_length=255, null=True, blank=True)),
                ('internet', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
