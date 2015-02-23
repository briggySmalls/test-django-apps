# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_remove_scrollpage_position_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrollpage',
            name='bg_colour',
            field=colorfield.fields.ColorField(max_length=7, default='ffffff'),
            preserve_default=True,
        ),
    ]
