# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0013_auto_20180615_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltrip',
            name='direction',
            field=models.CharField(blank=True, help_text='Direction for bi-directional routes.', max_length=7, choices=[('0', '0'), ('1', '1')]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='direction',
            field=models.CharField(blank=True, help_text='Direction for bi-directional routes.', max_length=7, choices=[('0', '0'), ('1', '1')]),
        ),
    ]
