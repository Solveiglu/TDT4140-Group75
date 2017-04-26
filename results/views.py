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
    yourAssignmentsList = []
    if request.user.groups.filter(name="Professors").exists():
        return redirect('professorResults')
    elif request.user.groups.filter(name="Students").exists():
        tempFinishedAssignment = FinishedAssignment.objects.all()
        tempAssignment = Assignment.objects.all()

        # Sorts by assignment. Finds all answered assignments. Tallies scores and adds to graph

        if request.user.groups.filter(name="Students").exists():
            for assignment in tempAssignment:
                scoreSingle = 0
                totalSingle = 0
                scoreTotal = 0
                totalTotal = 0
                answerScore = 0

                for finishedAssignmennt in tempFinishedAssignment:
                    if finishedAssignmennt.assignment.assignmentName == assignment.assignmentName:
                        allAnswersTemp = finishedAssignmennt.answers.all()

                        for i in allAnswersTemp:
                            totalSingle += 1
                            if i.isCorrect == True:
                                scoreSingle += 1
                        scoreTotal += scoreSingle
                        totalTotal += totalSingle
                        if finishedAssignmennt.user ==  request.user:
                            yourAssignmentsList.append(finishedAssignmennt)
                            score = 0
                            total = 0
                            answerTemp = finishedAssignmennt.answers.all()

                            for finishedAssignmennt in answerTemp:
                                total += 1
                                if finishedAssignmennt.isCorrect == True:
                                    score += 1
                            if totalTotal > 0:
                                answerScore = (score / total) * 100
                            if totalTotal > 0:
                                combinedScore = (scoreTotal / totalTotal) * 100
                                data.append([assignment.assignmentName, answerScore, combinedScore])
                                scoreList.append(answerScore)
        studentScore = SimpleDataSource(data=data)
        chart = LineChart(studentScore, options={'title': "Resultater"} )
        chart2 = BarChart(studentScore)
        if len(yourAssignmentsList) == 0:
            return redirect('index')
        return render(request, 'results.html', {
            'scoreList': scoreList,
            'results': yourAssignmentsList,
            'chart': chart
        })
    return redirect('index')


def professorResults(request):

    tempFinishedAssignment = FinishedAssignment.objects.all()
    tempAssignment = Assignment.objects.all()
    scoreList = []
    data = [['Øving', 'Gruppens Resultat']]

    #Sorts by assignment. Finds all answered assignments. Tallies scores and adds to graph

    if request.user.groups.filter(name="Professors").exists():
        for assignment in tempAssignment:
            scoreTotal = 0

            for finishedAssignment in tempFinishedAssignment:
                if finishedAssignment.assignment.assignmentName == assignment.assignmentName:
                    scoreTotal=+finishedAssignment.score
            data.append([assignment.assignmentName,scoreTotal ])
            scoreList.append(scoreTotal)
        studentScore = SimpleDataSource(data=data)
        chart = LineChart(studentScore, options={'title': "Resultater"})
        return render(request, 'professorResults.html', {
            'results': tempAssignment,
            'score': scoreList,
            'chart': chart
        })

    if request.user.groups.filter(name="Students").exists():
        return redirect('results')
    else:
        return redirect('index')


