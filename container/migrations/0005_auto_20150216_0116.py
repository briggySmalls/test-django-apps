# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('container', '0004_auto_20150213_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tab',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='tab',
            name='object_id',
        ),
        migrations.AddField(
            model_name='tab',
            name='article',
            field=models.ForeignKey(to='articles.Article', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tab',
            name='category',
            field=models.ForeignKey(to='articles.Category', blank=True, null=True),
            preserve_default=True,
        ),
    ]
