# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0013_producthuntleaderboardstatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntdaystatistics',
            name='num_new_users',
            field=models.IntegerField(null=True),
        ),
    ]
