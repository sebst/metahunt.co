from django.db import models

import json, urllib
from urllib.parse import urlparse

from .apis import ANGEL

import datetime

import requests

def find_angel_co(name, url, max_api_calls=2):
	# mindie.co!
	# itunes etc.
	res = []
	api_calls = 0

	if api_calls<max_api_calls:
		res.append(ANGEL.search({'method':'GET', 'query':url, 'type':'Startup'}))
		if len(res[api_calls])==1:
			return res[api_calls][0]
		api_calls += 1

	if api_calls<max_api_calls:
		res.append(ANGEL.search({'method':'GET', 'query':"www."+url, 'type':'Startup'}))
		if len(res[api_calls])==1:
			return res[api_calls][0]
		api_calls += 1

	if api_calls<max_api_calls:
		res.append(ANGEL.search({'method':'GET', 'query':name, 'type':'Startup'}))
		if len(res[api_calls])==1:
			return res[api_calls][0]
		api_calls += 1

	return None





class ProductHunt(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	ph_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=255)
	tagline = models.CharField(max_length=255)
	day = models.DateField()
	hunted_at = models.DateTimeField()
	ph_featured = models.BooleanField()
	comments_count = models.IntegerField()
	votes_count = models.IntegerField()
	discussion_url = models.URLField()
	redirect_url = models.URLField()
	screenshot_850px = models.URLField()
	slug = models.SlugField(unique=True)

	_real_domain = models.CharField(max_length=255, null=True, blank=True)

	details = models.TextField(null=True, blank=True)

	angellist_company = models.ForeignKey('AngellistCompany', null=True)
	crunchbase_company = models.ForeignKey('CrunchBaseODMOrganization', null=True)
	betalist_product = models.ForeignKey('BetalistProduct', null=True)


	hour = models.PositiveSmallIntegerField(null=True)



	def _get_real_domain(self):
		#exc: itunes, chrome.google, play.google, kickstarter, github, mailchimp, amazon.com, indiegogo, appspot, youtube, blogspot
		if self._real_domain:
			return self._real_domain
		try:
			url = self.redirect_url
			user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
			"""
			u = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': user_agent}))
			url = u.geturl()
			o = urllib.parse.urlparse(url)
			self._real_domain = o.hostname.replace("www.", "")
			"""
			headers = {'User-Agent': user_agent}
			#headers = {}
			r = requests.get(url, allow_redirects=False, headers=headers)
			url = r.headers['location']
			o = urllib.parse.urlparse(url)
			self._real_domain = o.hostname.replace("www.", "")
			#self.save()
			return self._real_domain
		except Exception as e:
			print ("did not get url for", self.name, e)
			pass
		return self._real_domain



	@property
	def real_domain(self):
		return self._real_domain

	def save(self, *args, **kwargs):
		return super(ProductHunt, self).save(*args, **kwargs)

	@property
	def details_dict(self):
		try:
			return json.loads(self.details)
		except:
			return {}

	def _update_makers(self):
		added_makers = []
		for maker in self.details_dict['makers']:
			_id = maker['id']
			_username = maker['username']

			try:
				M = ProductHuntMaker.objects.get(pk=_id)
			except:
				return 
				M = ProductHuntMaker()

			M.username = _username
			M.ph_id = _id
			M.save()
			
			M.made.add(self)
			added_makers.append(M)
			M.save()

		already = self.makers.all().exclude(pk__in=[i.pk for i in added_makers])
		for maker in already:
			maker.made.remove(self)
			maker.save()


	def _update_angellist_company(self):
		if self._real_domain is not None:
			#res = ANGEL.search({'method':'GET', 'query':self._real_domain, 'type':'Startup'})
			res = find_angel_co(self.name, self._real_domain)
			print(res)
			#_id = res[0]['id']
			try:
				print (res['name'], "found", self._real_domain)

				try:
					A = AngellistCompany.objects.get(_real_domain = self._real_domain)
				except:
					A = AngellistCompany()

				A.ac_id = res['id']
				A._details = json.dumps(res)
				A._jobs_json = "[]"
				A._real_domain = self._real_domain
				A.save()

				self.angellist_company = A 
				self.save()


			except Exception as e:
				print ("nothing found", self._real_domain, e)
		else:
			print ("domain none")


	def _update_crunchbase_company(self):
		r = CrunchBaseODMOrganization.objects.filter(homepage_domain=self._real_domain)
		if len(r)==1:
			self.crunchbase_company = r[0]
			self.save()


	def _update_betalist_product(self):
		try:
			b = BetalistProduct.objects.get(_real_domain__contains=self._real_domain)
		except:
			return
		self.betalist_product = b





class ProductHuntMaker(models.Model):
	ph_id = models.IntegerField(primary_key=True)
	username = models.CharField(max_length=255)

	signed_up_at = models.DateTimeField(null=True)

	made = models.ManyToManyField(ProductHunt, related_name='makers')


