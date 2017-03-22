from django.shortcuts import render
from assignments.models import *
# Create your views here.

def index(request):
    subjects = Subject.objects.all()
    return render(request, 'frontpage/frontpage.html', {
        'subjects': subjects
    })
