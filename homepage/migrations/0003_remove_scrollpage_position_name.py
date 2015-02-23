# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20150202_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrollpage',
            name='position_name',
        ),
    ]
