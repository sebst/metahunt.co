# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHunt',
            fields=[
                ('ph_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('tagline', models.CharField(max_length=255)),
                ('day', models.DateField()),
                ('hunted_at', models.DateTimeField()),
                ('ph_featured', models.BooleanField()),
                ('comments_count', models.IntegerField()),
                ('votes_count', models.IntegerField()),
                ('discussion_url', models.URLField()),
                ('redirect_url', models.URLField()),
                ('screenshot_850px', models.URLField()),
                ('slug', models.SlugField(unique=True)),
                ('_real_domain', models.CharField(max_length=255, blank=True, null=True)),
                ('details', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
