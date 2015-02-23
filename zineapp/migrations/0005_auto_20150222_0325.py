# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import zineapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('zineapp', '0004_auto_20150222_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zine',
            name='pdf_file',
            field=models.FileField(upload_to=zineapp.models.content_file_name, default=''),
            preserve_default=True,
        ),
    ]
