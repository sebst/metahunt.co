# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0023_producthuntdaystatistics_num_votes_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthunt',
            name='betalist_product',
            field=models.ForeignKey(null=True, to='metahunt.BetalistProduct'),
        ),
        migrations.AlterField(
            model_name='producthuntleaderboardstatistics',
            name='hunt',
            field=models.OneToOneField(primary_key=True, to='metahunt.ProductHunt', serialize=False, related_name='lb_stats'),
        ),
    ]
