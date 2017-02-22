from django.conf.urls import url

from . import views

# dersom man skriver ...../questions får man opp listen med alle spørsmål
urlpatterns = [
    url(r'^questions$', views.listQuestions, name='list-questions'),

    # (?P<question_id>[0-9]+) må skrives for å få tall. Kan nå skrive /questions/1, /questions/99, men ikke /questions/abc
    url(r'^questions/(?P<questionId>[0-9]+)$', views.showQuestion, name='show-question'),
]