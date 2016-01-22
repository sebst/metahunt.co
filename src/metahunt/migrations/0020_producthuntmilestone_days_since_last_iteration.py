# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0019_producthuntleaderboardstatistics_rank_avg'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntmilestone',
            name='days_since_last_iteration',
            field=models.IntegerField(null=True),
        ),
    ]
