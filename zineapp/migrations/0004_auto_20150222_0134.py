# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zineapp', '0003_zine_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zine',
            name='slug',
            field=models.CharField(max_length=200, editable=False),
            preserve_default=True,
        ),
    ]
