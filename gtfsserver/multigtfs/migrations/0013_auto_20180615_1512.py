# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0012_auto_20180610_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnewstop',
            name='stop_designation',
            field=models.CharField(help_text='What is the official designation status of the stop?', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalnewstop',
            name='stop_name',
            field=models.CharField(help_text='What is the name of the stop?', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='newstop',
            name='stop_designation',
            field=models.CharField(help_text='What is the official designation status of the stop?', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='newstop',
            name='stop_name',
            field=models.CharField(help_text='What is the name of the stop?', max_length=255, null=True, blank=True),
        ),
    ]
