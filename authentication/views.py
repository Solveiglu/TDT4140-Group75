from django.shortcuts import render

import sys
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
new_group, created = Group.objects.get_or_create(name='Students')
new_group, created = Group.objects.get_or_create(name='Professor')
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            rawPassword = form.cleaned_data.get('password1')
#            firstName = form.cleaned_data.get('firstname')
#            lastName = form.cleaned_data.get('lastname')
#            bio = form.cleaned_data.get('bio')
            user = authenticate(username=username, password=rawPassword)
            g = Group.objects.get(name='Students')
            g.user_set.add(user)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

    from django.contrib.auth import authenticate, login

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        return redirect('new-question')
    else:
        return redirect('home.html')

