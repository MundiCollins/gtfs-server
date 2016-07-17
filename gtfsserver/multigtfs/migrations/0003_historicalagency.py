# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multigtfs', '0002_add_approval_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAgency',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('agency_id', models.CharField(help_text='Unique identifier for transit agency', max_length=255, db_index=True, blank=True)),
                ('name', models.CharField(help_text='Full name of the transit agency', max_length=255)),
                ('url', models.URLField(help_text='URL of the transit agency', blank=True)),
                ('timezone', models.CharField(help_text='Timezone of the agency', max_length=255)),
                ('lang', models.CharField(help_text='ISO 639-1 code for the primary language', max_length=2, blank=True)),
                ('phone', models.CharField(help_text='Voice telephone number', max_length=255, blank=True)),
                ('fare_url', models.URLField(help_text='URL for purchasing tickets online', blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('feed', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='multigtfs.Feed', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical agency',
            },
        ),
    ]
