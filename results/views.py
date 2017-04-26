from django.shortcuts import render
from results.models import FinishedAssignment
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from assignments.models import *
from graphos.sources.simple import SimpleDataSource
from django.shortcuts import render
from graphos.renderers.gchart import LineChart, BarChart, ColumnChart

def results(request):

    temp = FinishedAssignment.objects.all()
    data = [['Øving', 'Ditt Resultat', 'Klassens Resultat']]
    scoreList = []
    if request.user.groups.filter(name="Professors").exists():
        return redirect('professorResults')
    elif request.user.groups.filter(name="Students").exists():
        tempFinishedAssignment = FinishedAssignment.objects.all()
        tempAssignment = Assignment.objects.all()
        # Sorts by assignment. Finds all answered assignments. Tallies scores and adds to graph
        if request.user.groups.filter(name="Students").exists():
            for x in tempAssignment:
                scoreSingle = 0
                totalSingle = 0
                scoreTotal = 0
                totalTotal = 0
                answerScore = 0


                for y in tempFinishedAssignment:
                    if y.assignment.assignmentName == x.assignmentName:
                        allAnswersTemp = y.answers.all()
                        for i in allAnswersTemp:
                            totalSingle += 1
                            if i.isCorrect == True:
                                scoreSingle += 1
                        scoreTotal += scoreSingle
                        totalTotal += totalSingle
                        if y.user ==  request.user:
                            score = 0
                            total = 0
                            answerTemp = y.answers.all()
                            for y in answerTemp:
                                total += 1
                                if y.isCorrect == True:
                                    score += 1
                            if totalTotal > 0:
                                answerScore = (score / total) * 100
                if totalTotal > 0:
                    combinedScore = (scoreTotal / totalTotal) * 100
                    data.append([x.assignmentName, answerScore, combinedScore])
                    scoreList.append(answerScore)
        studentScore = SimpleDataSource(data=data)
        chart = LineChart(studentScore, options={'title': "Resultater"} )
        chart2 = BarChart(studentScore)
        return render(request, 'results.html', {
            'scoreList': scoreList,
            'results': temp,
            'chart': chart,
            'chart2': chart2,
        })
    return redirect('index')




def professorResults(request):

    tempFinishedAssignment = FinishedAssignment.objects.all()
    tempAssignment = Assignment.objects.all()
    scoreList = []
    data = [['Øving', 'Gruppens Resultat']]
    #Sorts by assignment. Finds all answered assignments. Tallies scores and adds to graph
    if request.user.groups.filter(name="Professors").exists():
        for x in tempAssignment:
            scoreTotal = 0
            for y in tempFinishedAssignment:
                if y.assignment.assignmentName == x.assignmentName:
                    scoreTotal=+y.score
            data.append([x.assignmentName,scoreTotal ])
            scoreList.append(scoreTotal)
        studentScore = SimpleDataSource(data=data)
        chart = LineChart(studentScore, options={'title': "Resultater"})
        return render(request, 'professorResults.html', {
            'results': tempAssignment,
            'score': scoreList,
            'chart': chart,
        })

    if request.user.groups.filter(name="Students").exists():
        return redirect('results')
    else:
        return redirect('index')


