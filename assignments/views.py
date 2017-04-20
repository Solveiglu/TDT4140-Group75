import random

from django.contrib.auth.decorators import login_required
from django.db.models import TextField
from django.forms import BaseFormSet
from django.forms import BaseModelFormSet
from django.forms import *
from django.forms import ModelForm, Textarea, modelformset_factory
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from results.models import *
import datetime
from .models import Answer, Question, Assignment, Subject
from django.views import generic
from .models import Answer, Question, Assignment, Subject
from django.views import generic
def listQuestions(request):
    questions = Question.objects.all()
    return render(request, 'assignments/questionList.html', {
        'questions': questions
    })

def answer(request, questionId):
    question = get_object_or_404(Question, pk=questionId)

    try:
        selected_answer = question.answers.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'assignments/showQuestion.html', {
            'question': question,
            'error_message': "You didn't select an answer.",
        })

    if selected_answer.isCorrect:
        return render(request, 'assignments/showQuestion.html', {
            'question': question,
            'error_message': 'Riktig svar',
        })
    else:
        return render(request, 'assignments/showQuestion.html', {
            'question': question,
            'error_message': 'Feil svar',
        })

def showQuestion(request, questionId):
    try:
        question = Question.objects.get(id=questionId)
    except Question.DoesNotExist:
        return render(request, 'general/404.html', {
            'message': 'Spørsmål {} eksisterer ikke'.format(questionId)
        }, status=404)

    return render(request, 'assignments/showQuestion.html', {'question': question})

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['questionText', 'subject']
        widgets = {
            'questionText': Textarea(attrs={'cols': 60, 'rows': 4})
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answerText', 'isCorrect']
        widgets = {
            'answerText': Textarea(attrs={'cols': 60, 'rows': 4})
        }

    def clean(self):
        super(AnswerForm, self).clean()
        print(self.cleaned_data)
        answer_text = self.cleaned_data['answerText']
        answer_correct = self.cleaned_data['isCorrect']
        if answer_text.strip() == "" and answer_correct:
            raise ValidationError("Svaralternativet har ikke noe innhold.")

class BaseAnswerFormSet(BaseModelFormSet):
    def clean(self):
        super(BaseAnswerFormSet, self).clean()
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        answers = []
        correctAnswerExists = False
        for form in self.forms:
            if 'answerText' not in form.cleaned_data or 'isCorrect' not in form.cleaned_data:
                continue
            answer = form.cleaned_data['answerText'].strip()
            if answer in answers:
                raise ValidationError("Svaralternativene må være distinkte.")
            answers.append(answer)
            answer_correct = form.cleaned_data['isCorrect']
            if answer_correct:
                correctAnswerExists = True
        if not correctAnswerExists:
            raise ValidationError("Et av svaralternativene må være korrekt.")


def newQuestion(request):
    AnswerFormSet = modelformset_factory(Answer, AnswerForm, extra=4, formset=BaseAnswerFormSet)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, prefix='question')
        answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answers', queryset=Answer.objects.none())
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            for answer_form in answer_formset:
                answer = answer_form.save(commit=False)
                if answer.isCorrect is not None and answer.answerText is not None:
                    answer.question = question
                    answer.save()
            return redirect('show-question', question.id)
    else:
        question_form = QuestionForm(prefix='question')
        answer_formset = AnswerFormSet(prefix='answers', queryset=Answer.objects.none())

    return render(request, 'assignments/newQuestion.html', {
        'question_form': question_form,
        'answer_formset': answer_formset
    })

def editQuestion(request, questionId):
    question = Question.objects.get(id=questionId)

    AnswerFormSet = modelformset_factory(Answer, AnswerForm, extra=(4-question.answers.count()), formset=BaseAnswerFormSet)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, prefix='question', instance=question)
        answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answers', queryset=Answer.objects.filter(question_id=question.id))
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            for answer_form in answer_formset:
                answer = answer_form.save(commit=False)
                if answer.answerText.strip() == '' and answer.id is not None:
                    answer.delete()
                elif answer.isCorrect is not None and answer.answerText is not None:
                    answer.question = question
                    answer.save()
            return redirect('show-question', question.id)
        else:
            print("a form is invalid")
    else:
        question_form = QuestionForm(prefix='question', instance=question)
        answer_formset = AnswerFormSet(prefix='answers', queryset=Answer.objects.filter(question_id=question.id))

    return render(request, 'assignments/editQuestion.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
        'question_id': question.id
    })

