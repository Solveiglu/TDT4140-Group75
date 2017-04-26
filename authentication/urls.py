
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as authViews
from django.views.generic.base import TemplateView


from . import views

urlpatterns = [
    url(r'^signup', views.signup, name='signup'),

    url(r'^login/$', authViews.login, {'template_name': 'authentication/login.html'}, name='login'),

    url(r'^logout/$', authViews.logout, {'template_name': 'authentication/logout.html'}, name='logout'),
]



