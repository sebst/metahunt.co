# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0018_auto_20150505_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntleaderboardstatistics',
            name='rank_avg',
            field=models.FloatField(null=True),
        ),
    ]
