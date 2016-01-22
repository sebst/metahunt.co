from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils import timezone
from django.db.models import Min, Max, Sum, F

from .models import *

import datetime

import json

from collections import OrderedDict

from django.views.decorators.cache import cache_page


CACHE_DURATION = 60*30 # 30 mins
#CACHE_DURATION = CACHE_DURATION*24
#CACHE_DURATION=1

MIN_DAY = ProductHunt.objects.all().aggregate(Min('day'))['day__min']
MAX_DAY = ProductHunt.objects.all().aggregate(Max('day'))['day__max']

def prev(day, off=1):
	res = day - datetime.timedelta(days=off)
	if res < MIN_DAY or res > MAX_DAY:
		return None
	return res

def next(day, off=1):
	return prev(day, -off)



@cache_page(CACHE_DURATION)
def stats(request):


	

	ld = ProductHuntDayStatistics.objects.order_by('day').last()
	num_days = ProductHuntDayStatistics.objects.all().count()

	by_week_day = ProductHuntDayStatistics.objects.values('week_day').annotate(Sum('num_new_users'), Sum('num_featured'))

	by_weekday_dict = OrderedDict()

	products_7d = ProductHunt.objects.filter(day__gte=datetime.date.today()-datetime.timedelta(days=7))
	products_30d = ProductHunt.objects.filter(day__gte=datetime.date.today()-datetime.timedelta(days=30))
	

	for item in by_week_day:
		if item['week_day'] not in by_weekday_dict.keys():
			by_weekday_dict[item['week_day']] = {}
		by_weekday_dict[item['week_day']]['num_new_users'] = item['num_new_users__sum']
		by_weekday_dict[item['week_day']]['num_featured'] = item['num_featured__sum']

	

	betalist = ProductHunt.objects.filter(betalist_product__isnull=False)



	res = {
		'active': 'stats',
		

		'nums': {
			'users': ld.num_users,
			'featured': ld.num_featured_sum,
			'comments': ld.num_comments_sum,
			'votes': ld.num_votes_sum,
			'days': num_days
		},
		'avg': {
			'users': ld.num_users/num_days,
			'featured': ld.num_featured_sum/num_days,
			'votes': ld.num_votes_sum/num_days,
		},
		'by_week_day': by_weekday_dict,

		'products': {
			'7d': {
				'top': products_7d.order_by('-votes_count')[:5],
				'flop': products_7d.order_by('votes_count')[:5],
			},
			'30d': {
				'top': products_30d.order_by('-votes_count')[:5],
				'flop': products_30d.order_by('votes_count')[:5],
			},
		},

		'betalist': {
			'count': betalist.count(),
			'before': betalist.filter(betalist_product__published_at__lte=F('hunted_at')).count(),
			'after': betalist.filter(betalist_product__published_at__gte=F('hunted_at')).count(),
		}

	}


	

	#print(json.dumps(res))
	return render_to_response("metahunt/stats.html", 
								res, 
								context_instance=RequestContext(request))


	

@cache_page(CACHE_DURATION)
def ph_day_stats(request):
	stats = ProductHuntDayStatistics.objects.all().order_by('day')
	value_keys = ['num_featured', 'num_comments', 'num_votes', 'max_comments', 'max_votes', 'min_comments', 'min_votes', 'avg_comments', 'avg_votes', 'num_users', 'num_featured_sum', 'num_new_users']
	res = [ [ {'date': stat.day.strftime('%Y-%m-%d'), 'value': getattr(stat, value_key)} for stat in stats ] for value_key in value_keys]
	return HttpResponse(json.dumps(res))

	#stats = {i.day.strftime('%Y-%m-%d'): {j: getattr(i, j) for j in value_keys} for i in stats}
	#stats = OrderedDict(sorted(stats.items(), key=lambda t: t[0]))
	#return HttpResponse(json.dumps(stats))


@cache_page(CACHE_DURATION)
def milestones(request):

	milestones = ProductHuntMilestone.objects.all().order_by('day', 'typ').select_related('hunt')
	milestones_dict = OrderedDict()

	for milestone in milestones:
		month = milestone.day.strftime("%B %Y")
		if month in milestones_dict.keys():
			milestones_dict[month].append(milestone)
		else:
			milestones_dict[month] = [milestone,]

	print (milestones_dict)

	res = {
		'active': 'milestones',
		'milestones': milestones_dict
	}
	return render_to_response("metahunt/milestones.html", 
								res, 
								context_instance=RequestContext(request))

@cache_page(CACHE_DURATION)
def leaderboard(request):
	n = 500
	res = {
		'active': 'leaderboard',
		'n': n,
		'lb_alltime': ProductHuntLeaderBoardStatistics.objects.all().order_by('-num_votes').select_related('hunt')[:n],
		'lb_reach': ProductHuntLeaderBoardStatistics.objects.all().order_by('-reach_votes_all').select_related('hunt')[:n],
		'lb_ratio': ProductHuntLeaderBoardStatistics.objects.all().order_by('-ratio_votes').select_related('hunt')[:n],

	}
	return render_to_response("metahunt/leaderboard.html", 
								res, 
								context_instance=RequestContext(request))


@cache_page(CACHE_DURATION)
def timemachine(request):
	today = timezone.now().date()
	if 'day' in request.GET.keys():
		try:
			day = datetime.datetime.strptime(request.GET['day'], '%Y%m%d').date()
		except:
			return HttpResponseRedirect("/timemachine")
		
	else:
		day = today.replace(year=today.year-1)
		ago = "One year"
		return HttpResponseRedirect("?day=%s"%(day.strftime('%Y%m%d')))

	if day < MIN_DAY or day > MAX_DAY:
		return HttpResponseRedirect("?day=%s"%(MAX_DAY.strftime('%Y%m%d')))

	days_left = (today-day).days 
	ago = "%s days ago" % (days_left) if day != today.replace(year=today.year-1) else "One year ago"
	if days_left==1: ago = "Yesterday"
	if (days_left%7)==0:
		if (days_left/7)==1:
			ago = "Last week"
		else:
			ago = "%.0f weeks ago"%(days_left/7)
	if days_left==0: ago = "Today"

	hunts = ProductHunt.objects.filter(day=day).order_by('-votes_count')

	print(day, next(day), prev(day))


	res = {
		'active': 'timemachine',
		'today': today,
		'day': day,
		'prev': prev(day),
		'next': next(day),
		'hunts': hunts,
		'ago': ago,

		'before': {
			'start': MIN_DAY,
			'1y': today.replace(year=today.year-1),
			'7d': prev(today, 7)
		}
	}
	return render_to_response("metahunt/timemachine.html", 
								res, 
								context_instance=RequestContext(request))


@cache_page(CACHE_DURATION)
def index(request):
	res = {
		'active': 'index',
	}
	return render_to_response("metahunt/index.html", 
								res, 
								context_instance=RequestContext(request))	


@cache_page(CACHE_DURATION)
def about(request):
	res = {
		'active': 'about',
	}
	return render_to_response("metahunt/about.html", 
								res, 
								context_instance=RequestContext(request))

@cache_page(CACHE_DURATION)
def hunt(request, slug):

	ph = get_object_or_404(ProductHunt, slug=slug)

	res = {
		'active': 'hunt',
		'hunt': ph
	}

	return render_to_response("metahunt/hunt.html", 
								res, 
								context_instance=RequestContext(request))