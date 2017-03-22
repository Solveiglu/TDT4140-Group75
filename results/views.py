from django.shortcuts import render
from results.models import questionResult


def listResults(request):
    results = questionResult.objects.all()
    return render(request, 'resultlist.html', {
        'questionResult': results
    })


def showResult(request, questionResultId):
    try:
        results = questionResult.objects.get(id=questionResultId)
    except results.DoesNotExist:
        return render(request, 'general/404.html', {
            'message': 'Spørsmål {} eksisterer ikke'.format(showResult())
        }, status=404)

    return render(request, 'showResult.html', {'results': results})
