from django.conf.urls import url

from . import views

# dersom man skriver ...../questions får man opp listen med alle spørsmål
urlpatterns = [
    url(r'^results/resultslist', views.listResults, name='results'),


]



