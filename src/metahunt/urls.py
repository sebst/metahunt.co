from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
                       url(r'^$', 'metahunt.views.index', name='index'),   
                       #url(r'^d/(?P<day>[0-9]{8})/$', 'metahunt.views.day', name='day'),   
                       url(r'^hunt/(?P<slug>[0-9A-Za-z_-]+)/$', 'metahunt.views.hunt', name='hunt'),
                       #url(r'^jobs$', 'metahunt.views.jobs', name='jobs'),

                       url(r'^about$', 'metahunt.views.about', name='about'),
                       url(r'^stats$', 'metahunt.views.stats', name='stats'),
                       url(r'^stats/ph_day_stats\.json$', 'metahunt.views.ph_day_stats', name='ph_day_stats'),

                       url(r'^$', 'metahunt.views.index', name='index'),   
                       url(r'^milestones$', 'metahunt.views.milestones', name='milestones'),
                       url(r'^leaderboard$', 'metahunt.views.leaderboard', name='leaderboard'),
                       url(r'^timemachine$', 'metahunt.views.timemachine', name='timemachine'),

                       )