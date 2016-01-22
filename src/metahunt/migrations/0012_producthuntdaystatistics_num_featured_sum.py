# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0011_auto_20150428_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntdaystatistics',
            name='num_featured_sum',
            field=models.IntegerField(null=True),
        ),
    ]
