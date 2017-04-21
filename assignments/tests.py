import datetime
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.urls import reverse

from assignments.models import Question, Answer, Subject
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
        self.assertEqual(question.next_id(), 6)
        question = Question.objects.get(id=6)
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

    def test_valid_newQuestion(self):
        # vanlig innsending av newQuestion
        url = reverse('new-question')
        response = self.client.post(url, {
            'question-questionText': 'hello',
            'question-subject': 1,
            'answers-0-answerText': 'test',
            'answers-0-isCorrect': True,
            'answers-1-answerText': 'test 2',
            'answers-1-isCorrect': False,
            'answers-TOTAL_FORMS': '2',
            'answers-INITIAL_FORMS': '0',
            'answers-MAX_NUM_FORMS': '4'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        created_question = response.context['question']
        self.assertEqual(created_question.questionText, 'hello')
        self.assertEqual(created_question.subject_id, 1)
        answers = created_question.answers.all()
        self.assertEqual(len(answers), 2)
        answers_tuples = set([(answer.answerText, answer.isCorrect) for answer in answers])
        self.assertSetEqual(
            answers_tuples,
            {('test', True), ('test 2', False)}
        )

    def test_newQuestion_with_no_correct_answer(self):
        # ingen korrekte svar
        url = reverse('new-question')
        response = self.client.post(url, {
            'question-questionText': 'hello',
            'question-subject': 1,
            'answers-0-answerText': 'test',
            'answers-0-isCorrect': False,
            'answers-1-answerText': 'test 2',
            'answers-1-isCorrect': False,
            'answers-TOTAL_FORMS': '2',
            'answers-INITIAL_FORMS': '0',
            'answers-MAX_NUM_FORMS': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Et av svaralternativene må være korrekt.', response.context['answer_formset'].non_form_errors())

    def test_newQuestion_with_empty_answer(self):
        # korrekt svar uten svarinnhold
        url = reverse('new-question')
        response = self.client.post(url, {
            'question-questionText': 'hello',
            'question-subject': 1,
            'answers-0-answerText': '',
            'answers-0-isCorrect': True,
            'answers-1-answerText': 'test 2',
            'answers-1-isCorrect': False,
            'answers-TOTAL_FORMS': '2',
            'answers-INITIAL_FORMS': '0',
            'answers-MAX_NUM_FORMS': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Svaralternativet har ikke noe innhold.', str(response.context['answer_formset'][0].errors))

    def test_newQuestion_with_duplicate_answers(self):
        # duplikate svar
        url = reverse('new-question')
        response = self.client.post(url, {
            'question-questionText': 'hello',
            'question-subject': 1,
            'answers-0-answerText': 'test',
            'answers-0-isCorrect': True,
            'answers-1-answerText': 'test',
            'answers-1-isCorrect': False,
            'answers-TOTAL_FORMS': '2',
            'answers-INITIAL_FORMS': '0',
            'answers-MAX_NUM_FORMS': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Svaralternativene må være distinkte.', response.context['answer_formset'].non_form_errors())

    def test_valid_editQuestion(self):
        question = Question.objects.get(pk=1)
        url = reverse('edit-question', args=(question.id,))
        response = self.client.post(url, {
            'question-questionText': 'Hva er 1+2?',
            'question-subject': 1,
            'answers-0-answerText': '1',
            'answers-0-isCorrect': False,
            'answers-0-id': 1,
            'answers-1-answerText': '2',
            'answers-1-isCorrect': False,
            'answers-1-id': 2,
            'answers-2-answerText': '3',
            'answers-2-isCorrect': True,
            'answers-2-id': 3,
            'answers-TOTAL_FORMS': '3',
            'answers-INITIAL_FORMS': '3',
            'answers-MAX_NUM_FORMS': '4'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        edited_question = response.context['question']
        self.assertEqual(edited_question.questionText, 'Hva er 1+2?')

        answers_tuples = set([(answer.answerText, answer.isCorrect) for answer in edited_question.answers.all()])
        self.assertSetEqual(
            answers_tuples,
            {('1', False), ('2', False), ('3', True)}
        )

    def test_editQuestion_with_new_answer(self):
        question = Question.objects.get(pk=1)
        url = reverse('edit-question', args=(question.id,))
        response = self.client.post(url, {
            'question-questionText': 'Hva er 2+2?',
            'question-subject': 1,
            'answers-0-answerText': '1',
            'answers-0-isCorrect': False,
            'answers-0-id': 1,
            'answers-1-answerText': '2',
            'answers-1-isCorrect': False,
            'answers-1-id': 2,
            'answers-2-answerText': '3',
            'answers-2-isCorrect': False,
            'answers-2-id': 3,
            'answers-3-answerText': '4',
            'answers-3-isCorrect': True,
            'answers-TOTAL_FORMS': '4',
            'answers-INITIAL_FORMS': '3',
            'answers-MAX_NUM_FORMS': '4'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        edited_question = response.context['question']
        self.assertEqual(edited_question.questionText, 'Hva er 2+2?')

        answers_tuples = set([(answer.answerText, answer.isCorrect) for answer in edited_question.answers.all()])
        self.assertSetEqual(
            answers_tuples,
            {('1', False), ('2', False), ('3', False), ('4', True)}
        )

    def test_invalid_editQuestion(self):
        question = Question.objects.get(pk=1)
        url = reverse('edit-question', args=(question.id,))
        response = self.client.post(url, {
            'question-questionText': 'Hva er 1+2?',
            'question-subject': 1,
            'answers-0-answerText': '1',
            'answers-0-isCorrect': False,
            'answers-0-id': 1,
            'answers-1-answerText': '2',
            'answers-1-isCorrect': False,
            'answers-1-id': 2,
            'answers-2-answerText': '3',
            'answers-2-isCorrect': False,
            'answers-2-id': 3,
            'answers-TOTAL_FORMS': '3',
            'answers-INITIAL_FORMS': '3',
            'answers-MAX_NUM_FORMS': '4'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Et av svaralternativene må være korrekt.', response.context['answer_formset'].non_form_errors())

        response = self.client.post(url, {
            'question-questionText': 'Hva er 1+2?',
            'question-subject': 1,
            'answers-0-answerText': '1',
            'answers-0-isCorrect': True,
            'answers-0-id': 1,
            'answers-1-answerText': '1',
            'answers-1-isCorrect': False,
            'answers-1-id': 2,
            'answers-2-answerText': '3',
            'answers-2-isCorrect': False,
            'answers-2-id': 3,
            'answers-TOTAL_FORMS': '3',
            'answers-INITIAL_FORMS': '3',
            'answers-MAX_NUM_FORMS': '4'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Svaralternativene må være distinkte.', response.context['answer_formset'].non_form_errors())

    def test_get_deleteQuestion(self):
        question = Question.objects.get(pk=1)
        url = reverse('delete-question', args=(question.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('edit-question', args=(question.id,)))


    def test_deleteQuestion(self):
        question = Question.objects.get(pk=1)
        answers = question.answers.all()
        url = reverse('delete-question', args=(question.id,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('list-questions'))
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(pk=1)

        for answer in answers:
            with self.assertRaises(Answer.DoesNotExist):
                Answer.objects.get(pk=answer.id)

    def test_createAssignment_subjects(self):
        # henter ut riktige spørsmål når man velger subject
        url = reverse('new-assignment')
        response = self.client.get(url)
        self.assertListEqual(
            list(response.context['subjects']),
            list(Subject.objects.all())
        )
        url = '{}?subject=1'.format(url)
        response = self.client.get(url)
        self.assertEqual(response.context['subjectId'], 1)

        self.assertListEqual(
            list(response.context['assignment_form'].fields['questions'].queryset.all()),
            list(Subject.objects.get(pk=1).questions.all())
        )

    def test_createAssignment(self):
        # lage assignment
        url = reverse('new-assignment')
        response = self.client.post(url, {
            'assignment-assignmentName': 'OvingTest',
            'assignment-description': 'Kul test',
            'assignment-deadline': '2017-05-21 23:59:00',
            'assignment-questions': [1, 2]
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        assignment = response.context['assignment']
        self.assertEqual(assignment.assignmentName, 'OvingTest')
        self.assertEqual(assignment.description, 'Kul test')
        self.assertEqual(assignment.deadline, datetime.datetime(2017,5,21,23,59,00, tzinfo=datetime.timezone.utc))
        print(assignment.questions.all())

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
