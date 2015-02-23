# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('container', '0005_auto_20150216_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='scrollpage',
            field=models.ForeignKey(to='homepage.ScrollPage'),
            preserve_default=True,
        ),
    ]
