# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_remove_scrollpage_position_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('scrollpage', models.ForeignKey(to='homepage.ScrollPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tab',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('keyword', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=200)),
                ('container', models.ForeignKey(to='container.Container')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
