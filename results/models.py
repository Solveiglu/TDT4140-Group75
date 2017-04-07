from django.db import models
from django.contrib.auth.models import User
from assignments.models import Question
import assignments


class FinishedAssignment(models.Model):
    user = models.ForeignKey(to=User, related_name="results", blank=True, null=True)
    assignment = models.ForeignKey(assignments.models.Assignment, related_name='assignment')
    finished = models.DateTimeField(null=True)
    answers = models.ManyToManyField(assignments.models.Answer)