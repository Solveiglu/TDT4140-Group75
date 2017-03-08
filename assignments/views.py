from django.forms import formset_factory, ModelForm, Textarea
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from .models import Answer, Question
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
            'error_message': "Correct answer!",
        })
    else:
        return render(request, 'assignments/showQuestion.html', {
            'question': question,
            'error_message': "Wrong answer!",
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
        fields = ['questionText']
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



def newQuestion(request):
    AnswerFormSet = formset_factory(AnswerForm, extra=4)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, prefix='question')
        answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answers')
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
        answer_formset = AnswerFormSet(prefix='answers')

    return render(request, 'assignments/newQuestion.html', {
        'question_form': question_form,
        'answer_formset': answer_formset
    })
