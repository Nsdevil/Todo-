from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from . models import UserProfile

from team.models import Team

# Create your views here.

def signup(request):

    if request.method=='POST':
        form=UserCreationForm(request.POST)

        if form.is_valid():
            user=form.save()
            UserProfile.objects.create(user=user)
            team=Team.objects.create(name=user.username,created_by=user,plan_id=1)
            team.members.add(user)
            team.save()

            return redirect('/log-in')
    else:

        form = UserCreationForm()

    return render(request,'userprofile/signup.html',{
        'form':form
    })

@login_required
def myaccount(request):

    team=Team.objects.filter(created_by=request.user)[0]

    return render(request,'userprofile/myaccount.html',{
        'team':team,
    })