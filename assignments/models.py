from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.



class Subject(models.Model):
    subjectName = models.TextField(null=False)

    def __str__(self):
        return self.subjectName

class Question(models.Model):
    questionText = models.TextField(null=False)

    subject = models.ForeignKey(Subject, related_name='questions')

    def next_id(self):
        next = Question.objects.filter(id__gt=self.id).order_by('id').first()
        if next:
            return next.id
        else:
            return None

    def __str__(self):
        return self.questionText


class Assignment(models.Model):
    assignmentName = models.CharField(null=False, max_length=75, default="oving")
    deadline = models.DateTimeField(null=True, default=timezone.now)
    questions = models.ManyToManyField(Question)
    description = models.TextField(null=False)
    # owner = None means that every user can access the assignment
    owner = models.ForeignKey(User, related_name='assignments', null=True)
    passingGrade = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return self.assignmentName

class Answer(models.Model):
    answerText = models.TextField(null=False, blank=True)
    isCorrect = models.BooleanField(null=False)
    question = models.ForeignKey(Question, related_name='answers')

    def __str__(self):
        return self.answerText
