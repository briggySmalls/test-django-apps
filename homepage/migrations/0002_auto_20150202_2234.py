# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scrollpage',
            old_name='page_colour',
            new_name='bg_colour',
        ),
        migrations.RenameField(
            model_name='scrollpage',
            old_name='page_name',
            new_name='name',
        ),
    ]
