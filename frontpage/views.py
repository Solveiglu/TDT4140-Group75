from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from assignments.models import *
# Create your views here.

@login_required
def index(request):

    subjects = Subject.objects.all()
    assignments = Assignment.objects.all()
    print(request.user.groups.all())
    if request.user.groups.filter(name="Professors").exists():
        return redirect('assignments/new')
    else:
        return render(request, 'frontpage/frontpage.html', {
            'subjects': subjects,
            'assignments': assignments
        })
