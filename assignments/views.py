from django.shortcuts import render

# Create your views here.
from assignments.models import Question


def listQuestions(request):
    questions = Question.objects.all()
    return render(request, 'assignments/questionList.html', {
        'questions': questions
    })


def showQuestion(request, questionId):
    try:
        question = Question.objects.get(id=questionId)
    except Question.DoesNotExist:
        return render(request, 'general/404.html', {
            'message': 'Spørsmål {} eksisterer ikke'.format(questionId)
        }, status=404)

    answers = question.answers.all()
    return render(request, 'assignments/showQuestion.html', {'question': question, 'answers': answers})
