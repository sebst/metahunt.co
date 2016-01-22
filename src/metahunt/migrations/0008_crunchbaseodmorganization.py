# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metahunt', '0007_producthunt_angellist_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrunchBaseODMOrganization',
            fields=[
                ('crunchbase_uuid', models.UUIDField(serialize=False, primary_key=True)),
                ('type', models.CharField(default='Organization', max_length=255)),
                ('primary_role', models.CharField(default='company', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('crunchbase_url', models.URLField(blank=True, null=True)),
                ('homepage_domain', models.CharField(max_length=255, blank=True, null=True, db_index=True)),
                ('homepage_url', models.URLField(blank=True, null=True, max_length=255)),
                ('profile_image_url', models.URLField(blank=True, null=True, max_length=255)),
                ('twitter_url', models.URLField(blank=True, null=True, max_length=255)),
                ('linkedin_url', models.URLField(blank=True, null=True, max_length=255)),
                ('facebook_url', models.URLField(blank=True, null=True, max_length=255)),
                ('location_city', models.CharField(blank=True, null=True, max_length=255)),
                ('location_region', models.CharField(blank=True, null=True, max_length=255)),
                ('location_country_code', models.CharField(blank=True, null=True, max_length=255)),
                ('short_description', models.CharField(blank=True, null=True, max_length=255)),
                ('stock_symbol', models.CharField(blank=True, null=True, max_length=32)),
                ('_crunchbase_permalink', models.CharField(blank=True, null=True, max_length=255)),
                ('_twitter_handle', models.CharField(blank=True, null=True, max_length=255)),
            ],
        ),
    ]
