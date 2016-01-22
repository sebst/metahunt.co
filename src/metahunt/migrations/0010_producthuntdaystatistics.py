# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0009_producthunt_crunchbase_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHuntDayStatistics',
            fields=[
                ('day', models.DateField(serialize=False, primary_key=True)),
                ('num_featured', models.IntegerField(null=True)),
                ('num_comments', models.IntegerField(null=True)),
                ('num_votes', models.IntegerField(null=True)),
                ('max_comments', models.IntegerField(null=True)),
                ('max_votes', models.IntegerField(null=True)),
                ('min_comments', models.IntegerField(null=True)),
                ('min_votes', models.IntegerField(null=True)),
                ('avg_comments', models.FloatField(null=True)),
                ('avg_votes', models.FloatField(null=True)),
            ],
        ),
    ]
