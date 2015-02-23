# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('container', '0003_auto_20150213_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tab',
            name='content',
        ),
        migrations.AddField(
            model_name='tab',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tab',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
