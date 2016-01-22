import json
from django.core.management.base import BaseCommand
from metahunt.models import *

class Command(BaseCommand):
	args = ''
	help = 'Reads the dump from crunchbase'

	def handle(self, *args, **options):
		#return
		f = open("/Users/sebst/Code/ph-oneyearafter/crunchbase_odm_json_v101/organizations.json", 'r')
		orgs = json.load(f)['root']
		for org in orgs:
			o = CrunchBaseODMOrganization(**org)
			o.save()
		return
		f = open("/Users/sebst/Code/ph-oneyearafter/crunchbase_odm_json_v101/people.json", 'r')
		orgs = json.load(f)['root']
		for org in orgs:
			o = CrunchBaseODMPerson(**org)
			o.save()



