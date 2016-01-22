# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0021_producthuntdaystatistics_num_comments_sump'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producthuntdaystatistics',
            old_name='num_comments_sump',
            new_name='num_comments_sum',
        ),
    ]
