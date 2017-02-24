from django.shortcuts import get_object_or_404, render
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

