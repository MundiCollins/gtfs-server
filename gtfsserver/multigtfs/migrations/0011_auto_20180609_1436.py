# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0010_auto_20180609_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalride',
            name='vehicle_full',
            field=models.CharField(help_text='Whether the vehicle was full', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='vehicle_full',
            field=models.CharField(help_text='Whether the vehicle was full', max_length=255, null=True, blank=True),
        ),
    ]
