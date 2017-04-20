from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^results/results', views.results, name='results'),
    url(r'^results/professorResults', views.professorResults, name='professorResults')
]



