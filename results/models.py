from django.contrib.auth.models import User
from assignments.models import Question
import assignments
from django.db import models


class FinishedAssignment(models.Model):
    user = models.ForeignKey(to=User, related_name="results", blank=True, null=True)
    assignment = models.ForeignKey(assignments.models.Assignment, related_name='assignment')
    answer = models.ManyToManyField(assignments.models.Answer, related_name='answersToAssignment')

    def __str__(self):
        return self.assignment.assignmentName

    @property
    def score(self):
        score = 0
        for answer in self.answers.all():
            if answer.isCorrect:
                score += 1
        return score

    @property
    def passed(self):
        return self.score >= self.assignment.passingGrade

    class Meta:
        managed = True
