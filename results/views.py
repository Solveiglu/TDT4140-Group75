from django.shortcuts import render
from results.models import questionResult
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission


def listResults(request):
    results = questionResult.objects.all()
    user = request.user
    #permissionsList = [(x.id, x.name) for x in Permission.objects.filter(user=user)]
    #permissionsList = [(5,"Hei")]
    return render(request, 'resultlist.html', {
        'questionResult': results,
    })


def showResult(request, questionResultId):
    try:
        results = questionResult.objects.get(id=questionResultId)
    except results.DoesNotExist:
        return render(request, 'general/404.html', {
            'message': 'Spørsmål {} eksisterer ikke'.format(showResult())
        }, status=404)

    return render(request, 'showResult.html', {'results': results})
