# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0003_angellistcompany'),
    ]

    operations = [
        migrations.CreateModel(
            name='BetalistProduct',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('published_at', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('website_url', models.URLField()),
                ('pitch', models.TextField()),
                ('url', models.URLField()),
                ('_real_domain', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
    ]
