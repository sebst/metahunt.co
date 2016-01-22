# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0004_betalistproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='betalistproduct',
            name='day',
            field=models.DateField(null=True),
        ),
    ]
