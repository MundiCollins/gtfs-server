# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multigtfs', '0005_auto_20180502_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNewRoute',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('latitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('longitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('time', models.CharField(help_text='What time did the ride arrive?', max_length=255, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('ride', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='multigtfs.Ride', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical new route',
            },
        ),
        migrations.CreateModel(
            name='NewRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('latitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('longitude', models.CharField(help_text='WGS 84 latitude of stop or station', max_length=255, null=True, blank=True)),
                ('time', models.CharField(help_text='What time did the ride arrive?', max_length=255, null=True, blank=True)),
                ('ride', models.ForeignKey(to='multigtfs.Ride')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
