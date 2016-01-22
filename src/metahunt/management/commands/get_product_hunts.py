import json
from django.core.management.base import BaseCommand
from metahunt.models import *
from metahunt.datagainer import *

import datetime


from threading import Thread

import time

from  concurrent.futures import ThreadPoolExecutor


class Command(BaseCommand):
	args = ''
	help = 'Retrieves Product Hunts'

	def handle(self, *args, **options):
		#return
		start_date = datetime.date(2013, 11, 24)
		#start_date = datetime.date(2015, 4, 29)
		now = datetime.date.today()+datetime.timedelta(days=1)
		#now = start_date + datetime.timedelta(days=3)

		day = start_date
		threads = []

		executor = ThreadPoolExecutor(max_workers=32)

		while day < now:
			print (day)
			try:
				pass
				#gain(day.strftime('%Y-%m-%d'))
				#t = Thread(target=gain, args=(day.strftime('%Y-%m-%d'),))
				#threads.append( t   )
				#t.start()
				#time.sleep(1)
				executor.submit (gain, day.strftime('%Y-%m-%d'))

			except Exception as e:
				print(e)
				pass
			day += datetime.timedelta(days=1)

		#for x in threads:
		#	print (x)
		#	x.join()