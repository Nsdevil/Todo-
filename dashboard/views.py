from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from lead.models import Lead
from client.models import Client
from team.models import Team

# Create your views here.
@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user)[0]
    print(team)

    leads=Lead.objects.filter(team=team,converted_to_cient=False).order_by('-created_at')[:5]
    clients=Client.objects.filter(team=team).order_by('-created_at')[:5]

    return render(request,'dashboard/dashboard.html',{
        'leads':leads,
        'clients':clients
    })