# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0020_producthuntmilestone_days_since_last_iteration'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntdaystatistics',
            name='num_comments_sump',
            field=models.IntegerField(null=True),
        ),
    ]
