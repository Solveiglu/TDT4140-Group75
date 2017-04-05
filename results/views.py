from django.shortcuts import render
from results.models import questionResult, finishedAssignment
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from assignments.models import *
from graphos.sources.simple import SimpleDataSource
from django.shortcuts import render
from graphos.renderers.yui import LineChart, BarChart, ColumnChart



def results(request):
    temp = finishedAssignment.objects.all()
    userResults = []
    data = ['Øving', 'Ditt Resultat', 'Klassens Resultat']
    if request.user.groups.filter(name="Professors").exists():
        return render(request, 'professorResults.html', )
    else:
        for x in temp:
                if temp.assignment.user ==  request.user:
                    userResults.append(userResults[x])
        for x in userResults:
            data.append[[userResults.Assignment], userResults.Answers]
            data = ['Øving', 'Ditt Resultat', 'Klassens Resultat']
        data_source = SimpleDataSource(data=data)
        chart = LineChart(data_source)
        chart2 = BarChart(data_source)
        return render(request, 'results.html', {
            'results': userResults,
            'chart': chart,
            'chart2': chart2,
        })



def listResults(request):
    results = questionResult.objects.all()
    user = request.user
    return render(request, 'resultlist.html', {
        'questionResult': results,
    })

