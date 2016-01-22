# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0006_auto_20150427_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthunt',
            name='angellist_company',
            field=models.ForeignKey(null=True, to='metahunt.AngellistCompany'),
        ),
    ]
