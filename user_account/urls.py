__author__ = 'Marcin Pieczyński'

from django.conf.urls import url
from django.views.generic import TemplateView

from user_account import views


urlpatterns = [
    url(r'^$', views.NewUserView.as_view(), name='register'),
    url(r'^success/$', TemplateView.as_view(template_name="user_account/success.html"), name='success_created'),
    url(r'^activate/(?P<activation_key>\w+)/$', views.activate),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^home/$', views.home_view, name='home'),
    url(r'^user_edit/$', views.edit_user_view, name='user_edit')
]

