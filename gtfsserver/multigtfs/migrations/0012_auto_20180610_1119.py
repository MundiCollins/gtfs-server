# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0011_auto_20180609_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalride',
            name='direction',
            field=models.CharField(help_text='Whether inbound or outbound', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='duration',
            field=models.CharField(help_text='How long the trip took', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='direction',
            field=models.CharField(help_text='Whether inbound or outbound', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='duration',
            field=models.CharField(help_text='How long the trip took', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalride',
            name='new_route',
            field=models.CharField(default='false', help_text='Whether it is an existing or new route', max_length=255),
        ),
        migrations.AlterField(
            model_name='ride',
            name='new_route',
            field=models.CharField(default='false', help_text='Whether it is an existing or new route', max_length=255),
        ),
    ]
