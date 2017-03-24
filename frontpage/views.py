from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from assignments.models import *
# Create your views here.

@login_required
def index(request):

    user = request.user
    perms = user.get_all_permissions(obj=None)
    subjects = Subject.objects.all()
<<<<<<< HEAD
    print(request.user.groups.all())
    if request.user.groups.filter(name="Professors").exists():
        return redirect('assignments/new')
    else:
        return render(request, 'frontpage/frontpage.html', {
            'subjects': subjects
        })
=======
    if 'professorperms' in perms:
        return render(request,'assignments/new.html')
    else:
        return render(request, 'frontpage/frontpage.html', {
            'subjects': subjects
    })
>>>>>>> 86e35278fbbddba113b96f1c3a16dbc15e0b8468
