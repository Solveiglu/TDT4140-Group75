from django.db import models
from django.contrib.auth.models import User
from assignments.models import Question
import assignments


class questionResult(models.Model):
    result = models.BooleanField(null=False)
    user = models.ForeignKey(to=User, related_name="results", blank=True, null=True)
    question = models.ForeignKey(Question, related_name='result')

class finishedAssignment(models.Model):
    assignment = models.ForeignKey(assignments.models.Assignment, related_name='assignment')
    finished = models.DateTimeField(null=True)
    answers = models.ManyToManyField(assignments.models.Answer)