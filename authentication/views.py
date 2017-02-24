import sys
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from authentication.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home.html')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

#Create student and staff groups
studGroup, created = Group.objects.get_or_create(name='Staff')
staffGroup, created = Group.objects.get_or_create(name='student')

ct = ContentType.objects.get_for_model(Profile)
#Create permissions for student and staff
permissionStud = Permission.objects.create(codename='can_not_project',
                                           name='Can not add project',
                                           content_type=ct)
permissionStaff = Permission.objects.create(codename='can_add_project',
                                           name='Can add project',
                                           content_type=ct)
#add permissions to students and staff
studGroup.permissions.add(permissionStud)
staffGroup.permissions.add(permissionStaff)

@login_required
def my_protected_view(request):
    """A view that can only be accessed by logged-in users"""
    return render(request, 'protected.html', {'current_user': request.user})


