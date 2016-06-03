# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from django.conf.urls import url
from . import views


urlpatterns = [
    # ex: /polls/
    url(r'^$', views.main_page, name='main_page'),
    url(r'^grafik_update/$', views.grafik_update, name='grafik_update'),
    url(r'^team_update/$', views.team_update, name='team_update'),
    url(r'^(?P<pk>[0-9]+)/read_team/$', views.TeamDetailView.as_view(), name='read_team'),

]
