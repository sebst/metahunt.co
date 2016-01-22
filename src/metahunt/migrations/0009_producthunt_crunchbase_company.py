# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0008_crunchbaseodmorganization'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthunt',
            name='crunchbase_company',
            field=models.ForeignKey(to='metahunt.CrunchBaseODMOrganization', null=True),
        ),
    ]
