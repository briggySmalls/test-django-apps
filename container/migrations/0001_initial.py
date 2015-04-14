# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_auto_20150206_0043'),
        ('articles', '0002_article_full_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('scrollpage', models.ForeignKey(blank=True, null=True, to='homepage.ScrollPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=15)),
                ('order', models.PositiveIntegerField(default=2)),
                ('column_count', models.PositiveIntegerField(default=1)),
                ('article', models.ForeignKey(blank=True, null=True, to='articles.Article')),
                ('category', models.ForeignKey(blank=True, null=True, to='articles.Category')),
                ('container', models.ForeignKey(to='container.Container')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
