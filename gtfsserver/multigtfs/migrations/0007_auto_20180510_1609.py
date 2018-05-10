# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0006_historicalnewroute_newroute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalride',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='extra_data',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='route_latitude',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='route_longitude',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='vehicle_capacity',
        ),
        migrations.RemoveField(
            model_name='historicalride',
            name='vehicle_type',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='extra_data',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='route_latitude',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='route_longitude',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='vehicle_capacity',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='vehicle_type',
        ),
    ]
