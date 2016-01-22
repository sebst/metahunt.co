import json
from django.core.management.base import BaseCommand
from metahunt.models import *
from django.db.models import Min, Max


import datetime

class Command(BaseCommand):
    args = ''
    help = 'Retrieves Product Hunts'

    def handle(self, *args, **options):
        MIN_DAY = ProductHunt.objects.all().aggregate(Min('day'))['day__min']
        MAX_DAY = ProductHunt.objects.all().aggregate(Max('day'))['day__max']
        day = MIN_DAY
        while True:
            #break
            ProductHuntDayStatistics(day=day)._update_stats()
            day = day+datetime.timedelta(days=1)
            if day > MAX_DAY:
                break
        hunts = ProductHunt.objects.all()
        for hunt in hunts:
            lb_stat = ProductHuntLeaderBoardStatistics(hunt=hunt)
            lb_stat._update_stats()
            #print(hunt.pk)


        objs = ProductHuntLeaderBoardStatistics.objects.all().order_by('-num_votes')
        for i, obj in enumerate(objs):
            obj.rank_num = i+1
            obj.save()

        objs = ProductHuntLeaderBoardStatistics.objects.all().order_by('-reach_votes_all')
        for i, obj in enumerate(objs):
            obj.rank_reach = i+1
            obj.save()

        objs = ProductHuntLeaderBoardStatistics.objects.all().order_by('-ratio_votes')
        for i, obj in enumerate(objs):
            obj.rank_ratio = i+1

            obj.rank_avg = obj.rank_num/3 + obj.rank_reach/3 + obj.rank_ratio/3

            obj.save()