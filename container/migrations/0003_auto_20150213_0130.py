# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('container', '0002_auto_20150203_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='scrollpage',
            field=models.OneToOneField(to='homepage.ScrollPage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tab',
            name='content',
            field=ckeditor.fields.RichTextField(),
            preserve_default=True,
        ),
    ]
