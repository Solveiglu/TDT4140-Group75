from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^questions$', views.listQuestions, name='list-questions'),

    url(r'^questions/(?P<questionId>[0-9]+)/$', views.showQuestion, name='show-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/answer/$', views.answer, name='answer'),

    url(r'^questions/new', views.newQuestion, name='new-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/edit', views.editQuestion, name='edit-question'),

    url(r'^questions/(?P<questionId>[0-9]+)/delete', views.deleteQuestion, name='delete-question'),

    url(r'^new$', views.createAssignment, name='new-assignment'),

    url(r'^new-private$', views.createPrivateAssignment, name='new-private-assignment'),

    url(r'^(?P<assignmentId>[0-9]+)$', views.viewAssignment, name='assignment'),

    url(r'^show/(?P<assignmentId>[0-9]+)', views.showAssignment, name='show-assignment'),

    url(r'^(?P<assignmentId>[0-9]+)/edit', views.editAssignment, name='edit-assignment'),

    url(r'^(?P<assignmentId>[0-9]+)/delete', views.deleteAssignment, name='delete-assignment'),
]



