from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Client
from .forms import AddClientForm, AddCommentForm, AddFileForm
from team.models import Team
# Create your views here.


@login_required
def client_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request, 'client/client_list.html', {
        'clients': clients
    })


@login_required
def client_add_file(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.team = team
            file.client_id = pk
            file.created_by = request.user
            file.save()
            return redirect('clients:detail', pk=pk)
    return redirect('clients:detail', pk=pk)


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)
    else:
        form = AddCommentForm()
    return render(request, 'client/client_detail.html', {
        'client': client,
        'form': form,
        'fileform': AddFileForm()
    })


@login_required
def client_add(request):
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, 'The Task in Progress was Created')

            return redirect('clients:list')

    form = AddClientForm()
    return render(request, 'client/client_add.html', {
        'form': form,
        'team': team,
    })


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, 'The Task in Progress was deleted')
    return redirect('clients:list')


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Task in Progress was Edited')
            return redirect('clients:list')
    form = AddClientForm(instance=client)
    return render(request, 'client/client_edit.html', {
        'form': form
    })
