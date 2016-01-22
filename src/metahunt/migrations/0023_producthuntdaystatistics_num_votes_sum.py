# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0022_auto_20150505_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntdaystatistics',
            name='num_votes_sum',
            field=models.IntegerField(null=True),
        ),
    ]
