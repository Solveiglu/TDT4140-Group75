from django.test import TestCase
from django.core.urlresolvers import resolve
from django.urls import reverse

from assignments.models import Question
from assignments.views import listQuestions, showQuestion
# Create your tests here.

class QuestionTestCase(TestCase):

    fixtures = ['test_questions.json']

    def test_urls(self):
        self.assertEqual(resolve('/assignments/questions').func, listQuestions)

    def test_listQuestions_view(self):
        url = reverse('list-questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['questions']), list(Question.objects.all()))

    def test_showQuestion_view(self):
        question = Question.objects.first()
        url = reverse('show-question', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question'], question)

    def test_next_id(self):
        question = Question.objects.get(id=1)
        self.assertEqual(question.next_id(), 2)
        question = Question.objects.get(id=2)
        self.assertEqual(question.next_id(), 5)
        question = Question.objects.get(id=5)
        self.assertEqual(question.next_id(), None)

    def test_answer(self):
        question = Question.objects.get(id=1)
        url = reverse('answer', args=(question.id,))
        response = self.client.post(url, {'answer': 1})
        self.assertIn('feil', response.context['error_message'].lower())
        response = self.client.post(url, {'answer': 2})
        self.assertIn('riktig', response.context['error_message'].lower())
        response = self.client.post(url, {'answer': 100})
        self.assertEqual(response.context['error_message'], "You didn't select an answer.")

    def test_newQuestion(self):
        # vanlig innsending av newQuestion
        # ingen korrekte svar
        # korrekt svar uten svarinnhold
        # duplikate svar
        pass

    def test_editQuestion(self):
        # endre et svaralternativ
        # endre slik at ingen svaralternativer er riktige
        # endre et spørsmål
        pass

    def test_deleteQuestion(self):
        # slett et spørsmål
        pass

    def test_createAssignment(self):
        # henter ut riktige spørsmål når man velger subject
        # lage assignment
        pass

    def test_createPrivateAssignment(self):
        # generere en assignment
        # sjekke at det blir riktig antall spørsmål
        # sjekke at den genererer fra riktig tema
        pass

    def test_viewAssignment(self):
        pass

    def test_showAssignment(self):
        pass

    def test_editAssignment(self):
        pass
