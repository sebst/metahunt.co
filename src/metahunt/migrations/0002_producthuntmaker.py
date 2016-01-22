# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHuntMaker',
            fields=[
                ('ph_id', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('made', models.ManyToManyField(to='metahunt.ProductHunt', related_name='makers')),
            ],
        ),
    ]
