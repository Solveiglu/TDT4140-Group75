from django.shortcuts import render
from assignments.models import *
# Create your views here.

def index(request):

    user = request.user
    perms = user.get_all_permissions(obj=None)
    subjects = Subject.objects.all()
    if 'professorperms' in perms:
        return render(request,'assignments/new.html')
    else:
        return render(request, 'frontpage/frontpage.html', {
            'subjects': subjects
    })
