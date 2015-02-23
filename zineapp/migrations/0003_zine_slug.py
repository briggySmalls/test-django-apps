# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zineapp', '0002_auto_20150206_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='zine',
            name='slug',
            field=models.CharField(blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
