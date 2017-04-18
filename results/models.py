from django.contrib.auth.models import User
from assignments.models import Question
import assignments
from django.db import models


class QuestionResult(models.Model):
    result = models.BooleanField(null=False)
    user = models.ForeignKey(to=User, related_name="results", blank=True, null=True)
    question = models.ForeignKey(Question, related_name='result')

class FinishedAssignment(models.Model):
    assignment = models.ForeignKey(assignments.models.Assignment, related_name='assignment')
    answer = models.ManyToManyField(assignments.models.Answer, related_name='answersToAssignment')
    passed = models.BooleanField(null=False, default=False)
    score = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return self.assignment.assignmentName


    class Meta:
        managed = True