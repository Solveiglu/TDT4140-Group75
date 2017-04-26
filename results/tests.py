from django.test import TestCase
from assignments.models import *
from results.models import *
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.test import TestCase
from results.models import *
from django.urls import reverse


class resultsTestcase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user1.save()
        self.user2 = User.objects.create(username='user2')
        self.user2.save()
        self.student = Group.objects.create(name='Students')
        self.professor = Group.objects.create(name='Professors')
        self.user1.groups.add(self.student)
        self.user2.groups.add(self.professor)
        self.subject1 = Subject.objects.create(subjectName='testSubject')
        self.subject1.save()
        self.question1 = Question.objects.create(questionText='test1', subject=self.subject1)
        self.question1.save()
        self.question2 = Question.objects.create(questionText='test2', subject=self.subject1)
        self.question2.save()
        self.question3 = Question.objects.create(questionText='test3', subject=self.subject1)
        self.question3.save()
        self.answer1 = Answer.objects.create(answerText='test', isCorrect=True, question=Question.objects.get(id=1))
        self.answer1.save()
        self.answer2 = Answer.objects.create(answerText='test', isCorrect=True, question=Question.objects.get(id=2))
        self.answer2.save()
        self.answer3 = Answer.objects.create(answerText='test', isCorrect=False, question=Question.objects.get(id=3))
        self.answer3.save()
        self.assignment1 = Assignment.objects.create(assignmentName='studentTest', deadline='2017-03-26 23:59', description='test', passingGrade=80, owner=self.user1)
        self.assignment1.save()
        self.assignment1.questions.add(self.question1)
        self.assignment1.questions.add(self.question2)
        self.assignment1.questions.add(self.question3)
        self.assignment1.save()
        self.assignment2 = Assignment.objects.create(assignmentName='studentTest', deadline='2017-03-26 23:59', description='test', passingGrade=100, owner=self.user1)
        self.assignment2.save()
        self.assignment2.questions.add(self.question1)
        self.assignment2.questions.add(self.question2)
        self.assignment2.save()
        self.finishedassignment1 = FinishedAssignment.objects.create(user=self.user1, assignment=self.assignment1)
        self.finishedassignment2 = FinishedAssignment.objects.create(user=self.user1, assignment=self.assignment2)
        self.finishedassignment1.save()
        self.finishedassignment1.answers.add(self.answer1, self.answer2, self.answer3)
        self.finishedassignment2.save()
        self.finishedassignment2.answers.add(self.answer1, self.answer2)

    def test_CorrectAssignment(self):
        self.assertEqual(self.finishedassignment1.assignment, self.assignment1)
        self.assertEqual(self.finishedassignment2.assignment, self.assignment2)

    def test_passed(self):
        self.assertFalse(self.finishedassignment1.passed)
        self.assertTrue(self.finishedassignment2.passed)

    def test_score(self):
        self.assertEqual(round(self.finishedassignment1.score), round(2/3*100))
        self.assertEqual(self.finishedassignment2.score, 100.0)

    def test_professorResults(self):
        self.client.force_login(self.user1)
        url = reverse('professorResults',)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('results'))

    def test_results(self):
        self.client.force_login(self.user2)
        url = reverse('results',)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('professorResults'))