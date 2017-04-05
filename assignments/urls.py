from django.conf.urls import url

from . import views

# dersom man skriver ...../questions får man opp listen med alle spørsmål
urlpatterns = [
    url(r'^questions$', views.listQuestions, name='list-questions'),

    # (?P<question_id>[0-9]+) må skrives for å få tall. Kan nå skrive /questions/1, /questions/99, men ikke /questions/abc
    # url(r'^questions/(?P<questionId>[0-9]+)$', views.showQuestion, name='show-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/$', views.showQuestion, name='show-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/answer/$', views.answer, name='answer'),

    url(r'^questions/new', views.newQuestion, name='new-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/edit', views.editQuestion, name='edit-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/delete', views.deleteQuestion, name='delete-question'),
    url(r'^new$', views.createAssignment, name='new-assignment'),
    url(r'^new-private$', views.createPrivateAssignment, name='new-private-assignment'),

    url(r'^(?P<assignmentId>[0-9]+)$', views.viewAssignment, name='assignment'),
    url(r'^show/(?P<assignmentId>[0-9]+)', views.showAssignment, name='show-assignment')
]



