import json
from django.core.management.base import BaseCommand
from metahunt.models import *
from metahunt.datagainer import *

import datetime

class Command(BaseCommand):
	args = ''
	help = 'Retrieves Product Hunts'

	def handle(self, *args, **options):
		gain_ph_users()