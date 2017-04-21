from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from assignments.models import *
import datetime
from django.contrib.auth.models import User
# Create your views here.

@login_required
def index(request):
    subjects = Subject.objects.all()
    assignments = Assignment.objects.filter(Q(owner=None) | Q(owner=request.user)).all().order_by('deadline')
    today = datetime.date.today()
    active_assignments = Assignment.objects.filter(Q(owner=None) | Q(owner=request.user), deadline__gt=today).all().order_by('deadline')
    expired_assignments = Assignment.objects.filter(Q(owner=None) | Q(owner=request.user), deadline__lt=today).all().order_by('deadline')
    size = len(list(expired_assignments))
    if request.user.groups.filter(name="Professors").exists():
        return render(request, 'frontpage/professor_front.html', {
            'assignments': assignments
        })
    else:
        return render(request, 'frontpage/frontpage.html', {
            'subjects': subjects,
            'size': size,
            'active_assignments': active_assignments,
            'expired_assignments': expired_assignments
        })
