# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zineapp', '0005_auto_20150222_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zine',
            name='title',
            field=models.CharField(max_length=200, help_text='must be unique or there will be an error saving the files'),
            preserve_default=True,
        ),
    ]
