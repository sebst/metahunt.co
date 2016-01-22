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
        


        # Product Hunt started
        milestone = ProductHuntMilestone(
                day = MIN_DAY, 
                typ = "!started",
                iteration = 0
            )

        milestone.save()

        # doubling the user base
        daystat_start = ProductHuntDayStatistics.objects.get(day=MIN_DAY)
        last_num_users = daystat_start.num_users
        iteration = 0
        while True:
            try:
                ds = ProductHuntDayStatistics.objects.filter(num_users__gte=2*last_num_users).order_by('day')[0]
            except Exception as e:
                break
            last_num_users = ds.num_users
            milestone = ProductHuntMilestone(
                    day = ds.day,
                    typ = "users_doubled",
                    num = ds.num_users,
                    iteration = iteration
                )
            milestone.save()
            iteration += 1

        last_num_featured = daystat_start.num_featured_sum
        iteration = 0
        while True:
            try:
                ds = ProductHuntDayStatistics.objects.filter(num_featured_sum__gte=2*last_num_featured).order_by('day')[0]
            except Exception as e:
                break
            last_num_featured = ds.num_featured_sum
            milestone = ProductHuntMilestone(
                    day = ds.day,
                    typ = "products_doubled",
                    num = ds.num_featured_sum,
                    iteration = iteration
                )
            milestone.save()
            iteration += 1

        ranks = ProductHuntLeaderBoardStatistics.objects.all().order_by('rank_num')[:10]
        for rank in ranks:
            milestone = ProductHuntMilestone(
                    day = rank.hunt.day,
                    typ = "top10_num",
                    iteration = rank.rank_num,
                    hunt = rank.hunt,
                    num = rank.num_votes
                )
            milestone.save()

        ranks = ProductHuntLeaderBoardStatistics.objects.all().order_by('rank_ratio')[:10]
        for rank in ranks:
            milestone = ProductHuntMilestone(
                    day = rank.hunt.day,
                    typ = "top10_ratio",
                    iteration = rank.rank_ratio,
                    hunt = rank.hunt,
                    num = rank.ratio_votes
                )
            milestone.save()
        ranks = ProductHuntLeaderBoardStatistics.objects.all().order_by('rank_reach')[:10]
        for rank in ranks:
            milestone = ProductHuntMilestone(
                    day = rank.hunt.day,
                    typ = "top10_reach",
                    iteration = rank.rank_reach,
                    hunt = rank.hunt,
                    num = rank.reach_votes_all
                )
            milestone.save()


        ds = ProductHuntDayStatistics.objects.all().order_by('-num_new_users')[0]
        milestone = ProductHuntMilestone(
            day=ds.day,
            typ="max_new_users",
            iteration=0,
            num=ds.num_new_users
            )
        milestone.save()
        ds = ProductHuntDayStatistics.objects.all().order_by('-num_featured')[0]
        milestone = ProductHuntMilestone(
            day=ds.day,
            typ="max_featured",
            iteration=0,
            num=ds.num_featured
            )
        milestone.save()



