# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0012_producthuntdaystatistics_num_featured_sum'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHuntLeaderBoardStatistics',
            fields=[
                ('hunt', models.OneToOneField(primary_key=True, serialize=False, to='metahunt.ProductHunt')),
                ('num_comments', models.IntegerField(null=True)),
                ('num_votes', models.IntegerField(null=True)),
                ('reach_votes_all', models.FloatField(null=True)),
                ('ratio_votes', models.FloatField(null=True)),
            ],
        ),
    ]
