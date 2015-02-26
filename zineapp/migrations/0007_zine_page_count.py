# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zineapp', '0006_auto_20150223_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='zine',
            name='page_count',
            field=models.IntegerField(editable=False, null=True),
            preserve_default=True,
        ),
    ]