class AngellistCompany(models.Model):
	#hunt = models.ForeignKey(ProductHunt, primary_key=True, related_name="angelco")
	ac_id = models.IntegerField(primary_key = True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	_details = models.TextField(null=True, blank=True)

	_jobs_json = models.TextField()

	_real_domain = models.CharField(max_length=255, unique=True)






class BetalistProduct(models.Model):
	published_at = models.DateTimeField()
	name = models.CharField(max_length=255)
	website_url = models.URLField()
	pitch = models.TextField()
	url = models.URLField()
	day = models.DateField(null=True)


	_real_domain = models.CharField(max_length=255, null=True, blank=True)

	def save(self, *args, **kwargs):
		o = urllib.parse.urlparse(self.website_url)
		self._real_domain = o.hostname
		#self._real_domain = self._real_domain.replace("www.", "")
		self._real_domain = self._real_domain.replace("beta.", "")
		#self.clean()
		#self.day = self.published_at.date()
		return super(BetalistProduct, self).save(*args, **kwargs)












class CrunchBaseODMOrganization(models.Model):
	crunchbase_uuid = models.UUIDField(primary_key=True)
	type = models.CharField(max_length=255, default='Organization')
	primary_role = models.CharField(max_length=255, default="company")
	name = models.CharField(max_length=255)
	crunchbase_url = models.URLField(null=True, blank=True)
	homepage_domain = models.CharField(max_length=255, null=True, blank=True, db_index=True)
	homepage_url = models.URLField(null=True, blank=True, max_length=255)
	profile_image_url = models.URLField(null=True, blank=True, max_length=255)
	twitter_url = models.URLField(null=True, blank=True, max_length=255)
	linkedin_url = models.URLField(null=True, blank=True, max_length=255)
	facebook_url = models.URLField(null=True, blank=True, max_length=255)
	location_city = models.CharField(max_length=255, null=True, blank=True)
	location_region = models.CharField(max_length=255, null=True, blank=True)
	location_country_code = models.CharField(max_length=255, null=True, blank=True)
	short_description = models.CharField(max_length=255, null=True, blank=True)
	stock_symbol = models.CharField(max_length=32, null=True, blank=True)

	_crunchbase_permalink = models.CharField(max_length=255, null=True, blank=True)
	_twitter_handle = models.CharField(max_length=255, null=True, blank=True)


	def __str__(self):
		return self.crunchbase_url

	@property
	def has_location(self):
		return self.location_city is not None and self.location_region is not None and self.location_country_code is not None

	@property
	def crunchbase_permalink(self):
		if self._crunchbase_permalink is not None:
			return self._crunchbase_permalink
		try:
			return urlparse(self.crunchbase_url).path.split('/')[-1]
		except:
			return ""

	@property
	def twitter_handle(self):
		if self._twitter_handle is not None:
			return self._twitter_handle
		try:
			return urlparse(self.twitter_url).path.split('/')[-1]
		except:
			return ""

	@property
	def details(self):
		if self._details.count()>0:
			return json.loads(self._details.all()[0].details)
		else:
			r = json.dumps(CRUNCH.organization({'method':'GET', 'id':self.crunchbase_permalink}))
			_ = CrunchBaseOrganizationDetails(organization=self, details=r)
			_.save()
			return _



	def save(self, *args, **kwargs):
		
		self._crunchbase_permalink = self.crunchbase_permalink
		self._twitter_handle = self.twitter_handle
		return super(CrunchBaseODMOrganization, self).save(*args, **kwargs)


weekdays = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

from django.db.models import Sum

class ProductHuntDayStatistics(models.Model):
	day = models.DateField(primary_key=True)
	week_day = models.CharField(max_length=16, null=True, choices=((i, i) for i in weekdays))
	num_featured = models.IntegerField(null=True)
	num_comments = models.IntegerField(null=True)
	num_votes = models.IntegerField(null=True)
	max_comments = models.IntegerField(null=True)
	max_votes = models.IntegerField(null=True)
	min_comments = models.IntegerField(null=True)
	min_votes = models.IntegerField(null=True)
	avg_comments = models.FloatField(null=True)
	avg_votes = models.FloatField(null=True)

	num_users = models.IntegerField(null=True)

	num_featured_sum = models.IntegerField(null=True)

	num_new_users = models.IntegerField(null=True)

	num_comments_sum = models.IntegerField(null=True)
	num_votes_sum = models.IntegerField(null=True)

	def _update_stats(self):
		hunts = ProductHunt.objects.filter(day=self.day)
		self.num_featured = len(hunts)
		if self.num_featured == 0:
			self.num_comments = None
			self.num_votes = None

			self.max_comments = None
			self.max_votes = None

			self.min_comments = None
			self.min_votes = None

			avg_comments = None
			avg_votes = None
		else:
			self.num_comments = sum([i.comments_count for i in hunts])
			self.num_votes = sum([i.votes_count for i in hunts])

			self.max_comments = max([i.comments_count for i in hunts])
			self.max_votes = max([i.votes_count for i in hunts])

			self.min_comments = min([i.comments_count for i in hunts])
			self.min_votes = min([i.votes_count for i in hunts])

			self.avg_comments = self.num_comments / self.num_featured
			self.avg_votes = self.num_votes / self.num_featured


		self.week_day = weekdays[self.day.weekday()]

		self.num_users = ProductHuntMaker.objects.filter(signed_up_at__isnull=False, signed_up_at__lte=datetime.datetime.combine(self.day, datetime.time.max)).count()
		self.num_featured_sum = ProductHunt.objects.filter(day__lte=self.day).count()

		self.num_comments_sum = ProductHuntDayStatistics.objects.filter(day__lte=self.day).aggregate(Sum('num_comments'))['num_comments__sum']
		self.num_votes_sum = ProductHuntDayStatistics.objects.filter(day__lte=self.day).aggregate(Sum('num_votes'))['num_votes__sum']

		self.num_new_users = ProductHuntMaker.objects.filter(signed_up_at__isnull=False, signed_up_at__range=(datetime.datetime.combine(self.day, datetime.time.min), datetime.datetime.combine(self.day, datetime.time.max))).count()


		self.save()

class ProductHuntLeaderBoardStatistics(models.Model):
	hunt = models.OneToOneField(ProductHunt, primary_key=True, related_name='lb_stats')

	num_comments = models.IntegerField(null=True)
	num_votes = models.IntegerField(null=True)

	reach_votes_all = models.FloatField(null=True)
	ratio_votes = models.FloatField(null=True)

	rank_num = models.IntegerField(null=True)
	rank_reach = models.IntegerField(null=True)
	rank_ratio = models.IntegerField(null=True)

	rank_avg = models.FloatField(null=True)

	def _update_stats(self):
		self.num_comments = self.hunt.comments_count
		self.num_votes = self.hunt.votes_count

		daystat = ProductHuntDayStatistics.objects.get(day=self.hunt.day)

		self.reach_votes_all = self.num_votes / daystat.num_users
		self.ratio_votes = self.num_votes / daystat.num_votes

		self.save()

		
		"""
		n=25
		objs = ProductHuntLeaderBoardStatistics.objects.all().order_by('-num_votes')[:n]
		for i, obj in enumerate(objs):
			if obj == self:
				self.rank_num = i+1

				ps = ProductHuntLeaderBoardStatistics.objects.filter(rank_num=i+1)
				for i in ps:
					if i!=self:
						i.rank_num = None
						i.save()


				self.save()
				break
		objs = ProductHuntLeaderBoardStatistics.objects.all().order_by('-reach_votes_all')[:n]
		for i, obj in enumerate(objs):
			if obj == self:
				self.rank_reach = i+1

				ps = ProductHuntLeaderBoardStatistics.objects.filter(rank_reach=i+1)
				for i in ps:
					if i!=self:
						i.rank_reach = None
						i.save()

				self.save()
				break
		objs = ProductHuntLeaderBoardStatistics.objects.all().order_by('-ratio_votes')[:n]
		for i, obj in enumerate(objs):
			if obj == self:
				self.rank_ratio = i+1

				ps = ProductHuntLeaderBoardStatistics.objects.filter(rank_ratio=i+1)
				for i in ps:
					if i!=self:
						i.rank_ratio = None
						i.save()

				self.save()
				break
		"""



	@property
	def ratio_votes_pct(self):
		return "%.0f%%"%(self.ratio_votes*100)

	@property
	def reach_votes_all_pct(self):
		return "%.0f%%"%(self.reach_votes_all*100)


class ProductHuntMilestone(models.Model):
	day = models.DateField()
	typ = models.CharField(max_length=32 ) #choices = ( (i,i) for i in []  )
	iteration = models.PositiveSmallIntegerField(default=0)
	hunt = models.ForeignKey(ProductHunt, null=True)
	num = models.FloatField(null=True)
	text = models.TextField(null=True)

	days_since_last_iteration = models.IntegerField(null=True)

	@property
	def day_stats(self):
		return ProductHuntDayStatistics.objects.get(day=self.day)

	def save(self, *args, **kwargs):
		if self.pk is None:
			try:
				pk = ProductHuntMilestone.objects.get(typ=self.typ, iteration=self.iteration).pk
			except:
				pk = None
			self.pk = pk


		if self.iteration>0:
			try:
				last = ProductHuntMilestone.objects.get(typ=self.typ, iteration=self.iteration-1)
				self.days_since_last_iteration = (self.day-last.day).days
			except Exception as e:
				print(e)
				print(self.typ)

		return super(ProductHuntMilestone, self).save(*args, **kwargs)