def deleteQuestion(request, questionId):
    if request.method == "POST":
        question = Question.objects.get(id=questionId)
        for answer in question.answers.all():
            answer.delete()
        question.delete()
        return redirect('list-questions')
    else:
        return redirect('edit-question', questionId)

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignmentName', 'description', 'deadline', 'questions','passingGrade']
        widgets = {
            'questions': CheckboxSelectMultiple()
        }



def createAssignment(request):
    if request.method == 'POST':
        assignment_form = AssignmentForm(request.POST, request.FILES, prefix='assignment')
        if assignment_form.is_valid():
            assignment = assignment_form.save()
            return redirect('assignment', assignment.id)
    else:
        assignment_form = AssignmentForm(prefix='assignment')

    subjects = Subject.objects.all()
    subjectId = int(request.GET.get('subject', 0))
    if subjectId > 0:
        assignment_form.fields['questions'].queryset = Question.objects.filter(subject_id=subjectId)

    return render(request, 'professor/createAssignment.html', {
        'assignment_form': assignment_form,
        'subjects': subjects,
        'subjectId': subjectId
    })

class PrivateAssignmentForm(Form):
    assignment_name = CharField()
    number_of_questions = IntegerField()
    subject = ModelChoiceField(queryset=Subject.objects.all())

@login_required
def createPrivateAssignment(request):
    if request.method == 'POST':
        private_assignment_form = PrivateAssignmentForm(request.POST, request.FILES)
        if private_assignment_form.is_valid():
            assignment_name = private_assignment_form.cleaned_data['assignment_name']
            number_of_questions = private_assignment_form.cleaned_data['number_of_questions']
            subject = private_assignment_form.cleaned_data['subject']

            all_questions = subject.questions.all()

            questions = random.sample(list(all_questions), min(len(all_questions), number_of_questions))

            assignment = Assignment(assignmentName=assignment_name, owner_id=request.user.id)
            assignment.save()
            assignment.questions=questions

            print(assignment_name, number_of_questions, subject, assignment.id, assignment)

            return redirect('assignment', assignment.id)
    else:
        private_assignment_form = PrivateAssignmentForm()

    return render(request, 'assignments/createPrivateAssignment.html', {
        'private_assignment_form': private_assignment_form,
    })

def viewAssignment(request, assignmentId):
    assignment = Assignment.objects.get(id=assignmentId)
    totalScore = 0
    if request.method == 'POST':
        print('hello post post')
        print(request.POST)
        results = FinishedAssignment.objects.create(
            user = request.user,
            assignment = Assignment.objects.get(id=assignmentId),

        )
        for key, answer_id in request.POST.items():
            if key.startswith('answer-'):
                question_id = int(key.replace('answer-', ''))
                question = Question.objects.get(id=question_id)
                answer = Answer.objects.get(id=answer_id)
                if answer not in question.answers.all():
                    raise ValidationError('Question and answer do not match')
                else:
                    results.answer.add(answer)
        score = 0
        total = 0
        for answers in results.answer.all():
            if answers.isCorrect == True:
                score+=1
            total +=1
        totalScore=(score/total)*100
        results.score = totalScore
        if assignment.passingGrade < totalScore:
            results.passed = True
        results.save
        return redirect('results')

    return render(request, 'assignments/assignment.html', {
        'assignment': assignment
    })


def showAssignment(request, assignmentId):

    try:
        assignment = Assignment.objects.get(id=assignmentId)
    except Question.DoesNotExist:
        return render(request, 'general/404.html', {
            'message': 'Oppgave {} eksisterer ikke'.format(questionId)
        }, status=404)
    return render(request, 'professor/assignmentView.html', {
        'assignment': assignment
    })


@login_required
def editAssignment(request, assignmentId):

    if assignmentId:
        assignment = get_object_or_404(Assignment, pk=assignmentId)

    else:
        assignment = Assignment(owner=request.user)

    form = AssignmentForm(request.POST or None, instance=assignment)

    if request.POST and form.is_valid():
        form.save()

        return redirect('show-assignment', assignmentId)
    return render(request, 'professor/editAssignment.html', {
        'form': form,
        'assignment_id': assignmentId,
    })
