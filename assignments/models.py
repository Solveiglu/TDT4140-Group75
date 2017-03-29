from django.db import models

# Create your models here.



class Subject(models.Model):
    subjectName = models.TextField(null=False)

    def __str__(self):
        return self.subjectName

class Question(models.Model):
    # Bruker TextField i stedet for CharField pga. ingen lengdebegrensning
    questionText = models.TextField(null=False)

    subject = models.ForeignKey(Subject, related_name='questions')

    def next_id(self):
        next = Question.objects.filter(id__gt=self.id).order_by('id').first()
        if next:
            return next.id
        else:
            return None

class Answer(models.Model):
    answerText = models.TextField(null=False, blank=True)
    isCorrect = models.BooleanField(null=False)

    # fremmednøkkel som peker på Question
    question = models.ForeignKey(Question, related_name='answers')

class Assignment(models.Model):
    assignmentName = models.CharField(null=False, max_length=75)
    deadline = models.DateTimeField()
    questions = models.ManyToManyField(Question)
    description = models.TextField(null=False)
