# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0009_auto_20180604_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalride',
            name='new_route',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='notes',
            field=models.CharField(help_text='Notes on the ride', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='route_description',
            field=models.CharField(help_text='A description of the route', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='route_name',
            field=models.CharField(help_text='The name of the route', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='start_time',
            field=models.CharField(help_text='What time the recording started', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='surveyor_name',
            field=models.CharField(help_text='Who captured the ride', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='vehicle_capacity',
            field=models.CharField(help_text='NUmber of passenger seats', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='vehicle_type',
            field=models.CharField(help_text='What vehicle was used', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='new_route',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ride',
            name='notes',
            field=models.CharField(help_text='Notes on the ride', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='route_description',
            field=models.CharField(help_text='A description of the route', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='route_name',
            field=models.CharField(help_text='The name of the route', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='start_time',
            field=models.CharField(help_text='What time the recording started', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='surveyor_name',
            field=models.CharField(help_text='Who captured the ride', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='vehicle_capacity',
            field=models.CharField(help_text='NUmber of passenger seats', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(help_text='What vehicle was used', max_length=255, null=True, blank=True),
        ),
    ]
