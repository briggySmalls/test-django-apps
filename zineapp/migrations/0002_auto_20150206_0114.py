# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_auto_20150206_0043'),
        ('zineapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zine',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('pdf_file', models.FileField(default='', upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='zineapp',
            name='description',
        ),
        migrations.RemoveField(
            model_name='zineapp',
            name='pdf_file',
        ),
        migrations.RemoveField(
            model_name='zineapp',
            name='title',
        ),
        migrations.AddField(
            model_name='zineapp',
            name='scrollpage',
            field=models.ForeignKey(null=True, to='homepage.ScrollPage', blank=True),
            preserve_default=True,
        ),
    ]
