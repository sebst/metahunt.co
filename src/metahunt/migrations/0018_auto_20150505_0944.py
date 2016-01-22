# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0017_producthuntmilestone'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntleaderboardstatistics',
            name='rank_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='producthuntleaderboardstatistics',
            name='rank_ratio',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='producthuntleaderboardstatistics',
            name='rank_reach',
            field=models.IntegerField(null=True),
        ),
    ]
