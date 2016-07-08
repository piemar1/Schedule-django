# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.main_page, name='main_page'),

    url(r'^grafik_update/$', views.grafik_update, name='grafik_update'),
    url(r'^new_team/$', views.new_team, name='new_tem'),
    url(r'^new_schedule/$', views.new_schedule, name='new_schedule'),

    url(r'^(?P<pk>[0-9]+)/team/$', views.TeamDetailView.as_view(), name='team'),
    url(r'^(?P<pk>[0-9]+)/schedule/$', views.existed_schedule, name='existed_schedule'),

    url(r'^team_update/$', views.team_update, name='team_update'),
    url(r'^schedule_update/$', views.schedule_update, name='schedule_update'),

]
