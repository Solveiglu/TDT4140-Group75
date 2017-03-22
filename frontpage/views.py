from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request, 'frontpage/frontpage.html')

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'frontpage/active.html', {
        'subjects' : subjects
    })