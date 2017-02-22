from django.db import models

# Create your models here.


class Question(models.Model):
    # Bruker TextField i stedet for CharField pga. ingen lengdebegrensning
    questionText = models.TextField(null=False)


class Answer(models.Model):
    answerText = models.TextField(null=False)
    isCorrect = models.BooleanField(null=False)

    # fremmednøkkel som peker på Question
    question = models.ForeignKey(Question, related_name='answers')
