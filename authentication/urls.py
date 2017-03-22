from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^authentication/signup', views.signup, name='signup'),

]



