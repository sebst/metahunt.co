# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0002_producthuntmaker'),
    ]

    operations = [
        migrations.CreateModel(
            name='AngellistCompany',
            fields=[
                ('ac_id', models.IntegerField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('_details', models.TextField(null=True, blank=True)),
                ('_jobs_json', models.TextField()),
                ('_real_domain', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
