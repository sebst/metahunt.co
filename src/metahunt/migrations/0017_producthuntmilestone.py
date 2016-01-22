# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0016_auto_20150430_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHuntMilestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('day', models.DateField()),
                ('typ', models.CharField(max_length=32)),
                ('iteration', models.PositiveSmallIntegerField(default=0)),
                ('num', models.FloatField(null=True)),
                ('text', models.TextField(null=True)),
                ('hunt', models.ForeignKey(null=True, to='metahunt.ProductHunt')),
            ],
        ),
    ]
