# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0010_producthuntdaystatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthuntdaystatistics',
            name='num_users',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='producthuntmaker',
            name='signed_up_at',
            field=models.DateTimeField(null=True),
        ),
    ]
