# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0005_betalistproduct_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthunt',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 20, 41, 23, 763807, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producthunt',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 20, 41, 28, 451612, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
