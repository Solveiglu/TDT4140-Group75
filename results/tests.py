from django.test import TestCase
from assignments.models import *
from results.models import *
from django.contrib.auth.models import User


class testTakentest(TestCase):
    def setUp(self):
        Subject.objects.create(subjectName = 'testSubject')
        Question.objects.create(questionText = 'testtesttest',subject = Subject.objects.get(subjectName = 'testsubject'))
        Answer.objects.create(answerText ='test', isCorrect = True, question = Question.objects.get(id=1))
        Assignment.objects.create(assignmentName = 'studentTest', deadline = '2017-03-26 23:59:000', questions = Question.objects.get(id=1), description = 'test', passingGrade = 80, owner = User.objects.create(username ='testStudent'))
        FinishedAssignment.objects.create(user = User.objects.get(username = 'testStudent'), assignment = Assignment.objects.get(assignmentName = 'studentTest'), answers = Answer.objects.get(answerText = 'test'))


    def testCorrectResult(self):

        assignment = Assignment.objects.get(assignmentName = 'studentTest')
        finished = FinishedAssignment.objects.get(id = 1)
        answer = Answer.objects.get(answerText = 'test')
        self.assertEqual(finished.assignment, assignment)
        self.assertEqual(finished.answers.get(), answer)