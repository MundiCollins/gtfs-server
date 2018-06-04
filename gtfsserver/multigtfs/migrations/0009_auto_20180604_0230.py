# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0008_historicalnewfare_newfare'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalnewfare',
            old_name='rush_hour',
            new_name='air_quality',
        ),
        migrations.RenameField(
            model_name='newfare',
            old_name='rush_hour',
            new_name='air_quality',
        ),
    ]
