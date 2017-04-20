from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from assignments.models import *
from django.contrib.auth.models import User
# Create your views here.

@login_required
def index(request):

    subjects = Subject.objects.all()
    assignments = Assignment.objects.filter(Q(owner=None) | Q(owner=request.user)).all()
    #user = User.objects.all()
    if request.user.groups.filter(name="Professors").exists():
        return render(request, 'frontpage/professor_front.html', {
            'assignments': assignments
        })
    else:
        return render(request, 'frontpage/frontpage.html', {
            'subjects': subjects,
            'assignments': assignments
        })
