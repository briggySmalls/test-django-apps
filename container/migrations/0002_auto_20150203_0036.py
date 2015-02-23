# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('container', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tab',
            name='keyword',
            field=models.CharField(max_length=15),
            preserve_default=True,
        ),
    ]
