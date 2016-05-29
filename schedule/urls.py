from django.conf.urls import url
from . import views


urlpatterns = [
    # ex: /polls/
    url(r'^$', views.main_page, name='main_page'),
    url(r'^(?P<team_id>)$', views.grafik_update, name='grafik_update'),

]
