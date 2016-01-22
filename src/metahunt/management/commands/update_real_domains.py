import json
from django.core.management.base import BaseCommand
from metahunt.models import *
from metahunt.datagainer import *

import datetime


from threading import Thread

import time

from  concurrent.futures import ThreadPoolExecutor


def update_P(P):
	P._get_real_domain()
	P.save()
	return P


class Command(BaseCommand):
	args = ''
	help = 'Retrieves Product Hunts'

	def handle(self, *args, **options):
		executor = ThreadPoolExecutor(max_workers=2)

		hunts = ProductHunt.objects.filter(_real_domain__isnull=True).order_by('-day')
		for P in hunts:
			executor.submit (update_P, P)