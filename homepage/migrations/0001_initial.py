# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScrollPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('page_name', models.CharField(max_length=200)),
                ('position_name', models.CharField(max_length=200)),
                ('page_colour', colorfield.fields.ColorField(max_length=10)),
                ('homepage', models.ForeignKey(to='homepage.HomePage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
